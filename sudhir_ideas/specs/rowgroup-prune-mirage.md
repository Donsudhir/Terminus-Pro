### Decision

GO — Attempt 1. The preliminary three-bug sketch was replaced by one historical
validity contract whose producer, planner, and batch consumers are independently
observable and non-substitutable. Six-scope uniqueness and the independent
CM-010 absorption/stage-skipping attack both passed.

### Metadata

- version: 2
- Task name: rowgroup-prune-mirage
- Title: Plan Path Divergence
- Category: data-processing
- Languages: [rust, c++]
- Difficulty: hard
- Codebase size: small
- Subcategories: [tool_specific]
- Tags: [columnar-storage, query-planning, format-evolution, mixed-language]
- Milestones: 0

## Authoring Brief

### Public contract

Present an existing offline data system under `/app` where the same archived
orders produce different totals under supported execution modes. The solver must
rebuild the system, make equivalent modes return the same correct rows and totals
for archived and newly ingested stores, preserve repeatable report bytes, and
keep selective reads plus batch execution active on healthy cases. One public
end-to-end audit command writes a concise JSON report; one public ingest command
creates a fresh store. Archived mixed-generation stores remain readable without
rewriting them.

The eventual instruction should use a human incident-report voice. It must name
`/app/tools/build-all`, the bundled invocation `/app/bin/loam audit
/app/data/cases /app/output/audit.json`, the generalized
`/app/bin/loam audit <case-directory> <report-path>`, and
`/app/bin/loam ingest <CSV> <store-directory>`. The instruction names top-level
`status` (`complete`), `cases`, and `digest`; the existing public report stub
grounds each per-case answer/work field without turning the instruction into a
dense schema recital. These are operational/output contracts, not a description
of the diagnosis.

### Failure topology

One historical storage transition separated validity from value bytes while
retaining backward-compatible payloads. The Rust producer, C++ selective
planner, and one C++ batch kernel each preserve a different partial assumption
about the old representation. Mixed-generation stores therefore lose rows in a
selective plan, leak invalid lanes in a batch plan, or expose both effects.
Current-format controls stay healthy.

The producer boundary is required because fresh stores must persist internally
valid summaries inspected independently by the verifier. The planner boundary
is required because immutable archived stores cannot be regenerated. The batch
boundary is required because pages admitted correctly can still produce the
wrong aggregate. Broad full-scan or row-only repairs fail healthy controls that
require real work avoidance and batch selection.

### Investigation architecture

Use four reinforcing weakness areas: SQL/execution-plan investigation,
multi-component reasoning, partial failures, and recovery from an initially
plausible broad workaround. The causal progression is: reproduce the conditional
incident; split it by selective/full and row/batch modes; inspect stable payload,
validity, and summary artifacts; repair and independently validate fresh producer
output; align archived selective admission; align batch-lane semantics; sweep the
archive/generated/healthy matrix. Evidence spans runtime reports and work
counters, persisted filesystem artifacts, source, historically stale format
notes, and mixed-language build artifacts.

Random payload corruption, broken plan forcing, and nondeterministic costing are
plausible but deterministically falsifiable. The failing cases cross the format
transition; current-format sentinel-free and legitimate-equal-value stores are
healthy controls. Fixed page sizes, sorted inputs, frozen costing, no clocks, and
no threads keep the 48–72 meaningful-action investigation repeatable.

### Environment shape

- A Rust producer/compactor writes the small versioned columnar artifact.
- A C++ query binary reads stores, selects pages, executes row or batch modes,
  and emits structured audit rows and work counters.
- Archived stores cover historical, current, and healthy generations.
- Fresh CSV inputs exercise null-heavy, legitimate-equal-value, and dictionary
  cases through the public ingest surface.
- Architecture notes describe component responsibilities. One old format note
  contains a plausible historical assumption that runtime artifacts can falsify;
  it is not an instruction or solution hint.
- The complete system builds with local standard-library Rust/C++ toolchains and
  runs offline in one container.

### Required artifacts

Create a standard single-step task with `instruction.md`, `task.toml`, local-only
`output_contract.toml` and `construction_manifest.json`, a digest-pinned
`environment/Dockerfile`, required `environment/.dockerignore`, the complete
small codebase below, `solution/solve.sh`, and a CM-007-hardened pytest verifier.
The environment must contain at least 20 meaningful non-Docker files and no
answer-shaped reference output, AI scaffolding, runtime installs, or generated
build directories.

### Test plan

1. `test_p01`: generated fresh numeric input produces independently valid
   persisted summaries and correct selective-row answers; multiple internal
   representations are allowed; not chain-dependent.
2. `test_p02`: an archived mixed-generation range case returns the verifier-owned
   aggregate with selective row execution and still skips work; not chain-dependent.
3. `test_p03`: a generated interaction case remains correct after ingest and
   selective execution; depends on producer plus planner behavior.
4. `test_p04`: an archived no-skip batch equality case excludes invalid lanes
   while preserving legitimate equal-valued rows; not chain-dependent.
5. `test_p05`: a generated null-heavy batch case has valid persisted summaries
   and correct batch output; depends on producer plus batch behavior.
6. `test_p06`: an archived selective-batch interaction returns the correct
   aggregate; depends on planner plus batch behavior.
7. `test_p07`: fresh mixed-origin compaction remains correct across all four
   modes and its artifact passes independent parsing; producer ablation flips it.
8. `test_p08`: archived dictionary pages return equal answers under selective and
   full row modes while selective mode reads fewer pages; planner ablation flips it.
9. `test_p09`: archived batch range and null predicates agree with row execution;
   batch ablation flips it.
10. `test_p10`: generated legitimate historical-placeholder-shaped values remain
    data in fresh stores while summaries stay valid; producer ablation flips it.
11. `test_p11`: archived generation-neighbor cases remain selectively readable
    with correct page-local ordering interpretation; planner ablation flips it.
12. `test_p12`: generated dictionary/null interaction agrees across row and batch
    modes while healthy batch controls remain selected; batch ablation flips it.

Every scored function must combine its failing assertion with a healthy fast-path
or generalization assertion so the untouched baseline cannot pass a test merely
because one control is already healthy. Tests derive expected aggregates from
verifier-owned generated inputs or embedded immutable expectations and never
trust self-reported `status` alone.

### Drafting guardrails

Do not use `null`, `sentinel`, `bitmap`, `min`, `max`, `bound`, `dictionary`,
`prune`, `vector`, `stats`, `page`, or format-generation vocabulary in the public
instruction. Do not place those public incident nouns in fix-path symbols. Keep
artifact-inspection tools cause-neutral, avoid comments that explain intent on
the oracle frontier, and do not make the stale format note a treasure map.

### Construction Amendment 1 (2026-07-19, pre-gate)

The first static/collapse run found that enumerating every per-case JSON field in
the instruction made RC6 classify the otherwise symptoms-only incident as
spec-complete. Preserve instruction honesty by naming the exact bundled output
path and the top-level report fields/status inline, while grounding stable
per-case fields in the existing public report/type stubs. This does not remove or
hide any tested contract. The instruction noun audit also adds `output` and
`use`; neither appears in a fix-path symbol, parameter, or path. No file or
selected topology changes.

### Construction Amendment 2 (2026-07-20, REV-3 platform QC)

Platform QC failed `behavior_in_task_description`, `structured_data_schema`, and
`file_reference_mentioned` because Construction Amendment 1 left per-case fields
and `data.store` only in code stubs / lagging format notes. REV-3 restores
instruction honesty for the *output* contract without answer-shaped tallies:

- `instruction.md` names every graded JSON key inline (no dense backtick schema
  cluster — keeps RC6 symptoms-only) and names `<store-directory>/data.store`.
- Normative `/app/docs/report-schema.md` is the grading reference for those keys,
  marker semantics (`low` / `high` / `has_absent`), and ingest artifact naming.
- One clarifying symptom sentence covers incomplete markers and varied origin
  lanes across selective vs batch paths (reviewer warning).
- Do not embed fixture-specific expected aggregates in the instruction.
- Base image remains the sanctioned canonical GCC 13 bookworm digest (C/C++
  family); Rust/Cargo stay apt-pinned on that image for the dual-language lab.

### Construction Amendment 3 (2026-07-21, REV-4 platform difficulty TRIVIAL)

Platform difficulty run (submission `fac356b4`) rated the REV-3 zip TRIVIAL:
terminus-claude-opus-4-8 and terminus-gpt5-5 both 5/5, oracle 3/3, NOP 0/1.
CM-008 hardening applied; instruction.md text is unchanged (QC-passing REV-3
wording is preserved verbatim):

- **Breadcrumb removal.** `Slab.markers_complete` (computed in `store.cpp`,
  consumed by nothing solver-visible) is deleted; the generation→marker-trust
  model must now be reconstructed from artifact forensics. The
  `architecture.md` sentence stating the conservative-skip rule ("avoiding a
  read is allowed only when the marker proves that the slab cannot contribute")
  is deleted as a solution giveaway.
- **Sibling-oracle removal for the batch kernel.** `store.cpp` now also
  populates per-slab column lanes (`amount_lane`, `presence_lane`,
  `origin_lane`, `region_lane`) and `lattice/rill.cpp` is restructured as a
  lane/mask kernel (admission mask + lane accumulation). The planted defect is
  unchanged in meaning (mask built from the presence lane only) but the fix is
  no longer a one-glance copy of `row.cpp::is_live`; it requires translating
  the liveness rule into mask algebra. `row.cpp` is untouched.
- **New archived incident artifact `data/archive/vault.store`.** Mixed header
  generation (2/3/2). Page 0 is generation 2 with stale `has_absent=0` (an
  origin-blind old writer saw only the presence lane, so a retired-origin row
  is invisible in the flag) and stale text markers (`north|west` while rows
  carry `east`). This breaks the "trust generation-2 markers when
  has_absent=0" model the REV-3 oracle rewarded; the correct gate must treat
  all generation<3 markers as unverifiable (legacy-open). Four cause-neutral
  drill lines are appended to `data/cases/incident.case` so the selective vs
  full and row vs batch divergence is reproducible on the bundled drill.
- **Producer edge semantics.** `report-schema.md` gains the all-non-live slab
  convention (`low` 0, `high` 0, `has_absent` true). New agent-visible practice
  CSV `data/fresh/orders_c.csv` contains an all-non-live chunk and a
  placeholder-valued (`-999`) live row.
- **Three new tests.** `test_p13` (isnull with skipping on vault, row and batch
  lanes agree, pages_read < pages_total — flips B and C), `test_p14`
  (region_eq with skipping on vault, stale gen-2 text markers — flips B),
  `test_p15` (verifier-owned gamma CSV with all-non-live chunk and live -999:
  exact markers, range/eq/isnull consistency and skipping — flips A and C).
  Flipping contract updated: A {p01,p03,p05,p07,p10,p15}, B
  {p02,p03,p06,p08,p11,p13,p14}, C {p04,p05,p06,p09,p12,p13,p15}; max
  concentration 7/15 ≤ 0.5.
- **Oracle.** `veil.cpp` gate now derives trust from `generation < 3`
  (legacy-open) instead of the removed `markers_complete`; unknown-text /
  unknown-range and range normalization retained; `rill.cpp` oracle builds the
  admission mask from origin+presence lanes in the same kernel style.
- Inventory additions: `environment/data/archive/vault.store`,
  `environment/data/fresh/orders_c.csv`.

### Triviality Ledger

- **Disable selective reads:** blocked because healthy cases must report fewer
  pages read than the full control while returning the same verifier-owned answer.
- **Disable batch execution or delegate everything to row mode:** blocked because
  healthy large cases must report the batch path selected and generated batch
  cases are independently checked.
- **Rewrite archived stores:** blocked because tests hash and reset immutable
  archives before each case and fresh producer artifacts are checked separately.
- **Fix only the producer:** blocked because archived stores remain unchanged and
  selective/batch failures survive.
- **Fix only the planner:** blocked by independent fresh-artifact validation and
  no-skip batch cases.
- **Fix only the batch kernel:** blocked because skipped pages never reach it and
  fresh summaries remain invalid.
- **Treat every historical-placeholder-shaped value as absent:** blocked by
  current-format and generated legitimate-equal-value controls.
- **Hardcode bundled answers:** blocked by deterministic generated CSV values,
  arrangements, page boundaries, and predicates owned by the verifier.

### Per-gate Pitfall Inventory

- **RC1:** avoid deletion/revert solutions; each selected function must add real
  generation-aware or validity-aware logic.
- **RC2:** use the committed opaque paths/symbols/test names; no `broken`, `buggy`,
  `expected`, or incident vocabulary on solver-visible paths.
- **RC3:** assert exact domain aggregates, independently parsed artifact semantics,
  and stable work counters, never mere report existence/schema.
- **RC4:** expected aggregates and generated inputs are verifier-owned; do not read
  answer values from agent-editable environment files.
- **RC5:** archived stores are incident artifacts, not golden outputs; no correct
  report or repaired store may exist under `environment/`.
- **RC6:** instruction stays symptoms-only; command/schema disclosure is limited
  to the honest operational contract.
- **RC7:** genuine three-location semantic delta targets 100–150 lines; do not pad.
- **CR1/CR3/CR7:** follow the symbol table verbatim and keep one-letter parameters.
- **CR2:** verify the exact overlapping 5/12 ablation subsets after the oracle.
- **CR4:** scenario-controlled values arrive from artifacts/parameters, never
  appear as fix-path literals.
- **CR5/CR6:** decoys do real telemetry/report work; fix files have mechanics-only
  comments and no near-duplicate bodies.
- **CR8:** no visible file may call/import all three selected symbols; Rust and
  C++ orchestration stay naturally separated.
- **CR9:** every asserted report field/value has a home in the instruction or an
  existing public stub; no hidden output schema.
- **GX1/GX3:** tests execute the built system and independently parse artifacts;
  they do not inspect source or accept self-reported success.
- **GX9/GX10:** instruction does not enumerate scenario answers or place opposite
  plan/health polarities in one ambiguous sentence.
- **Static checks:** standard layout, anonymous metadata, offline flag, pinned
  Docker dependencies, `.dockerignore`, absolute paths, CM-007 pytest triad, LF
  scripts, and no runtime installation.

### Initial Draft Commitments

Task-root inventory (no additional path without spec amendment):

- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `construction_manifest.json`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Makefile`
- `environment/config/lab.conf`
- `environment/docs/architecture.md`
- `environment/docs/format-notes.md`
- `environment/tools/build-all`
- `environment/tools/reset-lab`
- `environment/rust/Cargo.toml`
- `environment/rust/src/main.rs`
- `environment/rust/src/model.rs`
- `environment/rust/src/codec.rs`
- `environment/rust/src/report.rs`
- `environment/rust/src/ember/mod.rs`
- `environment/rust/src/ember/fold.rs`
- `environment/rust/src/ember/reed.rs`
- `environment/rust/src/ember/pale.rs`
- `environment/cpp/Makefile`
- `environment/cpp/include/loam/types.hpp`
- `environment/cpp/include/loam/store.hpp`
- `environment/cpp/include/loam/plan.hpp`
- `environment/cpp/include/loam/exec.hpp`
- `environment/cpp/include/loam/report.hpp`
- `environment/cpp/src/main.cpp`
- `environment/cpp/src/store.cpp`
- `environment/cpp/src/parse.cpp`
- `environment/cpp/src/row.cpp`
- `environment/cpp/src/report.cpp`
- `environment/cpp/src/digest.cpp`
- `environment/cpp/src/harbor/veil.cpp`
- `environment/cpp/src/harbor/pale.cpp`
- `environment/cpp/src/lattice/rill.cpp`
- `environment/cpp/src/lattice/bay.cpp`
- `environment/data/archive/mixed.store`
- `environment/data/archive/current.store`
- `environment/data/archive/healthy.store`
- `environment/data/archive/vault.store`
- `environment/data/cases/incident.case`
- `environment/data/cases/control.case`
- `environment/data/fresh/orders_a.csv`
- `environment/data/fresh/orders_b.csv`
- `environment/data/fresh/orders_c.csv`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/test_outputs.py`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

- path: rust/src/ember/fold.rs
  symbol: tilt_a
  kind: function
  signature: `pub(crate) fn tilt_a(a: &[i64], b: &[u8], c: &[u8]) -> Result<Mark, FoldErr>`
  purpose: Builds one persisted marker set from value, presence, and origin lanes.
- path: cpp/src/harbor/veil.cpp
  symbol: turn_b
  kind: function
  signature: `Gate turn_b(const Slab& a, const Probe& b)`
  purpose: Decides whether one stored slab can contribute to one probe.
- path: cpp/src/lattice/rill.cpp
  symbol: sweep_c
  kind: function
  signature: `Tally sweep_c(const Slab& a, const Probe& b, const Gate& c)`
  purpose: Evaluates selected lanes in one batch and accumulates its tally.

#### flipping_point_contract

```yaml
locations:
  - id: A
    path: rust/src/ember/fold.rs
    controls_tests: [test_p01, test_p03, test_p05, test_p07, test_p10, test_p15]
  - id: B
    path: cpp/src/harbor/veil.cpp
    controls_tests: [test_p02, test_p03, test_p06, test_p08, test_p11, test_p13, test_p14]
  - id: C
    path: cpp/src/lattice/rill.cpp
    controls_tests: [test_p04, test_p05, test_p06, test_p09, test_p12, test_p13, test_p15]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

- path: rust/src/ember/pale.rs
  kind: helper
  rhymes_with: tilt_a
  non_fix_purpose: `tilt_d` summarizes operator telemetry from completed artifact jobs without reading persisted value lanes.
- path: cpp/src/harbor/pale.cpp
  kind: helper
  rhymes_with: turn_b
  non_fix_purpose: `turn_d` classifies display-only diagnostic rows for the human plan report.
- path: cpp/src/lattice/bay.cpp
  kind: helper
  rhymes_with: sweep_c
  non_fix_purpose: `sweep_e` aggregates already-computed timing and work counters for status output.

#### code_forbidden_tokens

```text
[finance, support, archived orders, orders, execution modes, execution mode,
modes, mode, totals, system, app, equivalent modes, equivalent mode,
same correct rows, correct rows, rows, same correct totals, correct totals,
archived stores, archived store, stores, store, newly ingested stores,
newly ingested store, selective reads, selective read, batch execution,
fast paths, fast path, healthy cases, healthy case, tools, build-all,
rebuild command, command, bin, loam, audit, case directory, report path,
report, UTF-8 JSON, JSON, status, cases, case row, case, case_id, row_count,
sum_amount, pages_total, pages_read, path, skipping, digest, repeated runs,
repeated run, runs, run, fresh inputs, inputs, input, ingest, CSV,
store directory, directory, same contract, archived mixed-generation stores,
archived mixed-generation store, rewriting, work, offline, answers, answer,
behavior, output, use]
```
