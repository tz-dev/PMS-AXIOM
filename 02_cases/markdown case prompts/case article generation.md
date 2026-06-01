# Case Article Generation

## PROMPT 1 - Base Article

You have already read and applied the relevant PMS / addon / MIP / AHP / QC YAML files in this chat.

Now create a chapter-ready, analytically substantial Markdown case article from the completed YAML analyses in this chat.

Use the completed YAML analyses as authoritative artefacts.

This is NOT a short case note.
This is NOT a compact capsule.
This is NOT a summary of selected fields.
This is a full human-readable article rendering of the completed YAML analyses.

MANDATORY TITLE RULE:
Begin with the exact case title from the completed YAML as an H2 heading:

## [EXACT CASE TITLE]

Do not invent a different title.
Do not use a topic label, paper section label, old working title, or overlay theme as the heading.

CORE TASK:
Transform the YAML analyses into polished academic Markdown prose.
Do not merely summarize.
Do not compress away the analytical architecture.
Do not omit major YAML blocks.
Do not output YAML.
Do not include code blocks.

Use the YAMLs in layered order:
1. PMS Core YAML
2. relevant add-on overlay YAML, if present
3. MIP YAML, if present
4. MIP-AHP / QC / QC-EXT YAML, if present

For each layer, preserve:
- what the layer is allowed to claim
- what it is not allowed to claim
- what it adds beyond the previous layer
- what remains non-captured
- what would weaken or falsify the reading

Required structure:

## [EXACT CASE TITLE]

### Case capsule

Include:
**Case file(s):** ...
**Stack:** ...
**Case type:** ...
**Concrete-scene status:** ...
**Output type:** ...
**Add-on decision:** ...
**MIP / AHP / QC status:** ...
**Claim boundary:** ...

### Why this case matters

Explain the philosophical closure-demand in depth.
Explain why this case belongs in AXIOM.
Explain what makes it structurally difficult.
Explain why it is not being solved metaphysically, empirically, clinically, legally, or diagnostically.

### Claim status and scope discipline

Render the YAML claim-typing in prose:
- case type
- claim status
- concrete-scene status
- empirical boundary
- metaphysical boundary
- diagnostic boundary
- legal/forensic boundary
- implementation boundary
- PMS Base validation boundary
- operationalization status

Do not reduce this to one paragraph if the YAML contains more distinctions.

### Scene and frame structure

Render the scene packet or conceptual scene:
- scene boundary
- frame □
- what is inside the frame
- what is outside the frame
- protected constraints
- roles, if present
- temporality Θ
- reversibility window
- exposure and asymmetry conditions

If the case is not a concrete scene, explain precisely what follows from that.

### PMS Core structural reading

Give a substantial PMS Core reading.

Do not only list operators.
Transform the operator analysis into prose.

Include all relevant PMS operators in order:
Δ, ∇, □, Λ, Α, Ω, Θ, Φ, Χ, Σ, Ψ.

For each operator:
- explain its case-specific role
- mark active / weak / not applicable status where relevant
- explain calibration issues
- explain dependency risks
- explain what would be overclaim if the operator were pushed too far

Especially preserve calibration for:
Χ, Φ, Σ, Ψ, Ω, Θ, and Λ.

### PMS dependency and calibration discipline

Explain:
- why later operators cannot be used cheaply
- where Σ or Ψ remain conditional
- why coherence is not proof
- why non-capture is not failure
- why PMS must not become a closure machine
- what dependency shortcuts would be invalid

### Derived structures

Render the YAML treatment of:
- Awareness_A
- Coherence_C
- Responsibility_R
- Action_E
- Dignity_in_Practice_D
- SELF_FIXPOINT

For each:
- say whether it is active, weak, conditional, not applicable, or analytic-only
- explain why
- preserve that derived structures are formula-derived, not primitive

### PMS drift-pattern status

Render the PMS drift-pattern analysis:
- AD_A>>E
- AD_Sigma_low
- any related coherence or under-discrimination risks

Make clear:
- risk is not finding
- under-specification is not failure
- non-assignment is not low score

### Add-on / overlay reading

Use this section only if an add-on exists.

Name the add-on explicitly.

Explain:
- why PMS Core alone is not the final layer here
- what the add-on makes visible that PMS Core alone does not isolate
- which add-on reduced signatures are active, weak, or not applicable
- which add-on constructs are non-operator overlay handles
- which add-on drift risks are active as risks, not findings
- how the add-on remains subordinate to PMS Base

For PMS-LOGIC specifically, render in depth:
- pre-moral justification layer
- logical boundary management
- post-moral effects
- non-closure
- effective capacity, if applicable
- non-innocence, if applicable
- responsibility without ought, if applicable
- reduced signatures
- boundary constructs
- failure mode constraints
- LOGIC drift risks
- counter-readings
- overlay non-capture zones
- MIP / AHP trigger status
- final LOGIC overlay formula or signature

Do not collapse this into a short overlay summary.

### Layer interaction

Explain how the PMS Core reading and add-on reading interact.

Include:
- what remains PMS Core
- what the add-on sharpens
- what the add-on must not be allowed to redefine
- where overlay language could overreach
- where non-closure remains visible

### Non-capture and rival readings

Render all rival readings from the YAML:
- epistemological
- phenomenological
- language-practice
- ethical
- anti-capture
- or other case-specific rival readings

Explain what each rival reading preserves that PMS or the add-on may not fully capture.

Do not treat rival readings as defects.

### Weakening, falsifier, and operationalization conditions

Render the YAML falsifier and weakening logic in full.

Include:
- what would weaken the PMS reading
- what would weaken the add-on reading
- what would make the reading under-discriminating
- what would make the reading over-assimilative
- what evidence or scene data would be required for stronger claims
- what operationalization remains unfulfilled

### Misuse boundary

Give a substantial misuse-boundary section.

Include:
- no diagnosis
- no person ranking
- no legal/forensic conclusion
- no metaphysical proof
- no empirical proof unless warranted
- no implementation validation
- no PMS Base validation
- no add-on-as-operator
- no drift-as-verdict
- no closure-by-authority

### Example placement notes

Do not generate examples yet.

Explain:
- what kinds of examples would fit
- what examples must avoid
- recommended example depth: micro | compact | worked | flagship
- where examples should be inserted later

LENGTH AND DEPTH REQUIREMENT:
Normal case target: 3,500–6,000 words.
Flagship or multi-layer case target: 6,000–9,000 words.
Do not compress below the analytical density of the YAMLs.
If the answer would be too long, split into exactly two parts.

SPLIT RULE:
If splitting is needed, output PART 1 first only.

PART 1 must include:
- title
- case capsule
- why this case matters
- claim status and scope discipline
- scene and frame structure
- PMS Core structural reading
- PMS dependency and calibration discipline
- derived structures
- message at the end: "Ready for Part 2." if output is split in two parts

End PART 1 after the derived structures section.
Do not continue into PMS drift-pattern status.

PART 2 must begin with:
### PMS drift-pattern status

and continue through:
### Example placement notes

Do not repeat PART 1.
Do not add prose outside the Markdown article.

Output Markdown only.

---

## PROMPT 2 - Generate 3 Examples

Now generate 3 article-ready examples for the Markdown case article drafted above.

The examples must fit the actual analysis and boundaries.
They should demonstrate the analysis; they must not replace it.
They should prepare material for a later conclusion, but must not write the conclusion.

Output Markdown only.
Do not output YAML.
Do not use code blocks.

Use this structure:

### Example 1 — [example title]

**Type:** micro | compact | worked | flagship  
**Recommended insertion point:** ...

Then write the example as polished article prose.

Each example must include:
- a bounded vignette
- what the example demonstrates
- PMS Core hooks
- add-on hooks if relevant
- MIP / AHP / QC status if relevant
- forbidden claims
- non-capture note
- article takeaway

Do not flatten these into labels only.
Write readable prose.

Rules:
- Do not generate full case YAMLs.
- Do not assign scores unless the section explicitly warrants that.
- Do not turn risks into findings.
- Do not turn examples into verdicts.
- Do not diagnose.
- Do not rank persons.
- Do not make legal/forensic, clinical, metaphysical, empirical, implementation, or PMS Base validation claims.
- Keep examples concrete enough to be readable but bounded enough not to overclaim.
- If the section is high-risk, make examples abstract/guardrail-only.
- Prefer examples that can be reused across nearby sections.
- Do not write the final case conclusion.

Recommended depth:
- micro: 250–400 words each
- compact: 400–700 words each
- worked: 800–1,200 words each
- flagship: 1,200–1,800 words each

For this case, choose the depth recommended in the article draft unless it clearly conflicts with the case boundaries.

Output Markdown only.

---

## PROMPT 3 - Produce Final Case Article

Now produce the final integrated Markdown case article.

Use:
- the completed YAML analyses in this chat
- the full Markdown article draft from Pass 1 (do NOT cut important, inner-logical content)
- the 3 Markdown examples from Pass 2

Purpose:
- Produce the final chapter-ready Markdown case article.
- Integrate the examples into the article at appropriate locations.
- Add the final conclusion.
- Preserve the analytical depth of the YAMLs and Pass 1.
- Do not compress the article into a summary.
- Do not remove major analytical sections from Pass 1.
- Do not add new case claims.
- Do not redo the YAML analysis.
- Do not turn examples into evidence.
- Do not make the conclusion sound more certain than the YAMLs allow.
- Do not introduce new examples.

MANDATORY TITLE RULE:
Begin with the exact case title from the completed YAML as an H2 heading:

## [EXACT CASE TITLE]

Required final structure:

## [EXACT CASE TITLE]

### Case capsule

### Why this case matters

### Claim status and scope discipline

### Scene and frame structure

### PMS Core structural reading

### PMS dependency and calibration discipline

### Derived structures

### PMS drift-pattern status

### Add-on / overlay reading
Use only if present.

### Layer interaction
Use only if an add-on, MIP, AHP, QC, or QC-EXT layer exists.

### Example 1 — [title]

### Example 2 — [title]

### Example 3 — [title]

### Non-capture and rival readings

### Weakening, falsifier, and operationalization conditions

### Misuse boundary

### Case conclusion

The conclusion should include:
1. Integrative result
2. What the examples contribute
3. What remains unclaimed
4. Boundary discipline
5. Final methodological takeaway

PRESERVATION RULE:
Do not shorten the Pass 1 analysis into a compact case note.
Do not delete operator-by-operator reading.
Do not delete derived-structure analysis.
Do not delete add-on reduced signatures or drift risks.
Do not delete falsifier / weakening / operationalization conditions.
Do not delete non-capture or rival readings.
Do not delete claim boundaries.

Boundary rules:
- no empirical proof unless explicitly warranted
- no diagnosis
- no person ranking
- no legal/forensic conclusion
- no metaphysical proof
- no implementation validation
- no PMS Base validation
- no drift finding unless explicitly warranted
- risk is not finding
- coherence is not proof
- non-assignment is not low score
- non-capture remains possible
- resistance, refusal, non-fit, disagreement, rupture, or absence are not automatically drift
- Dignity-in-Practice remains praxeological, not ontological
- add-on terms remain overlay handles, not PMS operators
- AHP/QC notes harden the analysis but do not rescore it

LENGTH AND DEPTH REQUIREMENT:
Normal final case article target: 5,000–8,000 words.
Flagship or multi-layer final case article target: 8,000–12,000 words.
Do not compress below the depth of the source YAMLs.

If the final article is too long, split into exactly two parts.

SPLIT RULE:
PART 1 must include:
- title
- case capsule
- why this case matters
- claim status and scope discipline
- scene and frame structure
- PMS Core structural reading
- PMS dependency and calibration discipline
- derived structures
- PMS drift-pattern status
- a message to the user "Part 1 finished. Ready to go for part 2."

PART 2 must begin with:
### Add-on / overlay reading

and continue through:
### Case conclusion

Do not repeat PART 1.
Output Markdown only.
No YAML.
No code blocks.
No meta-commentary.

---

## PROMPT 4 - Final Check

Is there anything that still needs to be updated, expanded, deepened, etc. — and are the examples sufficiently explained rather than under-explained? 

Check carefully, keep your conscience clean, and give EXACT find/replace blocks.
