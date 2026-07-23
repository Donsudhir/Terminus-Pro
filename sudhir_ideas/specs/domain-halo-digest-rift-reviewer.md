### Decision
GO — Attempt 1. Distributed three-location rank-map twin-parity topology across C and Rust (`native/`, `host/`); symptoms-only instruction; 0 FAIL / 0 WARN evidence.

### Metadata
- Task name: domain-halo-digest-rift
- Title: Domain Halo Digest Rift
- Category: scientific-computing
- Languages: [rust, c]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [domain-decomposition, field-digests, scientific-computing, ffi, twin-parity]
- Milestones: 0

### Investigation profile
The primary weakness area is long-horizon debugging, reinforced by multi-component reasoning, partial failures, and ambiguous bug reports. The task is one rank-map incident: local norms can look ordinary and exchange can look complete while global fold checksums disagree with a steady twin that never changed maps, and a nearby steady control stays healthy.

1. Run map-changed trajectories beside twin and steady control. Local-green / fold-red concentrates after the map change, justifying boundary-focused investigation.
2. Correlate logs, metrics, and parity_report fields. Disagreement tracks the rank-map boundary rather than fresh steady runs.
3. Trace native fringe pack/unpack across FFI. Boundary values follow a pre-map neighbor layout.
4. Probe host shared-boundary authority and stage metadata. Host marks complete one stage early while native buffers lag.
5. Inspect fold/reduce intermediates. Global checksums retain pre-map ordering or scratch.
6. Repair all three authorities, rebuild, and verify twin/control matrices end-to-end.

Evidence surfaces are code (`native/`, `host/`), runtime-state (`/app/bin/partlab` twin/control runs), logs (`fixtures/logs/run_trace.ndjson`), metrics (local-norm counters in `parity_report.json`), and filesystem (bundled cases and map artifacts). Competing hypotheses include a broken residual kernel after map change, random map-file corruption, and a twin-harness case mismatch; each has a deterministic steady-control, map-digest, or case-identity falsifier. The conditional matrix includes failing map-changed / generated variants plus healthy steady and never-map-changed twin controls. The estimate is 52 meaningful actions. All sources and fixtures are fixed and offline; resets avoid clocks, entropy, and filesystem-order dependence.

### Discovery budget
- Discovery: After a rank map change, native fringe pack/unpack still uses the pre-map neighbor layout, so boundary values look locally ordinary while twin fold checksums diverge.
  Planned location: environment/native/ledge.c::braid_q
  Why instruction must not reveal it: Naming fringe packing or a stale neighbor layout would collapse the native diagnosis into a disclosed buffer edit.
- Discovery: Host shared-boundary authority and stage metadata mark exchange complete one stage early while native buffers still lag, so status looks healthy while trajectories diverge from the twin.
  Planned location: environment/host/shelf.rs::latch_r
  Why instruction must not reveal it: Naming ownership, sync-stage lag, or early completion would directly expose the host repair and convert the task into a recipe.
- Discovery: Global fold/reduce retains pre-map ordering or scratch, so emitted fold checksums disagree even when upstream local norms look ordinary.
  Planned location: environment/native/ember.c::sift_s
  Why instruction must not reveal it: Naming pre-map ordering or retained scratch would reduce the fold work to a disclosed layout flip.

### Anti-trivialization verdict
| Check | Verdict | Reviewer basis |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest twin/control outcomes and schema citation do not reveal the three inconsistent authorities. |
| Hidden-instance | PASS | Bundled, generated, twin, and steady scenarios require a general repair. |
| Single-artifact repair | PASS | Three roots and regenerated twin matrices prevent artifact replacement. |
| Generalization | PASS | Generated map-change variants extend beyond the bundled incident. |
| Prompt-honesty | PASS | Invocation, schema path, twin/control outcomes, and hardcoding bans are documented. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects tests; cross-language map-change diagnosis creates difficulty. |
| Mechanical-fix filter | PASS | No dependency, timeout, reward, or metadata repair is the task. |
| Localized-fix | PASS | Three distinct roots each control 4/12 tests. |
| Oracle-locality | PASS | Planned semantic delta is substantive across three functions, not one short rewrite. |
| Small declarative-cluster | PASS | Report schema documents keys only; it does not contain the behavioral solution. |
| Grep-collapse | PASS | Complete noun provenance has no selected path, symbol, parameter, or test hit. |
| Pre-factored-helper | PASS | Opaque names, plausible baseline bodies, and decoys avoid stub completion. |
| Recipe-discount | PASS | Force-sync or global flush recipes leave fringe-pack and fold-order defects. |
| Security-aura discount | PASS | Scientific rank-map twin parity remains after removing any security framing. |
| Orthogonal-checklist | PASS | Twin parity, sample contracts, and steady stability are one coupled invariant. |
| Harness-discount | PASS | Deterministic Docker and fixtures provide reproducibility only. |
| One-pass solvability | PASS | Obvious entrypoints do not expose all three authorities or their coupling. |
| Hard-only gate | PASS | Professional mixed-language map-change diagnosis and three-boundary coordination remain. |
| Discovery budget test | PASS | Three non-trivial discoveries have concrete homes and disclosure reasons. |
| Instruction specificity test | PASS | Symptoms-only; schema is public contract; causes remain hidden. |
| Topology distribution test | PASS | Three ≥3-location topologies are viable and no one location suffices. |

### Topology enumeration (3 candidate fix topologies)
1. **topology_a_selected** — `native/ledge.c::braid_q`, `host/shelf.rs::latch_r`, `native/ember.c::sift_s`. No single location suffices because fringe-pack, stage-authority, and fold-order failures are independently observable on twin/control matrices.
2. **topology_b_lifecycle_chain** — `host/shelf.rs::latch_r`, `native/ledge.c::braid_q`, `host/relay.rs::stage_u`, `native/ember.c::sift_s`. Correct stage writes fail without fringe packing; correct upstream state fails under wrong fold order.
3. **topology_c_reduction_convention** — `native/brim.c::map_v`, `host/shelf.rs::latch_r`, `native/ember.c::sift_s`. Index maps, stage keys, and reduction order must agree end-to-end after a map change.

### Rubric axes
- **Verifiable — PASS:** twin checksums, sample contracts, steady byte identity, and regenerated reports are machine-checkable.
- **Well-specified — PASS:** symptoms, invocation, schema citation, and prohibited hardcoding are clear.
- **Solvable — PASS:** bounded existing pipeline; expert hours, not research years.
- **Difficult — PASS:** hard after honest disclosure; causes not named.
- **Interesting — PASS:** real rank-map / domain-decomposition engineering value in scientific solvers.
- **Outcome-verified — PASS:** any correct implementation accepted.

### Hardness axes
- **Discover — PASS:** three hidden facts must be recovered from code/runtime.
- **Synthesize — PASS:** two languages and three authorities.
- **Diagnose — PASS:** symptoms-only instruction.
- **Navigate coupling — PASS:** subset fixes leave other twin/control properties red.
- **Reason beyond training — PASS:** textbook exchange-flush recipes cannot clear pack+fold defects.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction defines success conditions and cites the normative report schema, but it does not identify the inconsistent authorities or fix sites.

## Reviewer Appendix

### Implementation plan
Build an existing mixed-language partitioned field lab that already compiles, applies a rank map change mid-run, continues, and emits a plausible parity report. Seed defects at the three selected locations so local norms and exchange status can look ordinary after the map change while global fold checksums disagree with a steady twin. Keep fresh steady runs correct as a healthy control. Provide C kernels, Rust orchestration, and report assembly so solvers diagnose and integrate rather than invent an entire PDE stack. Verifiers regenerate map-changed/steady pairs and check independent fold checksums. No Python in the solvable core.

### Proposed file inventory
Matches the authoring spec Initial Draft Commitments (≥20 environment files): native C ledge/brim/ember helpers; Rust host shelf/locker/relay/ffi/report; data/fixtures/docs/conf/tools; Docker + Makefile. Normative `docs/parity-report-schema.md` is solver-visible and cited from instruction.md. Canonical image: `public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe9e7d8e37ceb96ed907265a3a0df7f44e3737d0b100e7907a679acb36`.

### Oracle notes
`solve.sh` performs substantive repairs at A–C only: make `braid_q` pack/unpack fringe values under the post-map neighbor layout; make `latch_r` rebind shared-boundary authority so stage completion matches native buffer readiness; make `sift_s` fold checksums under the active post-map ordering without retained scratch. Do not replace fixtures, invent report values, or disable tests.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Coordinated edits across `native/ledge.c`, `host/shelf.rs`, and `native/ember.c` totaling well above a trivial one-function tweak; any strict subset fails declared flipping-point subsets.

Likely editable frontier:
- native/ledge.c
- host/shelf.rs
- native/ember.c
- (decoys native/brim.c, host/locker.rs, host/relay.rs are non-fix)

Requirement-to-file map:
- twin fold checksum / pointwise samples after map change -> native/ledge.c (+ interactions)
- stage/authority after map change -> host/shelf.rs
- fold order / report summary agreement -> native/ember.c
- healthy steady byte stability -> must remain green without breaking twin fixes (cross-cutting control)

Oracle estimated complexity: 90–160 lines of non-boilerplate logic across three files

Red flags:
- none currently; watch for accidental `halo`/`ghost`/`ownership`/`synced`/`repartition`/`digest` names on the fix path during construction

Residual hardness:
After the file tree is visible, the solver must still discover which authorities disagree and preserve one twin/control invariant through three locations.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
partitioned, field, lab, app, case, rank, map, change, mid-run, local, norms, ordinary, exchange, status, looks, complete, global, fold, checksums, disagree, steady, twin, never, changed, maps, pointwise, samples, numerically, fresh, runs, without, correct, byte-stable, clean, rebuilds, pipeline, map-changed, trajectories, agree, contracts, healthy, control, bin, partlab, output, parity_report, json, keys, layout, schema, docs, parity-report-schema, inputs, report, checks, regenerate, compiled, bundled

**Renames during drafting:**
- [`native/halo_pack.c` → `native/ledge.c`: removed cause noun halo]
- [`native/ghost_layer.c` → `native/ledge.c`: removed cause noun ghost]
- [`host/ownership.rs` → `host/shelf.rs`: removed cause noun ownership]
- [`host/synced_stage.rs` → `host/shelf.rs`: removed cause noun synced]
- [`native/digest_fold.c` → `native/ember.c`: removed instruction-adjacent digest/fold tell from path]
- [`pack_halo_fringe` → `braid_q`: avoided halo/fringe tell]
- [`mark_exchange_synced` → `latch_r`: avoided exchange/synced tell]
- [`fold_global_digest` → `sift_s`: avoided fold/digest vocabulary on the symbol]

**Test names audited:**
- test_m01 through test_m12

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - L1 (`native/ledge.c`): 4/12 = 0.3333
  - L2 (`host/shelf.rs`): 4/12 = 0.3333
  - L3 (`native/ember.c`): 4/12 = 0.3333
- Cap: 0.5. Max ratio observed: 0.3333. Status: PASS

### Per-test feasibility pre-check
- Test: test_m01 — Checks: twin fold checksum after map change — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m02 — Checks: twin pointwise samples after map change — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m03 — Checks: sample contracts vs twin under stage metadata — Valid approaches: 2+ — Chain-dependent: yes (stage IO) — Feasibility risk: MEDIUM
- Test: test_m04 — Checks: report fold fields vs independent fold — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m05 — Checks: sequential families isolate stage identity — Valid approaches: 2+ — Chain-dependent: yes (family order) — Feasibility risk: MEDIUM
- Test: test_m06 — Checks: combined pack+authority twin parity — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m07 — Checks: local-norm plausibility does not mask fold failure after repair — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m08 — Checks: fold uses post-map ordering — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m09 — Checks: summary agrees with emitted fold checksums — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_m10 — Checks: reordered execution determinism for twin parity — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: MEDIUM
- Test: test_m11 — Checks: steady control byte identity across rebuilds — Valid approaches: 2+ — Chain-dependent: yes — Feasibility risk: LOW
- Test: test_m12 — Checks: clean rebuild byte identity on fold+control path — Valid approaches: 1–2 — Chain-dependent: yes — Feasibility risk: MEDIUM

### Attack path
Reproduce twin fold disagreement beside a healthy steady control, falsify residual-kernel and random-map-IO hypotheses, then reconcile fringe packing, stage authority, and fold order across three roots. The path requires experiments and cross-language model building; no prompt noun, file name, or single failed assertion reveals all three locations.

### Distinctness notes
- vs mesh-checkpoint-operator-skew: remesh+resume shelf reuse across C++/Rust/Fortran vs rank-map fringe×stage×fold across Rust+C only.
- vs amg-coarsen-parity-rift: AMG coarsening hierarchy parity vs domain map-change twin digests.
- vs sparse-jacobian-color-contract: coloring contracts vs partitioned fold checksums after map change.
