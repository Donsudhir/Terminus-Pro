### Decision
GO — Attempt 1. Distributed three-location AMG hierarchy dual-reordering parity topology across Fortran, C++, and Rust (`lattice/`, `bridge/`, `orbit/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- version: 2
- Task name: amg-coarsen-parity-rift
- Title: AMG Coarsen Parity Rift
- Category: scientific-computing
- Languages: [fortran, c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [amg, multigrid, sparse-matrix, reordering, iterative-solvers]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do NOT include reviewer-only analysis, oracle steps, exact patch sites beyond the construction manifest, or an exhaustive hidden bug narrative here.

### Public contract

The algebraic multigrid lab under `/app` solves a sparse linear system with a hierarchy preconditioner. When the same matrix is presented under two equivalent reorderings, convergence curves and fine-grid solution digests diverge past tolerance versus a fixed healthy ordering control, even though smoothness indicators and coarse-size summaries can look acceptable.

Repair the pipeline so both reorderings meet residual and solution-digest contracts and the healthy ordering control stays green. Rebuild and invoke `/app/bin/amglab`. Emit `/app/output/parity_report.json` whose keys and layout follow the normative schema documented in `/app/docs/parity-report-schema.md`. Do not hard-code one permutation, replace the bundled inputs, or write the report by hand; the checks regenerate it through the compiled pipeline.

### Failure topology

Symptom clusters are dual-reordering residual/digest divergence, smoothness and coarse-size bait that can look acceptable, and a nearby healthy ordering control that stays green. Hardness comes from three interacting authorities — Fortran strength/membership selection, C++ transfer-operator assembly, and Rust apply/V-cycle identity binding — none of which alone explains every failure mode. The instruction stays symptoms-only; causes and algorithms are not named.

### Investigation architecture

Use four reinforcing weakness areas: long-horizon debugging, multi-component reasoning, partial failures, and ambiguous bug reports. The intended six-stage progression is: characterize dual-reordering disagreement beside the healthy ordering control; correlate logs/metrics with hierarchy construction; recover the order-indexed selection fact; recover the transfer-inheritance fact; recover the apply identity-mixing fact; then coordinate all three repairs and verify end-to-end dual-ordering/control outcomes. Evidence spans code, runtime observations, logs, metrics, and filesystem hierarchy/case state. The deterministic offline investigation is estimated at 52 meaningful terminal actions; that estimate is authoring evidence, never a scored process requirement.

### Environment shape

Major subsystems under `environment/`:

- `lattice/` — Fortran strength/membership selection and related helpers (selected + decoy)
- `bridge/` — C++ transfer-operator assembly, FFI glue, and status helpers
- `orbit/` — Rust orchestration, apply/V-cycle binding, report assembly
- `kernels/` — Fortran smoother/residual evaluation used by ordinary and control runs
- `data/` / `fixtures/` — bundled cases, hierarchy scratch samples, and cause-free run traces
- `docs/` — architecture notes plus normative `parity-report-schema.md` (WW-010)
- `conf/` — runtime defaults that are not a one-knob fix surface
- build scripts and a digest-pinned offline Dockerfile with `.dockerignore`

### Required artifacts

Step 2b must create instruction.md, task.toml, output_contract.toml if required by harness, environment/ with ≥20 substantive files, tests/ (test.sh + opaque scored tests), solution/solve.sh, and construction-manifest-faithful selected locations plus decoys. No milestones. No UI. `allow_internet = false`. Normative report keys live in `/app/docs/parity-report-schema.md` and must be cited from instruction.md (WW-010).

### Test plan

At least twelve opaque scored tests (`test_m01`–`test_m12`):

1. `test_m01` — dual-reordering residual contract agrees on bundled case (selection-sensitive)
2. `test_m02` — dual-reordering fine-grid solution digests agree on bundled case (selection-sensitive)
3. `test_m03` — transfer-sensitive residual contract across equivalent reorderings
4. `test_m04` — emitted digest fields in parity_report agree with independent fold under active presentation (apply-sensitive)
5. `test_m05` — sequential reordering families do not inherit a prior presentation identity (transfer-sensitive)
6. `test_m06` — combined dual-ordering parity with selection+transfer interaction
7. `test_m07` — smoothness/coarse-size plausibility does not mask residual/digest disagreement after repair (transfer-sensitive)
8. `test_m08` — apply identity binding uses graph-stable identity on both reorderings (apply-sensitive)
9. `test_m09` — report summary fields agree with emitted digests (apply-sensitive)
10. `test_m10` — reordered execution of the same family is deterministic for dual-ordering parity (selection+transfer)
11. `test_m11` — healthy ordering control remains green across clean rebuilds (transfer/control)
12. `test_m12` — clean rebuild byte identity of parity_report after apply path on dual+control matrix (apply+control)

Multiple valid algorithmic approaches are allowed if outcomes hold. Tests are metamorphic/property-based against regenerated reorderings and controls, not golden-file clones of the oracle.

### Drafting guardrails

Do not leak strength-of-connection, prolongation, restriction, V-cycle, order-indexed selection, or fix-path names through instruction text, comments, helper names on the fix path, test names, or fixture labels. Keep decoys doing real non-fix work. Forbidden instruction nouns are banned from fix-path code symbols only. Cite `/app/docs/parity-report-schema.md` from instruction.md for every graded JSON key.

### Triviality Ledger

- **Hard-code one canonical permutation:** blocked because regenerated reordering families and healthy-control checks reject presentation-specific tables and require both reorderings to pass without locking one order.
- **Rewrite golden digests / report by hand:** blocked by regenerated dual-ordering/control matrices and independent digest folds with no solver-visible expected digests.
- **Trust smoothness / coarse-size bait:** blocked by residual and solution-digest tests that stay red when bait looks acceptable.
- **Prompt-noun grep:** blocked by opaque selected paths/symbols and the audited forbidden-token list.
- **One location flipping the score:** blocked by twelve tests with three locations at 4/12 under the 0.5 concentration cap.
- **Decorative language diversity:** blocked because Fortran owns selection, C++ owns transfers, and Rust owns apply binding.
- **Fixture or manifest repair:** blocked because the baseline builds and runs while hidden tests regenerate dual-ordering pairs.

### Per-gate Pitfall Inventory

- **RC1 instruction honesty:** keep symptoms-only; re-audit after any wording change for algorithm/threshold/cause leaks (especially strength/prolong/restrict/apply phrasing).
- **RC2 oracle locality:** require substantive edits at A–C; reject single-file rewrite or compiler-flag-only “fixes.”
- **RC3 nop/baseline:** untouched baseline must compile, run, and fail a majority of scored tests for scientific reasons while the healthy ordering control already looks green.
- **RC4 anti-cheat:** regenerate reports and reorderings; never ship expected digests on solver-visible surfaces.
- **RC5 determinism:** no clocks, RNG, network, or host-dependent paths; clean rebuild byte identity required; pin reduction order.
- **RC6 category fit:** primary work is numerical AMG hierarchy parity under reordering, not generic debugging theater.
- **RC7 environment scale:** ship ≥20 meaningful environment files; no padding empty stubs.
- **GX1 Docker offline:** digest-pinned base, all deps at build time, `allow_internet = false`.
- **GX3 collapse/flipping-point:** verify each location controls only its declared ≤0.5 subset after oracle green.
- **GX9 naming/grep:** enforce construction-manifest symbols and forbidden-token ban on the fix path.
- **GX10 packaging:** exclude solution, tests, reviewer material, and caches from the image and zip.
- **Static checks:** anonymous author fields, version 2.0 task.toml, `.dockerignore` present.
- **WW-010 schema citation:** instruction.md must cite `/app/docs/parity-report-schema.md` for graded keys.
- **CM-007 verifier:** `cd /tests && PYTHONSAFEPATH=1 python -m pytest … --confcutdir=/tests`.
- **CM-011 / ADR-0014:** agent-facing languages remain fortran/c++/rust; pytest is verifier-only and must not appear in agent language metadata.

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
- `environment/lattice/knurl.f90`
- `environment/lattice/ledge.f90`
- `environment/lattice/ember.f90`
- `environment/lattice/include/knurl.h`
- `environment/lattice/include/common.h`
- `environment/bridge/splice.cpp`
- `environment/bridge/cable.cpp`
- `environment/bridge/relay.cpp`
- `environment/bridge/include/splice.h`
- `environment/bridge/include/common.h`
- `environment/orbit/main.rs`
- `environment/orbit/whorl.rs`
- `environment/orbit/braid.rs`
- `environment/orbit/ffi.rs`
- `environment/orbit/report.rs`
- `environment/orbit/error.rs`
- `environment/orbit/config.rs`
- `environment/kernels/ridge.f90`
- `environment/kernels/ridge.h`
- `environment/tools/build_all.sh`
- `environment/tools/run_amglab.sh`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`
- `construction_manifest.json`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: lattice/knurl.f90
  symbol: knurl_p
  kind: function
  signature: integer(c_int) function knurl_p(a, b, c) bind(C)
  purpose: Builds strength membership for the active presentation without depending on raw row order.

- path: bridge/splice.cpp
  symbol: splice_q
  kind: function
  signature: int32_t splice_q(const int32_t* a, int32_t b, uint64_t* c);
  purpose: Assembles transfer operators from membership under the active presentation.

- path: orbit/whorl.rs
  symbol: whorl_r
  kind: function
  signature: pub(crate) fn whorl_r(a: u64, b: &mut Orbit) -> i8
  purpose: Applies hierarchy steps with a stable identity binding for digest emission.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: lattice/knurl.f90
    controls_tests: [test_m01, test_m02, test_m06, test_m10]
  - id: B
    path: bridge/splice.cpp
    controls_tests: [test_m03, test_m05, test_m07, test_m11]
  - id: C
    path: orbit/whorl.rs
    controls_tests: [test_m04, test_m08, test_m09, test_m12]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: lattice/ledge.f90
  kind: helper
  rhymes_with: knurl_p
  non_fix_purpose: Computes ordinary smoothness-style diagnostic banners without affecting membership.

- path: bridge/cable.cpp
  kind: helper
  rhymes_with: splice_q
  non_fix_purpose: Maps display codes for status lines without affecting transfer assembly.

- path: orbit/braid.rs
  kind: helper
  rhymes_with: whorl_r
  non_fix_purpose: Folds scalar diagnostic marks into aggregate counters.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [algebraic, multigrid, lab, app, sparse, linear, system, hierarchy, preconditioner, matrix, reorderings, reordering, convergence, curves, fine-grid, solution, digests, digest, tolerance, healthy, ordering, control, smoothness, indicators, coarse-size, summaries, pipeline, residual, residuals, solution-digest, contracts, bin, amglab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, permutation, inputs, report, checks, compiled, bundled, equivalent, green, rebuild, invoke, emit, hand, hard-code, regenerate, presented, fixed, past, look, acceptable, both, meet, stays, whose, follow, normative, documented, one, write, through]
```
