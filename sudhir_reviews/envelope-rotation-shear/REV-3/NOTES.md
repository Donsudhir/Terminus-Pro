# REV-3 notes — envelope-rotation-shear

Opened: 2026-07-19T18:12:46Z

Reason: Platform difficulty MEDIUM because task metadata included Python despite a Go-only agent-facing core; agent analysis also found an instruction-sufficiency gap around preserving namespace-consistent generated reads while rejecting substitutions.

## Fixes applied

1. `task.toml` now declares only Go as the agent-facing language. Python remains verifier-only and must not be selected as the platform language.
2. `instruction.md` now explicitly pairs direct reads of valid live records in newly introduced service namespaces with strict rejection of intact cross-namespace substitutions, both without recovery.
3. The authoring spec and reviewer appendix contain a REV-3 amendment. The verifier remains behavior-based and does not require one internal fallback algorithm.
4. REV-3 form fields now include the positive generated-read contract and use the required `Agent …, ±N` rubric shape.

## Current evidence

- Spec lint: PASS.
- Static and Dockerfile gates: PASS.
- Collapse: 0 FAIL, 2 justified WARN, 21 PASS.
- Integrity: PASS after canonical preflight refreshed the checksum.
- Oracle 1x: `2026-07-19__23-51-22`, mean 1.0.
- NOP: `2026-07-19__23-52-55`, mean 0.0.
- Paper review: `STEP3B.md`, ACCEPT WITH NOTES.

## Next

Step 4 is complete. Oracle stress `2026-07-19__23-56-00` passed 10/10 with zero exceptions; post-stress NOP `2026-07-19__23-58-50` scored 0.0. The approval gate passed with the two paper-justified collapse WARNs and no blockers.

Re-upload `sudhir_tasks_ready_to_submit/envelope-rotation-shear.zip` (SHA-256 `670cac18709eecf34f899ce83125694e6fb93701940ec77453a40b5c65c50e4e`), paste REV-3 form fields, and select **Go** as the platform language.
