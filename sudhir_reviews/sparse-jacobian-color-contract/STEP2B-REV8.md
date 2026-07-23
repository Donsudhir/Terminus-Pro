# STEP2B — sparse-jacobian-color-contract REV-8

## Preflight
- `./scripts/check-task.sh` PASS (collapse WARN: RC6 FNV name required by
  reviewer; GX1/GX7 same class as prior REVs — justified, no content rewrite).
- Gates: static PASS, dockerfile PASS, collapse WARN, integrity PASS.

## Harbor
- Oracle 1x mean **1.0** — `jobs/2026-07-23__00-46-04` (includes new `test_k14`)
- NOP mean **0.0** — `jobs/2026-07-23__00-46-35`

## Reviewer mapping
| Ask | Response |
| --- | --- |
| Document FNV-1a or relax verifier | Documented exact FNV-1a-64 closed-object contract (includes `}`); verifier unchanged |
| Hash-locked verifier deps | Transitive pins + `--require-hashes` |
| schema_version + runtime.conf step tests | `test_k14` |

Step 2b complete for REV-8 content. Step 4 still needs oracle 10x before package.
