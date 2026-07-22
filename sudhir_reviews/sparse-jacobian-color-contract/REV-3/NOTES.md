# REV-3 notes — sparse-jacobian-color-contract

## Platform reject

EASY (opus 100%, gpt5 80%) after REV-2 made gauge sticky greppable. Instruction
sufficiency also wanted packed==structural-coefficient wording.

## Changes

- Instruction: structural residual linearization coefficient contract (no CR1 tokens)
- `gauge.rs`: compute-then-discard when primed (de-stick early return)
- `lane.c`: degree-ordered partitioner with incomplete group conflict check
- `knit.f90`: unknown-major emit (host expects row/col); oracle writes correct file
- `test_k02`: denser CLUSTER_TERMS family
- report-format: qualitative span semantics + structural values wording

## Collapse WARN

GX7 ephemeral malformed path literals in test_k13 — PASS-with-justification.
