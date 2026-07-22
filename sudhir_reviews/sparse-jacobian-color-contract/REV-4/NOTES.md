# REV-4 notes — sparse-jacobian-color-contract

## Platform reject (post REV-3)
EASY again (opus 100%, gpt5 80%). Instruction sufficiency PASS. Only k04 soft
(9/10). Agents rewrite host to copy declared term coefficients.

## Changes
- `kernels/ridge.f90`: equation-row participation weight `1+0.5*(i-1)` so operator
  Jacobian ≠ bare term table (poisons copy-coeff shortcuts; FD path recovers it;
  row weights keep column-permutation metamorphic tests valid)
- Instruction: operator first-order sensitivities / not bare term table
- Tests: `_expected_jacobian` applies the same weight; k04 adds narrow tag +
  packed-value asserts
- `engine.rs`: rename shared_gauge → span_scratch
- `vault.rs`: carry-only contamination (no scream `1<<gid`)
- gauge/knit/lane loci retained (oracle still fixes A–D)

## Collapse WARN
GX7 ephemeral malformed path literals in test_k13 — PASS-with-justification
(same class as REV-3).
