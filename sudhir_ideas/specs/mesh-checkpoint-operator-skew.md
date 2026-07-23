### Decision
GO — Attempt 1. Distributed three-location remesh+resume twin-parity topology across C++, Rust, and Fortran (`native/`, `host/`, `pack/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- version: 2
- Task name: mesh-checkpoint-operator-skew
- Title: Mesh Checkpoint Operator Skew
- Category: scientific-computing
- Languages: [c++, rust, fortran]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [checkpoint-restart, mesh, scientific-computing, ffi, twin-parity]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The scientific mesh lab under `/app` advances a bundled case that checkpoints mid-run, remeshes, then resumes. After resume, residual norms and iteration counts can look plausible, but solution-field digests disagree with a never-interrupted twin on the same case. Pointwise residual samples can also disagree with that twin while still looking numerically ordinary. Fresh runs without a checkpoint remain correct and must stay byte-stable across clean rebuilds.

Correct the pipeline so interrupted and uninterrupted trajectories agree on field digests and residual contracts, and so the healthy no-checkpoint control stays byte-identical. Rebuild and invoke `/app/bin/meshlab`. Emit `/app/output/parity_report.json` whose keys and layout follow the normative schema documented in `/app/docs/parity-report-schema.md`. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are residual-green / field-digest-red disagreement after remesh+resume, twin divergence on solution-field digests and pointwise residual samples, and a nearby healthy no-checkpoint control that remains correct. Hardness comes from three interacting authorities — native geometry lifecycle across the language boundary, host shelf/reuse after remesh, and pack-side fold/digest ordering — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Investigation architecture

Use four reinforcing weakness areas: long-horizon debugging, multi-component reasoning, partial failures, and ambiguous bug reports. The intended six-stage progression is: characterize twin disagreement beside the healthy no-checkpoint control; correlate logs/metrics with the remesh boundary; recover the geometry-token binding fact; recover the post-remesh reuse-keying fact; recover the pack-side fold-order fact; then coordinate all three repairs and verify end-to-end twin/control outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem shelf/case state. The deterministic offline investigation is estimated at 48 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `native/` — C++ geometry lifecycle and related helpers (selected + decoy)
- `host/` — Rust orchestration, mid-run shelf, reuse rebind, report assembly, FFI
- `pack/` — Fortran field fold/digest and diagnostic tallies
- `kernels/` — Fortran residual evaluation used by ordinary and twin runs
- `data/` / `fixtures/` — bundled cases, shelf samples, and cause-free run traces
- `docs/` — architecture notes plus normative `parity-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/parity-report-schema.md` and must be cited from instruction.md (WW-010).

### Test plan

At least twelve opaque scored tests (`test_m01`–`test_m12`):

1. `test_m01` — remesh+resume solution-field digest matches never-interrupted twin on bundled case (geometry-sensitive)
2. `test_m02` — pointwise residual samples agree with twin after remesh+resume (geometry-sensitive)
3. `test_m03` — interrupted trajectory residual contracts stay consistent with twin after shelf restore (shelf/reuse-sensitive)
4. `test_m04` — emitted digest fields in parity_report agree with independent fold of active ordering (fold-sensitive)
5. `test_m05` — sequential remesh+resume families do not inherit prior reuse identity (shelf/reuse-sensitive)
6. `test_m06` — combined twin parity under remesh+resume with geometry+reuse interaction (geometry+reuse)
7. `test_m07` — iteration/residual-norm plausibility does not mask digest disagreement after repair (reuse-sensitive)
8. `test_m08` — pack fold uses post-remesh ordering on interrupted trajectories (fold-sensitive)
9. `test_m09` — report summary fields agree with emitted digests (fold-sensitive)
10. `test_m10` — reordered execution of the same family is deterministic for twin parity (geometry+reuse)
11. `test_m11` — healthy no-checkpoint control remains byte-identical across clean rebuilds (reuse/control)
12. `test_m12` — clean rebuild byte identity of parity_report after fold path on twin+control matrix (fold+control)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated twins and controls, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak operator cache, stale assembly, invalidate, geometry-token, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/parity-report-schema.md` from instruction.md for every graded JSON key.

### Triviality Ledger

- **Global cache flush / preconditioner clear:** blocked because geometry-token binding and pack-side fold order remain broken even when reuse is forced cold, and no-checkpoint controls already pass without that flush.
- **Rewrite checkpoint bytes / golden digests:** blocked by regenerated twin/control matrices and independent fold checks with no solver-visible expected digests.
- **Fix only residual norms:** blocked by twin field-digest and pointwise sample tests that stay red when norms look plausible.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Decorative language diversity:** blocked because C++ owns geometry lifecycle, Rust owns shelf/reuse, and Fortran owns fold/digest.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate interrupted/uninterrupted pairs.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially operator/cache/invalidate phrasing).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for scientific reasons while no-checkpoint controls already look healthy.
- **RC4 anti-cheat:** regenerate reports and twins; never ship expected digests on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required; pin reduction order.
- **RC6 category fit:** primary work is numerical remesh+resume parity, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/parity-report-schema.md` for graded keys.

### Initial Draft Commitments

- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Makefile`
- `environment/verifier-requirements.txt`
- `environment/conf/runtime.conf`
- `environment/docs/architecture.md`
- `environment/docs/parity-report-schema.md`
- `environment/docs/data-format.md`
- `environment/data/families.case`
- `environment/fixtures/logs/run_trace.ndjson`
- `environment/fixtures/cases/alpha.bin`
- `environment/native/span.cpp`
- `environment/native/ledge.cpp`
- `environment/native/ember.cpp`
- `environment/native/include/span.h`
- `environment/native/include/common.h`
- `environment/host/main.rs`
- `environment/host/shelf.rs`
- `environment/host/locker.rs`
- `environment/host/relay.rs`
- `environment/host/ffi.rs`
- `environment/host/report.rs`
- `environment/host/error.rs`
- `environment/host/config.rs`
- `environment/pack/fold.f90`
- `environment/pack/tally.f90`
- `environment/kernels/ridge.f90`
- `environment/kernels/ridge.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_meshlab.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: native/span.cpp
  symbol: braid_q
  kind: function
  signature: int32_t braid_q(const int32_t* a, int32_t b, uint64_t* c);
  purpose: Records and restores a geometry generation token across the native lifecycle boundary.

- path: host/shelf.rs
  symbol: latch_r
  kind: function
  signature: pub(crate) fn latch_r(a: u64, b: &mut Shelf) -> i8
  purpose: Rebinds host reuse context from shelf state after a remesh-capable restore.

- path: pack/fold.f90
  symbol: sift_s
  kind: function
  signature: integer(c_int) function sift_s(a, b, c) bind(C)
  purpose: Folds solution samples into a stable digest under the active ordering.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: native/span.cpp
    controls_tests: [test_m01, test_m02, test_m06, test_m10]
  - id: B
    path: host/shelf.rs
    controls_tests: [test_m03, test_m05, test_m07, test_m11]
  - id: C
    path: pack/fold.f90
    controls_tests: [test_m04, test_m08, test_m09, test_m12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: native/ledge.cpp
  kind: helper
  rhymes_with: braid_q
  non_fix_purpose: Computes ordinary geometry statistics for diagnostic banners.

- path: host/locker.rs
  kind: helper
  rhymes_with: latch_r
  non_fix_purpose: Maps display codes for status lines without affecting shelf rebinds.

- path: pack/tally.f90
  kind: helper
  rhymes_with: sift_s
  non_fix_purpose: Folds scalar diagnostic marks into aggregate counters.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [scientific, mesh, lab, app, case, checkpoints, mid-run, remeshes, resumes, resume, residual, norms, iteration, counts, solution-field, digests, twin, pointwise, samples, runs, checkpoint, rebuilds, pipeline, interrupted, uninterrupted, trajectories, agreement, field, contracts, healthy, no-checkpoint, control, bin, meshlab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, inputs, report, checks, compiled, bundled]
```
