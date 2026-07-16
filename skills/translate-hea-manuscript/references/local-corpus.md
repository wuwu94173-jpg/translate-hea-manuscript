# Local-paper corpus ingestion

## Contents

1. [Purpose and guarantees](#purpose-and-guarantees)
2. [Supported inputs](#supported-inputs)
3. [Run the importer](#run-the-importer)
4. [Generated records](#generated-records)
5. [Validate local papers](#validate-local-papers)
6. [Combine local and online literature](#combine-local-and-online-literature)
7. [Privacy and rights](#privacy-and-rights)
8. [Failure handling](#failure-handling)
9. [Completion criteria](#completion-criteria)

## Purpose and guarantees

Use local-corpus mode when the user identifies individual papers or a directory already present on disk. Prioritize these user-selected papers before online discovery.

Treat every input as read-only. Do not move, rename, overwrite, edit, or delete a local source paper. Write generated Markdown and indexes only inside the chosen HEA translation project. Copy originals only when the user requests a self-contained corpus.

Treat local availability as authorization to read for the requested task, not as permission to redistribute. Preserve provenance and avoid reproducing substantial source prose in deliverables.

## Supported inputs

`scripts/local_corpus.py` directly handles:

- `.pdf`: extract metadata and the text layer; preserve page anchors;
- `.md` and `.markdown`: preserve existing text inside a traceable imported wrapper;
- `.txt`: decode common UTF-8/GB18030 text and convert to Markdown;
- `.docx`: extract paragraphs, heading levels, and simple tables using the bundled document runtime.

For scanned PDFs, complex Word layouts, LaTeX projects, HTML, EPUB, or other formats, first use the applicable PDF/document skill to produce a faithful text or Markdown representation, then ingest that output.

The importer can accept multiple files and directories. Directory traversal is non-recursive by default so unrelated nested material is not silently included.

## Run the importer

### Import selected files

```powershell
python scripts/local_corpus.py `
  "D:\papers\paper1.pdf" `
  "D:\papers\paper2.docx" `
  --output-dir HEA_translation_project
```

### Import a directory recursively

```powershell
python scripts/local_corpus.py `
  "D:\papers\HEA" `
  --output-dir HEA_translation_project `
  --recursive
```

### Create a self-contained copy

Add `--copy-originals` only when requested. Originals are copied to `02_reference_papers/local_originals/`; they are never moved. Existing generated outputs remain untouched unless `--overwrite` is explicitly supplied.

Use the bundled workspace Python runtime when the default Python lacks `pypdf` or `python-docx`.

## Generated records

The importer creates:

```text
02_reference_papers/local_literature_index.md
02_reference_papers/local_literature_index.csv
02_reference_papers/local_corpus_manifest.json
02_reference_papers/local_learning_queue.md
02_reference_papers/markdown/local_*.md
02_reference_papers/local_originals/       # only with --copy-originals
```

For every input, record:

```text
absolute source path | filename | file type | byte size | modification time
SHA-256 | detected title | authors | journal/subject | year | DOI
metadata backend/status | conversion status | duplicate relationship
generated Markdown | proposed translation uses
```

Metadata embedded in PDFs and DOCX files is often missing or wrong. DOI detection from the first pages is a convenience, not proof. Verify important metadata against the document itself or a DOI/journal record before citing it.

## Validate local papers

Review the local index before learning:

1. Confirm each file is a scholarly paper relevant to the manuscript.
2. Verify title, DOI, authors, year, and version where available.
3. Inspect duplicate flags. Exact SHA-256 duplicates and same-DOI versions should be learned once.
4. Open representative Markdown pages and verify column order, equations, symbols, captions, and section boundaries.
5. Route scanned or low-text PDFs to OCR/visual QA.
6. Assign explicit translation uses and inclusion/exclusion reasons.
7. Keep theses, reports, slides, supplementary files, and papers distinct in the index.

User-selected local papers may be high priority, but do not treat them as scientifically authoritative without checking relevance and quality.

## Combine local and online literature

In a mixed workflow:

1. Import local papers first.
2. Build a coverage matrix for computational methods, experimental methods, phase structure, mechanical properties, electronic structure/XPS, captions, and conclusions.
3. Search online only for uncovered topics, ambiguous terms, or missing high-quality expression examples.
4. Merge by normalized DOI. Use SHA-256 to detect exact local copies and title/year/authors to flag possible metadata duplicates.
5. Prefer the clearest lawful full-text version while recording whether it is submitted, accepted, or published.
6. Preserve both local and online provenance but include each paper only once in the 15–25-paper core count.
7. Combine `local_learning_queue.md` and `learning_queue.md` into one reviewed processing order.

Do not redownload an online paper when an equivalent readable local copy already exists.

## Privacy and rights

- Keep absolute local paths inside local manifests and reports; do not reproduce them in public-facing manuscript text.
- Never upload local papers or extracted full text to third-party services unless the user explicitly authorizes that transfer.
- Do not infer permission to redistribute a paper merely because it exists locally.
- Learn terminology, structure, and abstracted patterns; do not create a sentence bank of long verbatim passages.
- If a local paper contains confidential annotations or unpublished content, isolate it from externally sourced corpus records and flag the restriction.

## Failure handling

- **Unsupported extension:** report it and use the applicable document converter; do not rename the file to fake support.
- **Encrypted PDF:** request an unlocked user-authorized copy or use an approved password supplied by the user.
- **Scanned/empty PDF:** route to OCR and visual QA.
- **Malformed DOCX:** use the document skill and preserve the source.
- **Unknown text encoding:** record failure and ask for a known encoding or converted copy.
- **Duplicate hash:** retain the record but exclude it from the learning queue.
- **Same DOI, different hashes:** treat as possible versions; compare and select one canonical learning copy.
- **Missing DOI:** use a local hash plus title/year provenance; do not invent an identifier.
- **Conversion already exists:** reuse it unless the source hash changed or the user requests overwrite.

Continue with other local papers after isolated failures. Stop only if the source location is inaccessible, no supported papers are found, or conversion dependencies are unavailable.

## Completion criteria

Complete local-corpus mode only when:

1. Every in-scope source has an index entry and SHA-256 hash.
2. Original files remain unchanged.
3. Each usable unique paper has readable Markdown or an explicit OCR/document-conversion requirement.
4. Duplicate papers and versions are reconciled.
5. Metadata is verified or marked provisional.
6. Each included paper has a translation use and provenance.
7. Local and online queues are merged without double counting.
8. Corpus-learning outputs identify local sources by DOI/page where available and by file hash/section otherwise.
