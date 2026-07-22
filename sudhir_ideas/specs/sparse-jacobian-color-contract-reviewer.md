### Decision
GO — Attempt 1. Distributed four-location sparse-sensitivity topology across C, Rust, and Fortran; symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- Task name: sparse-jacobian-color-contract
- Title: Sparse Jacobian Color Contract
- Category: scientific-computing
- Languages: [c, rust, fortran]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [sparse-derivatives, finite-differences, scientific-computing, ffi, metamorphic-testing]
- Milestones: 0

### Discovery budget
- Discovery: The column partitioner treats a structurally symmetric nonzero pattern as a safe grouping even when the residual Jacobian is numerically unsymmetric, so structurally non-orthogonal unknowns share a probe.
  Planned location: environment/native/lane.c::mix_cols
  Why instruction must not reveal it: Naming structural symmetry, coloring, or orthogonality would collapse the C diagnosis into a textbook CPR lookup.
- Discovery: Resuming a saved probe plan rebinds group slots without clearing prior seed bits, so later groups inherit leaked contributions from earlier partitions.
  Planned location: environment/host/vault.rs::bind_slot
  Why instruction must not reveal it: Naming seed hygiene or plan-slot clearing would directly expose the Rust plan-boundary repair.
- Discovery: Absolute finite-difference step magnitude is derived from a residual norm cached when the first plan is built and reused after independent scale-equivalent batches arrive.
  Planned location: environment/host/gauge.rs::reset_span
  Why instruction must not reveal it: Stating that step policy must reset per batch would directly expose the magnitude lifecycle repair.
- Discovery: Compression packs nonzero contributions using one sparse orientation while the Fortran unpack reads the opposite orientation, scrambling retained entries after otherwise correct probes.
  Planned location: environment/analysis/knit.f90::merge_slots
  Why instruction must not reveal it: Naming CSR/CSC or row/column major unpack would reduce the Fortran work to a disclosed layout flip.

### Anti-trivialization verdict
All 21 checks PASS in attempt-1 evidence (`sudhir_ideas/specs/sparse-jacobian-color-contract-attempt-1-evidence.json`). Disclosure-collapse, hidden-instance, single-artifact, grep-collapse, recipe-discount, discovery-budget, instruction-specificity, and topology-distribution are explicitly green.

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `native/lane.c::mix_cols`, `host/vault.rs::bind_slot`, `host/gauge.rs::reset_span`, `analysis/knit.f90::merge_slots`. No single location suffices because partition, seed, magnitude, and unpack failures are independently observable.
2. **topology_b_probe_chain** — `mix_cols`, `ember.c::tap_seed`, `quill.c::pack_diff`, `vault.rs::bind_slot`. Correct groups fail without correct seeds/compression/plan binding.
3. **topology_c_index_convention** — `kernels/ridge.f90::eval_resid`, `mix_cols`, `gauge.rs::reset_span`, `knit.f90::merge_slots`. Index and scale conventions must agree end-to-end.

### Rubric axes
- Verifiable: PASS — metamorphic packed-matrix and directional-product checks are programmatic.
- Well-specified: PASS — symptoms, invocation, output, and prohibited hardcoding are clear.
- Solvable: PASS — bounded existing pipeline; expert hours, not research years.
- Difficult: PASS — hard after honest disclosure; causes not named.
- Interesting: PASS — real sparse-derivative engineering value.
- Outcome-verified: PASS — any correct implementation accepted.

### Hardness axes
- Discover: PASS — four hidden facts must be recovered from code/runtime.
- Synthesize: PASS — three languages and four authorities.
- Diagnose: PASS — symptoms-only instruction.
- Navigate coupling: PASS — subset fixes leave other metamorphic batches red.
- Reason beyond training: PASS — reference coloring cannot clear lifecycle/unpack defects.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction defines success conditions but not the inconsistent authorities or fix sites.

## Reviewer Appendix

### Implementation plan
Build an existing mixed-language residual sensitivity lab that already compiles and emits a plausible packed report. Seed defects at the four selected locations so ordinary batches look mostly healthy while permutation, resume, and scale-equivalent variants diverge. Provide healthy residual kernels, pattern IO, and report assembly so solvers diagnose and integrate rather than invent an entire sparse AD stack. Verifiers regenerate outputs and check independent directional probes.

### Proposed file inventory
Matches the authoring spec Initial Draft Commitments (≥20 environment files): native C partition/compression helpers and decoys; Rust host vault/gauge/locker/meter/ffi/report; Fortran knit/tally and residual kernel; data/docs/conf/tools; Docker + Makefile.

### Oracle notes
`solve.sh` performs substantive repairs at A–D only: make `mix_cols` require true structural orthogonality without unsafe symmetry; make `bind_slot` clear shelf bits on rebind; make `reset_span` rebuild magnitude from the current batch; make `merge_slots` unpack with the compression orientation. Do not replace fixtures or disable tests.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Coordinated edits across `native/lane.c`, `host/vault.rs`, `host/gauge.rs`, and `analysis/knit.f90` totaling well above a trivial one-function tweak; any strict subset fails declared flipping-point subsets.

Likely editable frontier:
- native/lane.c
- host/vault.rs
- host/gauge.rs
- analysis/knit.f90
- (decoys native/ledge.c, host/locker.rs, host/meter.rs, analysis/tally.f90 are non-fix)

Requirement-to-file map:
- permutation/support correctness -> native/lane.c (+ interactions)
- resume parity -> host/vault.rs
- scale parity / magnitude summary -> host/gauge.rs
- packed layout / summary agreement -> analysis/knit.f90

Oracle estimated complexity: 80–160 lines of non-boilerplate logic across four files

Red flags:
- none currently; watch for accidental `jacobian`/`color`/`seed` names on the fix path during construction

Residual hardness:
After the file tree is visible, the solver must still discover which authorities disagree and preserve one metamorphic invariant through four locations.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
residual, lab, app, sensitivity, report, batch, unknown, probe, plan, entry, matrix-vector, product, scale, support, mismatch, disagreement, matrix, audit, summary, pipeline, output, bin, senslab, variant, identity, nonzero, layout, directional, cardinality, structure, linearization, contract, reproducibility, digest, input, check, packed, json

**Renames during drafting:**
- [`native/color.c` → `native/lane.c`: removed coloring tell]
- [`host/plan.rs` → `host/vault.rs`: removed instruction noun plan]
- [`host/scale.rs` → `host/gauge.rs`: removed instruction noun scale]
- [`analysis/unpack.f90` → `analysis/knit.f90`: removed unpack tell]
- [`apply_seed` → `bind_slot`: avoided seed/probe vocabulary]

**Test names audited:**
- test_k01 through test_k12

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - L1 (`native/lane.c`): 4/12 = 0.3333
  - L2 (`host/vault.rs`): 4/12 = 0.3333
  - L3 (`host/gauge.rs`): 4/12 = 0.3333
  - L4 (`analysis/knit.f90`): 4/12 = 0.3333
- Cap: 0.34. Max ratio observed: 0.3333. Status: PASS

### Per-test feasibility pre-check
- Test: test_k01 — Checks: permutation parity of packed support/values — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_k02 — Checks: held-out directional probes vs packed entries — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_k03 — Checks: resume-from-plan equals cold start — Valid approaches: 2+ — Chain-dependent: yes (plan IO) — Feasibility risk: MEDIUM
- Test: test_k04 — Checks: scale-equivalent directional products — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: MEDIUM
- Test: test_k05 — Checks: mixed-scale batches isolate magnitude — Valid approaches: 2+ — Chain-dependent: yes (batch order) — Feasibility risk: MEDIUM
- Test: test_k06 — Checks: permutation+resume combined — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_k07 — Checks: audit support counts match packed layout — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_k08 — Checks: unpack vs dense probes on retained indices — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_k09 — Checks: summary agrees with emitted structure — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_k10 — Checks: reordered execution determinism — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_k11 — Checks: scale summary matches active batch — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_k12 — Checks: clean rebuild byte identity on scale+unpack path — Valid approaches: 1–2 — Chain-dependent: yes — Feasibility risk: MEDIUM
