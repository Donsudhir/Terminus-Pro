### Decision
GO — Attempt 1. Distributed four-location sparse-sensitivity topology across C, Rust, and Fortran; symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- version: 2
- Task name: sparse-jacobian-color-contract
- Title: Sparse Jacobian Color Contract
- Category: scientific-computing
- Languages: [c, rust, fortran]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [sparse-derivatives, finite-differences, scientific-computing, ffi, metamorphic-testing]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The residual lab under `/app` rebuilds a compressed sensitivity report from bundled residual batches. Ordinary batches look healthy, but equivalent batches that only permute unknowns, resume from a saved probe plan, or match directional probes can disagree on reconstructed packed entries and matrix-vector products. Scale-changed but algebraically equivalent batches also leave support mismatches or disagreement between the emitted packed matrix and the audit summary.

Correct the scientific pipeline so `/app/output/sensitivity_report.json` is deterministic and consistent for every bundled batch and its equivalent variants. Rebuild and run it through `/app/bin/senslab`. The report must preserve batch identity, packed nonzero layout, directional products, support summary, scale summary, and a reproducibility digest. Input cardinality and unknown identities must remain unchanged. Equivalent variants must emit equivalent packed sensitivity structure, every retained entry must agree with independent directional probes within the documented residual linearization contract, and the summary must agree with the emitted structure. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are incompatible packed sensitivity across permutation-equivalent batches, resume-from-plan divergence, scale-equivalent drift, support mismatches, and audit-summary disagreement. Hardness comes from four interacting authorities — partition construction, probe-plan binding, magnitude scoping, and sparse unpack — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Environment shape

Major subsystems under `environment/`:

- `native/` — C pattern and probe-group construction, seed application helpers, compression helpers
- `host/` — Rust orchestration, plan shelf binding, magnitude gauge, report assembly, FFI
- `analysis/` — Fortran unpack/reindex and diagnostic tallies
- `kernels/` — Fortran residual evaluation used by probes
- `data/` — bundled residual families and declared variants
- `docs/` — architecture and report-format notes that stay cause-free
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`.

### Test plan

At least twelve opaque scored tests (`test_k01`–`test_k12`):

1. `test_k01` — permutation-equivalent batches agree on packed support and values (partition-sensitive)
2. `test_k02` — held-out column probes match retained packed entries (partition-sensitive)
3. `test_k03` — resume-from-saved-plan matches cold start (plan-binding-sensitive)
4. `test_k04` — scale-equivalent batch preserves directional products (magnitude-sensitive)
5. `test_k05` — sequential mixed-scale batches do not inherit prior magnitude (magnitude-sensitive)
6. `test_k06` — combined permutation+resume parity (partition+plan)
7. `test_k07` — packed layout agrees with audit support counts (plan+unpack)
8. `test_k08` — unpack orientation preserves independent dense probes on retained indices (unpack)
9. `test_k09` — summary fields agree with emitted packed structure (unpack)
10. `test_k10` — reordered execution of the same family is deterministic (partition+plan)
11. `test_k11` — scale summary matches the active batch, not a prior cache (magnitude)
12. `test_k12` — byte-identical report across clean rebuilds after scale+unpack path (magnitude+unpack)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak coloring, CPR, Jacobian, seed, CSR/CSC, epsilon, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only.

### Triviality Ledger

- **Reference CPR drop-in:** blocked because plan lifecycle, magnitude scoping, and Fortran unpack orientation remain broken even with a correct partitioner.
- **Widen finite-difference step globally:** blocked by scale-parity and mixed-scale tests that fail when magnitude is not batch-scoped, and by partition/unpack failures unaffected by step size.
- **Golden packed-matrix hardcoding:** blocked by regenerated variants and independent directional probes with no solver-visible expected report.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with four locations at 4/12 under the 0.34 concentration cap.
- **Decorative language diversity:** blocked because C owns partitioning, Rust owns plan and magnitude authorities, and Fortran owns unpack/reindex.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests generate new families.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks.
- **RC2 oracle locality:** require substantive edits at A–D; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for scientific reasons.
- **RC4 anti-cheat:** regenerate reports; never ship expected packed matrices on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required.
- **RC6 category fit:** primary work is numerical sparse-derivative consistency, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.34 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present.

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
- `environment/docs/report-format.md`
- `environment/docs/data-format.md`
- `environment/data/families.resid`
- `environment/native/lane.c`
- `environment/native/ledge.c`
- `environment/native/ember.c`
- `environment/native/quill.c`
- `environment/native/include/lane.h`
- `environment/native/include/common.h`
- `environment/host/main.rs`
- `environment/host/vault.rs`
- `environment/host/gauge.rs`
- `environment/host/locker.rs`
- `environment/host/meter.rs`
- `environment/host/ffi.rs`
- `environment/host/report.rs`
- `environment/host/error.rs`
- `environment/host/config.rs`
- `environment/analysis/knit.f90`
- `environment/analysis/tally.f90`
- `environment/kernels/ridge.f90`
- `environment/kernels/ridge.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_senslab.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: native/lane.c
  symbol: mix_cols
  kind: function
  signature: int mix_cols(const int32_t *a, const int32_t *b, int32_t n, int32_t *c);
  purpose: Builds a partition of unknowns into probe groups from a nonzero pattern.

- path: host/vault.rs
  symbol: bind_slot
  kind: function
  signature: pub(crate) fn bind_slot(a: i32, b: &mut Shelf) -> i8
  purpose: Binds a restored or fresh probe-group slot into the host shelf without leaking prior bits.

- path: host/gauge.rs
  symbol: reset_span
  kind: function
  signature: pub(crate) fn reset_span(a: &mut Gauge, b: &[f64])
  purpose: Rebuilds per-run magnitude context used to choose finite-difference step sizes.

- path: analysis/knit.f90
  symbol: merge_slots
  kind: function
  signature: integer(c_int) function merge_slots(a, b, c) bind(C)
  purpose: Unpacks compressed probe results into a stable sparse representation and updates support totals.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: native/lane.c
    controls_tests: [test_k01, test_k02, test_k06, test_k10]
  - id: B
    path: host/vault.rs
    controls_tests: [test_k03, test_k06, test_k07, test_k10]
  - id: C
    path: host/gauge.rs
    controls_tests: [test_k04, test_k05, test_k11, test_k12]
  - id: D
    path: analysis/knit.f90
    controls_tests: [test_k07, test_k08, test_k09, test_k12]
no_single_location_flips_majority: true
concentration_cap: 0.34
```

#### decoy_manifest

```
- path: native/ledge.c
  kind: helper
  rhymes_with: mix_cols
  non_fix_purpose: Computes ordinary pattern statistics for diagnostic summaries.

- path: host/locker.rs
  kind: helper
  rhymes_with: bind_slot
  non_fix_purpose: Maps display codes for status banners without affecting probe plans.

- path: host/meter.rs
  kind: helper
  rhymes_with: reset_span
  non_fix_purpose: Clears reusable output slots after completed runs.

- path: analysis/tally.f90
  kind: helper
  rhymes_with: merge_slots
  non_fix_purpose: Folds scalar diagnostic marks into aggregate counters.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [residual, lab, app, sensitivity, report, batch, unknown, probe, plan, entry, matrix-vector, product, scale, support, mismatch, disagreement, matrix, audit, summary, pipeline, output, bin, senslab, variant, identity, nonzero, layout, directional, cardinality, structure, linearization, contract, reproducibility, digest, input, check, packed, json]
```
