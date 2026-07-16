---
name: translate-hea-manuscript
description: Translate, polish, and quality-control Chinese high-entropy-alloy manuscripts—especially NbTaMoW and NbTaMoWRe_x refractory HEAs—into submission-ready SCI English. Use for paragraph, section, caption, abstract, or full-manuscript translation; bilingual accuracy audits; terminology/style normalization; reading and learning from user-authorized local PDF/Markdown/TXT/DOCX papers; or automatic literature-assisted learning that discovers and ranks papers, downloads license-eligible open-access PDFs, converts them to searchable Markdown, and builds a source-traceable terminology and expression corpus for SQS/ATAT/CASTEP/DFT, XRD, SEM/EDS, nanoindentation, elastic properties, DOS, d-orbital hybridization, and XPS valence-band spectra.
---

# Translate HEA Manuscripts

Translate the author's existing Chinese manuscript; do not turn the task into a new review article. Preserve scientific meaning, data, scope, evidence strength, numbering, and traceability while producing natural materials-science English.

## Select the execution mode

- Use **segment mode** for a pasted paragraph, title, abstract, caption, or individual section. Translate immediately; do not build a 15–25-paper corpus unless the user requests it or a technical ambiguity requires verification.
- Use **full-project mode** for a complete manuscript, a project directory, or an explicit request to execute the entire workflow. Inspect existing files first and do not ask the user to paste material already present.
- Use **literature-learning mode** when the user asks to search, download, convert, or learn from papers. Run the license-aware automation, validate the resulting core corpus, extract source-anchored terminology and abstracted expression patterns, then use those resources during translation.
- Use **local-corpus mode** when the user supplies local papers or a directory. Read source files without modifying them, hash and deduplicate them, convert supported content to Markdown, validate extraction quality, and learn from each unique paper once.
- Use **audit mode** when an English draft already exists. Compare it against the Chinese source and report mistranslation, omission, unsupported addition, altered causal strength, terminology drift, and language problems before revising.
- If the target journal or house style is known, follow it. Otherwise use concise, formal, restrained materials-science English.

## Load the relevant references

Read only what the task needs:

- Read [references/workflow.md](references/workflow.md) for full-project setup, literature-corpus construction, PDF-to-Markdown processing, and chapter sequencing.
- Read [references/literature-automation.md](references/literature-automation.md) before any automatic search, download, conversion, or corpus-learning task.
- Read [references/local-corpus.md](references/local-corpus.md) before scanning, indexing, converting, or learning from local papers.
- Read [references/language-guide.md](references/language-guide.md) before translating technical content or normalizing terminology and section style.
- Read [references/quality-control.md](references/quality-control.md) before delivering any translation; use its segment template or full-manuscript review procedure.

## Apply non-negotiable constraints

1. Preserve every value, unit, sign, trend, variable, alloy composition, figure/table/equation number, qualifier, and limitation.
2. Do not invent experiments, parameters, mechanisms, references, instrument models, or conclusions.
3. Do not convert correlation, consistency, or a plausible explanation into proven causality.
4. Prefer scientific meaning, logical relation, and idiomatic academic English over Chinese word order. Split or merge sentences only when meaning remains unchanged.
5. Use one preferred English equivalent per Chinese technical term throughout the manuscript unless context genuinely requires a documented variant.
6. Mark substantive ambiguity for author verification; do not repeatedly ask about ordinary stylistic choices.
7. Learn terminology, syntax, information structure, and hedging from papers. Do not splice sentences or reproduce substantial source text.

## Execute segment translation

1. Identify the passage purpose, research object, technical terms, data, logical relations, evidence strength, tense, and cross-references.
2. Reuse established manuscript terminology. For an unresolved technical term, verify its meaning from authoritative sources when possible; record the preferred term and any rejected alternative.
3. Draft a complete, faithful translation.
4. Polish sentence structure, articles, number agreement, tense, prepositions, transitions, concision, and materials-science idiom.
5. Perform a sentence-level bilingual accuracy check and a terminology/data consistency check.
6. Deliver using the segment format in `references/quality-control.md`. Put all directly usable prose in **SCI英文译文**.

## Execute a full manuscript project

1. Inventory the existing Chinese source, sections, figures, tables, equations, references, and available English papers.
2. Establish canonical alloy names, variables, abbreviations, and a terminology glossary before translating prose.
3. If literature-assisted language learning is requested, ingest available local papers first, then use online discovery only to fill topic or terminology gaps. Select 15–25 highly relevant unique papers with a declared translation use; prioritize relevance and expression quality over volume.
4. Download and convert only license-eligible or otherwise user-authorized full text. Preserve source meaning, page anchors, access status, license metadata, and file hashes.
5. Translate title, abstract, and keywords first; continue chapter by chapter rather than translating the entire manuscript in one undifferentiated pass.
6. After each chapter, run terminology, composition, numeric, scientific-meaning, and English-language checks.
7. Merge the complete English manuscript and conduct three final passes: scientific accuracy, English logic/style, and whole-document consistency.
8. Deliver the manuscript plus the reports defined in `references/quality-control.md`.

## Execute automatic literature learning

1. Load and follow the environment's web-access rules before making network requests. Use the official OpenAlex API for discovery metadata and direct open-access locations for eligible PDFs.
2. Run `scripts/literature_pipeline.py` with the default HEA query set or manuscript-derived queries. Prefer `cc-only`; use `any-oa` only when the user authorizes broader open-access retrieval and the access status is recorded.
3. Treat automated ranking as candidate generation. Validate topic relevance, journal/source quality, document type, retraction status, and translation usefulness before naming 15–25 papers as the core corpus.
4. Continue past inaccessible or failed downloads. Record DOI, landing page, license/access status, and failure reason; never bypass a paywall or authentication control.
5. Convert downloaded text-layer PDFs with `scripts/pdf_to_markdown.py`. Route scanned, equation-heavy, table-heavy, or low-text pages to OCR or visual PDF QA instead of trusting malformed extraction.
6. Process `learning_queue.md` in rank order. Build or update the terminology glossary, standard-expression library, sentence-pattern library, figure-caption templates, and literature index with DOI and page anchors.
7. Abstract patterns rather than copying source sentences. Confirm ambiguous technical terms with at least two reliable sources or one authoritative definition before adopting a canonical translation.
8. Produce a corpus-learning report covering search queries, selection reasons, access/license status, extraction limitations, learned resources, and unresolved terminology.

## Execute local-corpus learning

1. Run `scripts/local_corpus.py` on the supplied files or directories. Use `--recursive` only when subdirectories are in scope.
2. Keep original files read-only. Do not move, rename, overwrite, or delete them. Use `--copy-originals` only when the user wants a self-contained project copy.
3. Support PDF, Markdown, TXT, and DOCX directly. Route other formats through the environment's applicable document skill before corpus ingestion.
4. Index the absolute source path, file type, size, modification time, SHA-256, detected metadata, conversion status, and duplicate relationship. Treat detected DOI/title metadata as provisional until verified.
5. Convert each unique paper to project Markdown. Preserve PDF page anchors; retain source hash/path provenance for Markdown, TXT, and DOCX imports.
6. Review `local_literature_index.md` and `local_learning_queue.md`. Exclude duplicate, irrelevant, corrupt, or low-quality conversions from learning.
7. Merge local and online records by DOI first and file hash second. Prefer the cleanest lawful full text, record the chosen version, and learn each paper once.
8. Build the same glossary, expression-pattern, caption, and corpus-learning resources used by online literature-learning mode.

## Handle files and evidence

- Preserve the source file and work in new output files unless the user explicitly requests in-place editing.
- Treat local paper directories as read-only inputs. Generated Markdown, indexes, and optional copies must remain inside the translation project.
- For DOCX, PDF, LaTeX, or spreadsheet-based source material, use the environment's applicable document skill and preserve layout-relevant identifiers.
- When external literature or terminology verification is needed, use the environment's approved web-access workflow and prefer journal pages, DOI records, official software documentation, and primary papers.
- Never place API keys in commands, logs, manifests, or Skill files. Read the OpenAlex key from `OPENALEX_API_KEY` when available; the script can perform only light trials without one.
- Download only from direct locations identified as open access under the selected policy or from files the user has already supplied or is authorized to access. Do not automate paywall circumvention.
- Do not expose absolute local paths outside local project reports; they may contain personal or institutional information.
- Cite or record a source only after verifying that it supports the specific terminology or expression use. Never fabricate bibliographic details.

## Completion standard

Finish only when the English text is directly reusable in Word or LaTeX, scientifically faithful to the Chinese source, terminologically consistent, natural to a materials-science reader, and accompanied by clearly isolated author queries for unresolved scientific ambiguity.
