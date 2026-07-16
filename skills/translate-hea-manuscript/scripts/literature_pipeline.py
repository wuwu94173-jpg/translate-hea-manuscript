#!/usr/bin/env python3
"""Discover, rank, download, and convert open-access HEA literature.

The default policy downloads only PDF locations carrying a Creative Commons
or public-domain license in OpenAlex metadata. The script never bypasses a
paywall and never logs an API key.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


DEFAULT_QUERIES = [
    '"refractory high-entropy alloy" NbTaMoW',
    '"NbMoTaW" OR "NbTaMoW" first-principles',
    '"special quasirandom structure" "high-entropy alloy"',
    '"elastic properties" "refractory high-entropy alloy"',
    'nanoindentation "refractory high-entropy alloy"',
    '(XRD OR "X-ray diffraction") "refractory high-entropy alloy"',
    '("density of states" OR DOS) "refractory high-entropy alloy"',
    '(XPS OR "valence-band spectrum") "high-entropy alloy"',
]

CORE_JOURNALS = {
    "acta materialia",
    "scripta materialia",
    "journal of alloys and compounds",
    "intermetallics",
    "materials & design",
    "materials and design",
    "computational materials science",
    "applied surface science",
    "physical review b",
    "journal of materials research and technology",
    "materials science and engineering: a",
    "materials science and engineering a",
}

TOPIC_WEIGHTS = {
    "nbtamow": 18,
    "nbmotaw": 18,
    "nbtamowre": 24,
    "refractory high-entropy alloy": 14,
    "refractory high entropy alloy": 14,
    "special quasirandom structure": 8,
    "atat": 6,
    "castep": 6,
    "first-principles": 5,
    "density functional theory": 5,
    "nanoindentation": 6,
    "x-ray diffraction": 4,
    "density of states": 6,
    "pseudogap": 5,
    "orbital hybridization": 5,
    "xps": 5,
    "valence-band": 5,
}

LEARNING_USE_RULES = {
    "Introduction": ["high-entropy alloy", "refractory", "alloy design"],
    "Computational Methods": [
        "special quasirandom",
        "sqs",
        "atat",
        "castep",
        "first-principles",
        "density functional",
    ],
    "Experimental Methods": ["arc melting", "sem", "eds", "xrd", "x-ray diffraction"],
    "Phase Structure": ["phase", "lattice", "xrd", "diffraction", "microstructure"],
    "Mechanical Properties": [
        "elastic",
        "modulus",
        "hardness",
        "nanoindentation",
        "mechanical",
    ],
    "Electronic Structure": [
        "density of states",
        "electronic structure",
        "xps",
        "valence band",
        "pseudogap",
        "hybridization",
    ],
    "Figure Captions": ["xrd", "spectrum", "micrograph", "load-displacement"],
}

CC_MARKERS = ("cc-by", "cc by", "cc0", "public-domain", "public domain")
SAFE_SCHEMES = {"http", "https"}


def normalize_space(value: Any) -> str:
    return re.sub(r"\s+", " ", "" if value is None else str(value)).strip()


def normalize_doi(value: Any) -> str:
    doi = normalize_space(value).lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
    return doi


def inverted_abstract(index: Any) -> str:
    if not isinstance(index, dict):
        return ""
    positioned: list[tuple[int, str]] = []
    for word, positions in index.items():
        if not isinstance(positions, list):
            continue
        for position in positions:
            if isinstance(position, int):
                positioned.append((position, str(word)))
    positioned.sort()
    return " ".join(word for _, word in positioned)


def location_source(location: Any) -> dict[str, Any]:
    if not isinstance(location, dict):
        return {}
    source = location.get("source")
    return source if isinstance(source, dict) else {}


def authors_from_work(work: dict[str, Any]) -> list[str]:
    authors: list[str] = []
    for authorship in work.get("authorships") or []:
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author") or {}
        name = normalize_space(author.get("display_name") if isinstance(author, dict) else "")
        if name:
            authors.append(name)
    return authors


def is_cc_license(location: dict[str, Any]) -> bool:
    value = " ".join(
        normalize_space(location.get(field)).lower() for field in ("license", "license_id")
    )
    return any(marker in value for marker in CC_MARKERS)


def choose_pdf_location(
    work: dict[str, Any], license_policy: str
) -> tuple[str, str, str, str]:
    candidates: list[dict[str, Any]] = []
    for key in ("best_oa_location", "primary_location"):
        location = work.get(key)
        if isinstance(location, dict):
            candidates.append(location)
    for location in work.get("locations") or []:
        if isinstance(location, dict):
            candidates.append(location)

    seen: set[str] = set()
    work_is_oa = bool((work.get("open_access") or {}).get("is_oa"))
    fallback_landing = ""
    for location in candidates:
        landing = normalize_space(location.get("landing_page_url"))
        fallback_landing = fallback_landing or landing
        pdf_url = normalize_space(location.get("pdf_url"))
        if not pdf_url or pdf_url in seen:
            continue
        seen.add(pdf_url)
        parsed = urllib.parse.urlparse(pdf_url)
        if parsed.scheme.lower() not in SAFE_SCHEMES or not parsed.hostname:
            continue
        location_is_oa = location.get("is_oa") is True or work_is_oa
        if not location_is_oa:
            continue
        if license_policy == "cc-only" and not is_cc_license(location):
            continue
        license_value = normalize_space(location.get("license") or location.get("license_id"))
        version = normalize_space(location.get("version"))
        return pdf_url, landing, license_value, version
    return "", fallback_landing, "", ""


def learning_uses(text: str) -> list[str]:
    lowered = text.lower()
    uses = [name for name, terms in LEARNING_USE_RULES.items() if any(t in lowered for t in terms)]
    return uses or ["Introduction"]


def score_record(record: dict[str, Any]) -> float:
    text = f"{record['title']} {record['abstract']}".lower()
    score = math.log1p(max(float(record.get("openalex_relevance") or 0), 0)) * 4
    for phrase, weight in TOPIC_WEIGHTS.items():
        if phrase and phrase in text:
            score += weight
    if record.get("journal", "").lower() in CORE_JOURNALS:
        score += 8
    if record.get("pdf_url"):
        score += 4
    if record.get("license"):
        score += 2
    score += min(math.log1p(max(int(record.get("cited_by_count") or 0), 0)), 6)
    score += min(len(record.get("main_translation_use") or []), 5)
    return round(score, 3)


def record_from_work(
    work: dict[str, Any], matched_query: str, license_policy: str
) -> dict[str, Any] | None:
    if work.get("is_retracted") or work.get("is_paratext"):
        return None
    title = normalize_space(work.get("display_name") or work.get("title"))
    if not title:
        return None
    primary = work.get("primary_location") if isinstance(work.get("primary_location"), dict) else {}
    best = work.get("best_oa_location") if isinstance(work.get("best_oa_location"), dict) else {}
    source = location_source(primary) or location_source(best)
    authors = authors_from_work(work)
    abstract = inverted_abstract(work.get("abstract_inverted_index"))
    pdf_url, landing_url, license_value, version = choose_pdf_location(work, license_policy)
    record: dict[str, Any] = {
        "openalex_id": normalize_space(work.get("id")),
        "doi": normalize_doi(work.get("doi")),
        "title": title,
        "authors": authors,
        "authors_text": "; ".join(authors),
        "first_author": authors[0] if authors else "unknown",
        "journal": normalize_space(source.get("display_name")),
        "year": work.get("publication_year") or "",
        "publication_date": normalize_space(work.get("publication_date")),
        "type": normalize_space(work.get("type")),
        "language": normalize_space(work.get("language")),
        "cited_by_count": int(work.get("cited_by_count") or 0),
        "abstract": abstract,
        "landing_page_url": landing_url,
        "pdf_url": pdf_url,
        "license": license_value,
        "oa_version": version,
        "oa_status": normalize_space((work.get("open_access") or {}).get("oa_status")),
        "openalex_relevance": work.get("relevance_score") or 0,
        "matched_queries": [matched_query] if matched_query else [],
        "main_translation_use": learning_uses(f"{title} {abstract}"),
        "download_status": "pending" if pdf_url else "not_eligible",
        "download_error": "",
        "pdf_filename": "",
        "pdf_sha256": "",
        "markdown_filename": "",
        "conversion_status": "pending" if pdf_url else "not_applicable",
    }
    record["score"] = score_record(record)
    return record


def dedupe_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record in records:
        key = record.get("doi") or record.get("openalex_id") or record.get("title", "").lower()
        if key not in merged:
            merged[key] = record
            continue
        current = merged[key]
        current["matched_queries"] = sorted(
            set(current.get("matched_queries") or []) | set(record.get("matched_queries") or [])
        )
        current["main_translation_use"] = sorted(
            set(current.get("main_translation_use") or [])
            | set(record.get("main_translation_use") or [])
        )
        if record.get("pdf_url") and not current.get("pdf_url"):
            for field in ("pdf_url", "landing_page_url", "license", "oa_version"):
                current[field] = record.get(field, "")
            current["download_status"] = "pending"
        current["score"] = max(float(current.get("score") or 0), float(record.get("score") or 0))
    return sorted(merged.values(), key=lambda item: (-float(item["score"]), str(item["title"])))


def request_json(url: str, user_agent: str, timeout: int, retries: int = 3) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
            time.sleep(min(delay, 30))
        except urllib.error.URLError:
            if attempt == retries:
                raise
            time.sleep(min(2**attempt, 30))
    raise RuntimeError("Unreachable retry state")


def build_openalex_url(args: argparse.Namespace, query: str) -> str:
    filters = ["type:article", "language:en", "is_retracted:false", "is_paratext:false"]
    if args.from_year:
        filters.append(f"from_publication_date:{args.from_year}-01-01")
    if args.to_year:
        filters.append(f"to_publication_date:{args.to_year}-12-31")
    fields = [
        "id",
        "doi",
        "display_name",
        "publication_year",
        "publication_date",
        "type",
        "language",
        "cited_by_count",
        "is_retracted",
        "is_paratext",
        "primary_location",
        "locations",
        "best_oa_location",
        "open_access",
        "authorships",
        "abstract_inverted_index",
        "relevance_score",
    ]
    params = {
        "search": query,
        "filter": ",".join(filters),
        "per_page": str(args.per_query),
        "select": ",".join(fields),
    }
    if args.api_key:
        params["api_key"] = args.api_key
    if args.mailto:
        params["mailto"] = args.mailto
    return "https://api.openalex.org/works?" + urllib.parse.urlencode(params)


def load_queries(args: argparse.Namespace) -> list[str]:
    queries = list(args.query or [])
    if args.query_file:
        queries.extend(
            line.strip()
            for line in args.query_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    return queries or list(DEFAULT_QUERIES)


def load_metadata_file(path: Path, license_policy: str) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        works = data.get("results") or data.get("works") or []
    elif isinstance(data, list):
        works = data
    else:
        raise ValueError("Metadata file must contain a list or an object with results/works.")
    records = []
    for work in works:
        if isinstance(work, dict):
            record = record_from_work(work, "offline-metadata", license_policy)
            if record:
                records.append(record)
    return records


def sanitize_filename(value: str, limit: int = 70) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return (value or "paper")[:limit]


def paper_filename(record: dict[str, Any], index: int) -> str:
    digest_source = record.get("doi") or record.get("openalex_id") or record.get("title")
    digest = hashlib.sha1(str(digest_source).encode("utf-8")).hexdigest()[:8]
    author = sanitize_filename(str(record.get("first_author") or "unknown"), 20)
    title = sanitize_filename(str(record.get("title") or "paper"), 55)
    year = sanitize_filename(str(record.get("year") or "nd"), 8)
    return f"{index:02d}_{year}_{author}_{title}_{digest}.pdf"


def validate_remote_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() not in SAFE_SCHEMES or not parsed.hostname:
        raise ValueError("Only public HTTP(S) PDF URLs are accepted.")
    if parsed.username or parsed.password:
        raise ValueError("Credential-bearing URLs are not accepted.")
    host = parsed.hostname.lower()
    if host in {"localhost", "127.0.0.1", "::1"} or host.endswith(".local"):
        raise ValueError("Local or private hosts are not accepted.")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address and (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
    ):
        raise ValueError("Local or private IP addresses are not accepted.")


def download_pdf(
    url: str,
    destination: Path,
    user_agent: str,
    timeout: int,
    max_bytes: int,
    overwrite: bool,
) -> tuple[str, str]:
    if destination.exists() and not overwrite:
        with destination.open("rb") as existing:
            if existing.read(5) != b"%PDF-":
                raise ValueError("Existing file is not a PDF; use --overwrite after inspection.")
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        return "exists", digest
    validate_remote_url(url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.1",
        },
    )
    temporary = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    total = 0
    first_chunk = b""
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, temporary.open("wb") as output:
            validate_remote_url(response.geturl())
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                if not first_chunk:
                    first_chunk = chunk[:16]
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError(f"PDF exceeds size limit ({max_bytes} bytes).")
                digest.update(chunk)
                output.write(chunk)
        if not first_chunk.startswith(b"%PDF-"):
            raise ValueError("Downloaded content is not a PDF.")
        temporary.replace(destination)
        return "downloaded", digest.hexdigest()
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def markdown_escape(value: Any) -> str:
    return normalize_space(value).replace("|", "\\|")


def write_indexes(base: Path, records: list[dict[str, Any]], license_policy: str) -> None:
    index_dir = base / "02_reference_papers"
    index_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "license_policy": license_policy,
        "papers": records,
    }
    (index_dir / "download_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    csv_fields = [
        "rank",
        "score",
        "title",
        "authors_text",
        "journal",
        "year",
        "doi",
        "openalex_id",
        "cited_by_count",
        "oa_status",
        "license",
        "oa_version",
        "landing_page_url",
        "pdf_url",
        "download_status",
        "download_error",
        "pdf_filename",
        "pdf_sha256",
        "conversion_status",
        "markdown_filename",
        "main_translation_use_text",
        "matched_queries_text",
    ]
    with (index_dir / "literature_index.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for rank, record in enumerate(records, 1):
            row = dict(record)
            row["rank"] = rank
            row["main_translation_use_text"] = "; ".join(record.get("main_translation_use") or [])
            row["matched_queries_text"] = "; ".join(record.get("matched_queries") or [])
            writer.writerow({field: row.get(field, "") for field in csv_fields})

    lines = [
        "# Literature index",
        "",
        "> Automatically ranked candidates. Validate scientific relevance and source quality before treating a paper as core corpus evidence.",
        "",
        f"License policy: `{license_policy}`",
        "",
        "| Rank | Score | Year | Paper | Journal | OA/license | Status | Translation use |",
        "|---:|---:|---:|---|---|---|---|---|",
    ]
    for rank, record in enumerate(records, 1):
        doi = record.get("doi")
        title = markdown_escape(record.get("title"))
        paper = f"[{title}](https://doi.org/{doi})" if doi else title
        oa = "/".join(filter(None, [record.get("oa_status"), record.get("license")])) or "metadata only"
        lines.append(
            "| {rank} | {score} | {year} | {paper} | {journal} | {oa} | {status} | {uses} |".format(
                rank=rank,
                score=record.get("score", ""),
                year=markdown_escape(record.get("year")),
                paper=paper,
                journal=markdown_escape(record.get("journal")),
                oa=markdown_escape(oa),
                status=markdown_escape(record.get("download_status")),
                uses=markdown_escape(", ".join(record.get("main_translation_use") or [])),
            )
        )
    (index_dir / "literature_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    queue = [
        "# Literature learning queue",
        "",
        "Process downloaded Markdown in rank order. Extract terminology and reusable patterns with page anchors; do not copy paper-specific prose into the manuscript.",
        "",
    ]
    for rank, record in enumerate(records, 1):
        if not record.get("markdown_filename"):
            continue
        queue.extend(
            [
                f"## {rank}. {record['title']}",
                "",
                f"- Markdown: `markdown/{record['markdown_filename']}`",
                f"- DOI: `{record.get('doi') or 'none'}`",
                f"- Translation use: {', '.join(record.get('main_translation_use') or [])}",
                "- Extract: canonical terms, evidence-calibrated verbs, abstracted sentence patterns, paragraph logic, and caption patterns.",
                "- Record: page anchor, DOI, context, evidence strength, replaceable slots, and misuse warning.",
                "",
            ]
        )
    (index_dir / "learning_queue.md").write_text("\n".join(queue), encoding="utf-8")


def run_conversion(
    record: dict[str, Any], pdf_dir: Path, markdown_dir: Path, overwrite: bool
) -> None:
    if not record.get("pdf_filename"):
        return
    try:
        from pdf_to_markdown import convert_pdf

        metadata = {
            "title": record.get("title"),
            "authors": record.get("authors_text"),
            "journal": record.get("journal"),
            "year": record.get("year"),
            "doi": record.get("doi"),
            "openalex_id": record.get("openalex_id"),
            "license": record.get("license"),
            "main_translation_use": ", ".join(record.get("main_translation_use") or []),
            "language_quality": "pending agent review",
        }
        pdf_path = pdf_dir / record["pdf_filename"]
        markdown_name = f"{pdf_path.stem}.md"
        report = convert_pdf(pdf_path, markdown_dir / markdown_name, metadata, overwrite)
        record["markdown_filename"] = markdown_name
        record["conversion_status"] = report.get("status", "converted")
        record["conversion_report"] = report
    except Exception as exc:
        record["conversion_status"] = "failed"
        record["conversion_error"] = f"{type(exc).__name__}: {exc}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an indexed, license-aware open-access HEA literature corpus."
    )
    parser.add_argument("--output-dir", type=Path, required=True, help="HEA translation project directory")
    parser.add_argument("--query", action="append", help="OpenAlex search query; repeatable")
    parser.add_argument("--query-file", type=Path, help="UTF-8 file with one query per line")
    parser.add_argument("--metadata-file", type=Path, help="Offline OpenAlex JSON response for testing/reprocessing")
    parser.add_argument("--max-results", type=int, default=25, help="Maximum ranked corpus candidates (default: 25)")
    parser.add_argument("--per-query", type=int, default=25, help="Results requested per query, 1-100")
    parser.add_argument("--from-year", type=int, help="Earliest publication year")
    parser.add_argument("--to-year", type=int, help="Latest publication year")
    parser.add_argument("--mailto", default=os.environ.get("OPENALEX_MAILTO", ""), help="Contact email for API etiquette")
    parser.add_argument("--download", action="store_true", help="Download eligible OA PDFs")
    parser.add_argument("--convert", action="store_true", help="Convert downloaded PDFs to Markdown")
    parser.add_argument(
        "--license-policy",
        choices=("cc-only", "any-oa"),
        default="cc-only",
        help="Default cc-only is conservative; any-oa still requires an OA PDF location",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing PDFs/Markdown")
    parser.add_argument("--timeout", type=int, default=45, help="Network timeout in seconds")
    parser.add_argument("--max-pdf-mb", type=int, default=50, help="Maximum PDF size")
    parser.set_defaults(api_key=os.environ.get("OPENALEX_API_KEY", ""))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.per_query <= 100:
        print("--per-query must be between 1 and 100", file=sys.stderr)
        return 2
    if not 1 <= args.max_results <= 100:
        print("--max-results must be between 1 and 100", file=sys.stderr)
        return 2
    if args.convert and not args.download and not args.metadata_file:
        print("--convert normally requires --download or an offline metadata file", file=sys.stderr)
        return 2

    output_dir = args.output_dir.resolve()
    pdf_dir = output_dir / "02_reference_papers" / "pdf"
    markdown_dir = output_dir / "02_reference_papers" / "markdown"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    markdown_dir.mkdir(parents=True, exist_ok=True)

    user_agent = "translate-hea-manuscript/1.1"
    if args.mailto:
        user_agent += f" (mailto:{args.mailto})"
    raw_records: list[dict[str, Any]] = []
    if args.metadata_file:
        raw_records.extend(load_metadata_file(args.metadata_file.resolve(), args.license_policy))
    else:
        if not args.api_key:
            print("Warning: no OpenAlex API key; current no-key daily allowance is intended for light trials.", file=sys.stderr)
        for query in load_queries(args):
            url = build_openalex_url(args, query)
            try:
                payload = request_json(url, user_agent, args.timeout)
            except Exception as exc:
                print(f"Search failed for {query!r}: {type(exc).__name__}: {exc}", file=sys.stderr)
                continue
            for work in payload.get("results") or []:
                if isinstance(work, dict):
                    record = record_from_work(work, query, args.license_policy)
                    if record:
                        raw_records.append(record)

    records = dedupe_records(raw_records)[: args.max_results]
    if not records:
        print("No candidate works were produced.", file=sys.stderr)
        write_indexes(output_dir, [], args.license_policy)
        return 1

    for rank, record in enumerate(records, 1):
        if args.download and record.get("pdf_url"):
            filename = paper_filename(record, rank)
            destination = pdf_dir / filename
            try:
                status, digest = download_pdf(
                    record["pdf_url"],
                    destination,
                    user_agent,
                    args.timeout,
                    args.max_pdf_mb * 1024 * 1024,
                    args.overwrite,
                )
                record["download_status"] = status
                record["pdf_filename"] = filename
                record["pdf_sha256"] = digest
            except Exception as exc:
                record["download_status"] = "failed"
                record["download_error"] = f"{type(exc).__name__}: {exc}"
        if args.convert and record.get("pdf_filename"):
            run_conversion(record, pdf_dir, markdown_dir, args.overwrite)

    write_indexes(output_dir, records, args.license_policy)
    downloaded = sum(r.get("download_status") in {"downloaded", "exists"} for r in records)
    converted = sum(r.get("conversion_status") in {"converted", "exists"} for r in records)
    print(f"Candidates: {len(records)}; PDFs available locally: {downloaded}; Markdown files: {converted}")
    print(output_dir / "02_reference_papers" / "literature_index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
