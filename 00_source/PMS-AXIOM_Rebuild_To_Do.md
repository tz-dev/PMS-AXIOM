# PMS-AXIOM Rebuild To-Do

This file documents the completed PMS-AXIOM rebuild path.

The legacy full paper was split into the current project structure. The old paper remains source material only. Parts of the old text were copied into the new structure where still usable, but they were revised, shortened, and structurally adapted. This applies especially to orientation material, block introductions, block endings, boundary/governance material, and the conclusion.

The case layer was not copied as old full case bodies. All cases were rebuilt through the YAML and Markdown workflow described below.

## 00_source

`00_source/` contains the legacy source and rebuild documentation.

```text
00_source/PMS-AXIOM_legacy_full.md
00_source/PMS-AXIOM_Rebuild_To_Do.md
````

`PMS-AXIOM_legacy_full.md` is source material only.

## 01_blocks

`01_blocks/` contains the rebuilt paper-facing blocks.

The legacy full paper was split into:

```text
01_blocks/01_orientation_methodology.md
01_blocks/02_part_i_pms_core.md
01_blocks/03_part_ii_pms_logic.md
01_blocks/04_part_iii_pms_anticipation.md
01_blocks/05_part_iv_pms_conflict.md
01_blocks/06_part_v_pms_critique.md
01_blocks/07_part_vi_pms_eden.md
01_blocks/08_part_vii_pms_sex.md
01_blocks/09_part_viii_pms_qc.md
01_blocks/10_boundary_governance_non_mixing.md
01_blocks/11_conclusion.md
```

The block files contain the paper-facing version of the rebuilt text.

The beginning and ending sections of the blocks were copied from the legacy paper where useful, then revised to match the current AXIOM structure, stack discipline, and case-layer workflow.

The case sections inside the blocks are shortened paper-facing renderings. They are based on the rebuilt case artefacts in `02_cases/`, not on copied old full case bodies.

## 02_cases

`02_cases/` contains the rebuilt full case layer.

```text
02_cases/markdown/
02_cases/markdown case prompts/
02_cases/yaml/
02_cases/yaml case templates/
```

The YAML files are the authoritative machine-readable case artefacts.

The Markdown files are the fuller readable case notes.

The block case sections in `01_blocks/` are derived from these YAML and Markdown artefacts.

### YAML case rebuild workflow

YAML cases were rebuilt using the YAML templates in:

```text
02_cases/yaml case templates/
```

Templates include:

```text
case template anticipation.yaml
case template conflict.yaml
case template core.yaml
case template critique.yaml
case template eden.yaml
case template logic.yaml
case template qc-ext.yaml
case template qc.yaml
case template sex.yaml
```

The YAML generation workflow followed these prompts:

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

This workflow produced the full structured YAML case layer in:

```text
02_cases/yaml/
```

The YAML layer includes PMS core cases, PMS add-on cases, QC/QC-EXT cases, and downstream MIP/AHP artefacts where used.

Stack discipline in the YAML layer:

```text
PMS core
PMS core + add-on
PMS core + QC
PMS core + QC + QC-EXT
PMS core / add-on artefact + MIP
PMS core / add-on artefact + MIP + AHP
```

PMS core cases have no add-on.

Add-on cases use the relevant overlay only.

MIP and AHP are downstream artefact layers, not PMS operators and not person-evaluation layers.

### Markdown case rebuild workflow

Readable Markdown case notes were rebuilt using the prompts in:

```text
02_cases/markdown case prompts/
```

Prompt files:

```text
block article generation.md
case article generation.md
case yaml generation.md
```

The Markdown article workflow followed these steps:

```text
PROMPT 1 - Base Article
PROMPT 2 - Generate 3 Examples
PROMPT 3 - Produce Final Case Article
PROMPT 4 - Final Check
```

This workflow produced the fuller readable case notes in:

```text
02_cases/markdown/
```

The Markdown notes explain the case purpose, active stack, add-on choice or no-add-on status, structural reading, examples, output type, misuse boundary, rival readings, and case takeaway.

They are not copied old case bodies.

### Paper-facing case renderings

After YAML and Markdown case reconstruction, shorter case renderings were created for the relevant block files in:

```text
01_blocks/
```

These renderings preserve the paper argument without reproducing the full case bodies.

Each paper-facing case rendering keeps:

```text
case purpose
active stack
add-on choice / no-add-on status
what the analysis shows
output type
misuse boundary
```

The full case structure remains in `02_cases/yaml/`.

The fuller readable case note remains in `02_cases/markdown/`.

## 03_model

`03_model/` contains the project-level machine-readable model/index layer.

It is used for schema, index, and validation material.

Full case YAML bodies remain in:

```text
02_cases/yaml/
```

## 04_reference

`04_reference/` contains human-readable reference and navigation material for the rebuilt project.

## 05_PMS-AXIOM Reader

The reader tooling lives in:

```text
05_PMS-AXIOM Reader/
```

Current files:

```text
05_PMS-AXIOM Reader/axiom_reader.py
05_PMS-AXIOM Reader/screenshot.png
```

The reader was adapted to the current PMS-AXIOM folder structure and the rebuilt case layer.

## README.md

`README.md` was updated to reflect the rebuilt project structure, including:

```text
00_source/
01_blocks/
02_cases/
03_model/
04_reference/
05_PMS-AXIOM Reader/
```

## Layer discipline

The rebuild preserves the PMS-AXIOM layer discipline:

```text
PMS core supplies the canonical Δ–Ψ operator grammar.
PMS add-ons are non-mixing overlay lenses.
Add-ons do not redefine PMS operators.
MIP evaluates analysis artefacts and use conditions, not people.
AHP hardens analysis artefacts; it does not rescore or create new findings.
AXIOM maps frames, closure-demands, Λ-residues, operator chains, add-on signatures, drift risks, output types, and optional governance hooks.
AXIOM does not diagnose, evaluate persons, rank dignity, assign guilt, prescribe enforcement, or create a new base model.
```
