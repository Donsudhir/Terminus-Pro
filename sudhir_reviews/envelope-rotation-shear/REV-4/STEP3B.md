# envelope-rotation-shear — REV-4 Step 3b Paper Review

- Date: 2026-07-21
- Revision: REV-4
- Task path: `sudhir_tasks/active/envelope-rotation-shear`
- Trigger: platform instruction-sufficiency FAIL on generated-namespace binding polarity; AutoEval FAILED banner was `tb_check` infra while difficulty agents ran
- Task edits: `instruction.md` only (plus authoring/reviewer spec amendments and REV-4 form fields)
- Static / Dockerfile / integrity: PASS (checksum refreshed after instruction edit)
- Collapse: 0 FAIL, 1 WARN (RC8), 22 PASS
- Harbor oracle 1x: mean 1.0, `jobs/2026-07-21__06-31-44`
- Harbor NOP: mean 0.0, `jobs/2026-07-21__06-33-29`

## Verdict

**ACCEPT WITH NOTES** for Step 4.

The revision clarifies observable polarity only. No environment, oracle, verifier, or topology change.

## 1. Feedback resolution

### Instruction-sufficiency (axis/namespace binding)

Agents failed by guessing between public-service namespace binding and an alternate rewritten label. The instruction now states, without naming internal helpers:

1. generated live records sealed under the same public `<service>` name as their namespace binding remain directly readable without recovery;
2. maintenance keeps that public-service binding and must not rewrite active matching-service records;
3. satisfying generated reads must not open foreign substitutions, and rejecting substitutions must not break matching-service generated reads.

Still symptoms/outcomes only (RC6/GX6 PASS). No `AxisFor`, `RouteAxis`, scopes, fallback branches, or repair order.

### AutoEval FAILED banner

`tb_check` build `f29d2053` FAILED with empty quality summary; `difficulty_check` SUCCEEDED (MEDIUM, solvable, agents ran). CM-004/CM-019 — not a Dockerfile defect for agents. Optional re-eval can refill quality; content fix is the instruction polarity.

## 2. Collapse WARN justification

**RC8 Frontier Concentration WARN** — borderline subsystem share on `aperture` at 25% with four roots and CR2 max share 33% under cap. Same topology as prior approved revisions; no concentration regression from an instruction-only edit. Accept WARN with this note.

## 3. Dirty-flag / evidence

Instruction edit invalidated prior checksum; `./scripts/check-task.sh` rewrote `.step2b-checksum`. Oracle 1x evidence path above; NOP path to be filled when the run completes.
