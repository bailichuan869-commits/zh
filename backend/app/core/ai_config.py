from __future__ import annotations

import json
import ipaddress
import os
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_CONFIG = {
    "provider": "openai-compatible",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4.1-mini",
    "enabled": False,
    "api_key": "",
}


def validate_base_url(base_url: str) -> str:
    normalized = base_url.strip().rstrip("/")
    parsed = urlparse(normalized)
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("服务地址必须是有效的 HTTPS 地址")
    try:
        loopback = ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        loopback = parsed.hostname.lower() == "localhost"
    if parsed.scheme != "https" and not (parsed.scheme == "http" and loopback):
        raise ValueError("服务地址必须使用 HTTPS；仅本机回环地址允许 HTTP")
    return normalized


def config_path() -> Path:
    configured = os.environ.get("CPA_ZH_AI_CONFIG_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    local_app_data = os.environ.get("LOCALAPPDATA")
    root = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
    return root / "CPA-ZH" / "ai-config.json"


def load_ai_config() -> dict[str, object]:
    config = dict(DEFAULT_CONFIG)
    path = config_path()
    if not path.exists():
        return config
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return config
    if isinstance(saved, dict):
        config.update({key: saved[key] for key in DEFAULT_CONFIG if key in saved})
    return config


def public_ai_config() -> dict[str, object]:
    config = load_ai_config()
    return {
        "provider": str(config["provider"]),
        "base_url": str(config["base_url"]),
        "model": str(config["model"]),
        "enabled": bool(config["enabled"]),
        "key_configured": bool(config["api_key"]),
    }


def save_ai_config(provider: str, base_url: str, model: str, enabled: bool, api_key: str) -> dict[str, object]:
    normalized_base_url = validate_base_url(base_url)
    if not model.strip():
        raise ValueError("模型名称不能为空")
    previous = load_ai_config()
    previous_base_url = str(previous["base_url"]).rstrip("/")
    retained_key = str(previous["api_key"]) if normalized_base_url == previous_base_url else ""
    config = {
        "provider": provider.strip() or "openai-compatible",
        "base_url": normalized_base_url,
        "model": model.strip(),
        "enabled": enabled,
        "api_key": api_key.strip() or retained_key,
    }
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(config, handle, ensure_ascii=False)
        temporary_path = Path(handle.name)
    os.replace(temporary_path, path)
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return public_ai_config()


def test_ai_connection() -> dict[str, str]:
    config = load_ai_config()
    if not config["enabled"] or not config["api_key"]:
        raise ValueError("请先启用配置并保存 API 密钥")
    base_url = validate_base_url(str(config["base_url"]))
    request = urllib.request.Request(
        f"{base_url}/models",
        headers={"Authorization": f"Bearer {config['api_key']}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if not 200 <= response.status < 300:
                raise ValueError(f"服务返回 HTTP {response.status}")
    except urllib.error.HTTPError as error:
        raise ValueError(f"服务返回 HTTP {error.code}") from None
    except urllib.error.URLError:
        raise ValueError("无法连接到模型服务") from None
    return {"status": "ok", "message": "模型服务连接成功"}
