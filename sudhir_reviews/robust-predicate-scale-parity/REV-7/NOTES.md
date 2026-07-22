# REV-7 notes — robust-predicate-scale-parity

## Platform reject

TRIVIAL (opus 5/5, gpt5 5/5). Root cause: CM-008 (always-refine escape + greppable
B/C + named probes). AutoEval FAILED banner treated as CM-004 noise.

## Collapse WARN justification (0 FAIL / 5 WARN)

Same intentional discoverability posture as REV-5/REV-6:

- RC6 / GX6 — instruction states observable probe + conservatism contracts (CM-002),
  not file/symbol recipes.
- GX9 — 50% saturation from schema/probe contracts required for solvability.
- Other WARNs (oracle predictability / symbol-table) unchanged distributed
  four-locus frontier; no new FAIL.

## Hardening

- Series tests: cancel → `raw==2`; well-conditioned → exact `raw`.
- Bury B: `normalize_progress` collapses refine into +1.
- Bury C: warmup-reuse discards recomputed window while `armed`.
