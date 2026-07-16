# Automatic literature discovery and learning

## Contents

1. [Goal and boundaries](#goal-and-boundaries)
2. [Prerequisites](#prerequisites)
3. [Automated pipeline](#automated-pipeline)
4. [Running the helper](#running-the-helper)
5. [Candidate validation](#candidate-validation)
6. [PDF conversion quality](#pdf-conversion-quality)
7. [Corpus learning](#corpus-learning)
8. [Provenance requirements](#provenance-requirements)
9. [Failure handling](#failure-handling)
10. [Completion criteria](#completion-criteria)

## Goal and boundaries

Automate this sequence when the user requests literature-assisted learning:

```text
derive/search queries → discover candidates → deduplicate and rank
→ download license-eligible open-access PDFs → convert to Markdown
→ validate 15–25 core papers → extract traceable language resources
→ translate chapter by chapter → generate quality-control reports
```

Treat “learning” as construction and use of a local, source-traceable corpus. Do not describe it as model fine-tuning or permanent retraining.

If the user supplies local papers, ingest them first using `scripts/local_corpus.py` and the rules in `local-corpus.md`. Use online discovery to fill gaps rather than redownloading equivalent papers.

Never bypass a paywall, CAPTCHA, authentication requirement, robots restriction, or publisher access control. A DOI or publicly visible landing page does not itself prove that the PDF may be downloaded. Use the access and license fields recorded in the manifest, user-supplied files, or a user-authorized logged-in workflow.

## Prerequisites

Before network activity:

1. Load and follow the environment's `web-access` skill or equivalent approved browsing policy.
2. Confirm that network writes and downloads are within the user's requested project.
3. Prefer a free OpenAlex API key for repeatable searches. Read it from `OPENALEX_API_KEY`; never print, persist, or embed it.
4. Optionally read the contact email from `OPENALEX_MAILTO` for API etiquette.
5. Use the bundled workspace Python runtime when available because it includes PDF-processing dependencies.

OpenAlex metadata search has a limited no-key trial allowance. If the API reports authentication, quota, or rate-limit errors, stop repeated retries and ask the user to configure a free key or provide papers directly.

## Automated pipeline

Use `scripts/literature_pipeline.py` for deterministic metadata handling and file operations. It performs:

- multiple HEA-focused OpenAlex searches;
- English journal-article filtering and retraction/paratext exclusion;
- DOI/OpenAlex-ID deduplication;
- topic, journal, citation, open-access, and translation-use scoring;
- conservative license selection;
- bounded PDF download with format validation and SHA-256 hashing;
- page-anchored Markdown conversion;
- CSV, Markdown, and JSON indexes;
- creation of a ranked `learning_queue.md`.

The ranking is a triage aid, not peer-review judgment. An agent must validate the final core corpus.

Default queries cover NbTaMoW/NbMoTaW, RHEAs, SQS, ATAT/CASTEP/DFT, elastic properties, XRD, nanoindentation, DOS, and XPS. Add manuscript-derived queries for unusual variables, methods, or target-journal terminology.

## Running the helper

Run from the Skill directory or use absolute paths.

### Conservative automatic run

```powershell
python scripts/literature_pipeline.py `
  --output-dir HEA_translation_project `
  --max-results 25 `
  --download `
  --convert
```

This uses the default `cc-only` policy and downloads only direct PDF locations whose OpenAlex location metadata carries a Creative Commons or public-domain marker.

### Add project-specific searches

```powershell
python scripts/literature_pipeline.py `
  --output-dir HEA_translation_project `
  --query '"NbTaMoWRe" electronic structure' `
  --query '"calculated DOS" XPS "high-entropy alloy"' `
  --from-year 2010 `
  --max-results 25 `
  --download `
  --convert
```

### Metadata-only discovery

Omit `--download` and `--convert`. Use this first when the user wants to approve the candidate list before files are retrieved.

### Offline reprocessing or testing

Use `--metadata-file saved_openalex_response.json` to build indexes without querying the API. Existing PDFs are preserved unless `--overwrite` is explicitly supplied.

### Broader open-access policy

Use `--license-policy any-oa` only when the user authorizes it. This allows direct PDF locations marked open access even when a reusable Creative Commons license is absent. Keep the recorded license/access status and use the content only within applicable rights; do not redistribute it automatically.

## Candidate validation

Review `02_reference_papers/literature_index.md` and the JSON manifest before corpus learning. For each candidate, verify:

- title, DOI, year, authors, journal/source, and article type;
- absence of retraction or obvious metadata mismatch;
- direct relevance to the manuscript system, method, measurement, or expression need;
- availability of enough text to support the intended language-learning use;
- access/license status and whether the downloaded version is submitted, accepted, or published;
- source quality and whether the paper is primary research, a method source, or a carefully chosen review.

Select 15–25 core papers. Assign at least one explicit use: Introduction, Computational Methods, Experimental Methods, Phase Structure, Mechanical Properties, Electronic Structure, Conclusions, or Figure Captions. Exclude generic HEA papers that do not materially help translation.

Do not rank solely by citation count. New or niche papers may have high terminology value despite low citations; heavily cited papers may be linguistically or scientifically mismatched.

## PDF conversion quality

The converter extracts the PDF text layer and preserves `## Page N` anchors. It does not guarantee:

- correct multi-column reading order;
- faithful equations, subscripts, superscripts, or special symbols;
- reconstructed tables;
- figure text or image-only captions;
- usable text from scanned pages;
- removal of every header, footer, or hyphenation artifact.

Inspect each conversion report. If pages are flagged as low text or the prose is visibly scrambled, use the environment's PDF/OCR workflow and visually compare representative pages. Never learn a technical term from corrupted extraction.

Keep extracted wording separate from agent-authored notes and templates. Preserve the PDF filename, DOI, license, conversion backend, and page anchors in Markdown frontmatter.

## Corpus learning

Process `learning_queue.md` in rank order and update these resources incrementally:

```text
03_translation_resources/terminology_glossary.md
03_translation_resources/terminology_glossary.csv
03_translation_resources/standard_expressions.md
03_translation_resources/sentence_patterns.md
03_translation_resources/figure_caption_templates.md
03_translation_resources/tense_and_grammar_rules.md
03_translation_resources/journal_style_guide.md
03_translation_resources/corpus_learning_report.md
```

For each paper:

1. Read the sections relevant to its assigned translation use; do not summarize the entire paper unless needed.
2. Extract candidate terminology with surrounding scientific context.
3. Distinguish definitions, method names, measured quantities, calculated quantities, and interpretive terms.
4. Extract useful verbs, clause structures, paragraph sequencing, hedging, comparison logic, and caption patterns.
5. Convert source-specific sentences into abstract patterns with replaceable slots.
6. Record common misuse, evidence strength, applicable section, DOI, and page anchor.
7. Compare against the existing glossary and resolve conflicts rather than appending uncontrolled synonyms.
8. Verify an ambiguous canonical term against at least two reliable sources or one authoritative method/software definition.

Do not copy long sentences or paragraphs. Avoid mosaic writing assembled from source fragments. A reusable pattern should contain the structural lesson, not distinctive source wording.

## Provenance requirements

Use these fields for terminology entries:

```text
中文术语 | 首选英文术语 | 可接受替代表达 | 缩写 | 适用语境
不推荐表达 | DOI | 页码/章节 | 证据类型 | 备注
```

Use these fields for expression patterns:

```text
功能类别 | 抽象句式 | 可替换槽位 | 证据强度 | 适用章节
常见误用 | DOI | 页码/章节 | 是否采用
```

The corpus-learning report must state:

- exact queries and search date;
- API/source used;
- number of candidates, eligible PDFs, successful downloads, conversions, and core papers;
- inclusion/exclusion reasons;
- licenses and versions represented;
- failed downloads and missing full text;
- OCR or extraction limitations;
- new or changed canonical terms;
- unresolved scientific ambiguity.

## Failure handling

- **No API key/quota exceeded:** preserve completed metadata and request a free key or postpone remaining queries.
- **PDF URL returns HTML or access denial:** record failure and retain DOI/landing page; do not scrape around the control.
- **Missing license under `cc-only`:** keep metadata but do not download automatically.
- **Duplicate DOI/version:** retain one canonical record and document the selected version.
- **Corrupt/scanned PDF:** route to PDF visual QA or OCR; do not trust empty Markdown.
- **Publisher copy unavailable but repository copy exists:** prefer the recorded lawful repository location and note its version.
- **Insufficient relevant papers:** broaden scientific synonyms or adjacent alloy systems deliberately; never lower the relevance threshold silently.
- **Potentially wrong metadata:** verify against the DOI landing page or journal record before using it as evidence.

Continue processing other papers after isolated failures. Stop the pipeline only when a systemic condition—authentication, network policy, quota, or missing PDF backend—prevents meaningful progress.

## Completion criteria

Complete literature-learning mode only when:

1. The candidate index and download manifest are present.
2. Every attempted paper has an access, download, and conversion status.
3. The 15–25-paper core corpus has explicit translation uses and inclusion reasons.
4. Low-quality conversions are corrected or excluded.
5. Terminology and expression resources include DOI and page/section provenance.
6. Conflicting or ambiguous terms are resolved or flagged.
7. The corpus-learning report records limitations and failures.
8. Translation uses the learned resources without copying source prose or changing the Chinese manuscript's scientific meaning.
