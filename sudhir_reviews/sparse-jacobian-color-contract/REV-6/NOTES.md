# REV-6 notes — sparse-jacobian-color-contract

## Platform reject (post REV-5)
EASY (opus 80%, gpt5 80%). Instruction sufficiency FAIL on probe directions.
Last-mile: invented probe vector; unsolicited `floor_pow2` on step.

## Changes
- `instruction.md` + `docs/report-format.md`: disclose bundled companion
  directions (4-col / 5-col / general) and exact step formula
  `max(max(ref*1e-6, floor)*gain, floor)` with no invented quantization
- Move companion table into `quill_companion` (C); host calls FFI only
- Deepen `quill_tint` diagonal participation (`1 + 0.5 i + 0.05 i²`) so
  linear `1+0.5i` host copies fail absolute packed-value checks
- `lane.c`: founder-only equation conflict kept; decoy full-member tag scan
- Tests: dim-5 products on k02/k08; third sequential span family on k05;
  shared `_companion_direction` helper

## Collapse WARN
- GX1: residual vocab-anywhere noise (no BUG/FIXME in oracle subsystem)
- GX7: ephemeral malformed path literals in test_k13 — PASS-with-justification
  (same class as prior REVs)
