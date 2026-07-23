### Decision
GO — Attempt 1. Distributed three-location rank-map twin-parity topology across C and Rust (`native/`, `host/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- version: 2
- Task name: domain-halo-digest-rift
- Title: Domain Halo Digest Rift
- Category: scientific-computing
- Languages: [rust, c]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [domain-decomposition, field-digests, scientific-computing, ffi, twin-parity]
- Milestones: 0
- Canonical final Docker image: `public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe9e7d8e37ceb96ed907265a3a0df7f44e3737d0b100e7907a679acb36`

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The partitioned field lab under `/app` advances a bundled case that applies a rank map change mid-run, then continues. After the map change, local norms look ordinary and exchange status looks complete, but global fold checksums disagree with a steady twin that never changed maps on the same case. Pointwise samples can also disagree with that twin while still looking numerically ordinary. Fresh steady runs without a map change remain correct and must stay byte-stable across clean rebuilds.

Correct the pipeline so map-changed and steady trajectories agree on fold checksums and sample contracts, and so the healthy steady control stays byte-identical. Rebuild and invoke `/app/bin/partlab`. Emit `/app/output/parity_report.json` whose keys and layout follow the normative schema documented in `/app/docs/parity-report-schema.md`. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are local-norm-green / global-fold-red disagreement after a rank map change, twin divergence on fold checksums and pointwise samples, and a nearby healthy steady control that never changes maps and remains correct. Hardness comes from three interacting authorities — native fringe packing across the language boundary, shared-boundary stage metadata in the orchestrator, and fold/reduce ordering for global checksums — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

Distinct from mesh-checkpoint-operator-skew (remesh+resume with C++/Rust/Fortran shelf reuse), amg-coarsen-parity-rift (AMG coarsening parity), and sparse-jacobian-color-contract (coloring contracts).

### Investigation architecture

Use four reinforcing weakness areas: long-horizon debugging, multi-component reasoning, partial failures, and ambiguous bug reports. The intended six-stage progression is: characterize twin disagreement beside the healthy steady control; correlate logs/metrics with the rank-map boundary; recover the native fringe-pack fact; recover the host stage-authority fact; recover the fold-order fact; then coordinate all three repairs and verify end-to-end twin/control outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem case/map state. The deterministic offline investigation is estimated at 52 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `native/` — C numerical kernels, fringe pack/unpack, fold helpers (selected + decoy)
- `host/` — Rust partition orchestration, stage metadata, report assembly, FFI
- `data/` / `fixtures/` — bundled cases, rank-map samples, and cause-free run traces
- `docs/` — architecture notes plus normative `parity-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

No Python in the solvable core (ADR-0014). Verifier-only pytest is allowed outside `environment/`.

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/parity-report-schema.md` and must be cited from instruction.md (WW-010). Final image must pin the canonical Rust 1.85 slim digest above.

### Test plan

At least twelve opaque scored tests (`test_m01`–`test_m12`):

1. `test_m01` — after rank map change, global fold checksum matches steady twin on bundled case (pack-sensitive)
2. `test_m02` — pointwise samples agree with twin after map change (pack-sensitive)
3. `test_m03` — sample contracts stay consistent with twin when host stage metadata is exercised (authority-sensitive)
4. `test_m04` — emitted fold fields in parity_report agree with independent fold of active ordering (fold-sensitive)
5. `test_m05` — sequential map-change families do not inherit prior stage identity (authority-sensitive)
6. `test_m06` — combined twin parity under map change with pack+authority interaction (pack+authority)
7. `test_m07` — local-norm plausibility does not mask fold disagreement after repair (authority-sensitive)
8. `test_m08` — fold uses post-map ordering on map-changed trajectories (fold-sensitive)
9. `test_m09` — report summary fields agree with emitted fold checksums (fold-sensitive)
10. `test_m10` — reordered execution of the same family is deterministic for twin parity (pack+authority)
11. `test_m11` — healthy steady control remains byte-identical across clean rebuilds (authority/control)
12. `test_m12` — clean rebuild byte identity of parity_report after fold path on twin+control matrix (fold+control)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated twins and controls, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak fringe packing, shared-face ownership, sync-stage lag, reduction ordering, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/parity-report-schema.md` from instruction.md for every graded JSON key. Do not place Python in `environment/` solvable core.

### Triviality Ledger

- **Global exchange flush / force full sync:** blocked because fringe packing and fold order remain broken even when stage flags are forced complete, and steady controls already pass without that flush.
- **Rewrite map bytes / golden checksums:** blocked by regenerated twin/control matrices and independent fold checks with no solver-visible expected checksums.
- **Fix only local norms:** blocked by twin fold-checksum and pointwise sample tests that stay red when norms look ordinary.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Decorative language diversity:** blocked because C owns fringe pack and fold kernels while Rust owns stage authority; both must coordinate across FFI.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate map-changed/steady pairs.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially ownership/synced/ghost/halo phrasing in fix symbols).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for scientific reasons while steady controls already look healthy.
- **RC4 anti-cheat:** regenerate reports and twins; never ship expected checksums on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required; pin reduction order.
- **RC6 category fit:** primary work is numerical rank-map twin parity, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned Rust 1.85 slim base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/parity-report-schema.md` for graded keys.
- **ADR-0014:** no Python-primary solvable core under `environment/`.

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
- `environment/fixtures/maps/delta.bin`
- `environment/native/ledge.c`
- `environment/native/brim.c`
- `environment/native/ember.c`
- `environment/native/include/ledge.h`
- `environment/native/include/common.h`
- `environment/host/main.rs`
- `environment/host/shelf.rs`
- `environment/host/locker.rs`
- `environment/host/relay.rs`
- `environment/host/ffi.rs`
- `environment/host/report.rs`
- `environment/host/error.rs`
- `environment/host/config.rs`
- `environment/tools/build_all.sh`
- `environment/tools/run_partlab.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: native/ledge.c
  symbol: braid_q
  kind: function
  signature: int32_t braid_q(const int32_t* a, int32_t b, uint64_t* c);
  purpose: Packs and unpacks fringe boundary values after a rank-map change across the native kernel boundary.

- path: host/shelf.rs
  symbol: latch_r
  kind: function
  signature: pub(crate) fn latch_r(a: u64, b: &mut Shelf) -> i8
  purpose: Rebinds shared-boundary authority and stage metadata so host completion aligns with native buffer readiness.

- path: native/ember.c
  symbol: sift_s
  kind: function
  signature: int32_t sift_s(const uint64_t* a, int32_t b, uint64_t* c);
  purpose: Folds field samples into a stable global checksum under the active post-map ordering.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: native/ledge.c
    controls_tests: [test_m01, test_m02, test_m06, test_m10]
  - id: B
    path: host/shelf.rs
    controls_tests: [test_m03, test_m05, test_m07, test_m11]
  - id: C
    path: native/ember.c
    controls_tests: [test_m04, test_m08, test_m09, test_m12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: native/brim.c
  kind: helper
  rhymes_with: braid_q
  non_fix_purpose: Computes ordinary local norm banners for diagnostic lines.

- path: host/locker.rs
  kind: helper
  rhymes_with: latch_r
  non_fix_purpose: Maps display codes for status lines without affecting stage rebinds.

- path: host/relay.rs
  kind: helper
  rhymes_with: sift_s
  non_fix_purpose: Forwards opaque FFI handles between host modules without altering fold order.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [partitioned, field, lab, app, case, rank, map, change, mid-run, local, norms, ordinary, exchange, status, looks, complete, global, fold, checksums, disagree, steady, twin, never, changed, maps, pointwise, samples, numerically, fresh, runs, without, correct, byte-stable, clean, rebuilds, pipeline, map-changed, trajectories, agree, contracts, healthy, control, bin, partlab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, inputs, report, checks, regenerate, compiled, bundled]
```
