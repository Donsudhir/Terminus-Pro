# REV-8 notes — sparse-jacobian-color-contract

## Why
Platform Needs Revision after agent-run analysis flagged instruction
sufficiency on the digest boundary, plus reviewer asks for hash-locked
verifier deps and config coverage.

## Reviewer asks (stb `d9082cd8…`)
1. Document the exact FNV-1a digest algorithm **or** relax the verifier to
   the documented contract.
2. Replace verifier requirements with a complete pinned **hash-locked** set.
3. Add tests for `schema_version` plus changed `runtime.conf` step settings.

## Changes (minimal; no core pipeline rewrite)
- `environment/docs/report-format.md` — exact FNV-1a-64 contract; hashed
  payload is the **complete** compact object without `digest` (**includes**
  closing `}`); offset/prime/`%016x` spelled out.
- `instruction.md` — points at report-format for schema + FNV-1a; states
  closing-`}` inclusion; notes `runtime.conf` step knobs must move emitted
  `step`; softens mode-echo / ids wording to avoid GX9 answer-key saturation.
- `tests/test_outputs.py` — `_assert_digest` documents the closed-object
  contract (logic unchanged); new `test_k14` for `schema_version` (derived
  from report-format) + `step_gain` / `step_floor` overrides.
- `environment/verifier-requirements.txt` — full transitive pins with
  `--hash=sha256:…`; Dockerfile `pip install --require-hashes`.
- `output_contract.toml` — `schema_version` / `report-format` instruction checks.

## Not changed
- Host digest renderer (`report.rs`) still hashes `prefix + "}"`.
- Oracle / native / gauge / coloring / unpack loci untouched.
- Existing test_k01–k13 contracts unchanged.

## Evidence
- Cheap gates: static PASS, dockerfile PASS, collapse WARN (RC6/GX1/GX7 —
  FNV name required by reviewer; same class as prior REVs).
- Harbor oracle 1x mean **1.0** — `jobs/2026-07-23__00-46-04`
- Harbor NOP mean **0.0** — `jobs/2026-07-23__00-46-35`

## Next
Step 4 oracle 10x → DSV/rubric form-capture → package → re-upload.
