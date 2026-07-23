# EDIT_LEDGER — sparse-jacobian-color-contract

## Revision 1 (2026-07-19) — Step 3b honest-instruction repair

- `instruction.md` — document SENSLAB_INPUT/OUTPUT and `--mode-echo`; avoid `span_info` / backtick schema dumps
- `environment/host/router.rs` — rename `--resume-check` → `--mode-echo`
- `tests/test_outputs.py` — call `--mode-echo`
- `environment/host/vault.rs` — rename local `leaked` → `carry`
- Regenerated `.step2b-checksum`; cheap gates re-PASS

PLACEHOLDER10:21:11Z — Revision 2

- CM-006: clarify contracts, strengthen tests, replace rubric
  - `instruction.md`: gauge isolation, lex run order, ledger.active/dims.nnz,
    scale-summary ref/step (no `span_info` token — CR1)
  - `environment/docs/report-format.md`: exact `span_info.ref` / `.step`
  - `tests/test_outputs.py`: absolute span checks, ids `1..cols`, ordered labels,
    `test_k13` malformed fail-closed
  - REV-2 form rubric: domain output-based (no SQLite/repo criteria)

## 2026-07-19T11:46:56Z — Revision 3

- EASY: de-stick C, harden A/D, structural-coeff contract

## 2026-07-19T11:46:50Z — Revision 3

- EASY → MEDIUM hardening (CM-008 after REV-2):
  - instruction: packed values = structural residual linearization coefficients
  - gauge.rs: compute-then-discard when primed (no scream early-return-only shape)
  - lane.c: degree-ordered incomplete group conflict check
  - knit.f90: unknown-major emit; oracle writes correct (row,col) merge_slots
  - test_k02: denser CLUSTER_TERMS family

## 2026-07-19T12:52:19Z — Revision 4

- REV-3 still EASY (opus 100% gpt5 80%); agents shortcut exact term coeffs; only k04 soft
- ridge.f90: equation-row weight so operator J ≠ bare term table (FD recovers)
- instruction: operator first-order sensitivities / not bare term table
- tests: weighted `_expected_jacobian`; k04 narrow tag + packed-value asserts
- engine: `span_scratch` rename; vault: carry-only seed contamination

## 2026-07-19T15:06:19Z — Revision 5

- REV-4 still EASY (opus 100% gpt5 80%); agents clear structural bugs; only soft k05/k11 gauge-norm near-miss
## REV-5 detail

- Still EASY after REV-4: almost all tests 10/10; soft k05/k11 gauge-norm
- quill_tint: move row participation out of ridge (poison ridge-only copy)
- gauge: ∞-norm + primed sticky compound bug
- instruction: Euclidean magnitude + ledger.groups conflict contract
- tests: exact chromatic group counts on bundled families


## 2026-07-19T17:46:39Z — Revision 6

- REV-5 EASY 80/80 + probe-direction underspec; harden for MEDIUM and name bundled directions
- instruction + report-format: disclose companion vectors + exact step formula
- quill_companion (C) owns bundled directions; host FFI only
- quill_tint deepen to `1 + 0.5i + 0.05i²` (anti linear-tint host copy)
- lane.c decoy tag-member scan; founder-only equation conflict retained
- tests: dim-5 products k02/k08; three-family sequential span k05
- Harbor: oracle 1x / NOP / oracle 10x clean; zip `dcc1c8f4…`

## 2026-07-21T01:28:26Z — Revision 7

- CM-019: difficulty/tb_check CodeExecution FAILED + BatchGetBuilds ThrottlingException; hedge build_timeout and re-package for remeasure
- Not the review-report “non-canonical” rust base — `rust:1.85-slim@sha256:9f841bbe…` is sanctioned
- `task.toml`: build/verifier timeout 1200s, memory 8192MB (agent stays at platform cap 1800)
- `tests/test.sh`: CM-016 early `reward.txt=0`
- Harbor: oracle 1x / NOP / oracle 10x clean; zip sha256 `50ba0424…`

## 2026-07-23T00:48:00Z — Revision 8

- Reviewer: document FNV-1a digest (closing `}`), hash-lock verifier deps,
  test `schema_version` + `runtime.conf` step overrides
- Spec: report-format FNV-1a-64 contract explicit; instruction cites it;
  digest renderer/tests keep closed-object hashing (no relax / no rewrite)
- Verifier: transitive `--hash=sha256` requirements + `pip --require-hashes`
- Tests: `test_k14` schema_version + step_gain/step_floor overrides
- Harbor: oracle 1x mean 1.0 (`jobs/2026-07-23__00-46-04`); NOP 0.0
  (`jobs/2026-07-23__00-46-35`); oracle 10x mean 1.0 10/10
  (`jobs/2026-07-23__00-56-36`)
- Package: `sudhir_tasks_ready_to_submit/sparse-jacobian-color-contract.zip`
  sha256 `4343b5da35ba3096f35b50f043c2fabe1c7ef4d47af202d30c035b4bedf9efb2`

## 2026-07-22T19:03:39Z — Revision 8

- Platform: document FNV-1a digest; hash-lock verifier deps; test schema_version + runtime.conf step overrides

## 2026-07-22T22:11:18Z — Revision 9

- CM-019 AutoEval CodeExecution FAILED again (tb_check + difficulty_check empty logs); no human content feedback
