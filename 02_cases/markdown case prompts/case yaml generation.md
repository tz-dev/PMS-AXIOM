# Case YAML Generation

## Prompt 1 — read PMS.yaml

Read the attached PMS.yaml exactly, deeply, and completely.

Treat PMS.yaml as the only PMS Base reference for this chat.

Do not analyze any case yet.
Do not summarize PMS.yaml.
Do not provide content feedback.
Do not generate a template.
Do not infer or invent missing structures.

After reading, respond only with:

Read completely.

---

## Prompt 2 — PMS.yaml Case Pre-Analysis

You have already read PMS.yaml completely.

Using only PMS.yaml as PMS Base, analyze the following case structurally through PMS_1.3.

CASE TITLE: Boundary erosion (Privacy → Publicness)

CASE MATERIAL:
Confidential feedback / internal resolution vs public accountability discourse. Boundary erosion is the drift where material made for a bounded repair frame is moved into a public/tribunal frame.

Produce a compact PMS case pre-analysis with:

- case typing
- claim status
- concrete-scene status
- empirical / metaphysical / diagnostic / legal-forensic / implementation / PMS Base validation boundaries
- active / weak / not applicable operators Δ, ∇, □, Λ, Α, Ω, Θ, Φ, Χ, Σ, Ψ
- operator dependency risks
- major calibration points, especially for Χ, Φ, Σ, Ψ, Ω, Θ, and Λ where relevant
- derived structures status:
  - Awareness_A
  - Coherence_C
  - Responsibility_R
  - Action_E
  - Dignity_in_Practice_D
  - SELF_FIXPOINT
- asymmetry drift-pattern status:
  - AD_A>>E
  - AD_Sigma_low
- non-capture zones
- rival readings or rival formalizations
- falsifier conditions
- coherence risk / under-discrimination risk
- operationalization requirements
- final recommended PMS case formula

Do not claim empirical, metaphysical, diagnostic, legal/forensic, clinical, implementation, or PMS Base validation unless explicitly warranted by the case material.

Do not treat PMS coherence as sufficient by itself.

Do not automatically translate resistance, rupture, non-fit, disagreement, absence, or rival framing into PMS drift, incomplete calibration, incomplete integration, recontextualization, or maturity failure.

Preserve possible non-capture.

Keep the analysis reversible, bounded, non-diagnostic, non-tribunal, non-person-ranking, and open to rival formalizations.

Do not shorten texts/answers/responses/fields/points to be filled.

Stay as close to PMS.yaml as possible, and do not omit any requested pre-analysis items.

---

## Prompt 3 — PMS Case Application Template

You have already read PMS.yaml completely.

You have also produced a PMS case pre-analysis for the following case:

CASE TITLE: Boundary erosion (Privacy → Publicness)

Now fill the attached PMS Case Application Template completely for the case.

PMS BASE DISCIPLINE:

- PMS.yaml is the only PMS Base reference.
- The PMS case pre-analysis is only an application aid.
- The template is an application schema, not PMS Base.
- If PMS.yaml, the pre-analysis, and the template conflict, PMS.yaml has priority.
- Do not modify, rewrite, or extend PMS.yaml.
- Do not copy PMS.yaml wholesale into the case analysis unless the template explicitly requires a reference field.
- Do not treat any domain application, governance layer, implementation layer, bridge mapping, critique layer, prior analysis, or case template as PMS Base unless it is explicitly present in PMS.yaml.

STRICT PMS CONSTRAINTS:

- Use only the PMS operators, principles, derived structures, guardrails, dependency logic, entry conditions, and application discipline defined in PMS.yaml.
- Do not invent PMS operators, axes, layers, principles, derived structures, guardrails, or add-ons.
- Preserve the PMS operator inventory:
  Δ, ∇, □, Λ, Α, Ω, Θ, Φ, Χ, Σ, Ψ.
- Preserve PMS operator order, dependencies, definitions, provides-fields, examples, and status-within-PMS where the template asks for them.
- Treat derived structures as derived, not primitive.
- If using Awareness, Coherence, Responsibility, Action, Dignity-in-Practice, SELF_FIXPOINT, or drift patterns, derive them from PMS.yaml formulas and do not treat them as independent axioms.
- Treat Dignity-in-Practice as a praxeological application constraint, not as ontological ranking or moral superiority.
- Treat asymmetry drift patterns as conditional structural risks, not diagnoses, person-types, moral verdicts, or clinical categories.

CLAIM-TYPING DISCIPLINE:

Explicitly type the claim being made using the template fields, including:

- claim_status
- case_type
- empirical_status
- result_status
- not_a_concrete_scene
- pms_base_validation

Distinguish carefully between:

- PMS-internal structural derivation
- concrete scene analysis
- conceptual domain projection
- empirical finding
- metaphysical claim
- diagnostic claim
- legal/forensic claim
- implementation claim
- PMS Base validation

If the case is not a concrete praxis scene, mark:

not_a_concrete_scene: true

Do not claim metaphysical, diagnostic, legal/forensic, empirical, clinical, implementation, or PMS Base validation unless the case material explicitly provides the needed grounds.

QUALITY-CONTROL DISCIPLINE:

- Treat PMS coherence as insufficient by itself.
- A coherent PMS derivation must still show discriminative force.
- Preserve possible non-capture.
- Do not automatically translate resistance, rupture, non-fit, disagreement, rival framing, unresolved absence, or missing evidence into PMS drift, incomplete calibration, incomplete integration, recontextualization, or maturity failure.
- Include falsifier conditions.
- State what would weaken, under-specify, overextend, or invalidate the PMS reading of the case.
- Include calibration points for every operator carrying major analytic weight, especially Χ, Φ, Σ, Ψ, Ω, Θ, and Λ when relevant.
- Keep the analysis reversible, scene-bound or case-type-bound, non-diagnostic, non-tribunal, non-person-ranking, and open to rival formalizations.
- If the case strongly fits PMS, explicitly mark the coherence_risk that the PMS reading may become too smooth or under-discriminating.
- Include operationalization requirements if the analysis would require empirical, comparative, computational, legal, clinical, or applied validation.
- Mark such requirements as not fulfilled unless the case provides the needed evidence.
- Do not shorten texts/answers/responses/fields/points.

TEMPLATE COMPLETION REQUIREMENTS:

- Fill the provided PMS Case Application Template completely.
- Output one complete valid English YAML document.
- Use the template as the required case-output schema.
- Do not omit any field required by the provided template.
- Replace every placeholder in the template with a case-specific value.
- Do not leave placeholder brackets such as <...>, [...], or "...".
- Do not add commentary before or after the YAML.
- Do not output Markdown prose outside the YAML code block.
- Use only one YAML code block unless splitting is required by length.

DRIFT-PATTERN TEMPLATE UPDATE REQUIREMENT:

Where the template contains the AD_A>>E axis effects block, use this form:

axis_effects:
  awareness_axis: "<over_expanded | not_applicable | under_specified>"
  action_axis: "<suppressed_or_chronically_delayed | not_applicable | under_specified>"

Where the template contains the AD_Sigma_low axis effects block, use this form:

axis_effects:
  coherence_axis: "<volatile | not_applicable | under_specified>"
  responsibility_axis: "<inconsistent | not_applicable | under_specified>"

When filling the case, replace these placeholders with case-specific values.

BEFORE OUTPUTTING, INTERNALLY CHECK:

- YAML parses as valid YAML.
- The output follows the provided template.
- Every required template field is present.
- No placeholders remain.
- PMS.yaml has not been redefined.
- No non-PMS operators or structures have been added.
- All eleven PMS operators are represented where required by the template.
- Derived structures are formula-derived, not primitive.
- Dignity-in-Practice is not treated as ontological dignity.
- Possible non-capture is preserved.
- Rival readings remain open.
- Falsifier conditions are included.
- PMS Base validation is not claimed.

OUTPUT FORMAT:

If the output fits in one response, return only one YAML code block:

```yaml
[complete filled YAML document]
````

IF THE OUTPUT IS TOO LONG:

Split into exactly two parts at a clean top-level YAML boundary.

PART 1 must include everything from:

schema_version

through and including the complete:

dependency_table_reference

block.

End PART 1 immediately after the complete dependency_table_reference block.
Do not continue into derived_structure_discipline in PART 1.

PART 2 must begin with:

derived_structure_discipline

and continue through and including:

final_structural_formula

Do not repeat PART 1 in PART 2.
Preserve indentation so PART 1 and PART 2 can be concatenated into one valid YAML document.

If splitting, output PART 1 first and label the code block comment only inside YAML as:

-# PART 1 OF 2

At the beginning of PART 2, label the code block comment only inside YAML as:

-# PART 2 OF 2

Do not add prose outside the YAML code blocks.

---

## Prompt 4 — Final Validation against PMS.yaml and Template

You have already read PMS.yaml completely.

Now validate the completed case YAML against PMS.yaml and the provided PMS Case Application Template.

Check strictly for:

* valid YAML
* complete template coverage
* no remaining placeholders
* correct claim typing
* no PMS Base revision
* no non-PMS operators
* all eleven PMS operators present where required
* correct operator order
* correct operator dependencies
* correct derived-structure formulas
* Dignity-in-Practice treated only as praxeological application constraint
* SELF_FIXPOINT treated as derived, not primitive
* drift patterns treated as conditional structural risks, not diagnoses
* possible non-capture preserved
* rival readings preserved
* falsifier conditions included
* operationalization requirements marked fulfilled only if evidence is supplied
* no metaphysical, empirical, diagnostic, legal/forensic, clinical, implementation, or PMS Base validation overclaim

Return:

1. PASS / FAIL / PASS_WITH_MINOR_NOTES
2. Exact issues found
3. Exact search/replace blocks for every necessary correction
4. A final one-sentence conformity judgment

---

## Prompt 5 — Brief Content Check

Continue in German. Check the structure against the template again; some parts seem textually a bit too short to me — or am I seeing that wrong, which may well be the case? Provide search/replace blocks where appropriate: preferably a few larger ones rather than many small ones; correctly indented; each SEARCH and each REPLACE in its own separate chat code block. Not too much should be “added on,” especially because the performance of the YAML, PMS, and case template should also be demonstrated. So keep your conscience clean.

---

## Prompt 6 — Read PMS-ADDON.yaml

```text
Read PMS-ADDON.yaml completely.

Treat PMS-ADDON.yaml as an overlay/application profile only.
PMS.yaml remains the only PMS Base reference.

Do not analyze yet.
Respond only:

Read completely.
```

## Prompt 7 — Generate ADDON Block (NOT for EDEN/SEX, see Prompt 12)

```text
Using PMS-ADDON.yaml as an overlay/application profile, apply ADDON to the completed PMS Core case YAML.

Do not redefine PMS operators.
Do not change PMS dependencies.
Do not rewrite the Core pass.
Treat QC-EXT reduced signatures as overlay shorthand only.

Produce only the additional ADDON overlay YAML block to append or integrate into the extended case YAML.
```

---

## Prompt 8 — Brief ADDON Content Check

Continue in German. Check the structure against the template again; some parts seem textually a bit too short to me — or am I seeing that wrong, which may well be the case? Provide search/replace blocks where appropriate: preferably a few larger ones rather than many small ones; correctly indented; each SEARCH and each REPLACE in its own separate chat code block. Not too much should be “added on,” especially because the performance of the YAML, PMS, and case template should also be demonstrated. So keep your conscience clean.

---

## Prompt 9 — MIP

Now create a further analysis with the MIP YAML — reflection mode off, full-depth analysis(!), output YAML in a chat code block, content in English — based on the case analyses with PMS.yaml & PMS-ADDON.yaml. Do not omit any field; be conscientious.

---

## Prompt 10 — MIP AHP

Now analyze the last output with this MIP add-on, again fully and in depth; be conscientious, omit no field, content in English, output YAML in a chat code block.

---

## Prompt 11 — MIP & AHP Check

Check again whether both outputs fully conform to the MIP / MIP_AHP schema. If not, create an exact to-do list. Fixes should be provided as exact search/replace blocks, correctly indented, with each SEARCH and each REPLACE in its own separate chat code block.

---

## Prompt 12 — EDEN / SEX

Using PMS-EDEN.yaml as an overlay/application profile, apply EDEN to the completed PMS Core case YAML.

Do not redefine PMS operators.
Do not change PMS dependencies.
Do not rewrite the Core pass.
Treat EDEN reduced signatures as overlay shorthand only.

Use the provided EDEN case add-on template as the required output schema.

Fill the EDEN overlay YAML completely, precisely, and case-specifically.

Do not omit any required section.
Do not omit nested fields.
Do not leave placeholders.
Do not shorten texts, answers, responses, fields, or points to be filled.
Do not replace detailed case-specific analysis with generic template language.
Do not add commentary before or after the YAML.

The EDEN overlay is large.
Therefore, always split the output into exactly two parts.

OUTPUT RULE:

Return PART 1 OF 2 first only.

PART 1 must begin with:

pms_eden_overlay_application:

and must continue through and include the complete:

reduced_signatures

block.

End PART 1 immediately after the complete reduced_signatures block.
Do not continue into drift_catalogue in PART 1.

Inside the YAML code block, label PART 1 only with a YAML comment:

# PART 1 OF 2

Do not add prose outside the YAML code block.

After PART 1, stop.

When the user says “continue” or “PART 2”, output PART 2 OF 2.

PART 2 must begin with the next top-level child block under pms_eden_overlay_application:

drift_catalogue:

and must continue through and include the final:

eden_overlay_synthesis

block.

PART 2 must preserve indentation so that PART 1 and PART 2 can be concatenated into one valid YAML document under:

pms_eden_overlay_application:

At the beginning of PART 2, label the code block with a YAML comment only:

# PART 2 OF 2

Do not repeat PART 1 in PART 2.
Do not repeat the top-level key pms_eden_overlay_application in PART 2.
Do not add prose outside the YAML code block.

SPLIT BOUNDARY:

PART 1:

* starts at:
  pms_eden_overlay_application:
* ends after the complete:
  reduced_signatures:
  block

PART 2:

* starts at:
  drift_catalogue:
* ends after the complete:
  eden_overlay_synthesis:
  block

Before outputting each part, internally check:

* YAML indentation is preserved.
* The split occurs only at the specified clean boundary.
* PART 1 does not enter drift_catalogue.
* PART 2 does not repeat pms_eden_overlay_application.
* All fields in the provided EDEN template are eventually filled across PART 1 and PART 2.
* PMS Base is not redefined.
* EDEN remains an overlay/application profile only.
* No PMS operators, dependencies, derived structures, or guardrails are changed.
* Paper-internal EDEN terms remain non-operators.
* Switch labels are not person labels.
* PFO is not treated as a group label or ideology claim.
* NRK is not treated as Action_E.
* Description/application firewall is preserved.
* Χ, reversibility, and Dignity-in-Practice are preserved.
* Alternative explanations, boundary conditions, and non-capture remain open.

Output PART 1 now.
