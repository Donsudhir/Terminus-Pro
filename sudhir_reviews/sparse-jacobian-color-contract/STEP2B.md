# STEP2B — sparse-jacobian-color-contract

Date: 2026-07-19  
Task: TASK-SJCC-001  
Path: `sudhir_tasks/active/sparse-jacobian-color-contract/`

## Created

Full Step 2b tree per authoring spec and ADR-0009:

- Metadata: `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`
- Environment (≥20 substantive files): C native partition helpers, Rust host (split entry points), Fortran unpack/residual kernels, bundled data, docs, conf, digest-pinned offline Dockerfile with `.dockerignore`
- Verifier: `tests/test.sh`, `tests/test_outputs.py` with opaque `test_k01`–`test_k12`
- Oracle: `solution/solve.sh` — additive heredocs for A–C, surgical Python line swap for D (`knit.f90`)

## Seeded defects (present in baseline)

| ID | Location | Bug |
|----|----------|-----|
| A | `native/lane.c::mix_cols` | structural-symmetry shortcut groups columns without equation-row orthogonality |
| B | `host/vault.rs::bind_slot` | ORs roster leakage into staged seed bits on rebind/resume |
| C | `host/gauge.rs::reset_span` | early return when `primed` caches magnitude/step across later batches |
| D | `analysis/knit.f90::merge_slots` | reads compressed `(row,col)` with swapped orientation |

Decoys (`ledge.c`, `locker.rs`, `meter.rs`, `tally.f90`) perform real non-fix work.

## Collapse remediation (this session)

Cleared prior RC1/RC6/CR1/CR8/GX1/GX2 failures:

1. **RC1** — oracle expands A–C bodies (net +85 LOC); D is a two-line surgical swap.
2. **RC6** — symptoms-only instruction (no schema clusters, ALL_CAPS reason tokens, or inspect CLI flags).
3. **CR1** — oracle-touched symbols limited to manifest A–D; helpers moved out of fix-path files (`roster.rs`, `partition.rs`, `unpack.rs`, inlined lane helpers).
4. **CR8** — no file references >2 fix-path symbols (engine/ffi max 2).
5. **GX1** — no correctional-vocab comments near frontiers; oracle does not delete explanatory comments.
6. **GX2** — `knit.f90` fixed via targeted Python replace, not whole-file rewrite.

## Verified (fresh Docker evidence, 2026-07-19)

Rebuild image without bind-mounting `environment/` (avoids `solve.sh` mutating host baseline):

```text
docker build -t sjcc-test sudhir_tasks/active/sparse-jacobian-color-contract/environment/
```

### NOP / baseline (no solve.sh)

```text
docker run --rm -v $TASK/tests:/tests sjcc-test bash -lc \
  '/app/tools/build_all.sh >/dev/null 2>&1; python -m pytest /tests/test_outputs.py -q --tb=line'

FFFFFFFF.FF.                                                             [100%]
10 failed, 2 passed in 1.51s
FAILED test_k01, test_k02, test_k03, test_k04, test_k05,
       test_k06, test_k07, test_k08, test_k10, test_k11
PASSED test_k09, test_k12
```

### Oracle (`solution/solve.sh` then pytest; solution mounted read-only)

```text
docker run --rm -v $TASK/tests:/tests -v $TASK/solution:/solution:ro sjcc-test bash -lc \
  '/app/tools/build_all.sh >/dev/null 2>&1; bash /solution/solve.sh >/dev/null 2>&1; \
   python -m pytest /tests/test_outputs.py -q --tb=line'

............                                                             [100%]
12 passed in 1.06s
```

## Preflight / checksum

```text
./scripts/check-task.sh sudhir_tasks/active/sparse-jacobian-color-contract
# Preflight passed (Phase A + B + C).
# wrote .step2b-checksum (45 files)
```

## Gates (`sudhir_task.py gates sparse-jacobian-color-contract`)

Fresh command evidence after collapse remediation + `asciinema --version` Dockerfile hygiene:

```text
Gate summary for 'sparse-jacobian-color-contract':
  static=PASS, dockerfile=PASS, collapse=PASS, integrity=PASS
```

Collapse detail: `0 FAIL, 0 WARN, 23 PASS` — VERDICT PASS.

## Remaining gaps

1. Step 3b paper review / Step 4 (oracle 10×) / packaging not started.
2. Do **not** bind-mount `environment/` when running `solve.sh` in Docker, or the host baseline will be overwritten.

## Notes

- Binary: `/app/bin/senslab` → `/app/output/sensitivity_report.json`
- Patterns from `robust-predicate-scale-parity` (Dockerfile pins, task.toml v2, test harness); geometry/predicate logic not reused.
