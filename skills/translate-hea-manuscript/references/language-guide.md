# HEA language and terminology guide

## Contents

1. [Canonical terminology](#canonical-terminology)
2. [Disambiguation rules](#disambiguation-rules)
3. [Alloy naming](#alloy-naming)
4. [Evidence and causality](#evidence-and-causality)
5. [Tense](#tense)
6. [Section-specific guidance](#section-specific-guidance)
7. [Expression-learning rules](#expression-learning-rules)

## Canonical terminology

Use these defaults unless the manuscript definition or target journal requires another form:

| Concept | Preferred English |
|---|---|
| 高熵合金 | high-entropy alloy (HEA) |
| 难熔高熵合金 | refractory high-entropy alloy (RHEA) |
| 特殊准随机结构 | special quasirandom structure (SQS) |
| 第一性原理计算 | first-principles calculations |
| 密度泛函理论 | density functional theory (DFT) |
| 广义梯度近似 | generalized gradient approximation (GGA) |
| PBE泛函 | Perdew–Burke–Ernzerhof (PBE) functional |
| 体心立方结构 | body-centered cubic (BCC) structure |
| 晶格参数 | lattice parameter |
| 弹性常数 | elastic constants |
| 体积模量 | bulk modulus |
| 剪切模量 | shear modulus |
| 杨氏模量 | Young's modulus |
| 泊松比 | Poisson's ratio |
| 纳米压痕 | nanoindentation |
| 载荷—位移曲线 | load–displacement curve |
| 总态密度 | total density of states (TDOS) |
| 分态密度 | partial/projected density of states (PDOS), after resolving context |
| 费米能级 | Fermi level |
| 赝能隙 | pseudogap |
| d轨道杂化 | d-orbital hybridization |
| XPS价带谱 | XPS valence-band spectrum |

Extend the glossary for phase stability, structural stability, thermodynamic stability, mechanical stability, lattice distortion, elemental segregation/distribution, plane-wave cutoff energy, k-point mesh, convergence criteria, cohesive/binding energy, Pugh ratio, Cauchy pressure, elastic anisotropy, indentation quantities, bonding/antibonding states, and spectral peak position/intensity/shape.

## Disambiguation rules

Do not choose between the following pairs without checking definitions, formulas, measurement method, or context:

- `cohesive energy` vs `binding energy`;
- `Young's modulus` vs generic `elastic modulus`;
- `reduced modulus` vs `indentation modulus`;
- `phase stability` vs `structural stability`;
- `mechanical stability` vs `thermodynamic stability`;
- `partial density of states` vs `projected density of states`;
- `orbital hybridization` vs `orbital overlap`;
- `valence band` vs `valence-band spectrum`.

If the Chinese text does not contain enough scientific information, preserve the ambiguity in the draft where possible and list a concise author query. Never silently invent a precise technical meaning.

## Alloy naming

Establish one notation at the start and preserve subscripts:

```text
NbTaMoW
NbTaMoWRe
NbTaMoWRe_x
```

Do not alternate casually among `NbTaMoWRe alloy`, `Re-containing alloy`, `Re-doped alloy`, `Re-added alloy`, and `Re-alloyed alloy`. Choose a defined short form after first mention.

Translate “Re加入” according to scientific action and grammar: `Re addition`, `Re alloying`, `the incorporation of Re`, or `the introduction of Re`. Avoid `Re doping` for ordinary substitutional alloying unless the study explicitly treats Re as a dopant.

## Evidence and causality

Match verbs to evidence:

- Use `shows`, `indicates`, `suggests`, `supports`, `is consistent with`, `may be attributed to`, and `is likely associated with` for increasing but bounded evidentiary strength.
- Use `demonstrates` or `confirms` only when the supplied evidence directly warrants them.
- Avoid `prove`, `fully confirm`, `undoubtedly`, `obviously`, `completely`, and `perfectly` unless logically indispensable and fully supported.
- Distinguish observation, correlation, plausible mechanism, indirect evidence, direct evidence, and established causation.
- Prefer `may be attributed to`, `is likely related to`, `can be rationalized by`, `suggests that`, or `is consistent with` when causality is inferential.

Do not add a mechanism merely to make a results paragraph sound complete.

## Tense

- Use the present tense for established facts, equations/definitions, information directly shown by a figure or table, principal conclusions, and manuscript organization: `Figure 3 shows...`, `The alloy exhibits...`.
- Use the past tense for completed sample preparation, experiments, calculations, calibration, and procedural steps: `The SQS models were generated...`.
- Use past or present perfect for prior literature according to the chosen journal style, and remain consistent within a discourse context.
- Do not switch tense without a semantic reason.

## Section-specific guidance

### Title

State the material system and scientific problem accurately and concisely. Use `effect`, `role`, or `mechanism` only as justified. Avoid slogan-like titles and the literal phrase `regulation mechanism` unless idiomatic for the target journal and scientifically accurate.

### Abstract

Organize background/problem → methods → principal results → mechanism-level interpretation → significance. Add no value or conclusion absent from the main text.

### Introduction

Maintain a funnel structure, natural literature transitions, an explicit knowledge gap, and a clear study objective. Do not translate a Chinese list of citations into an English list. Avoid empty openings such as repeated `With the development of...`.

### Computational methods

State accurately how ATAT, Materials Studio, and CASTEP relate. Do not describe Materials Studio itself as the computational method. Preserve the functional, plane-wave cutoff, k-point mesh, optimization and convergence parameters, SQS details, and mechanical-stability criteria needed for reproducibility.

### Experimental methods

Keep preparation order and test conditions clear. Do not invent instrument models. Distinguish what was `characterized`, `examined`, `measured`, or `analyzed`; vary verbs only when their meanings remain accurate.

### Results and discussion

Prefer this paragraph logic when supported:

```text
objective observation → quantitative comparison → trend
→ bounded explanation → relation to other evidence/literature → local conclusion
```

Do not place mechanism before observation, repeat every plotted value, overuse `This indicates that`, or combine results and conclusions into one overloaded sentence.

### Conclusions

Summarize the most important findings, Re-related changes, and supported electronic-structure insight concisely. Do not repeat all values, introduce new arguments, or overstate outlooks.

### Figure and table captions

Make captions independently understandable; identify subpanels and use consistent present-tense or noun-phrase style. Apply `normalized`, `calculated`, and `experimental` precisely. State whether the Fermi level is set to 0 eV when relevant. Do not insert extended discussion into captions.

## Expression-learning rules

Learn terminology, verbs, syntax, information organization, paragraph logic, caption conventions, hedging, and transitions. Do not save only a paper-specific sentence; abstract it into a reusable pattern, such as:

```text
The addition of [alloying element] leads to an increase in the
[lattice parameter/property] of [alloy system].
```

For each pattern, record applicable context, evidence level, replaceable slots, common misuse, source, and whether it fits the manuscript. Keep direct quotations minimal and clearly attributable.
