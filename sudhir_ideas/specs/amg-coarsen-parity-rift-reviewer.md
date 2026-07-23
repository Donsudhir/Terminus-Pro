### Decision
GO — Attempt 1. Distributed three-location AMG hierarchy dual-reordering parity topology across Fortran, C++, and Rust (`lattice/`, `bridge/`, `orbit/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- Task name: amg-coarsen-parity-rift
- Title: AMG Coarsen Parity Rift
- Category: scientific-computing
- Languages: [fortran, c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [amg, multigrid, sparse-matrix, reordering, iterative-solvers]
- Milestones: 0

### Investigation profile
The primary weakness area is long-horizon debugging, reinforced by multi-component reasoning, partial failures, and ambiguous bug reports. The task is one AMG hierarchy incident: under equivalent reorderings, convergence and fine-grid digests diverge while smoothness and coarse-size can look acceptable, and a nearby healthy ordering control stays green.

1. Run dual reorderings beside the healthy ordering control. Residual/digest-red with smoothness bait concentrates after hierarchy construction, justifying hierarchy-focused investigation.
2. Correlate logs, metrics, and parity_report fields. Disagreement tracks hierarchy membership and apply identity rather than healthy-control runs.
3. Trace Fortran lattice selection intermediates. Strength/membership follows presentation order rather than graph-stable identity.
4. Probe C++ bridge transfer assembly under both reorderings. Transfers inherit the order-dependent coarse set without remapping.
5. Inspect Rust orbit apply/V-cycle intermediates. Apply coupling mixes identity conventions so digests diverge while bait stays green.
6. Repair all three authorities, rebuild, and verify dual-ordering/control matrices end-to-end.

Evidence surfaces are code (`lattice/`, `bridge/`, `orbit/`), runtime-state (`/app/bin/amglab` dual/control runs), logs (`fixtures/logs/run_trace.ndjson`), metrics (residual/digest fields in `parity_report.json`), and filesystem (bundled cases and hierarchy scratch). Competing hypotheses include a broken smoother under reordering, unstable floating digests, and non-equivalent fixtures; each has a deterministic healthy-control, residual-contract, or case-identity falsifier. The conditional matrix includes failing dual-reordering / generated variants plus healthy ordering control and smoothness-bait rejection. The estimate is 52 meaningful actions. All sources and fixtures are fixed and offline; resets avoid clocks, entropy, and filesystem-order dependence.

### Discovery budget
- Discovery: Strength/coarse-set selection walks the presentation order of matrix rows rather than a graph-stable identity, so equivalent reorderings change the selected set while smoothness heuristics still look plausible.
  Planned location: environment/lattice/knurl.f90::knurl_p
  Why instruction must not reveal it: Naming order-indexed strength selection or coarse-set dependence would collapse the Fortran diagnosis into a disclosed indexing edit.
- Discovery: Transfer (prolongation/restriction) construction inherits the order-dependent coarse set without remapping under reordering, so the hierarchy operators disagree across equivalent presentations.
  Planned location: environment/bridge/splice.cpp::splice_q
  Why instruction must not reveal it: Naming prolongation, restriction, or inheritance of the coarse set would directly expose the C++ repair and convert the task into a recipe.
- Discovery: Apply/V-cycle coupling mixes identity conventions across ordered and unordered paths, so fine-grid solution digests diverge even when smoothness and coarse-size summaries look acceptable.
  Planned location: environment/orbit/whorl.rs::whorl_r
  Why instruction must not reveal it: Naming mixed identity conventions or V-cycle apply keying would reduce the Rust work to a disclosed remap.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest dual-ordering/control outcomes and schema citation do not reveal the three inconsistent authorities. |
| Hidden-instance | PASS | Bundled, generated, dual-reordering, and healthy-control scenarios require a general repair. |
| Single-artifact repair | PASS | Three roots and regenerated matrices prevent artifact replacement. |
| Generalization | PASS | Generated reordering variants extend beyond the bundled incident. |
| Prompt-honesty | PASS | Invocation, schema path, dual/control outcomes, and hardcoding bans are documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; cross-language hierarchy diagnosis creates difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Three distinct roots each control 4/12 tests. |
| Oracle-locality | PASS | Planned semantic delta is substantive across three functions, not one short rewrite. |
| Small declarative-cluster | PASS | Report schema documents keys only; it does not contain the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, and decoys avoid stub completion. |
| Recipe-discount | PASS | Classical-AMG or single-permutation recipes leave selection/transfer/apply defects. |
| Security-aura discount | PASS | Scientific AMG hierarchy parity remains after removing any security framing. |
| Orthogonal-checklist | PASS | Dual residual/digest parity, bait rejection, and healthy-control stability are one coupled invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious entrypoints do not expose all three authorities or their coupling. |
| Hard-only gate | PASS | Professional mixed-language AMG hierarchy diagnosis and three-boundary coordination remain. |
| Discovery budget test | PASS | Three non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Symptoms-only; schema is public contract; causes remain hidden. |
| Topology distribution test | PASS | Three ≥3-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `lattice/knurl.f90::knurl_p`, `bridge/splice.cpp::splice_q`, `orbit/whorl.rs::whorl_r`. No single location suffices because selection, transfer-inheritance, and apply-identity failures are independently observable on dual/control matrices.
2. **topology_b_hierarchy_chain** — `lattice/knurl.f90::knurl_p`, `bridge/splice.cpp::splice_q`, `orbit/whorl.rs::whorl_r`, `bridge/relay.cpp::rebind_u`. Correct selection fails without transfer assembly and apply rebind; correct upstream state fails under wrong digest identity.
3. **topology_c_identity_convention** — `lattice/index.f90::map_v`, `bridge/splice.cpp::splice_q`, `orbit/whorl.rs::whorl_r`. Membership maps, transfer keys, and apply identity must agree end-to-end under reordering.

### Rubric axes
- **Verifiable — PASS:** dual digests, residual contracts, healthy-control green, and regenerated reports are machine-checkable.
- **Well-specified — PASS:** symptoms, invocation, schema citation, and prohibited hardcoding are clear.
- **Solvable — PASS:** bounded existing pipeline; expert hours, not research years.
- **Difficult — PASS:** hard after honest disclosure; causes not named.
- **Interesting — PASS:** real AMG hierarchy engineering value in sparse iterative solvers.
- **Outcome-verified — PASS:** any correct implementation accepted.

### Hardness axes
- **Discover — PASS:** three hidden facts must be recovered from code/runtime.
- **Synthesize — PASS:** three languages and three authorities.
- **Diagnose — PASS:** symptoms-only instruction.
- **Navigate coupling — PASS:** subset fixes leave other dual/control properties red.
- **Reason beyond training — PASS:** textbook AMG recipes cannot clear selection+transfer+apply defects under metamorphic reorderings.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction defines success conditions and cites the normative report schema, but it does not identify the inconsistent authorities or fix sites.

## Reviewer Appendix

### Implementation plan
Build an existing mixed-language AMG lab that already compiles, constructs a hierarchy, applies it, and emits a plausible parity report. Seed defects at the three selected locations so smoothness indicators and coarse-size summaries can look acceptable under equivalent reorderings while residuals and fine-grid digests disagree, and keep a fixed healthy ordering control green. Provide smoother/residual kernels, transfer assembly, and report emission so solvers diagnose and integrate rather than invent an entire multigrid stack. Verifiers regenerate dual-reordering pairs and check independent digest folds without accepting permutation hard-coding.

### Proposed file inventory
Matches the authoring spec Initial Draft Commitments (≥20 environment files): Fortran lattice knurl/ledge/ember helpers; C++ bridge splice/cable/relay; Rust orbit whorl/braid/ffi/report; Fortran residual kernel; data/fixtures/docs/conf/tools; Docker + Makefile. Normative `docs/parity-report-schema.md` is solver-visible and cited from instruction.md.

### Oracle notes
`solve.sh` performs substantive repairs at A–C only: make `knurl_p` select membership by graph-stable identity rather than raw presentation order; make `splice_q` assemble transfers from that membership under the active presentation without inheriting a broken order-only set; make `whorl_r` bind apply identity stably for digest emission. Do not replace fixtures, invent report values, hard-code one permutation, or disable tests.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Coordinated substantive edits to `knurl_p`, `splice_q`, and `whorl_r` across three language roots; any strict subset leaves at least one dual-ordering residual, digest, or healthy-control property failing.

Likely editable frontier:
- lattice/knurl.f90
- bridge/splice.cpp
- orbit/whorl.rs

Requirement-to-file map:
- dual-reordering residual/digest parity -> coordinated A–C
- smoothness/coarse-size bait rejection -> residual/digest tests (not bait fields)
- healthy ordering control stays green -> B/C control subsets plus regenerated matrices
- no hard-coded permutation -> regenerated reordering families

Oracle estimated complexity: ~120–220 lines of non-boilerplate logic across three functions plus FFI glue touch-ups

Red flags:
- none for this plan stage; watch during construction for scream-sticky order comments and sibling correct implementations of the buggy functions

Residual hardness:
After the file tree is visible, the solver must still recover why equivalent reorderings disagree across selection, transfer, and apply authorities and preserve one dual-ordering/control invariant through all three locations without hard-coding a permutation.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
algebraic, multigrid, lab, app, sparse, linear, system, hierarchy, preconditioner, matrix, reorderings, reordering, convergence, curves, fine-grid, solution, digests, digest, tolerance, healthy, ordering, control, smoothness, indicators, coarse-size, summaries, pipeline, residual, residuals, solution-digest, contracts, bin, amglab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, permutation, inputs, report, checks, compiled, bundled, equivalent, green, rebuild, invoke, emit, hand, hard-code, regenerate, presented, fixed, past, look, acceptable, both, meet, stays, whose, follow, normative, documented, one, write, through

**Renames during drafting:**
- `lattice/strength.f90` → `lattice/knurl.f90`: removed cause-revealing strength vocabulary
- `bridge/prolong.cpp` → `bridge/splice.cpp`: removed cause-revealing prolongation vocabulary
- `orbit/apply.rs` → `orbit/whorl.rs`: removed instruction noun `app` as substring of apply
- `select_coarse_set` → `knurl_p`: avoided coarse/selection vocabulary
- `build_transfer` → `splice_q`: avoided transfer vocabulary
- `apply_vcycle` → `whorl_r`: avoided apply vocabulary and `app` substring

**Test names audited:**
- test_m01
- test_m02
- test_m03
- test_m04
- test_m05
- test_m06
- test_m07
- test_m08
- test_m09
- test_m10
- test_m11
- test_m12

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - L1 (`lattice/knurl.f90`): 4/12 = 0.333
  - L2 (`bridge/splice.cpp`): 4/12 = 0.333
  - L3 (`orbit/whorl.rs`): 4/12 = 0.333
- Cap: 0.5. Max ratio observed: 0.333. Status: PASS

### Per-test feasibility pre-check
- Test: test_m01 — Checks dual-reordering residual contract on bundled case — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m02 — Checks dual-reordering fine-grid digests on bundled case — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m03 — Checks transfer-sensitive residual contract — Valid approaches: 2+ — Chain-dependent: partial on selection — Feasibility risk: MEDIUM
- Test: test_m04 — Checks report digests vs independent fold — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m05 — Checks sequential families do not inherit prior presentation identity — Valid approaches: 2+ — Chain-dependent: yes on transfer repair — Feasibility risk: MEDIUM
- Test: test_m06 — Checks combined selection+transfer dual-ordering parity — Valid approaches: 2+ — Chain-dependent: yes on A+B — Feasibility risk: MEDIUM
- Test: test_m07 — Checks bait does not mask residual/digest failure — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m08 — Checks apply identity binding under both reorderings — Valid approaches: 2+ — Chain-dependent: partial on upstream — Feasibility risk: MEDIUM
- Test: test_m09 — Checks report summary agrees with digests — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m10 — Checks deterministic dual-ordering parity under reordered execution — Valid approaches: 2+ — Chain-dependent: yes on A+B — Feasibility risk: MEDIUM
- Test: test_m11 — Checks healthy ordering control stays green across rebuilds — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m12 — Checks clean rebuild byte identity of parity_report — Valid approaches: 2+ — Chain-dependent: yes on apply path — Feasibility risk: LOW
