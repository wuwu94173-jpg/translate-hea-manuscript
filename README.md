# translate-hea-manuscript

A Codex skill for translating Chinese high-entropy-alloy manuscripts into submission-ready SCI English, with source-traceable learning from local papers and license-eligible open-access literature.

这是一个面向高熵合金与难熔高熵合金论文的 Codex Skill，可读取本地论文、构建文献语料库，并在保持科学含义和数据一致性的前提下完成英文学术翻译与质量检查。

## Capabilities

- Translate titles, abstracts, captions, sections, or full Chinese manuscripts.
- Read local PDF, Markdown, TXT, and DOCX papers without modifying the originals.
- Hash and deduplicate local papers, then convert usable content to traceable Markdown.
- Discover papers through OpenAlex and download only locations allowed by the selected open-access policy.
- Build terminology, sentence-pattern, caption, tense, and journal-style resources with DOI/page provenance.
- Audit terminology, data, alloy notation, evidence strength, causality, grammar, and whole-manuscript consistency.
- Focus on NbTaMoW/NbTaMoWRe_x, SQS/ATAT/CASTEP/DFT, XRD, SEM/EDS, elastic properties, nanoindentation, DOS, orbital hybridization, and XPS valence-band spectra.

## Repository layout

```text
skills/translate-hea-manuscript/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

Repository documentation, tests, and licensing stay outside the installable skill directory.

## Install

Clone the repository, then copy `skills/translate-hea-manuscript` into the Codex skills directory.

PowerShell:

```powershell
Copy-Item -Recurse -Force `
  .\skills\translate-hea-manuscript `
  "$env:USERPROFILE\.codex\skills\translate-hea-manuscript"
```

macOS/Linux:

```bash
cp -R skills/translate-hea-manuscript ~/.codex/skills/translate-hea-manuscript
```

Then invoke:

```text
$translate-hea-manuscript
```

## Typical workflow

```text
read the Chinese manuscript
→ ingest and deduplicate local papers
→ identify corpus gaps
→ discover/download eligible open-access papers
→ convert papers to page-anchored Markdown
→ learn terminology and abstracted expression patterns
→ translate chapter by chapter
→ run scientific, language, and consistency reviews
```

Example request:

```text
$translate-hea-manuscript

Read the local papers in this project, build a terminology and expression corpus,
use open-access literature to fill any gaps, and translate my Chinese HEA manuscript.
```

## Standalone script dependencies

Codex Desktop normally supplies the required PDF/document runtime. For standalone Python use:

```bash
python -m pip install -r requirements.txt
```

The OpenAlex discovery helper reads an API key from the `OPENALEX_API_KEY` environment variable when available. Do not commit API keys or generated corpora.

## Safety and copyright

- Original local papers are read-only unless the user explicitly requests project copies.
- The default online download policy is `cc-only`.
- The workflow does not bypass paywalls, authentication, CAPTCHAs, or publisher controls.
- Downloaded papers retain their own copyrights and licenses and are not covered by this repository's MIT license.
- The skill learns terminology, organization, and abstracted patterns; it does not assemble manuscripts from copied source passages.
- Generated local manifests may contain absolute paths and should not be published.

## Validation

```bash
python -m unittest discover -s tests -v
python -m py_compile skills/translate-hea-manuscript/scripts/*.py
```

## License

Skill code and repository documentation are licensed under the [MIT License](LICENSE). Third-party papers and user manuscripts are excluded.
