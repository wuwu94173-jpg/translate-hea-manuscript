#!/usr/bin/env python3
"""Convert text-based scholarly PDFs to traceable Markdown.

The converter intentionally preserves page boundaries. It does not claim to
recover equations, tables, or reading order perfectly; those limitations are
reported so the calling agent can route low-quality files to OCR or visual QA.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def yaml_string(value: Any) -> str:
    text = "" if value is None else str(value)
    return json.dumps(text, ensure_ascii=False)


def clean_text(text: str) -> str:
    text = CONTROL_CHARS.sub("", text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if cleaned and not blank:
                cleaned.append("")
            blank = True
            continue
        cleaned.append(stripped)
        blank = False
    return "\n".join(cleaned).strip()


def extract_pages(pdf_path: Path) -> tuple[list[str], str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "pypdf is required. In Codex Desktop, run this script with the "
            "bundled workspace Python runtime."
        ) from exc

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        try:
            pages.append(clean_text(page.extract_text() or ""))
        except Exception as exc:  # malformed pages should not abort the corpus
            pages.append(f"[Page extraction failed: {type(exc).__name__}: {exc}]")
    return pages, "pypdf"


def render_markdown(
    pages: Iterable[str], metadata: dict[str, Any], source_pdf: Path, backend: str
) -> tuple[str, dict[str, Any]]:
    page_list = list(pages)
    char_counts = [len(page) for page in page_list]
    low_text_pages = [i + 1 for i, count in enumerate(char_counts) if count < 80]
    frontmatter = [
        "---",
        f"title: {yaml_string(metadata.get('title'))}",
        f"authors: {yaml_string(metadata.get('authors'))}",
        f"journal: {yaml_string(metadata.get('journal'))}",
        f"year: {yaml_string(metadata.get('year'))}",
        f"doi: {yaml_string(metadata.get('doi'))}",
        f"openalex_id: {yaml_string(metadata.get('openalex_id'))}",
        f"license: {yaml_string(metadata.get('license'))}",
        f"source_origin: {yaml_string(metadata.get('source_origin'))}",
        f"source_local_path: {yaml_string(metadata.get('source_local_path'))}",
        f"source_sha256: {yaml_string(metadata.get('source_sha256'))}",
        f"source_pdf: {yaml_string(source_pdf.name)}",
        f"main_translation_use: {yaml_string(metadata.get('main_translation_use'))}",
        f"language_quality: {yaml_string(metadata.get('language_quality'))}",
        f"conversion_backend: {yaml_string(backend)}",
        "---",
        "",
        "> Automated text-layer extraction. Verify equations, tables, symbols, "
        "multi-column reading order, and pages flagged as low text before use.",
        "",
    ]
    body: list[str] = []
    for page_number, page_text in enumerate(page_list, 1):
        body.extend([f"## Page {page_number}", "", page_text or "[No extractable text]", ""])
    report = {
        "source_pdf": str(source_pdf),
        "pages": len(page_list),
        "total_characters": sum(char_counts),
        "average_characters_per_page": round(sum(char_counts) / max(len(page_list), 1), 1),
        "low_text_pages": low_text_pages,
        "ocr_or_visual_qa_recommended": bool(low_text_pages),
        "backend": backend,
    }
    return "\n".join(frontmatter + body).rstrip() + "\n", report


def convert_pdf(
    pdf_path: Path,
    markdown_path: Path,
    metadata: dict[str, Any] | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    pdf_path = pdf_path.resolve()
    markdown_path = markdown_path.resolve()
    if markdown_path.exists() and not overwrite:
        return {
            "source_pdf": str(pdf_path),
            "markdown": str(markdown_path),
            "status": "exists",
        }
    pages, backend = extract_pages(pdf_path)
    markdown, report = render_markdown(pages, metadata or {}, pdf_path, backend)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown, encoding="utf-8")
    report.update({"markdown": str(markdown_path), "status": "converted"})
    return report


def load_metadata(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Metadata JSON must be an object.")
    return data


def iter_pdfs(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.glob("*.pdf") if p.is_file())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a scholarly PDF or directory of PDFs to page-anchored Markdown."
    )
    parser.add_argument("input", type=Path, help="PDF file or directory containing PDFs")
    parser.add_argument("--output-dir", type=Path, help="Markdown output directory")
    parser.add_argument("--metadata-json", type=Path, help="Metadata object for a single PDF")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing Markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Input does not exist: {input_path}", file=sys.stderr)
        return 2
    pdfs = iter_pdfs(input_path)
    if not pdfs:
        print(f"No PDFs found: {input_path}", file=sys.stderr)
        return 2
    output_dir = (args.output_dir or (input_path.parent if input_path.is_file() else input_path)).resolve()
    metadata = load_metadata(args.metadata_json)
    reports = []
    for pdf in pdfs:
        report = convert_pdf(pdf, output_dir / f"{pdf.stem}.md", metadata, args.overwrite)
        reports.append(report)
        print(f"{report['status']}: {pdf.name}")
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
