# PMS-AXIOM

## A Praxeological Cartography of Classical Closure-Demands Across the PMS Stack (Δ–Ψ)

PMS-AXIOM is a cartographic and indexing project built on the Praxeological Meta-Structure (PMS). It maps classical philosophical, governance-relevant, relational, consent-adjacent, and QC-workflow problem families as structural closure-demands inside explicit frames.

PMS supplies the canonical Δ–Ψ operator grammar. PMS-AXIOM does not extend that grammar, does not introduce new PMS operators, and does not create a new base model.

The project compiles cases into a structured artefact layer and renders them in the paper as compact chapter-facing case sections.

The guiding rule is:

```text
Where closure is structurally warranted, render it.
Where closure exceeds the frame, preserve Λ.
Where an artefact may travel as authority, attach the boundary.
````

---

## What PMS-AXIOM Is

PMS-AXIOM is:

* a cartographic / indexing paper,
* a structured case suite,
* a rebuild of a legacy full paper into a block/case architecture,
* an application of PMS core and PMS overlays under strict non-mixing discipline,
* a reproducible case artefact layer with YAML and Markdown case files,
* a reader-friendly paper layer with compact case renderings.

It treats inherited problem labels as:

```text
closure-demands
inside explicit frames (□)
with visible residues (Λ)
under declared stack conditions
and bounded output types
```

The project is designed for structural legibility, comparison, indexing, auditability, and misuse resistance.

---

## What PMS-AXIOM Is Not

PMS-AXIOM is not:

* a new PMS version,
* a new base theory,
* a diagnostic framework,
* a moral ranking tool,
* a person-evaluation system,
* a verdict machine,
* a governance or enforcement mechanism,
* a legal, clinical, forensic, empirical, or implementation authority,
* a QC correctness, performance, hardware, or physical-certification framework.

AXIOM maps structures.

It does not diagnose persons, rank dignity, assign guilt, prescribe enforcement, certify systems, or claim final metaphysical solutions.

---

## Core Thesis

Many classical problems persist because they are framed as ontological, moral, psychological, or purely logical disputes when they can also be rendered as structural closure-demands.

PMS-AXIOM does not claim that such problems are thereby “solved.”

It shows:

* what closure is being demanded,
* which frame makes that demand meaningful,
* which PMS operators carry the structure,
* which residue remains,
* whether an add-on is justified,
* which output type is admissible,
* and where misuse begins.

The central thesis is:

```text
Problems do not end where answers fail.
They end where structural closure is exhausted.
```

---

## Repository Structure

```text
PMS-AXIOM/
├── 00_source/
│   ├── PMS-AXIOM_legacy_full.md
│   └── PMS-AXIOM_Rebuild_To_Do.md
│
├── 01_blocks/
│   ├── 01_orientation_methodology.md
│   ├── 02_part_i_pms_core.md
│   ├── 03_part_ii_pms_logic.md
│   ├── 04_part_iii_pms_anticipation.md
│   ├── 05_part_iv_pms_conflict.md
│   ├── 06_part_v_pms_critique.md
│   ├── 07_part_vi_pms_eden.md
│   ├── 08_part_vii_pms_sex.md
│   ├── 09_part_viii_pms_qc.md
│   ├── 10_boundary_governance_non_mixing.md
│   └── 11_conclusion.md
│
├── 02_cases/
│   ├── markdown/
│   ├── markdown case prompts/
│   ├── yaml/
│   └── yaml case templates/
│
├── 03_model/
│   ├── PMS-AXIOM_Case_Index.yaml
│   └── PMS-AXIOM_Case_Schema.yaml
│
├── 04_PMS-AXIOM reader/
│   ├── axiom_reader.py
│   └── screenshot.png
│
└── README.md
```

---

## Layer Roles

### `00_source/`

`00_source/` contains source and rebuild documentation.

The legacy full paper remains source material only. It is not the final paper layer.

Relevant material from the old document was copied, split, shortened, revised, and adapted into the rebuilt structure.

### `01_blocks/`

`01_blocks/` contains the rebuilt paper-facing blocks.

The old full paper was split into orientation/methodology, eight part blocks, boundary/governance/non-mixing, and conclusion.

The case sections inside the blocks are compact paper-facing renderings. They are derived from the full case artefacts in `02_cases/`.

They are not full case bodies.

### `02_cases/`

`02_cases/` contains the full case layer.

It contains:

```text
02_cases/yaml/
02_cases/markdown/
02_cases/yaml case templates/
02_cases/markdown case prompts/
```

The YAML files are the authoritative machine-readable case artefacts.

The Markdown files are fuller readable case notes.

The block renderings in `01_blocks/` are derived from these YAML and Markdown artefacts.

### `03_model/`

`03_model/` contains project-level machine-readable model/index material.

Current files:

```text
03_model/PMS-AXIOM_Case_Index.yaml
03_model/PMS-AXIOM_Case_Schema.yaml
```

`PMS-AXIOM_Case_Index.yaml` is the canonical machine-readable case index.

`PMS-AXIOM_Case_Schema.yaml` records the project-level case schema and validation expectations.

Full case YAML bodies do not belong here. They remain in:

```text
02_cases/yaml/
```

### `04_PMS-AXIOM reader/`

`04_PMS-AXIOM reader/` contains the local desktop reader for navigating and inspecting the PMS-AXIOM corpus.

Current files:

```text
04_PMS-AXIOM reader/axiom_reader.py
04_PMS-AXIOM reader/screenshot.png
```

The reader is a convenience tool for local navigation and inspection. It does not replace canonical Markdown/YAML, modify PMS-AXIOM, validate PMS Base, validate case findings, certify QC workflows, assign person findings, or create governance authority.

---

## PMS-AXIOM Reader

The repository includes a single-file Tkinter reader:

```text
04_PMS-AXIOM reader/axiom_reader.py
```

Run:

```bash
python "04_PMS-AXIOM reader/axiom_reader.py"
python "04_PMS-AXIOM reader/axiom_reader.py" /path/to/PMS-AXIOM
python "04_PMS-AXIOM reader/axiom_reader.py" /path/to/PMS-AXIOM.zip
```

The reader supports local folder and ZIP loading.

It provides:

* corpus navigation for source files, blocks, Markdown case artefacts, YAML case artefacts, prompts/templates, and model files,
* case-aware navigation by Part I–VIII,
* bounded block-case rendering so a selected case does not scroll into the next case,
* switch-view buttons for each case:
  * block Markdown,
  * Markdown case artefact,
  * PMS core YAML,
  * add-on / QC / QC-EXT YAML where present,
  * MIP YAML where present,
  * AHP YAML where present,
* Markdown rendering with heading navigation,
* standalone YAML rendering with lightweight syntax highlighting,
* corpus-wide search,
* dark mode,
* reader fullscreen mode.

Screenshot:

![PMS-AXIOM Reader](04_PMS-AXIOM%20reader/screenshot.png)

Boundary:

```text
The Reader navigates and inspects local PMS-AXIOM Markdown/YAML.
It does not validate PMS Base.
It does not create case findings.
It does not certify QC workflows.
It does not evaluate persons.
It does not modify canonical files.
```

---

## Rebuild Path

The old full paper was not kept as final text.

It was rebuilt into a layered architecture:

```text
legacy full paper
→ source material
→ rebuilt paper blocks
→ rebuilt YAML case artefacts
→ rebuilt Markdown case notes
→ compact paper-facing case renderings
```

Parts of the legacy paper were copied where still useful, but revised and structurally adapted.

This applies especially to:

* orientation material,
* methodology,
* block introductions,
* block endings,
* boundary/governance material,
* conclusion material.

The cases were not copied as old full case bodies.

All cases were rebuilt through the YAML and Markdown workflow.

---

## Case Rebuild Workflow

### YAML case workflow

YAML cases were rebuilt using templates from:

```text
02_cases/yaml case templates/
```

Template files include:

```text
case template core.yaml
case template logic.yaml
case template anticipation.yaml
case template conflict.yaml
case template critique.yaml
case template eden.yaml
case template sex.yaml
case template qc.yaml
case template qc-ext.yaml
```

The YAML generation workflow followed this prompt sequence:

```text
Prompt 1 — read PMS.yaml
Prompt 2 — PMS.yaml Case Pre-Analysis
Prompt 3 — PMS Case Application Template
Prompt 4 — Final Validation against PMS.yaml and Template
Prompt 5 — Brief Content Check
Prompt 6 — Read PMS-ADDON.yaml
Prompt 7 — Generate ADDON Block (NOT for EDEN/SEX, see Prompt 12)
Prompt 8 — Brief ADDON Content Check
Prompt 9 — MIP
Prompt 10 — MIP AHP
Prompt 11 — MIP & AHP Check
Prompt 12 — EDEN / SEX (split output in two by default)
```

This produced the full structured YAML case layer in:

```text
02_cases/yaml/
```

### Markdown case workflow

Readable Markdown case notes were rebuilt using prompts from:

```text
02_cases/markdown case prompts/
```

Prompt files include:

```text
block article generation.md
case article generation.md
case yaml generation.md
```

The Markdown article workflow followed this sequence:

```text
PROMPT 1 - Base Article
PROMPT 2 - Generate 3 Examples
PROMPT 3 - Produce Final Case Article
PROMPT 4 - Final Check
```

This produced fuller readable case notes in:

```text
02_cases/markdown/
```

### Paper-facing renderings

After YAML and Markdown reconstruction, shorter case renderings were created for the relevant paper blocks in:

```text
01_blocks/
```

Each paper-facing case rendering preserves:

```text
case purpose
active stack
add-on choice / no-add-on status
what the analysis shows
output type
misuse boundary
```

The full structure remains in YAML.

The fuller readable explanation remains in Markdown.

---

## Stack Discipline

PMS-AXIOM uses explicit stack discipline.

The stack is determined by the case artefact.

### PMS core

```text
PMS core
```

PMS core only.

No add-on is attached.

No add-on signature or add-on drift catalogue is used.

### PMS core + add-on

```text
PMS core → PMS + [ADD-ON]
```

The add-on is a non-mixing overlay lens.

It sharpens a domain-specific risk field.

It does not redefine PMS operators.

### PMS core + QC

```text
PMS core → PMS + QC
```

QC is a workflow-audit mapping layer.

It makes QC-adjacent workflow structure inspectable.

It does not certify quantum systems or validate implementations.

### PMS core + QC + QC-EXT

```text
PMS core → PMS + QC → PMS + QC-EXT
```

QC-EXT is used only where extension-level QC structure is explicitly warranted.

Where QPE, Grover, attractor/fixed-point, basis, measurement-domain, or stabilizer detail is missing, non-activation is the correct result.

### MIP

```text
PMS core / add-on artefact → MIP
```

MIP is downstream artefact governance.

It evaluates artefact use conditions, not persons.

### MIP + AHP

```text
PMS core / add-on artefact → MIP → AHP
```

AHP is second-order analysis-artefact hardening.

It does not rescore, activate D, upgrade transmission status, or create new findings.

---

## Non-Mixing Rule

PMS core supplies the canonical Δ–Ψ operator grammar.

Add-ons are overlay lenses.

They may add:

```text
reduced signatures
drift catalogues
regime labels
validity handles
reach levels
publicness handles
audit handles
policy checks
```

They may not add new PMS operators.

They may not redefine existing PMS operators.

They may not silently escalate a PMS core case into an add-on case.

They may not convert risk into finding.

They may not convert structural readability into authority.

---

## Case Suite

### Part I — PMS Core

Output types: boundary, taxonomy, structural reading.

Cases:

1. Personal identity over time
2. Free will vs determinism
3. Moral luck
4. Universals
5. Causality
6. Time / temporality
7. Invariance
8. Poincaré recurrence
9. Freedom
10. Responsibility
11. Truth
12. Meaning / sense

### Part II — PMS + LOGIC

Output types: taxonomy, boundary, anti-drift policy, structural reading.

Cases:

13. Problem of induction
14. Underdetermination
15. Gettier problems
16. Grounding regress
17. Rule-following paradox
18. Hermeneutic circle
19. Truth theories
20. Why philosophy seeks closure
21. Dogmatism / Σ-totalization
22. Explanation / closure drive

### Part III — PMS + ANTICIPATION

Output types: calibration report, boundary policy, structural reading.

Cases:

23. Other minds
24. Calibrating trust correctly
25. Forecasting without prophecy
26. Reversible planning
27. Irreversible commitments
28. Downstream effects of decisions

### Part IV — PMS + CONFLICT

Output types: tragedy formalism, repair policy, boundary-managed non-resolution.

Cases:

29. Conflict as structural incompatibility
30. Escalation vs repair
31. Trolley dilemmas
32. Tragedy as a category
33. Structural injustice
34. Dirty hands / forced choice
35. Asymmetry lock-in

### Part V — PMS + CRITIQUE

Output types: reach policy, disclosure/publicness rule, structural reading.

Cases:

36. Critique Reach
37. Interpretability vs. Reality
38. Epistemic Injustice
39. Legitimacy Without Authority
40. Privacy vs. Publicness

### Part VI — PMS + EDEN

Output type: regime taxonomy.

Cases:

41. Pseudo-Symmetry
42. Recognition
43. Trust
44. Boundary Erosion
45. Repair Relationships

### Part VII — PMS + SEX

Output type: validity gate.

Cases:

46. Consent Under Asymmetry
47. Consent Laundering
48. Boundary Confusion

### Part VIII — PMS + QC / QC-EXT

Output type: audit trace.

Cases:

49. QC-Workflow Governance
50. Oracle-Asymmetry Audit
51. Measurement & Non-events
52. Stabilised Iteration

---

## Output Types

PMS-AXIOM uses bounded output types.

These are not prescriptions, verdicts, diagnoses, or certifications.

They include:

```text
Boundary
Taxonomy
Boundary / anti-drift policy
Regime taxonomy
Reach policy
Disclosure / publicness rule
Validity gate
Audit trace
```

Each output type declares what the case may legitimately yield.

Claims beyond the declared output type are treated as drift risks or category errors.

---

## Misuse Boundaries

PMS-AXIOM blocks the following conversions:

```text
structural readability → verdict
operator fit → proof
coherence → evidence
drift risk → drift finding
reduced signature → diagnosis
taxonomy → ranking
boundary → prescription
policy → enforcement
validity gate → legal conclusion
audit trace → certification
QC macro → physical claim
MIP hook → person evaluation
AHP hardening → evidentiary upgrade
D-language → dignity ranking
Λ-residue → failure
non-assignment → low score
publicness → accountability by default
repair language → achieved repair
consent sign → consent validity
asymmetry → guilt
formal exit → real exit
trace existence → review
review vocabulary → governance
```

Risk is not finding.

Fit is not proof.

Coherence is not evidence.

A structurally smooth reading may still be under-specified.

---

## Intended Use

PMS-AXIOM is intended for:

* structural theory work,
* philosophical reformulation,
* case comparison,
* indexing of closure-demands,
* audit-sensitive reasoning,
* machine-readable case inspection,
* boundary-aware use of PMS overlays,
* analysis of where reasoning must stop.

It is not intended for:

* adjudicating persons,
* enforcing policy,
* diagnosing relationships,
* deciding consent,
* ranking dignity,
* assigning guilt,
* certifying systems,
* replacing domain expertise.

Any use of PMS-AXIOM must preserve:

```text
frame discipline
Χ-distance
reversibility where possible
Dignity-in-Practice constraints
Λ-residue
declared output type
misuse boundary
```

---

## Root Paper Assembly

The rebuilt root paper is assembled from the paper-facing blocks in:

```text
01_blocks/
```

The paper preserves the full chapter architecture while avoiding full in-paper case bodies.

The block files contain compact chapter-facing case renderings only.

Full machine-readable case structures remain in:

```text
02_cases/yaml/
```

Fuller readable explanations remain in:

```text
02_cases/markdown/
```

Project-level indexing and schema material remain in:

```text
03_model/
```

The local reader remains in:

```text
04_PMS-AXIOM reader/
```

The root paper depends on the case layer, but does not replace it.

---

## Final Note

PMS-AXIOM does not solve classical problems by producing final answers.

It shows what kind of closure is being demanded, what would be required to support it, and where the demand must stop.

PMS provides the operator theory.

PMS-AXIOM shows how to use it across a structured case suite without operator mixing, add-on inflation, governance laundering, person evaluation, or false closure.

---

## Links and Resources

### PMS Core Theory and Model

| Category        | Resource                                                                                 | Description                                            |
| --------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Project website | [PMS Theory Site](https://pms-theory.netlify.app)                                        | Canonical PMS theory reference                         |
| GitHub repo     | [PMS Theory / Repository](https://github.com/tz-dev/Praxeological-Meta-Structure-Theory) | PMS grammar, theory texts, YAML/JSON model definitions |
| DOI             | [PMS Theory DOI](https://doi.org/10.5281/zenodo.17075154)                                | Archived reference version of the PMS base theory      |

### PMS Domain Lenses and Overlays

| Category    | Resource                                                       | Description                                                        |
| ----------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| GitHub repo | [PMS-ANTICIPATION](https://github.com/tz-dev/PMS-ANTICIPATION) | Anticipatory praxis under uncertainty                              |
| GitHub repo | [PMS-CRITIQUE](https://github.com/tz-dev/PMS-CRITIQUE)         | Critique as interruption, recontextualization, and correction      |
| GitHub repo | [PMS-CONFLICT](https://github.com/tz-dev/PMS-CONFLICT)         | Conflict as stabilized incompatibility                             |
| GitHub repo | [PMS-EDEN](https://github.com/tz-dev/PMS-EDEN)                 | Drift from praxis to comparison, pseudo-symmetry, reciprocity loss |
| GitHub repo | [PMS-LOGIC](https://github.com/tz-dev/PMS-LOGIC)               | Structural responsibility, logical limits, post-moral effects      |
| GitHub repo | [PMS-SEX](https://github.com/tz-dev/PMS-SEX)                   | Sexuality as framed impulse, asymmetry, time, exit, and binding    |
| GitHub repo | [PMS-QC](https://github.com/tz-dev/PMS-QC)                     | PMS structural layer for quantum computing                         |

### PMS Downstream Applications and Architectures

| Category    | Resource                                                             | Description                                                                                                                                                                                                                                                                                                             |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub repo | [PMS-AXIOM](https://github.com/tz-dev/PMS-AXIOM)                     | Cartography of classical closure-demands across the PMS stack                                                                                                                                                                                                                                                           |
| GitHub repo | [PMS-STACK](https://github.com/tz-dev/PMS-STACK)                     | Implementation-layer PMS architecture specification for abstract machine, virtual CPU, OS, runtime, language, security, networking, distributed systems, tooling, simulation, verification, boot, and cluster profiles ([book website](https://pms-stack.netlify.app) / [amazon](https://www.amazon.com/dp/B0G6G7V38P)) |
| GitHub repo | [PMS-RUST](https://github.com/tz-dev/PMS-RUST)                       | Executable PMS-STACK Evidence Spine: Rust kernel, REPL, validation, JSONL, vFS, AI bridge                                                                                                                                                                                                                               |
| GitHub repo | [PMS-EMERGENCE MODEL](https://github.com/tz-dev/PMS-EMERGENCE_MODEL) | Claim-disciplined developmental architecture for trace-backed emergence                                                                                                                                                                                                                                                 |
| GitHub repo | [PMS — UNDER LOAD](https://github.com/tz-dev/PMS---UNDER-LOAD)       | Structural self-critique of PMS under calibration, coverage, stack drift, publicness, and self-application                                                                                                                                                                                                              |

### MIP: Adjacent Praxeological Ecosystem

| Category | Resource | Description |
|---|---|---|
| GitHub repo | [Maturity-in-Practice Repository](https://github.com/tz-dev/Maturity-in-Practice) | Maturity in Practice model + attack surface hardening addon ([book website EN](https://maturity-in-practice.netlify.app) / [book website DE](https://reife-im-vollzug.netlify.app) / [amazon EN](https://www.amazon.com/dp/B0G4XBKNNR) / [amazon DE](https://www.amazon.de/dp/B0G4SPBDQD)) |
| Book website | [Maturity in Practice (EN)](https://maturity-in-practice.netlify.app) | English book website for *Maturity in Practice – A Praxeological Anthropology* |
| Book website | [Reife im Vollzug (DE)](https://reife-im-vollzug.netlify.app) | German book website for *Reife im Vollzug – Eine praxeologische Anthropologie* |
| Book on Amazon | [Maturity in Practice on Amazon](https://www.amazon.com/dp/B0G4XBKNNR) | Published English edition |
| Book on Amazon | [Reife im Vollzug on Amazon](https://www.amazon.de/dp/B0G4SPBDQD) | Published German edition |

### Interactive Assistants

| Category      | Resource                                                                                                                           | Description                                     |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| GPT assistant | [PMS Model Assistant](https://chatgpt.com/g/g-69358a2a4980819183da6a97893389cf-pms-model-assistant)                                | Interactive PMS.yaml exploration and validation |
| GPT assistant | [Maturity in Action](https://chat.openai.com/g/g-693460d3def48191ad08647301645a2e-maturity-in-action-a-praxeological-anthropology) | Applied praxeological anthropology assistant    |

---

## 🤝 Contributing

Contributions, critiques, and structural questions are welcome.

### Contribution scope (structural only)

In scope:

* additional case mappings following the schema and guardrails,
* clarifications of drift or closure patterns,
* documentation improvements that strengthen misuse resistance,
* tooling that consumes PMS.yaml + PMS-AXIOM cases without redefining operators.

Out of scope:

* new operators or dependency changes,
* person-typing or diagnostic language,
* normative or enforcement claims,
* implicit governance without declaration.

---

## 📜 License

* The **paper** is released under **CC BY 4.0**.

Specification artefacts follow the repository’s LICENSE unless stated otherwise.

---

## 📬 Contact

Maintained by **tz-dev**.
For discussion or questions, please use GitHub issues.
