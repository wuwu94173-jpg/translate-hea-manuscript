# Translation output and quality control

## Contents

1. [Segment output](#segment-output)
2. [Chapter-level checks](#chapter-level-checks)
3. [Three-pass final review](#three-pass-final-review)
4. [Full-project deliverables](#full-project-deliverables)
5. [Final acceptance criteria](#final-acceptance-criteria)

## Segment output

Use this structure for a pasted passage unless the user requests a different format:

```markdown
## 1. 中文原文

[保留原文，不做改动]

## 2. SCI英文译文

[给出可直接用于论文的完整英文]

## 3. 关键术语对照

| 中文术语 | 本次采用的英文 | 说明 |
|---|---|---|

## 4. 翻译调整说明

- [只说明影响结构、逻辑、证据强度、时态或术语的重要调整]

## 5. 需要作者核实的问题

- [仅列实质性科学歧义；如无则写“无”]
```

Do not explain every lexical choice. Keep the directly usable final prose together in `SCI英文译文`.

Valid author queries include:

- whether “稳定性” means structural, phase, thermodynamic, or mechanical stability;
- whether “弹性模量” means Young's, reduced, or indentation modulus;
- whether the stated formula corresponds to cohesive or binding energy;
- an unclear data unit, composition notation, or sign;
- inconsistent figure/table numbers or a scientifically contradictory statement.

Do not query the author merely because several stylistically acceptable translations exist.

## Chapter-level checks

Run all five checks after each section.

### 1. Terminology consistency

Detect multiple English renderings of the same Chinese term. Verify preferred term, abbreviation definition, capitalization, hyphenation, and first-use expansion.

### 2. Alloy and notation consistency

Check NbTaMoW, NbTaMoWRe, NbTaMoWRe_x, Re content, variable definitions, and subscript/superscript formatting. Confirm that generic short forms refer unambiguously to the intended composition.

### 3. Numeric and identifier consistency

Compare all values, units, percentages, ranges, uncertainty/error notation, positive/negative signs, decimal places, equations, figure/table numbers, panel labels, and citation numbers against the source.

### 4. Scientific-meaning consistency

Check for omission, mistranslation, unsupported addition, changed scope, altered research object, lost qualifier, reversed trend, changed logical relation, stronger conclusion, or possibility rewritten as certainty.

### 5. English-language quality

Check articles, singular/plural, subject–verb agreement, tense and voice, prepositions, punctuation, sentence length, repetition, Chinglish, vague pronouns, dangling modifiers, transitions, paragraph focus, and materials-science idiom.

Record every material correction with enough context to trace it to a source section or sentence.

## Three-pass final review

### Pass 1: scientific accuracy

Use the Chinese manuscript as the authority. Compare paragraph by paragraph. Resolve or explicitly flag every discrepancy in meaning, data, scope, evidence strength, and cross-reference.

### Pass 2: language and logic

Read the English manuscript independently. Improve clarity, cohesion, paragraph progression, concision, and journal-appropriate style without consulting the Chinese sentence structure as a writing template.

### Pass 3: whole-document consistency

Check terminology, abbreviations, alloy names, variables, subscripts/superscripts, units, figures/tables, tense, heading hierarchy, citation style, and conclusion strength across the complete manuscript.

After any substantive revision in Pass 2 or 3, recheck the affected passage against the Chinese source.

## Full-project deliverables

Produce these files or their user-requested equivalents:

```text
04_translation/full_english_manuscript.md
05_quality_control/terminology_consistency_report.md
05_quality_control/scientific_accuracy_report.md
05_quality_control/grammar_style_report.md
05_quality_control/final_translation_report.md
```

When literature-learning mode is used, also deliver:

```text
02_reference_papers/literature_index.md
02_reference_papers/literature_index.csv
02_reference_papers/download_manifest.json
02_reference_papers/learning_queue.md
03_translation_resources/corpus_learning_report.md
```

When local-corpus mode is used, also deliver:

```text
02_reference_papers/local_literature_index.md
02_reference_papers/local_literature_index.csv
02_reference_papers/local_corpus_manifest.json
02_reference_papers/local_learning_queue.md
```

The terminology report should list the canonical term, variants found, locations, and resolution. The scientific report should list checked sections, material discrepancies, corrections, and unresolved author queries. The grammar/style report should summarize systematic issues and important revisions without narrating every edit. The final report should state source coverage, completed checks, remaining risks, and deliverable locations.

The corpus-learning report should state exact queries, search date, candidate/core-paper counts, inclusion and exclusion reasons, access/license status, failed downloads, conversion limitations, learned resources, and unresolved terminology. Do not represent inaccessible metadata-only records as papers that were read.

For local papers, state source-file coverage, hashes, duplicate/version resolution, conversion quality, provisional metadata, and any OCR/document-conversion requirements. Confirm that originals were not modified. Do not expose absolute local paths in public-facing manuscript content.

## Final acceptance criteria

Accept the translation only if it:

1. Can be copied into Word or LaTeX for further formatting.
2. Preserves section structure and all figure, table, equation, and citation identifiers.
3. Matches every source value and trend.
4. Uses HEA and materials-science terminology consistently.
5. Reads as natural academic English rather than a word-for-word rendering.
6. Contains no invented experiment, parameter, result, mechanism, instrument model, or reference.
7. Does not sacrifice scientific meaning for rhetorical polish.
8. Clearly marks unresolved technical ambiguity.
9. Keeps major adjustments traceable.
10. Includes the required consistency and accuracy records for a full project.
