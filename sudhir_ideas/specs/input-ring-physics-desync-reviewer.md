### Decision
GO — Attempt 2. Distributed three-location fixed-timestep replay topology across C++ and Rust (`lane/`, `draw/`, `mark/`); symptoms-only instruction; duration-gated long/short matrix; 0 FAIL / 0 WARN evidence.

### Metadata
- Task name: input-ring-physics-desync
- Title: Input Ring Physics Desync
- Category: games
- Languages: [c++, rust]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [deterministic-replay, game-simulation, input-buffer, fixed-timestep, state-digest]
- Milestones: 0

### Investigation profile

Weakness areas (4): long_horizon_debugging (primary), multi_component_reasoning, partial_failures, ambiguous_bug_report.

Causal stages:
1. Characterize long digest-wrong / overlay-green beside short bit-stable control.
2. Correlate traces/metrics/report fields with duration bands.
3. Recover lane-vs-tick consume-boundary disagreement.
4. Recover per-step draw-count mismatch under long traces.
5. Recover seal sample-phase disagreement vs post-apply snapshot.
6. Coordinate three repairs and verify long/short + anti-approximate outcomes.

Evidence surfaces: code, runtime-state, logs, metrics, filesystem.
Competing hypotheses: approximate/nondeterministic integrator; corrupt recorded digests; harness slot mismatch — each with deterministic falsifiers.
Failing scenarios: long same-seed replay; generated long families; approximate shortcuts. Healthy control: short bit-identical replay.
Meaningful-action estimate: 52. Deterministic offline single-container reproduction. Domain: games fixed-timestep deterministic replay — not trivia.

### Discovery budget

- Discovery: Lane slot retirement disagrees with the integrator consume boundary, so long traces accumulate phase error while short controls stay green.
  Planned location: environment/lane/knit.cpp::knit_u
  Why instruction must not reveal it: Naming a ring/lane tick-boundary mismatch would collapse the first diagnosis into a disclosed buffer-index edit.

- Discovery: Fixed-step draw applies a mismatched number of buffered intents per step under long traces, producing digest drift while tick-count overlays remain green.
  Planned location: environment/draw/step.rs::pull_v
  Why instruction must not reveal it: Naming per-step consume count or draw skew would directly expose the Rust repair and convert the task into a recipe.

- Discovery: Seal-side digest samples are taken at a phase that does not match the post-apply body snapshot used for recorded outcomes.
  Planned location: environment/mark/fold.cpp::fold_w
  Why instruction must not reveal it: Naming sample-phase drift or pre-apply hashing would reduce the seal work to a disclosed timing flip.

### Anti-trivialization verdict

| # | Check | Verdict | Reasoning |
| --- | --- | --- | --- |
| 1 | Disclosure-collapse | PASS | Honest long/short contracts do not name which authority is wrong. |
| 2 | Hidden-instance | PASS | Regenerated families, not one hidden corrupt file. |
| 3 | Single-artifact repair | PASS | Three coordinated roots required. |
| 4 | Generalization | PASS | Long/short matrices regenerate beyond named fixtures. |
| 5 | Prompt-honesty | PASS | Symptoms, schema citation, anti-approximate rule; no causes. |
| 6 | Cheating-vs-difficulty | PASS | Anti-cheat is scaffolding; hardness is consume/sample diagnosis. |
| 7 | Mechanical-fix filter | PASS | Not deps/timeouts/reward formatting. |
| 8 | Localized-fix | PASS | Three roots; 4/12 each. |
| 9 | Oracle-locality | PASS | Substantive multi-file edits planned. |
| 10 | Small declarative-cluster | PASS | No table/knob cluster solves it. |
| 11 | Grep-collapse | PASS | Opaque knit_u/pull_v/fold_w paths. |
| 12 | Pre-factored-helper | PASS | Helpers do not mirror prompt nouns. |
| 13 | Recipe-discount | PASS | Fixed-dt / world-hash recipes insufficient. |
| 14 | Security-aura discount | PASS | Games/simulation, not security theater. |
| 15 | Orthogonal-checklist | PASS | One coupled duration-gated invariant. |
| 16 | Harness-discount | PASS | Docker realism ≠ hardness. |
| 17 | One-pass solvability | PASS | Obvious entrypoint does not expose three loci. |
| 18 | Hard-only gate | PASS | Expert-hours multi-root diagnosis; not medium. |
| 19 | Discovery budget test | PASS | Three non-trivial discoveries committed. |
| 20 | Instruction specificity | PASS | symptoms-only. |
| 21 | Topology distribution | PASS | Three topologies × ≥3 locations each. |

### Topology enumeration (3 candidate fix topologies)

1. **topology_a_selected** — lane/knit.cpp::knit_u, draw/step.rs::pull_v, mark/fold.cpp::fold_w. No single location suffices: correct lane can still be drawn wrong; correct draw can still sample wrong; seal-only leaves lane/draw red.
2. **topology_b_lifecycle_chain** — knit_u, retire_x, pull_v, fold_w. Four-stage consume chain; each stage unlocks the next.
3. **topology_c_reduction_convention** — map_y, pull_v, fold_w. Incompatible index/batch/fold conventions under long traces; changing one only moves disagreement.

### Rubric axes

- Verifiable: PASS — programmatic long/short digest and report checks.
- Well-specified: PASS — two readers can grade the same outcomes from the public contract.
- Solvable: PASS — expert-hours on a bounded existing lab.
- Difficult: PASS — residual multi-root diagnosis after honest disclosure.
- Interesting: PASS — paid deterministic-replay work in engines.
- Outcome-verified: PASS — grade results, not oracle shape.

### Hardness axes

- Discover: PASS — lane/draw/sample facts absent from instruction.
- Synthesize: PASS — three roots must coordinate.
- Diagnose: PASS — symptoms only; causes withheld.
- Navigate coupling: PASS — local fixes break distant duration-gated invariants.
- Reason beyond training: PASS — not a textbook fixed-timestep recipe.

### Instruction completeness test

Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction defines observable long/short outcomes and a schema path but does not identify which of the three authorities is inconsistent or how they must coordinate.

## Reviewer Appendix

### Implementation plan

Ship a headless C++/Rust simulation lab that builds and runs offline. Baseline long same-seed replays emit green tick-count overlays while entity-state digests disagree with recorded outcomes; short healthy controls already look bit-stable. The agent must investigate duration-gated behavior across lane, draw, and mark roots, then coordinate repairs so long digests match recorded outcomes without breaking short controls or accepting approximate physics. Hardness is the coupled consume/sample diagnosis, not fixture hunting.

### Proposed file inventory

- environment/Dockerfile, .dockerignore, Makefile, verifier-requirements.txt, conf/runtime.conf
- environment/docs/{architecture,replay-report-schema,data-format}.md
- environment/data/families.trace
- environment/fixtures/logs/run_trace.ndjson, fixtures/traces/alpha.bin
- environment/lane/{knit,ledge,ember}.cpp, lane/include/{knit,common}.h
- environment/draw/{main,step,locker,relay,ffi,report,error,config}.rs
- environment/mark/{fold,tally}.cpp
- environment/core/driver.cpp, core/include/driver.h
- environment/tools/{build_all,run_simlab}.sh
- instruction.md, task.toml, output_contract.toml
- tests/test.sh, tests/test_outputs.py
- solution/solve.sh, construction_manifest.json

≥20 substantive environment files excluding Docker files.

### Oracle notes

solve.sh applies coordinated substantive edits to knit_u (lane-vs-tick boundary), pull_v (per-step draw count), and fold_w (post-apply sample phase), then rebuilds. It does not rewrite recordings or plant golden reports. Ablation of any one location flips only its declared test subset.

### Collapse audit

Stage: implementation-plan

Smallest plausible successful patch:
Coordinated substantive edits to one C++ lane-boundary function, one Rust draw/apply function, and one C++ seal/sample function.

Likely editable frontier:
- lane/knit.cpp
- draw/step.rs
- mark/fold.cpp

Requirement-to-file map:
- long digest parity -> lane + draw + mark coordination
- short control byte identity -> draw/control path with lane/mark non-regression
- anti-approximate -> draw path plus long digest contracts
- report schema fields -> mark fold + report assembly (non-fix glue)

Oracle estimated complexity: >30 lines of non-boilerplate logic across three locations.

Red flags:
- none at plan stage; watch `bin` substring collisions during naming; keep decoys non-fix.

Residual hardness:
After the file tree is visible, the solver must still discover why long traces accumulate consume/sample disagreement across three authorities while short controls stay green, then preserve one duration-gated invariant.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
headless, game, lab, app, inputs, deterministic, replay, live, sessions, seed, entity-state, digests, ticks, tick-count, overlays, healthy-control, bit-stable, pipeline, long, replays, recorded, outcome, short, control, approximate, physics, bin, simlab, output, replay_report, json, keys, layout, schema, docs, replay-report-schema, bundled, report, checks, compiled, healthy, bit-identical, normative

**Renames during drafting:**
- `ring/input_buf.cpp` → `lane/knit.cpp`: removed input/ring vocabulary
- `physics/consume.rs` → `draw/step.rs`: removed physics/consume vocabulary
- `digest/sample.cpp` → `mark/fold.cpp`: removed digest/sample vocabulary
- `advance_tick_ring` → `knit_u`: avoided tick/ring and `bin` substring in bind_*
- `apply_physics_inputs` → `pull_v`: avoided physics/inputs vocabulary
- `hash_entity_state` → `fold_w`: avoided entity/state/digest vocabulary

**Test names audited:**
- test_m01 through test_m12

**Concentration math:**
- Total tests across flipping_point_contract: 12
- Per location:
  - L1 (`lane/knit.cpp`): 4/12 = 0.333
  - L2 (`draw/step.rs`): 4/12 = 0.333
  - L3 (`mark/fold.cpp`): 4/12 = 0.333
- Cap: 0.5. Max ratio observed: 0.333. Status: PASS

### Per-test feasibility pre-check

- Test: test_m01 — Checks long digest vs recorded outcome — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m02 — Checks regenerated long family parity — Valid approaches: 2+ — Chain-dependent: partial on m01 contract — Feasibility risk: LOW
- Test: test_m03 — Checks short control byte identity — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m04 — Checks report digests vs independent fold — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: MEDIUM
- Test: test_m05 — Checks approximate shortcut fails — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m06 — Checks lane+draw interaction on long parity — Valid approaches: 2+ — Chain-dependent: yes on A+B — Feasibility risk: MEDIUM
- Test: test_m07 — Checks overlay coherence does not mask digests — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m08 — Checks post-apply sample phase — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: MEDIUM
- Test: test_m09 — Checks report summary vs digests — Valid approaches: 2+ — Chain-dependent: yes on mark — Feasibility risk: LOW
- Test: test_m10 — Checks reordered long family determinism — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m11 — Checks short control after long families — Valid approaches: 2+ — Chain-dependent: no — Feasibility risk: LOW
- Test: test_m12 — Checks rebuild byte identity of report — Valid approaches: 2+ — Chain-dependent: yes on mark+control — Feasibility risk: MEDIUM
