"""Loopback-only preview/confirm API for controlled CPA-ZH maintenance writes."""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BACKEND = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
from app.core.ai_config import public_ai_config, save_ai_config, test_ai_connection

try:
    from kb_common import parse_frontmatter, update_frontmatter
except ModuleNotFoundError:
    from tools.kb_common import parse_frontmatter, update_frontmatter

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "knowledge-base" / "CPA-ZH"
PYTHON = sys.executable
TOKEN = os.environ.get("CPA_ZH_MAINTENANCE_TOKEN", "")
PORT = int(os.environ.get("KB_MAINTENANCE_PORT", "8766"))
ORIGINS = [item.strip() for item in os.environ.get("CPA_ZH_WEB_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",") if item.strip()]
DEMO_MODE = os.environ.get("CPA_ZH_DEMO_MODE", "0") == "1"
PREVIEWS: dict[str, dict] = {}
UPLOAD_SESSIONS: dict[str, dict] = {}
UPLOAD_ROOT = ROOT / "workspace" / "tmp" / "kb-import-sessions"
UPLOAD_TTL_SECONDS = 1800
MAX_UPLOAD_FILES = 20
MAX_UPLOAD_FILE_BYTES = 25 * 1024 * 1024
MAX_UPLOAD_TOTAL_BYTES = 100 * 1024 * 1024
SUPPORTED_UPLOAD_SUFFIXES = {".md", ".txt", ".csv", ".html", ".htm", ".xml", ".docx", ".pdf"}

app = FastAPI(title="CPA-ZH Maintenance API", version="1.0.0", docs_url="/maintenance/docs")
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Accept", "Content-Type", "Authorization"])


class QAPreview(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    answer: str = Field(min_length=2, max_length=10000)
    title: str = Field(default="", max_length=200)
    slug: str = Field(default="", max_length=120)
    source: str = Field(default="local-qa-log", max_length=160)
    tags: str = Field(default="", max_length=500)
    related: str = Field(default="", max_length=1000)


class IngestPreview(BaseModel):
    source_path: str = Field(min_length=1, max_length=1000)
    raw_subdir: str = Field(min_length=1, max_length=160)
    batch_slug: str = Field(min_length=1, max_length=120)
    title: str = Field(default="", max_length=200)
    source_type: str = Field(default="local-source", max_length=80)
    official_source: str = Field(default="本地资料", max_length=200)
    official_url: str = Field(default="", max_length=1000)
    tags: str = Field(default="", max_length=500)


class UploadCommitItem(BaseModel):
    id: str = Field(min_length=8, max_length=64)
    batch_name: str = Field(min_length=1, max_length=120)


class UploadCommit(BaseModel):
    session_token: str = Field(min_length=16, max_length=100)
    items: list[UploadCommitItem] = Field(min_length=1, max_length=MAX_UPLOAD_FILES)


class ReviewPreview(BaseModel):
    path: str = Field(min_length=1, max_length=500)
    confirmed: bool
    content_sha256: str = Field(default="", min_length=0, max_length=64)


class AIConfigPayload(BaseModel):
    provider: str = Field(default="openai-compatible", max_length=80)
    base_url: str = Field(min_length=8, max_length=500)
    model: str = Field(min_length=1, max_length=200)
    enabled: bool = False
    api_key: str = Field(default="", max_length=1000)


def _auth(authorization: str | None) -> None:
    if DEMO_MODE:
        if authorization != "Bearer demo":
            raise HTTPException(401, "开发模拟模式令牌无效")
        return
    if not TOKEN:
        raise HTTPException(503, "维护服务尚未配置 CPA_ZH_MAINTENANCE_TOKEN")
    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(401, "维护令牌无效")


@app.get("/maintenance/v1/ai-config")
def get_ai_config(authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    return public_ai_config()


@app.post("/maintenance/v1/ai-config")
def update_ai_config(payload: AIConfigPayload, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    if DEMO_MODE:
        return {**payload.model_dump(exclude={"api_key"}), "key_configured": bool(payload.api_key), "simulated": True}
    try:
        return save_ai_config(**payload.model_dump())
    except ValueError as error:
        raise HTTPException(400, str(error)) from None


@app.post("/maintenance/v1/ai-config/test")
def test_ai_config(authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    if DEMO_MODE:
        return {"status": "ok", "message": "开发模拟模式：未请求外部模型服务"}
    try:
        return test_ai_connection()
    except ValueError as error:
        raise HTTPException(400, str(error)) from None


def _slug(value: str, fallback: str) -> str:
    candidate = value.strip() or fallback
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,119}", candidate):
        raise HTTPException(400, "slug 只能包含小写字母、数字和连字符")
    return candidate


def _source_path(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists() or not path.is_file() and not path.is_dir():
        raise HTTPException(400, "来源路径不存在或不是文件/目录")
    return path


def _run(args: list[str]) -> str:
    result = subprocess.run([PYTHON, str(ROOT / "tools" / "kb.py"), *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=180)
    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode:
        raise HTTPException(502, output[-4000:] or "维护命令执行失败")
    return output[-4000:]


def _remove_upload_directory(directory: Path) -> None:
    root = UPLOAD_ROOT.resolve()
    candidate = Path(directory).resolve()
    if candidate == root:
        return
    try:
        candidate.relative_to(root)
    except ValueError:
        return
    shutil.rmtree(candidate, ignore_errors=True)


def _cleanup_upload_sessions() -> None:
    now = time.time()
    expired = [token for token, session in UPLOAD_SESSIONS.items() if now - session["created"] > UPLOAD_TTL_SECONDS]
    for token in expired:
        session = UPLOAD_SESSIONS.pop(token)
        _remove_upload_directory(session["directory"])
    if not UPLOAD_ROOT.exists():
        return
    root = UPLOAD_ROOT.resolve()
    for directory in UPLOAD_ROOT.iterdir():
        if not directory.is_dir():
            continue
        try:
            directory.resolve().relative_to(root)
        except ValueError:
            continue
        if now - directory.stat().st_mtime > UPLOAD_TTL_SECONDS:
            _remove_upload_directory(directory)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_upload_item(item: dict, session_directory: Path) -> None:
    root = session_directory.resolve()
    for key, expected in (("source_path", item.get("sha256")), ("markdown_path", item.get("markdown_sha256"))):
        path = Path(item[key]).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            raise HTTPException(409, "上传预览文件位置无效") from None
        if not path.is_file() or _file_sha256(path) != expected:
            raise HTTPException(409, "上传预览内容已改变，请重新上传并预览")


_cleanup_upload_sessions()


def _upload_session(token: str) -> dict:
    _cleanup_upload_sessions()
    session = UPLOAD_SESSIONS.get(token)
    if not session:
        raise HTTPException(400, "上传预览不存在或已过期，请重新选择文件")
    return session


def _extract_uploaded_markdown(path: Path, original_name: str) -> tuple[str, str]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".md":
            markdown = path.read_text(encoding="utf-8-sig", errors="strict")
            method = "Markdown 原文"
        else:
            try:
                from convert_raw_to_md import extract_csv, extract_docx, extract_html, extract_txt
            except ModuleNotFoundError:
                from tools.convert_raw_to_md import extract_csv, extract_docx, extract_html, extract_txt
            if suffix in {".html", ".htm", ".xml"}:
                body, method = extract_html(path), "HTML 正文抽取"
            elif suffix == ".docx":
                body, method = extract_docx(path), "DOCX 正文抽取"
            elif suffix == ".csv":
                body, method = extract_csv(path), "CSV 表格转换"
            elif suffix == ".txt":
                body, method = extract_txt(path), "文本读取"
            elif suffix == ".pdf":
                try:
                    from kb_pdf_to_markdown import extract_pdf_best
                except ModuleNotFoundError:
                    from tools.kb_pdf_to_markdown import extract_pdf_best
                body, engine, quality = extract_pdf_best(path)
                method = f"PDF {engine} 抽取（{quality}）"
            else:
                raise ValueError("不支持的文件类型")
            if not body.strip() or body.lstrip().startswith("（PDF 解析失败"):
                raise ValueError("未提取到可识别正文，扫描版 PDF 请先完成 OCR")
            title = Path(original_name).stem.strip() or "上传文档"
            markdown = f"# {title}\n\n{body.strip()}\n"
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(422, f"{original_name}：{error}") from None
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"
    if len(markdown.strip()) < 5:
        raise HTTPException(422, f"{original_name}：未提取到足够的 Markdown 正文")
    return markdown, method


def _batch_name_from_markdown(markdown: str, filename: str) -> str:
    body = re.sub(r"\A---\s*\n.*?\n---\s*", "", markdown, count=1, flags=re.DOTALL)
    headings = re.findall(r"^#{1,3}\s+(.+?)\s*$", body, flags=re.MULTILINE)
    candidates = [*headings, *body.splitlines(), Path(filename).stem]
    filename_stem = re.sub(r"\s+", " ", Path(filename).stem).strip().casefold()
    for value in candidates:
        value = re.sub(r"!?(?:\[([^]]*)\])\([^)]*\)", r"\1", value)
        value = re.sub(r"^[\s#>*_`~|\-]+|[\s#>*_`~|\-]+$", "", value)
        value = re.sub(r"\s+", " ", value).strip("：:，,。.;；")
        if Path(filename).suffix.lower() != ".md" and value.casefold() == filename_stem:
            continue
        if len(value) >= 2 and not re.fullmatch(r"[-:|\s]+", value):
            return value[:80]
    return "本地资料导入"


def _upload_batch_slug(batch_name: str, item_id: str) -> str:
    digest = hashlib.sha256(f"{batch_name}\0{item_id}".encode("utf-8")).hexdigest()[:10]
    return f"upload-{date.today().strftime('%Y%m%d')}-{digest}"


@app.post("/maintenance/v1/ingest/upload")
async def upload_ingest(files: list[UploadFile] = File(...), authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    _cleanup_upload_sessions()
    if not files or len(files) > MAX_UPLOAD_FILES:
        raise HTTPException(400, f"每次请选择 1 至 {MAX_UPLOAD_FILES} 个文件")
    session_token = secrets.token_urlsafe(24)
    session_dir = UPLOAD_ROOT / session_token
    session_dir.mkdir(parents=True, exist_ok=False)
    items: list[dict] = []
    total_bytes = 0
    try:
        for index, upload in enumerate(files, start=1):
            original_name = Path(upload.filename or "").name.strip()
            suffix = Path(original_name).suffix.lower()
            if not original_name or suffix not in SUPPORTED_UPLOAD_SUFFIXES:
                raise HTTPException(415, f"{original_name or '未命名文件'}：暂不支持该文件类型")
            content = await upload.read(MAX_UPLOAD_FILE_BYTES + 1)
            if len(content) > MAX_UPLOAD_FILE_BYTES:
                raise HTTPException(413, f"{original_name}：单个文件不能超过 25 MB")
            total_bytes += len(content)
            if total_bytes > MAX_UPLOAD_TOTAL_BYTES:
                raise HTTPException(413, "单次上传总大小不能超过 100 MB")
            digest = hashlib.sha256(content).hexdigest()
            item_id = f"{index:02d}-{digest[:16]}"
            item_dir = session_dir / item_id
            item_dir.mkdir()
            source_path = item_dir / original_name
            source_path.write_bytes(content)
            markdown, extraction_method = _extract_uploaded_markdown(source_path, original_name)
            markdown_path = item_dir / "extracted.md"
            markdown_path.write_text(markdown, encoding="utf-8", newline="\n")
            items.append({
                "id": item_id,
                "filename": original_name,
                "size": len(content),
                "sha256": digest,
                "markdown_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
                "source_path": source_path,
                "markdown_path": markdown_path,
                "markdown_preview": markdown[:6000],
                "markdown_length": len(markdown),
                "preview_truncated": len(markdown) > 6000,
                "batch_name": _batch_name_from_markdown(markdown, original_name),
                "extraction_method": extraction_method,
            })
    except Exception:
        shutil.rmtree(session_dir, ignore_errors=True)
        raise
    finally:
        for upload in files:
            await upload.close()
    UPLOAD_SESSIONS[session_token] = {"created": time.time(), "directory": session_dir, "items": items}
    public_items = [{key: value for key, value in item.items() if key not in {"sha256", "source_path", "markdown_path"}} for item in items]
    return {"session_token": session_token, "items": public_items, "expires_in": UPLOAD_TTL_SECONDS}


@app.get("/maintenance/v1/ingest/{session_token}/items/{item_id}/markdown")
def uploaded_markdown(session_token: str, item_id: str, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    session = _upload_session(session_token)
    item = next((candidate for candidate in session["items"] if candidate["id"] == item_id), None)
    if not item:
        raise HTTPException(404, "上传文件不存在")
    return {"markdown": item["markdown_path"].read_text(encoding="utf-8")}


@app.post("/maintenance/v1/ingest/batch-commit")
def batch_ingest_commit(payload: UploadCommit, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    session = _upload_session(payload.session_token)
    session_items = {item["id"]: item for item in session["items"]}
    requested_ids = [item.id for item in payload.items]
    if len(set(requested_ids)) != len(requested_ids) or any(item_id not in session_items for item_id in requested_ids):
        raise HTTPException(409, "提交文件与上传预览不一致")

    plans: list[tuple[dict, str, str, list[str]]] = []
    for requested in payload.items:
        item = session_items[requested.id]
        _validate_upload_item(item, session["directory"])
        batch_name = requested.batch_name.strip()
        if not batch_name:
            raise HTTPException(400, f"{item['filename']}：批次名称不能为空")
        batch_slug = _upload_batch_slug(batch_name, item["id"])
        raw_subdir = f"imports/{date.today().strftime('%Y-%m')}/{batch_slug}"
        target = (KB / "raw" / raw_subdir).resolve()
        if target.exists():
            raise HTTPException(409, f"{item['filename']}：目标批次已存在，请重新上传")
        args = [
            "ingest-local", "--source", str(item["source_path"]), "--raw-subdir", raw_subdir,
            "--batch-slug", batch_slug, "--title", batch_name, "--source-type", "local-upload",
            "--official-source", "本地上传", "--source-label", f"browser-upload:{item['filename']}",
            "--tags", "local-upload,auto-extracted",
        ]
        if item["source_path"].suffix.lower() != ".md":
            args.extend(["--derived-markdown", str(item["markdown_path"])])
        plans.append((item, batch_name, raw_subdir, args))

    if DEMO_MODE:
        UPLOAD_SESSIONS.pop(payload.session_token, None)
        shutil.rmtree(session["directory"], ignore_errors=True)
        names = "、".join(batch_name for _item, batch_name, _subdir, _args in plans)
        return {"status": "committed", "output": f"开发模拟确认完成：{names}（未写入知识库）。", "health": "demo: skipped cache, index, and health commands", "imported_count": len(plans)}

    for _item, _batch_name, _raw_subdir, args in plans:
        _run(args)
    try:
        for _item, _batch_name, raw_subdir, args in plans:
            _run([*args, "--commit"])
    except Exception:
        imports_root = (KB / "raw" / "imports").resolve()
        for _item, _batch_name, raw_subdir, _args in plans:
            target = (KB / "raw" / raw_subdir).resolve()
            if target.is_relative_to(imports_root):
                shutil.rmtree(target, ignore_errors=True)
        raise
    UPLOAD_SESSIONS.pop(payload.session_token, None)
    shutil.rmtree(session["directory"], ignore_errors=True)
    _run(["cache", "build"])
    _run(["index"])
    health = _run(["health"])
    output = "\n".join(f"- {batch_name} -> raw/{raw_subdir}" for _item, batch_name, raw_subdir, _args in plans)
    return {"status": "committed", "output": output, "health": health, "imported_count": len(plans)}


def _preview(kind: str, payload: dict, args: list[str]) -> dict:
    output = "开发模拟预览：不会写入知识库，也不会执行维护命令。" if DEMO_MODE else _run(args)
    digest = hashlib.sha256(json.dumps({"kind": kind, "payload": payload}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:24]
    token = f"{int(time.time())}-{digest}"
    PREVIEWS[token] = {"kind": kind, "payload": payload, "args": args, "created": time.time()}
    return {"preview_token": token, "kind": kind, "output": output, "expires_in": 600}


def _commit(token: str, kind: str, payload: dict) -> dict:
    item = PREVIEWS.pop(token, None)
    if not item or time.time() - item["created"] > 600:
        raise HTTPException(400, "预览不存在或已过期，请重新预览")
    if item["kind"] != kind or item["payload"] != payload:
        raise HTTPException(409, "提交内容与预览不一致")
    if DEMO_MODE:
        return {"status": "committed", "output": "开发模拟确认完成：未写入知识库。", "health": "demo: skipped cache, index, and health commands"}
    args = [arg for arg in item["args"] if arg != "--commit"] + ["--commit"]
    output = _run(args)
    _run(["cache", "build"])
    _run(["index"])
    health = _run(["health"])
    return {"status": "committed", "output": output, "health": health}


def _review_target(value: str) -> Path:
    normalized = value.replace("\\", "/")
    if not normalized.startswith("wiki/") or not normalized.endswith(".md"):
        raise HTTPException(400, "复核页面必须是 wiki 下的 Markdown 文件")
    target = (KB / normalized).resolve()
    try:
        target.relative_to(KB / "wiki")
    except ValueError:
        raise HTTPException(400, "非法复核页面路径") from None
    if not target.exists():
        raise HTTPException(404, "复核页面不存在")
    return target


def _review_metadata(path: Path) -> tuple[dict, str]:
    metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    if metadata.get("review_status") != "pending-human-review":
        raise HTTPException(409, "该页面不在待人工复核队列")
    if not metadata.get("source_verified") or metadata.get("page_role") not in {"knowledge", "case"}:
        raise HTTPException(409, "该页面不满足答疑准入条件")
    return metadata, body


@app.get("/maintenance/v1/review/pending")
def pending_review(authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    items: list[dict[str, str]] = []
    for path in sorted((KB / "wiki").rglob("*.md")):
        if any(part.startswith("_") for part in path.relative_to(KB / "wiki").parts):
            continue
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if metadata.get("review_status") == "pending-human-review" and metadata.get("source_verified") and metadata.get("page_role") in {"knowledge", "case"}:
            items.append({"path": path.relative_to(KB).as_posix(), "title": str(metadata.get("title") or path.stem), "page_role": str(metadata.get("page_role")), "maturity": str(metadata.get("maturity") or "draft"), "raw_path": str(metadata.get("raw_path") or ""), "body_preview": body[:12000], "content_sha256": _file_sha256(path)})
    return {"items": items}


@app.get("/maintenance/v1/review/detail")
def review_detail(path: str, authorization: str | None = Header(default=None)) -> dict:
    """Return the current full page body for the review screen."""
    _auth(authorization)
    target = _review_target(path)
    metadata, body = _review_metadata(target)
    return {
        "path": target.relative_to(KB).as_posix(),
        "title": str(metadata.get("title") or target.stem),
        "page_role": str(metadata.get("page_role") or ""),
        "maturity": str(metadata.get("maturity") or "draft"),
        "raw_path": str(metadata.get("raw_path") or ""),
        "body": body,
        "content_sha256": _file_sha256(target),
    }


@app.post("/maintenance/v1/review/preview")
def review_preview(payload: ReviewPreview, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    if not payload.confirmed:
        raise HTTPException(400, "必须确认已完成人工专业复核")
    target = _review_target(payload.path)
    metadata, body = _review_metadata(target)
    content_sha256 = _file_sha256(target)
    if payload.content_sha256 and payload.content_sha256 != content_sha256:
        raise HTTPException(409, "页面内容已改变，请重新加载待复核列表")
    data = payload.model_dump()
    data["path"] = target.relative_to(KB).as_posix()
    data["content_sha256"] = content_sha256
    changes = {"maturity": "reviewed", "answer_ready": True, "review_status": "user-approved", "updated": date.today().isoformat()}
    output = "将更新以下元数据：\n" + "\n".join(f"- {key}: {metadata.get(key, '')} -> {value}" for key, value in changes.items())
    digest = hashlib.sha256(json.dumps({"kind": "review", "payload": data}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:24]
    token = f"{int(time.time())}-{digest}"
    PREVIEWS[token] = {"kind": "review", "payload": data, "path": target, "changes": changes, "created": time.time()}
    return {"preview_token": token, "kind": "review", "output": output, "expires_in": 600, "review": {"path": data["path"], "title": metadata.get("title", target.stem), "raw_path": metadata.get("raw_path", ""), "body": body, "changes": changes, "content_sha256": content_sha256}}


@app.post("/maintenance/v1/review/commit")
def review_commit(payload: ReviewPreview, preview_token: str, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    data = payload.model_dump()
    data["path"] = _review_target(data["path"]).relative_to(KB).as_posix()
    item = PREVIEWS.get(preview_token)
    if not item or time.time() - item["created"] > 600:
        raise HTTPException(400, "预览不存在或已过期，请重新预览")
    if item["kind"] != "review" or item["payload"] != data:
        raise HTTPException(409, "提交内容与预览不一致")
    target = item["path"]
    _review_metadata(target)
    if _file_sha256(target) != item["payload"].get("content_sha256"):
        raise HTTPException(409, "页面内容已改变，请重新预览")
    if not payload.confirmed:
        raise HTTPException(400, "必须确认已完成人工专业复核")
    PREVIEWS.pop(preview_token, None)
    if DEMO_MODE:
        return {"status": "committed", "output": f"开发模拟确认完成：{data['path']}（未写入知识库）。", "health": "demo: skipped index and health commands"}
    target.write_text(update_frontmatter(target.read_text(encoding="utf-8"), item["changes"]), encoding="utf-8")
    _run(["index"])
    health = _run(["health"])
    return {"status": "committed", "output": f"已确认复核：{data['path']}", "health": health}


@app.post("/maintenance/v1/qa/preview")
def qa_preview(payload: QAPreview, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    data = payload.model_dump()
    slug = _slug(data["slug"], "qa-capture")
    args = ["qa-capture", "--question", data["question"], "--answer", data["answer"], "--slug", slug, "--source", data["source"]]
    for flag in ("title", "tags", "related"):
        if data[flag]: args.extend([f"--{flag}", data[flag]])
    return _preview("qa", data, args)


@app.post("/maintenance/v1/qa/commit")
def qa_commit(payload: QAPreview, preview_token: str, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    return _commit(preview_token, "qa", payload.model_dump())


@app.post("/maintenance/v1/ingest/preview")
def ingest_preview(payload: IngestPreview, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    data = payload.model_dump()
    source = _source_path(data.pop("source_path"))
    if not re.fullmatch(r"[a-zA-Z0-9/_-]{1,160}", data["raw_subdir"]):
        raise HTTPException(400, "raw_subdir 只能包含字母、数字、斜线、下划线和连字符")
    batch = _slug(data["batch_slug"], "source-batch")
    args = ["ingest-local", "--source", str(source), "--raw-subdir", data["raw_subdir"], "--batch-slug", batch, "--source-type", data["source_type"], "--official-source", data["official_source"], "--tags", data["tags"]]
    for flag in ("title", "official_url"):
        if data[flag]: args.extend([f"--{flag.replace('_', '-')}", data[flag]])
    data["source_path"] = str(source)
    return _preview("ingest", data, args)


@app.post("/maintenance/v1/ingest/commit")
def ingest_commit(payload: IngestPreview, preview_token: str, authorization: str | None = Header(default=None)) -> dict:
    _auth(authorization)
    data = payload.model_dump()
    data["source_path"] = str(_source_path(data["source_path"]))
    return _commit(preview_token, "ingest", data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
