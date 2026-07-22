# REV-2 notes — sparse-jacobian-color-contract

## Reviewer ask (CM-006)

Clarify public contracts; strengthen malformed/ids/span_info tests; replace
off-domain rubric. Difficulty already HARD/solvable — do not over-harden.

## Changes

- `instruction.md`: per-batch gauge isolation, lex run order, ledger.active /
  dims.nnz, scale summary ref/step meanings (avoid token `span_info` for CR1).
- `environment/docs/report-format.md`: exact `span_info.ref` / `span_info.step`.
- `tests/test_outputs.py`: absolute span expectations, ids `1..cols`, ordering
  assert, `test_k13` malformed fail-closed.
- Rubric: domain output-based (no SQLite/repo process lines).

## Collapse WARN

GX7 path-literal WARN from ephemeral malformed fixture paths under `/tmp` in
`test_k13` — not solver-facing answer leakage. PASS-with-justification.

## Package

Zip: `sudhir_tasks_ready_to_submit/sparse-jacobian-color-contract.zip`
SHA-256: `1fb0d85bf896f02c08042a6c7c33a9006b46c1f206a8e13426ba6de84cf47e41`
