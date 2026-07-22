# REV-4 notes — envelope-rotation-shear

Opened: 2026-07-21

Reason: Platform instruction-sufficiency FAIL on generated-namespace read vs
substitution rejection (axis/namespace-binding ambiguity). Sidebar AutoEval
FAILED was `tb_check` infra with empty quality summary while difficulty agents
ran (MEDIUM 60%/60%).

## Fixes applied

1. `instruction.md` now states the public-service namespace-binding contract for
   generated live records, require maintain to keep that binding and skip
   rewriting active matching-service records, and pairs the polarities so
   agents do not open foreign substitutions or break matching-service reads.
2. Authoring + reviewer specs carry a REV-4 amendment (observable clarification
   only; no oracle/topology change).
3. Form fields refreshed for the clearer polarity.

## Current evidence

- Spec lint / static / Dockerfile / integrity: PASS.
- Collapse: 0 FAIL, 1 justified WARN (RC8), 22 PASS — `STEP3B.md`.
- Oracle 1x: `2026-07-21__06-31-44`, mean 1.0.
- NOP (post-stress): `2026-07-21__06-36-45`, mean 0.0.
- Oracle 10x: `2026-07-21__06-34-26`, 10/10 mean 1.0.
- Approval gate: PASS (collapse WARN paper-justified).
- Zip: `sudhir_tasks_ready_to_submit/envelope-rotation-shear.zip`
  SHA-256 `95066f6b07081538af232c7d2eb382606105ef6006142b0101b53b45a07dbec1`

## Next

Re-upload the zip, paste REV-4 form fields, select **Go**. Do not treat a
stale `tb_check` FAILED banner as “agents never ran” if difficulty populates.
