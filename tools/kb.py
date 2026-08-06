from __future__ import annotations

import argparse

from kb_cli_support import add_enabled_flags, add_present_options, run_script


DEFAULT_KB_ROOT = "knowledge-base/CPA-ZH"

SIMPLE_COMMANDS = {
    "health": ("kb_health_check.py", []),
    "verify": ("verify_cpa_zh_delivery.py", []),
    "index": ("kb_search.py", ["index"]),
    "stats": ("kb_search.py", ["stats"]),
    "manifest": ("kb_manifest_audit.py", []),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified maintenance entrypoint for the CPA-ZH knowledge base."
    )
    parser.add_argument(
        "--root",
        default=DEFAULT_KB_ROOT,
        help=f"Knowledge base root. Default: {DEFAULT_KB_ROOT}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Run the one-command health check.")
    verify_parser = subparsers.add_parser("verify", help="Run the full migration and release verification gate.")
    verify_parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend tests and production build.")
    subparsers.add_parser("index", help="Rebuild the local search index.")
    subparsers.add_parser("stats", help="Show search index statistics.")

    search_parser = subparsers.add_parser("search", help="Search the local knowledge base.")
    search_parser.add_argument("query", nargs="+", help="Search words.")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum result count.")

    cache_parser = subparsers.add_parser("cache", help="Build or inspect raw text cache.")
    cache_subparsers = cache_parser.add_subparsers(dest="cache_command", required=True)
    cache_build_parser = cache_subparsers.add_parser("build", help="Build the raw text cache.")
    cache_build_parser.add_argument("--force", action="store_true", help="Refresh all cache entries.")
    cache_subparsers.add_parser("stats", help="Show text cache statistics.")

    subparsers.add_parser("manifest", help="Audit raw manifest consistency.")

    raw_audit_parser = subparsers.add_parser(
        "raw-audit", help="Audit raw/attachment dual-track source quality."
    )
    raw_audit_parser.add_argument(
        "--output", default="workspace/outputs/kb_dual_track_audit.md", help="Markdown report path."
    )

    raw_repair_parser = subparsers.add_parser(
        "raw-repair", help="Repair official raw sources and attachment mappings."
    )
    raw_repair_parser.add_argument(
        "--scope", choices=["accounting", "policies", "ethics", "all"], default="all"
    )
    raw_repair_parser.add_argument("--apply", action="store_true", help="Write repairs; default is dry-run.")
    raw_landing_repair_parser = subparsers.add_parser(
        "raw-landing-repair", help="Repair attachment-only application case landing pages."
    )
    raw_landing_repair_parser.add_argument("--apply", action="store_true", help="Write repairs; default is dry-run.")
    raw_index_repair_parser = subparsers.add_parser(
        "raw-index-repair", help="Repair application case column index Markdown pages."
    )
    raw_index_repair_parser.add_argument("--apply", action="store_true", help="Write repairs; default is dry-run.")
    raw_structure_parser = subparsers.add_parser(
        "raw-structure-audit", help="Audit structural fidelity of raw Markdown derivatives."
    )
    raw_structure_parser.add_argument(
        "--scope", choices=["authoritative", "cases", "lectures", "all"], default="all"
    )
    raw_structure_parser.add_argument(
        "--output", default="workspace/outputs/raw_structure_audit.md", help="Markdown report path."
    )
    raw_structure_parser.add_argument(
        "--write-maintenance-report", action="store_true", help="Also write wiki/_maintenance/raw-structure-review.md."
    )
    raw_reextract_parser = subparsers.add_parser(
        "raw-reextract", help="Rebuild raw Markdown with source-backed structure."
    )
    raw_reextract_parser.add_argument(
        "--scope", choices=["authoritative", "cases", "lectures", "all"], default="all"
    )
    raw_reextract_parser.add_argument(
        "--profile", choices=["faithful", "readable"], default="faithful"
    )
    raw_reextract_parser.add_argument("--apply", action="store_true", help="Write files; default is dry-run.")
    raw_reextract_parser.add_argument(
        "--output",
        default="workspace/outputs/raw_structure_reextract_report.md",
        help="Comparison report path.",
    )
    classify_parser = subparsers.add_parser("classify", help="Classify wiki/raw assets and build navigation data.")
    classify_parser.add_argument("classify_command", choices=["report", "apply", "build", "categories"])
    schema_parser = subparsers.add_parser("schema", help="Check wiki frontmatter and section governance.")
    schema_parser.add_argument("--write-report", action="store_true", help="Write the section upgrade dashboard.")
    schema_parser.add_argument(
        "--output",
        default="wiki/concepts/kb-section-upgrade-dashboard.md",
        help="Output path under the knowledge base root.",
    )
    completeness_parser = subparsers.add_parser(
        "completeness", help="Scan wiki pages for repeatable content-completeness gaps."
    )
    completeness_parser.add_argument(
        "--write-report", action="store_true", help="Write the Markdown and JSON completeness reports."
    )
    completeness_parser.add_argument(
        "--output",
        default="wiki/concepts/kb-content-completeness-report.md",
        help="Markdown report path under the knowledge base root.",
    )
    completeness_parser.add_argument(
        "--json-output",
        default="workspace/outputs/kb_completeness.json",
        help="JSON report path relative to the project root.",
    )
    governance_parser = subparsers.add_parser(
        "governance", help="Audit asset metadata, lifecycle, admission, and source-registry coverage."
    )
    governance_parser.add_argument("--write-report", action="store_true", help="Write the Markdown and JSON reports.")
    governance_parser.add_argument(
        "--output",
        default="wiki/concepts/kb-governance-dashboard.md",
        help="Markdown report path under the knowledge base root.",
    )
    governance_parser.add_argument(
        "--json-output",
        default="workspace/outputs/kb_governance.json",
        help="JSON report path relative to the project root.",
    )

    ingest_parser = subparsers.add_parser("ingest-local", help="Ingest local files into the raw archive.")
    ingest_parser.add_argument("--source", required=True, help="Local file or directory to ingest.")
    ingest_parser.add_argument("--raw-subdir", required=True, help="Target subdirectory under raw/.")
    ingest_parser.add_argument("--batch-slug", required=True, help="Batch slug used in manifest metadata.")
    ingest_parser.add_argument("--title", default="", help="Human-readable batch title.")
    ingest_parser.add_argument("--source-type", default="local-source", help="Source type stored in manifest.")
    ingest_parser.add_argument("--official-source", default="本地资料", help="Official/source label.")
    ingest_parser.add_argument("--official-url", default="", help="Official URL when available.")
    ingest_parser.add_argument("--official-page-status", default="local", help="official_page_status value.")
    ingest_parser.add_argument("--document-no", default="", help="Document number when all files share one.")
    ingest_parser.add_argument("--wiki-page", default="", help="Wiki page to link manifest items to.")
    ingest_parser.add_argument("--tags", default="", help="Comma-separated tags.")
    ingest_parser.add_argument("--source-page", default="", help="Optional wiki/sources page slug to create.")
    ingest_parser.add_argument("--source-label", default="", help="Portable source label stored instead of the local path.")
    ingest_parser.add_argument("--imported-on", default="", help="Import date, defaults to today.")
    ingest_parser.add_argument("--append", action="store_true", help="Append to an existing batch manifest.")
    ingest_parser.add_argument("--derived-markdown", default="", help="Extracted Markdown for a single source file.")
    ingest_parser.add_argument("--commit", action="store_true", help="Actually copy files and write metadata.")

    case_card_parser = subparsers.add_parser("case-card", help="Generate a draft case card from a local source file.")
    case_card_parser.add_argument("--source", required=True, help="Raw/local source file.")
    case_card_parser.add_argument("--slug", default="", help="Output case slug.")
    case_card_parser.add_argument("--title", default="", help="Case title.")
    case_card_parser.add_argument("--source-id", default="local-case-batch", help="Source page id without sources/ prefix.")
    case_card_parser.add_argument("--case-type", default="draft-case-card", help="case_type frontmatter value.")
    case_card_parser.add_argument("--raw-path", default="", help="Raw path to store in frontmatter.")
    case_card_parser.add_argument("--tags", default="", help="Comma-separated extra tags.")
    case_card_parser.add_argument("--related", default="", help="Comma-separated extra wiki links.")
    case_card_parser.add_argument("--commit", action="store_true", help="Write the draft into wiki/cases.")
    case_card_parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing case page.")

    case_index_parser = subparsers.add_parser("case-index", help="Suggest case-topic-index back-links.")
    case_index_parser.add_argument("--write-report", action="store_true", help="Write the suggestion report.")
    case_index_parser.add_argument(
        "--output",
        default="wiki/concepts/case-index-suggestion-report.md",
        help="Output path under the knowledge base root.",
    )

    qa_parser = subparsers.add_parser("qa-capture", help="Capture a local Q&A into wiki/questions.")
    qa_parser.add_argument("--question", default="", help="Question text.")
    qa_parser.add_argument("--answer", default="", help="Answer text.")
    qa_parser.add_argument("--question-file", default="", help="UTF-8 file containing the question.")
    qa_parser.add_argument("--answer-file", default="", help="UTF-8 file containing the answer.")
    qa_parser.add_argument("--title", default="", help="Page title.")
    qa_parser.add_argument("--slug", default="", help="Output slug.")
    qa_parser.add_argument("--source", default="local-qa-log", help="Source id stored in frontmatter.")
    qa_parser.add_argument("--tags", default="", help="Comma-separated extra tags.")
    qa_parser.add_argument("--related", default="", help="Comma-separated wiki links or slugs.")
    qa_parser.add_argument("--status", default="draft", help="Status value.")
    qa_parser.add_argument("--asked-on", default="", help="Question date, defaults to today in the helper.")
    qa_parser.add_argument("--commit", action="store_true", help="Write the question page.")
    qa_parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing question page.")

    archive_doc_parser = subparsers.add_parser("archive-doc", help="Archive one official/local source document.")
    archive_doc_parser.add_argument("--source", required=True, help="Local source file to archive.")
    archive_doc_parser.add_argument("--raw-subdir", required=True, help="Target manifest directory under raw/.")
    archive_doc_parser.add_argument("--slug", required=True, help="Item slug directory.")
    archive_doc_parser.add_argument("--title", required=True, help="Document title.")
    archive_doc_parser.add_argument("--document-no", default="", help="Document number.")
    archive_doc_parser.add_argument("--official-url", default="", help="Official page URL.")
    archive_doc_parser.add_argument("--attachment-url", default="", help="Official attachment URL.")
    archive_doc_parser.add_argument("--official-source", default="本地资料", help="Official/source label.")
    archive_doc_parser.add_argument("--official-page-status", default="local", help="verified/local/pending/etc.")
    archive_doc_parser.add_argument("--wiki-page", default="", help="Wiki page to link the item to.")
    archive_doc_parser.add_argument("--source-note", default="", help="Source note.")
    archive_doc_parser.add_argument("--content-type", default="", help="Override content type.")
    archive_doc_parser.add_argument("--text-extraction-status", default="", help="Override text extraction status.")
    archive_doc_parser.add_argument("--ocr-status", default="", help="Override OCR status.")
    archive_doc_parser.add_argument("--archived-on", default="", help="Archive date, defaults to today.")
    archive_doc_parser.add_argument("--append", action="store_true", help="Append to existing manifest.")
    archive_doc_parser.add_argument("--commit", action="store_true", help="Actually write files.")

    pdf_md_parser = subparsers.add_parser("pdf-md", help="Convert text-based PDFs to Markdown and flag OCR-needed PDFs.")
    pdf_md_parser.add_argument("--source", required=True, help="PDF file or directory containing PDFs.")
    pdf_md_parser.add_argument(
        "--output-subdir",
        default="cache/pdf-markdown/files",
        help="Output directory under the knowledge base root.",
    )
    pdf_md_parser.add_argument("--commit", action="store_true", help="Actually write Markdown files and manifest.")
    pdf_md_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing Markdown outputs.")
    pdf_md_parser.add_argument(
        "--engine",
        default="auto",
        choices=["auto", "pymupdf", "pdfplumber", "pdfminer", "pypdf"],
        help="Extraction engine. Default: auto.",
    )

    links_parser = subparsers.add_parser("links", help="Collect or check official URLs.")
    links_parser.add_argument("--include-wiki", action="store_true", help="Also collect URLs in wiki pages.")
    links_parser.add_argument("--check", action="store_true", help="Perform network checks.")
    links_parser.add_argument("--timeout", type=int, default=20, help="Network timeout seconds.")

    sources_parser = subparsers.add_parser("sources", help="Report raw source status.")
    sources_subparsers = sources_parser.add_subparsers(dest="sources_command", required=True)
    sources_subparsers.add_parser("summary", help="Print source status counts.")
    sources_report_parser = sources_subparsers.add_parser("write-report", help="Write the wiki source status dashboard.")
    sources_report_parser.add_argument(
        "--output",
        default="wiki/concepts/source-status-dashboard.md",
        help="Output path under the knowledge base root.",
    )

    readme_parser = subparsers.add_parser("readme", help="Refresh CPA-ZH README statistics.")
    readme_parser.add_argument("--date", default="", help="Date to write into README, defaults to today.")

    args = parser.parse_args()

    if args.command in SIMPLE_COMMANDS:
        script_name, script_args = SIMPLE_COMMANDS[args.command]
        if args.command == "verify" and args.skip_frontend:
            script_args = ["--skip-frontend"]
        return run_script(script_name, args.root, script_args)
    if args.command == "search":
        return run_script(
            "kb_search.py",
            args.root,
            ["query", " ".join(args.query), "--limit", str(args.limit)],
        )
    if args.command == "cache":
        cache_args = [args.cache_command]
        if args.cache_command == "build" and args.force:
            cache_args.append("--force")
        return run_script("kb_text_cache.py", args.root, cache_args)
    if args.command == "schema":
        schema_args: list[str] = []
        if args.write_report:
            schema_args.append("--write-report")
        if args.output != "wiki/concepts/kb-section-upgrade-dashboard.md":
            schema_args.extend(["--output", args.output])
        return run_script("kb_schema_check.py", args.root, schema_args)
    if args.command == "completeness":
        completeness_args: list[str] = []
        if args.write_report:
            completeness_args.append("--write-report")
        if args.output != "wiki/concepts/kb-content-completeness-report.md":
            completeness_args.extend(["--output", args.output])
        if args.json_output != "workspace/outputs/kb_completeness.json":
            completeness_args.extend(["--json-output", args.json_output])
        return run_script("kb_completeness.py", args.root, completeness_args)
    if args.command == "governance":
        governance_args: list[str] = []
        if args.write_report:
            governance_args.append("--write-report")
        if args.output != "wiki/concepts/kb-governance-dashboard.md":
            governance_args.extend(["--output", args.output])
        if args.json_output != "workspace/outputs/kb_governance.json":
            governance_args.extend(["--json-output", args.json_output])
        return run_script("kb_governance.py", args.root, governance_args)
    if args.command == "raw-audit":
        return run_script("kb_dual_track_audit.py", args.root, ["--output", args.output])
    if args.command == "raw-repair":
        repair_args = ["--scope", args.scope]
        if args.apply:
            repair_args.append("--apply")
        return run_script("kb_raw_repair.py", args.root, repair_args)
    if args.command == "raw-landing-repair":
        repair_args = []
        if args.apply:
            repair_args.append("--apply")
        return run_script("repair_application_case_landing_pages.py", args.root, repair_args)
    if args.command == "raw-index-repair":
        repair_args = []
        if args.apply:
            repair_args.append("--apply")
        return run_script("repair_application_case_index_pages.py", args.root, repair_args)
    if args.command == "raw-structure-audit":
        structure_args = ["audit", "--scope", args.scope, "--output", args.output]
        if args.write_maintenance_report:
            structure_args.append("--write-maintenance-report")
        return run_script(
            "kb_raw_structure.py",
            args.root,
            structure_args,
        )
    if args.command == "raw-reextract":
        structure_args = [
            "reextract",
            "--scope",
            args.scope,
            "--profile",
            args.profile,
            "--output",
            args.output,
        ]
        if args.apply:
            structure_args.append("--apply")
        return run_script("kb_raw_structure.py", args.root, structure_args)
    if args.command == "classify":
        return run_script("classify_wiki.py", args.root, [args.classify_command])
    if args.command == "ingest-local":
        ingest_args = [
            "--source",
            args.source,
            "--raw-subdir",
            args.raw_subdir,
            "--batch-slug",
            args.batch_slug,
            "--source-type",
            args.source_type,
            "--official-source",
            args.official_source,
            "--official-page-status",
            args.official_page_status,
        ]
        optional_pairs = {
            "--title": args.title,
            "--official-url": args.official_url,
            "--document-no": args.document_no,
            "--wiki-page": args.wiki_page,
            "--tags": args.tags,
            "--source-page": args.source_page,
            "--source-label": args.source_label,
            "--imported-on": args.imported_on,
            "--derived-markdown": args.derived_markdown,
        }
        add_present_options(ingest_args, optional_pairs)
        add_enabled_flags(ingest_args, {"--append": args.append, "--commit": args.commit})
        return run_script("kb_ingest_local.py", args.root, ingest_args)
    if args.command == "case-card":
        case_args = ["--source", args.source]
        optional_pairs = {
            "--slug": args.slug,
            "--title": args.title,
            "--source-id": args.source_id,
            "--case-type": args.case_type,
            "--raw-path": args.raw_path,
            "--tags": args.tags,
            "--related": args.related,
        }
        add_present_options(case_args, optional_pairs)
        add_enabled_flags(case_args, {"--commit": args.commit, "--overwrite": args.overwrite})
        return run_script("kb_case_card.py", args.root, case_args)
    if args.command == "case-index":
        case_index_args: list[str] = []
        if args.write_report:
            case_index_args.append("--write-report")
        if args.output != "wiki/concepts/case-index-suggestion-report.md":
            case_index_args.extend(["--output", args.output])
        return run_script("kb_case_index_suggest.py", args.root, case_index_args)
    if args.command == "qa-capture":
        qa_args: list[str] = []
        optional_pairs = {
            "--question": args.question,
            "--answer": args.answer,
            "--question-file": args.question_file,
            "--answer-file": args.answer_file,
            "--title": args.title,
            "--slug": args.slug,
            "--source": args.source,
            "--tags": args.tags,
            "--related": args.related,
            "--status": args.status,
            "--asked-on": args.asked_on,
        }
        add_present_options(qa_args, optional_pairs)
        add_enabled_flags(qa_args, {"--commit": args.commit, "--overwrite": args.overwrite})
        return run_script("kb_qa_capture.py", args.root, qa_args)
    if args.command == "archive-doc":
        archive_args = [
            "--source",
            args.source,
            "--raw-subdir",
            args.raw_subdir,
            "--slug",
            args.slug,
            "--title",
            args.title,
            "--official-source",
            args.official_source,
            "--official-page-status",
            args.official_page_status,
        ]
        optional_pairs = {
            "--document-no": args.document_no,
            "--official-url": args.official_url,
            "--attachment-url": args.attachment_url,
            "--wiki-page": args.wiki_page,
            "--source-note": args.source_note,
            "--content-type": args.content_type,
            "--text-extraction-status": args.text_extraction_status,
            "--ocr-status": args.ocr_status,
            "--archived-on": args.archived_on,
        }
        add_present_options(archive_args, optional_pairs)
        add_enabled_flags(archive_args, {"--append": args.append, "--commit": args.commit})
        return run_script("kb_archive_doc.py", args.root, archive_args)
    if args.command == "pdf-md":
        pdf_md_args = [
            "--source",
            args.source,
            "--output-subdir",
            args.output_subdir,
            "--engine",
            args.engine,
        ]
        if args.commit:
            pdf_md_args.append("--commit")
        if args.overwrite:
            pdf_md_args.append("--overwrite")
        return run_script("kb_pdf_to_markdown.py", args.root, pdf_md_args)
    if args.command == "links":
        link_args: list[str] = []
        if args.include_wiki:
            link_args.append("--include-wiki")
        if args.check:
            link_args.append("--check")
        if args.timeout != 20:
            link_args.extend(["--timeout", str(args.timeout)])
        return run_script("kb_link_check.py", args.root, link_args)
    if args.command == "sources":
        source_args = [args.sources_command]
        if args.sources_command == "write-report" and args.output != "wiki/concepts/source-status-dashboard.md":
            source_args.extend(["--output", args.output])
        return run_script("kb_source_status.py", args.root, source_args)
    if args.command == "readme":
        readme_args = ["--date", args.date] if args.date else []
        return run_script("kb_update_readme_stats.py", args.root, readme_args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
