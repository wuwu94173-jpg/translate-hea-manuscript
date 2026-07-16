# Full-project workflow

## Contents

1. [Priority and scope](#priority-and-scope)
2. [Source inventory](#source-inventory)
3. [Recommended project layout](#recommended-project-layout)
4. [Literature-assisted expression learning](#literature-assisted-expression-learning)
5. [Core-paper Markdown conversion](#core-paper-markdown-conversion)
6. [Translation-resource construction](#translation-resource-construction)
7. [Chapter sequence](#chapter-sequence)
8. [Execution checklist](#execution-checklist)

## Priority and scope

Keep this priority order:

```text
accurate Chinese-to-English translation
> terminology consistency
> idiomatic academic expression
> scientific logic and paragraph cohesion
> translation corpus construction
> literature review
```

Treat literature retrieval and Markdown conversion as supporting steps, not the final objective. The principal system is NbTaMoW/NbTaMoWRe_x, including SQS construction, CASTEP first-principles calculations, phase structure, XRD, SEM/EDS, elastic properties, nanoindentation, DOS, d-orbital hybridization, and XPS valence-band spectra.

## Source inventory

Inspect the current project before asking for input. Identify:

- Chinese manuscript file(s) and format;
- title, abstract, keywords, headings, and section order;
- figure and table captions, subfigure labels, and in-text citations;
- equations, variables, units, superscripts, and subscripts;
- alloy naming and Re-content notation;
- existing English passages, glossaries, target-journal instructions, and reference PDFs;
- ambiguous or internally inconsistent scientific statements.

Keep the source unchanged. Create derived outputs separately unless the user requests tracked or in-place editing.

## Recommended project layout

Create only the directories needed for the current scope:

```text
HEA_translation_project/
├── 01_source_chinese/
│   ├── original_chinese_paper.md
│   └── figures_and_captions.md
├── 02_reference_papers/
│   ├── pdf/
│   ├── markdown/
│   ├── local_originals/
│   ├── literature_index.md
│   ├── literature_index.csv
│   ├── download_manifest.json
│   ├── learning_queue.md
│   ├── local_literature_index.md
│   ├── local_literature_index.csv
│   ├── local_corpus_manifest.json
│   └── local_learning_queue.md
├── 03_translation_resources/
│   ├── terminology_glossary.md
│   ├── terminology_glossary.csv
│   ├── standard_expressions.md
│   ├── sentence_patterns.md
│   ├── figure_caption_templates.md
│   ├── tense_and_grammar_rules.md
│   ├── journal_style_guide.md
│   └── corpus_learning_report.md
├── 04_translation/
│   ├── 01_title_abstract_keywords.md
│   ├── 02_introduction.md
│   ├── 03_methods.md
│   ├── 04_structure_results.md
│   ├── 05_mechanical_properties.md
│   ├── 06_electronic_structure.md
│   ├── 07_conclusions.md
│   └── full_english_manuscript.md
└── 05_quality_control/
    ├── terminology_consistency_report.md
    ├── scientific_accuracy_report.md
    ├── grammar_style_report.md
    └── final_translation_report.md
```

Adapt filenames to the actual manuscript. Do not create empty scaffolding that will not be used.

## Literature-assisted expression learning

Use this stage only for a full workflow, a user-requested corpus, or a genuine terminology gap. Select roughly 15–25 highly relevant English papers rather than accumulating a broad HEA bibliography.

For automatic discovery, license-aware downloading, conversion, provenance, and failure handling, read [literature-automation.md](literature-automation.md) and use the bundled scripts. Validate automated ranking before designating the core corpus.

When local papers are supplied, read [local-corpus.md](local-corpus.md), ingest them first, and search online only for gaps. Count duplicate local/online versions once.

Prioritize primary research from reliable materials-science journals such as *Acta Materialia*, *Scripta Materialia*, *Journal of Alloys and Compounds*, *Intermetallics*, *Materials & Design*, *Computational Materials Science*, *Applied Surface Science*, *Physical Review B*, *Journal of Materials Research and Technology*, and *Materials Science and Engineering A*.

Search by translation need, for example:

- `NbTaMoW refractory high-entropy alloy`, `NbTaMoWRe alloy`, `Re alloying refractory high-entropy alloy`;
- `ATAT SQS refractory high-entropy alloy`, `CASTEP high-entropy alloy`, `mechanical stability criteria cubic crystals`;
- `simulated and experimental XRD high-entropy alloy`, `SEM EDS refractory high-entropy alloy`;
- `nanoindentation NbMoTaW`, `Oliver–Pharr high-entropy alloy`, `load-displacement refractory alloy`;
- `calculated DOS XPS valence band`, `d-orbital hybridization refractory high-entropy alloy`, `pseudogap high-entropy alloy`.

For each selected paper, record:

```text
title | authors | journal | year | DOI/URL | access status
main translation use | relevant sections | terminology value
expression quality | limitations or applicability notes
```

Assign a concrete use: Introduction, Computational Methods, Experimental Methods, Phase Structure, Mechanical Properties, Electronic Structure, Conclusions, or Figure Captions. Exclude papers whose only value is generic HEA topical overlap.

## Core-paper Markdown conversion

Convert only lawfully available core full texts. Preserve title, abstract, keywords, headings, methods, results/discussion, conclusion, relevant captions, and exact scientific meaning. Remove repeated headers/footers, page numbers, meaningless line breaks, OCR noise, and irrelevant reference-format debris.

Start each converted file with:

```yaml
---
title: ""
authors: ""
journal: ""
year: ""
doi: ""
main_translation_use: ""
language_quality: ""
---
```

Clearly distinguish extracted source wording from agent-created notes or reusable abstractions.

## Translation-resource construction

Build the glossary with these fields:

```text
中文术语 | 首选英文术语 | 可接受替代表达 | 缩写 | 适用语境
不推荐表达 | 参考来源 | 备注
```

Build expression resources by function: research purpose, computational methods, experimental methods, result description, quantitative comparison, mechanism interpretation, theory–experiment agreement, section transitions, and figure captions.

Abstract every learned sentence into a reusable pattern. Record its scenario, evidence strength, replaceable slots, common misuse, and applicability. Never assemble the manuscript by copying paper sentences.

## Chapter sequence

Translate in this order:

1. Title, abstract, and keywords.
2. Introduction.
3. Computational and experimental methods.
4. Phase/structure results.
5. Mechanical properties and nanoindentation.
6. Electronic structure and XPS comparison.
7. Conclusions.
8. Figure and table captions, if not handled with their sections.

Before each section, identify its purpose, scientific question, core data, evidence level, terminology, cross-references, and relationship to adjacent sections. After each section, perform the checks in `quality-control.md`.

## Execution checklist

1. Inspect existing source files and figures.
2. Map headings, captions, equations, and identifiers.
3. Establish canonical terminology and alloy notation.
4. Ingest and deduplicate available local papers without modifying originals.
5. Identify corpus coverage gaps and retrieve additional papers only when applicable.
6. Download only license-eligible or user-authorized full texts; retain access status and failure reasons.
7. Convert selected full texts to page-anchored Markdown only when useful and permitted; visually QA weak extraction.
8. Merge local and online records and process each unique paper once.
9. Build or update source-traceable terminology and expression resources.
10. Translate chapter by chapter.
11. Run chapter-level bilingual and consistency checks.
12. Merge the English manuscript.
13. Run three final review passes.
14. Deliver the manuscript and quality-control reports.
