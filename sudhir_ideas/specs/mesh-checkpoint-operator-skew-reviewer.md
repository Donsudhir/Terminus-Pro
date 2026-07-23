### Decision
GO — Attempt 1. Distributed three-location remesh+resume twin-parity topology across C++, Rust, and Fortran (`native/`, `host/`, `pack/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- Task name: mesh-checkpoint-operator-skew
- Title: Mesh Checkpoint Operator Skew
- Category: scientific-computing
- Languages: [c++, rust, fortran]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [checkpoint-restart, mesh, scientific-computing, ffi, twin-parity]
- Milestones: 0

### Investigation profile
The primary weakness area is long-horizon debugging, reinforced by multi-component reasoning, partial failures, and ambiguous bug reports. The task is one remesh+resume incident: residual norms can look plausible while solution-field digests disagree with a never-interrupted twin, and a nearby no-checkpoint control stays healthy.

1. Run remesh+resume beside twin and no-checkpoint control. Residual-green / digest-red concentrates after remesh, justifying boundary-focused investigation.
2. Correlate logs, metrics, and parity_report fields. Disagreement tracks the pause/remesh/resume boundary rather than fresh runs.
3. Trace shelf contents and native geometry lifecycle across FFI. A geometry generation token is omitted or rebound incorrectly.
4. Probe host reuse decisions before and after remesh. Reuse continues under a pre-remesh identity.
5. Inspect pack-side fold/digest intermediates. Digests retain pre-remesh ordering or scratch.
6. Repair all three authorities, rebuild, and verify twin/control matrices end-to-end.

Evidence surfaces are code (`native/`, `host/`, `pack/`), runtime-state (`/app/bin/meshlab` twin/control runs), logs (`fixtures/logs/run_trace.ndjson`), metrics (iteration/residual counters in `parity_report.json`), and filesystem (bundled cases and shelf artifacts). Competing hypotheses include a broken residual kernel after remesh, random checkpoint I/O corruption, and a twin-harness case mismatch; each has a deterministic no-checkpoint, shelf-digest, or case-identity falsifier. The conditional matrix includes failing remesh+resume / generated variants plus healthy no-checkpoint and never-interrupted twin controls. The estimate is 48 meaningful actions. All sources and fixtures are fixed and offline; resets avoid clocks, entropy, and filesystem-order dependence.

### Discovery budget
- Discovery: The mid-run checkpoint omits or misbinds a geometry generation token that must round-trip across the C++/Rust boundary so post-remesh identity matches the never-interrupted twin.
  Planned location: environment/native/span.cpp::braid_q
  Why instruction must not reveal it: Naming a missing geometry token or cross-language binding would collapse the native diagnosis into a disclosed serialization edit.
- Discovery: After remesh, host-side assembly/operator reuse continues under a pre-remesh identity key, so residual norms can look plausible while the solution trajectory diverges from the twin.
  Planned location: environment/host/shelf.rs::latch_r
  Why instruction must not reveal it: Naming operator reuse, cache keying, or invalidation would directly expose the host repair and convert the task into a recipe.
- Discovery: Pack-side field packing and digest folding retain pre-remesh ordering or scratch, so emitted solution-field digests disagree even when upstream residuals look ordinary.
  Planned location: environment/pack/fold.f90::sift_s
  Why instruction must not reveal it: Naming pre-remesh ordering or retained scratch would reduce the Fortran work to a disclosed layout flip.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest twin/control outcomes and schema citation do not reveal the three inconsistent authorities. |
| Hidden-instance | PASS | Bundled, generated, twin, and no-checkpoint scenarios require a general repair. |
| Single-artifact repair | PASS | Three roots and regenerated twin matrices prevent artifact replacement. |
| Generalization | PASS | Generated remesh+resume variants extend beyond the bundled incident. |
| Prompt-honesty | PASS | Invocation, schema path, twin/control outcomes, and hardcoding bans are documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; cross-language remesh diagnosis creates difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Three distinct roots each control 4/12 tests. |
| Oracle-locality | PASS | Planned semantic delta is substantive across three functions, not one short rewrite. |
| Small declarative-cluster | PASS | Report schema documents keys only; it does not contain the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, and decoys avoid stub completion. |
| Recipe-discount | PASS | Checkpoint I/O or global flush recipes leave geometry-token and fold-order defects. |
| Security-aura discount | PASS | Scientific remesh+resume parity remains after removing any security framing. |
| Orthogonal-checklist | PASS | Twin parity, residual contracts, and no-checkpoint stability are one coupled invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious entrypoints do not expose all three authorities or their coupling. |
| Hard-only gate | PASS | Professional mixed-language remesh+resume diagnosis and three-boundary coordination remain. |
| Discovery budget test | PASS | Three non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Symptoms-only; schema is public contract; causes remain hidden. |
| Topology distribution test | PASS | Three ≥3-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `native/span.cpp::braid_q`, `host/shelf.rs::latch_r`, `pack/fold.f90::sift_s`. No single location suffices because geometry-token, reuse-keying, and fold-order failures are independently observable on twin/control matrices.
2. **topology_b_lifecycle_chain** — `host/shelf.rs::latch_r`, `native/span.cpp::braid_q`, `host/relay.rs::rebind_u`, `pack/fold.f90::sift_s`. Correct shelf writes fail without geometry identity and resume rebind; correct upstream state fails under wrong fold order.
3. **topology_c_reduction_convention** — `native/index.cpp::map_v`, `host/shelf.rs::latch_r`, `pack/fold.f90::sift_s`. Index maps, reuse keys, and reduction order must agree end-to-end after remesh.

### Rubric axes
- **Verifiable — PASS:** twin digests, residual contracts, no-checkpoint byte identity, and regenerated reports are machine-checkable.
- **Well-specified — PASS:** symptoms, invocation, schema citation, and prohibited hardcoding are clear.
- **Solvable — PASS:** bounded existing pipeline; expert hours, not research years.
- **Difficult — PASS:** hard after honest disclosure; causes not named.
- **Interesting — PASS:** real remesh+resume engineering value in scientific solvers.
- **Outcome-verified — PASS:** any correct implementation accepted.

### Hardness axes
- **Discover — PASS:** three hidden facts must be recovered from code/runtime.
- **Synthesize — PASS:** three languages and three authorities.
- **Diagnose — PASS:** symptoms-only instruction.
- **Navigate coupling — PASS:** subset fixes leave other twin/control properties red.
- **Reason beyond training — PASS:** textbook checkpoint recipes cannot clear reuse+fold defects.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction defines success conditions and cites the normative report schema, but it does not identify the inconsistent authorities or fix sites.

## Reviewer Appendix

### Implementation plan
Build an existing mixed-language mesh solver that already compiles, checkpoints mid-run, remeshes, resumes, and emits a plausible parity report. Seed defects at the three selected locations so residual norms and iteration counts can look ordinary after resume while solution-field digests disagree with a never-interrupted twin. Keep fresh no-checkpoint runs correct as a healthy control. Provide residual kernels, shelf IO, and report assembly so solvers diagnose and integrate rather than invent an entire FEM stack. Verifiers regenerate interrupted/uninterrupted pairs and check independent digest folds.

### Proposed file inventory
Matches the authoring spec Initial Draft Commitments (≥20 environment files): native C++ span/ledge/ember helpers; Rust host shelf/locker/relay/ffi/report; Fortran fold/tally and residual kernel; data/fixtures/docs/conf/tools; Docker + Makefile. Normative `docs/parity-report-schema.md` is solver-visible and cited from instruction.md.

### Oracle notes
`solve.sh` performs substantive repairs at A–C only: make `braid_q` persist and restore the geometry generation token across the language boundary; make `latch_r` rebind reuse context from post-remesh identity rather than a pre-remesh key; make `sift_s` fold digests under the active post-remesh ordering without retained scratch. Do not replace fixtures, invent report values, or disable tests.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Coordinated edits across `native/span.cpp`, `host/shelf.rs`, and `pack/fold.f90` totaling well above a trivial one-function tweak; any strict subset fails declared flipping-point subsets.

Likely editable frontier:
- native/span.cpp
- host/shelf.rs
- pack/fold.f90
- (decoys native/ledge.cpp, host/locker.rs, pack/tally.f90 are non-fix)

Requirement-to-file map:
- twin digest / pointwise residual after remesh+resume -> native/span.cpp (+ interactions)
- shelf restore / reuse after remesh -> host/shelf.rs
- digest fold / report summary agreement -> pack/fold.f90
- healthy no-checkpoint byte stability -> must remain green without breaking twin fixes (cross-cutting control)

Oracle estimated complexity: 90–160 lines of non-boilerplate logic across three files

Red flags:
- none currently; watch for accidental `operator`/`cache`/`invalidate`/`remesh`/`checkpoint` names on the fix path during construction

Residual hardness:
After the file tree is visible, the solver must still discover which authorities disagree and preserve one twin/control invariant through three locations.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
scientific, mesh, lab, app, case, checkpoints, mid-run, remeshes, resumes, resume, residual, norms, iteration, counts, solution-field, digests, twin, pointwise, samples, runs, checkpoint, rebuilds, pipeline, interrupted, uninterrupted, trajectories, agreement, field, contracts, healthy, no-checkpoint, control, bin, meshlab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, inputs, report, checks, compiled, bundled

**Renames during drafting:**
- [`native/mesh_geom.cpp` → `native/span.cpp`: removed instruction noun mesh]
- [`host/checkpoint.rs` → `host/shelf.rs`: removed instruction noun checkpoint]
- [`host/operator_cache.rs` → `host/shelf.rs`: removed cause-revealing operator/cache naming]
- [`pack/field_digest.f90` → `pack/fold.f90`: removed field/digests nouns]
- [`bind_geometry_token` → `braid_q`: avoided geometry/token tell]
- [`invalidate_operator` → `latch_r`: avoided invalidate/operator tell]
- [`fold_solution_digest` → `sift_s`: avoided solution/digest vocabulary]

**Test names audited:**
- test_m01 through test_m12

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - L1 (`native/span.cpp`): 4/12 = 0.3333
  - L2 (`host/shelf.rs`): 4/12 = 0.3333
  - L3 (`pack/fold.f90`): 4/12 = 0.3333
- Cap: 0.5. Max ratio observed: 0.3333. Status: PASS

### Per-test feasibility pre-check
- Test: test_m01 — Checks: twin solution-field digest after remesh+resume — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m02 — Checks: twin pointwise residual samples after remesh+resume — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m03 — Checks: residual contracts after shelf restore vs twin — Valid approaches: 2+ — Chain-dependent: yes (shelf IO) — Feasibility risk: MEDIUM
- Test: test_m04 — Checks: report digests vs independent fold — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m05 — Checks: sequential families isolate reuse identity — Valid approaches: 2+ — Chain-dependent: yes (family order) — Feasibility risk: MEDIUM
- Test: test_m06 — Checks: combined geometry+reuse twin parity — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m07 — Checks: residual-norm plausibility does not mask digest failure after repair — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m08 — Checks: pack fold uses post-remesh ordering — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m09 — Checks: summary agrees with emitted digests — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_m10 — Checks: reordered execution determinism for twin parity — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m11 — Checks: no-checkpoint control byte identity across rebuilds — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_m12 — Checks: clean rebuild byte identity on fold+control path — Valid approaches: 1–2 — Chain-dependent: yes — Feasibility risk: MEDIUM
