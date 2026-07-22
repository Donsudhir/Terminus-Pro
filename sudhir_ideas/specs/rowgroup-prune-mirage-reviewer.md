### Decision

GO — Attempt 1. One historical validity authority now drives the producer,
planner, and batch failure chain. Six-scope uniqueness and independent CM-010
semantic review passed before mechanical recording.

### Metadata

- Task name: rowgroup-prune-mirage
- Title: Plan Path Divergence
- Category: data-processing
- Languages: [rust, c++]
- Difficulty: hard
- Codebase size: small
- Subcategories: [tool_specific]
- Tags: [columnar-storage, query-planning, format-evolution, mixed-language]
- Milestones: 0

### Investigation profile

**Weakness areas:** SQL/execution-plan investigation (primary), multi-component
reasoning, partial failures, and recovery from disproven broad workarounds.

**Causal stages:**

1. Reproduce the archived-store discrepancy and establish that repeated runs are
   stable while current-format controls remain healthy.
2. Force selective/full and row/batch combinations. This separates lost-page
   symptoms from invalid-lane symptoms and exposes one interaction case.
3. Inspect checksums, value lanes, validity coverage, stored summaries, and
   page-local coding. Payload integrity survives, falsifying corruption.
4. Ingest generated CSVs and independently parse their artifacts. Repairing the
   producer makes new summaries valid but cannot alter immutable archives.
5. Correlate archived metadata with selective decisions. Align backward-compatible
   admission while preserving real work avoidance on healthy controls.
6. Compare row and batch execution over the same admitted data. The remaining
   disagreement identifies validity-after-selection in one batch kernel.
7. Sweep archived, generated, null-heavy, legitimate-equal-value, dictionary,
   and healthy cases under every mode and repeat byte-for-byte.

**Evidence surfaces:** structured runtime results/work counters; persisted store
artifacts; Rust and C++ code; architecture plus a falsifiable historical note;
built binaries and fresh stores; behavioral verifier cases.

**Competing hypotheses:**

- Archived payload corruption is plausible, but stable checksums and correct
  full-row reads over the same bytes falsify it.
- Mode forcing is broken is plausible, but healthy cases select each requested
  mode and expose the expected pages-read difference while answers agree.
- Cost-model nondeterminism is plausible, but repeated runs choose identical
  modes/counters and wrongness follows generation/mode combinations.

**Conditional matrix:** mixed-generation archives and generated null/legitimate-
equal-value stores fail; current-format sentinel-free and current-format
legitimate-equal-value stores are healthy. Fast-path controls forbid disabling
selective reads or batch execution.

**Action estimate:** 56 meaningful actions, credible range 48–72.

**Determinism:** fixed archives, deterministic CSV generation, fixed page size,
frozen cost policy, sorted traversal, no threads, no clocks, and verifier-owned
expected aggregates in one offline container.

**Domain statement:** this is professional columnar storage/query-engine work.
The solver must reason about format evolution, correctness-bearing summaries,
plan equivalence, execution semantics, and backward compatibility, not recall one
SQL rule or one file-format field.

### Discovery budget

- Discovery: mixed-generation stores retain enough origin/validity evidence to
  distinguish historical placeholders from legitimate equal-valued rows.
  Planned location: archived artifacts, format note, cause-neutral inspect output,
  and C++ decoder.
  Why hidden: naming the representation would collapse the first forensic stage.
- Discovery: fresh summaries are built from value lanes before authoritative
  validity is applied.
  Planned location: `rust/src/ember/fold.rs` and generated artifacts.
  Why hidden: it would identify the producer fix directly.
- Discovery: selective admission consumes archived summaries under the wrong
  generation/page-local domain.
  Planned location: `cpp/src/harbor/veil.cpp`, metadata, and plan counters.
  Why hidden: it would turn plan forensics into a disclosed planner patch.
- Discovery: one batch kernel selects lanes before applying validity.
  Planned location: `cpp/src/lattice/rill.cpp` and row/batch diagnostics.
  Why hidden: it would state the execution fix.

### Anti-trivialization verdict

| Check | Verdict | Reason |
| --- | --- | --- |
| Disclosure-collapse | PASS | Honest commands, schema, and outcomes do not disclose the validity migration. |
| Hidden-instance | PASS | Generated cases require a general contract, not one bad file. |
| Single-artifact repair | PASS | Fresh artifacts, immutable archives, and two execution paths are independently graded. |
| Generalization | PASS | Values, layouts, page boundaries, and predicates vary deterministically. |
| Prompt-honesty | PASS | All operational/output obligations are inline in the instruction. |
| Cheating-vs-difficulty | PASS | Anti-hardcoding protects grading; artifact/plan reasoning remains the real work. |
| Mechanical-fix filter | PASS | Repair is Rust/C++ domain logic, not harness plumbing. |
| Localized-fix | PASS | Three typed authorities each control 5/12 overlapping tests. |
| Oracle-locality | PASS | Genuine 100–150 line semantic delta across three roots. |
| Small declarative cluster | PASS | No version table or policy switch contains the answer. |
| Grep-collapse | PASS | Opaque paths/symbols/tests have no instruction-noun substring hit. |
| Pre-factored helper | PASS | Baseline functions do ordinary production work with non-domain names. |
| Recipe-discount | PASS | Stock null/index/vector recipes do not define the mixed-generation handoff. |
| Security-aura discount | PASS | No security aura is used. |
| Orthogonal-checklist | PASS | All failures are successive consumers of one validity authority. |
| Harness-discount | PASS | Container/matrix provide determinism, not hardness. |
| One-pass solvability | PASS | CLI/report code does not reveal producer/planner/kernel divergence. |
| Hard-only gate | PASS | Senior mixed-language storage diagnosis over a credible long horizon. |
| Discovery budget | PASS | Four non-trivial discoveries have distinct evidence homes. |
| Instruction specificity | PASS | Symptoms-only with minimal operational/schema disclosure. |
| Topology distribution | PASS | Three candidate topologies, each with at least three non-substitutable sites. |

### Topology enumeration (3 candidate fix topologies)

1. **Selected typed pipeline:**
   - `rust/src/ember/fold.rs::tilt_a`
   - `cpp/src/harbor/veil.cpp::turn_b`
   - `cpp/src/lattice/rill.cpp::sweep_c`
   No one location suffices: producer cannot change archives, planner cannot create
   fresh summaries or evaluate lanes, and kernel cannot recover skipped data.
2. **Normalized descriptor:**
   - `rust/src/codec.rs::shape_d`
   - `cpp/src/store.cpp::read_e`
   - `cpp/src/exec.cpp::apply_f`
   Decoder lacks query context, reader lacks lane execution, and executor cannot
   rewrite producer metadata.
3. **Dual-summary provenance:**
   - `rust/src/ember/reed.rs::carry_g`
   - `cpp/src/harbor/index.cpp::choose_h`
   - `cpp/src/lattice/mask.cpp::filter_i`
   Provenance alone cannot choose data, plan metadata cannot enforce validity, and
   a mask cannot repair stored summaries or skipped pages.

### Rubric axes

- **Verifiable — PASS:** exact aggregates, independent artifact parsing, forced
  modes, work counters, and repeated bytes are deterministic.
- **Well-specified — PASS:** rebuild, audit, ingest, report schema, archive
  compatibility, and fast-path outcomes are explicit.
- **Solvable — PASS:** every source, artifact, diagnostic, and dependency is local.
- **Difficult — PASS:** requires separating producer data from consumer semantics
  and coordinating Rust/C++ without broad fallbacks.
- **Interesting — PASS:** plan-dependent financial totals after format migration
  are realistic, high-impact database failures.
- **Outcome-verified — PASS:** verifier grades behavior and artifacts, never source
  text or command history.

### Hardness axes

- **Discover:** plan matrices and artifacts reveal facts absent from the prompt.
- **Synthesize:** producer, persisted representation, planner, and executor must be
  modeled together.
- **Diagnose:** symptoms do not name nulls, summaries, dictionaries, or kernels.
- **Navigate coupling:** each local repair leaves a distinct observed failure and
  broad fallbacks break healthy fast-path controls.
- **Reason beyond training:** the project-specific mixed-generation authority
  cannot be recovered from a generic database recipe.

### Instruction completeness test

No. The instruction is sufficient to run and judge the system, but it does not
identify which representation changed, which summaries are untrustworthy, or why
selective and batch modes fail differently. The repository and runtime must be
investigated.

## Reviewer Appendix

### Implementation plan

Build a compact but realistic custom columnar lab. Rust ingests CSV and compacts
historical/current lanes into a textual-binary store with fixed-size pages,
explicit presence/origin lanes, page-local string dictionaries, and persisted
summary markers. C++ parses case packs, reads stores, chooses selective/full
access, executes row/batch aggregates, and emits JSON with answer plus work
counters. The broken baseline compiles and reports plausible values.

Historical stores include a mixed transition artifact, a current artifact, and a
healthy control. Fresh CSVs allow the public ingest path and verifier-generated
cases. Architecture documentation is accurate at component level; format notes
retain one plausible old assumption that is falsified by current artifacts. No
file tells the solver how to repair the system.

### Proposed file inventory

The exact inventory is committed in the authoring spec. It contains four task
metadata/control files, 41 meaningful environment paths (Rust producer, C++
planner/executor, tools, docs, config, archives/cases/CSV), one oracle script, and
two verifier files. The environment count is comfortably `small`, not padded.

### Oracle notes

`solve.sh` edits only the three committed frontier files. `tilt_a` must derive
summary markers after resolving presence/origin semantics and exclude absent lanes
without discarding legitimate equal-valued data. `turn_b` must interpret archived
markers conservatively under each artifact's local generation/coding authority;
unknown or ambiguous metadata admits the page rather than dropping it. `sweep_c`
must apply validity before predicate selection and aggregation while leaving
legitimate lanes intact. Then rebuild and run the bundled audit.

The oracle must not rewrite archives, alter tests, disable modes, or change report
schema. Scenario values arrive from artifacts and parameters. Expected semantic
delta is 100–150 non-boilerplate lines.

### Collapse audit

Stage: implementation-plan

Smallest plausible successful patch:
A coordinated Rust producer correction plus two C++ consumer corrections in the
three committed functions. A shared helper is a valid alternate design only if
fresh producer output and both consumer call sites adopt it; this still requires
three boundaries.

Likely editable frontier:
- `rust/src/ember/fold.rs`
- `cpp/src/harbor/veil.cpp`
- `cpp/src/lattice/rill.cpp`
- nearby type/codec modules for understanding, not oracle edits

Requirement-to-file map:
- fresh artifact validity -> Rust producer + codec + independent verifier parser
- archived selective correctness -> C++ store reader + planner boundary
- row/batch equivalence -> C++ row reference + batch boundary
- fast-path preservation -> planner/executor work counters + healthy controls
- repeated bytes -> report/digest modules (already healthy)

Oracle estimated complexity: 100–150 substantive changed lines.

Red flags: custom format can become benchmark theater if oversized; keep only
integer/string, count/sum, equality/range/null, fixed pages, and no joins or full
SQL parser. The C++/Rust split must remain failure-bearing, not decorative.

Residual hardness:
Even with the tree visible, the solver must prove payload integrity, distinguish
producer summaries from planner interpretation, preserve immutable archives,
identify the row/batch semantic split, and keep optimized paths active.

Collapse verdict: PASS.

### Naming-pass record

**Instruction nouns extracted:**
finance, support, archived orders, orders, execution modes, execution mode,
modes, mode, totals, system, app, equivalent modes, equivalent mode, same correct
rows, correct rows, rows, same correct totals, correct totals, archived stores,
archived store, stores, store, newly ingested stores, newly ingested store,
selective reads, selective read, batch execution, fast paths, fast path, healthy
cases, healthy case, tools, build-all, rebuild command, command, bin, loam, audit,
case directory, report path, report, UTF-8 JSON, JSON, status, cases, case row,
case, case_id, row_count, sum_amount, pages_total, pages_read, path, skipping,
digest, repeated runs, repeated run, runs, run, fresh inputs, inputs, input,
ingest, CSV, store directory, directory, same contract, archived mixed-generation
stores, archived mixed-generation store, rewriting, work, offline, answers,
answer, behavior, output, use.

**Renames during drafting:**

- `rust/src/pages/stats.rs::build_page_stats` →
  `rust/src/ember/fold.rs::tilt_a`: removed producer intent vocabulary.
- `cpp/src/planner/prune.cpp::admit_page` →
  `cpp/src/harbor/veil.cpp::turn_b`: removed selective-path vocabulary.
- `cpp/src/executor/vector_scan.cpp::scan_batch` →
  `cpp/src/lattice/rill.cpp::sweep_c`: removed batch-kernel vocabulary.
- descriptive verifier names → `test_p01`…`test_p12`: removed mechanism clues.

**Test names audited:**
`test_p01`, `test_p02`, `test_p03`, `test_p04`, `test_p05`, `test_p06`,
`test_p07`, `test_p08`, `test_p09`, `test_p10`, `test_p11`, `test_p12`.

**Concentration math:**

- Total tests: 12
- A (`rust/src/ember/fold.rs`): 5/12 = 0.4166666667
- B (`cpp/src/harbor/veil.cpp`): 5/12 = 0.4166666667
- C (`cpp/src/lattice/rill.cpp`): 5/12 = 0.4166666667
- Cap: 0.5. Max: 0.4166666667. Status: PASS.

### Per-test feasibility pre-check

- Test: `test_p01`
  Checks: generated fresh numeric artifact plus selective-row answer.
  Valid approaches: 2+ (producer repair or equivalent correct artifact creation).
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p02`
  Checks: archived selective-row aggregate plus real work avoidance.
  Valid approaches: 2+ (planner interpretation or safe equivalent admission).
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p03`
  Checks: fresh producer/planner interaction on generated boundaries.
  Valid approaches: 2+.
  Chain-dependent: yes, producer and planner.
  Feasibility risk: MEDIUM.
- Test: `test_p04`
  Checks: archived no-skip batch validity and legitimate equal values.
  Valid approaches: 2+ (kernel order or equivalent lane mask).
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p05`
  Checks: generated null-heavy artifact and batch aggregate.
  Valid approaches: 2+.
  Chain-dependent: yes, producer and batch.
  Feasibility risk: MEDIUM.
- Test: `test_p06`
  Checks: archived selective-batch interaction.
  Valid approaches: 2+.
  Chain-dependent: yes, planner and batch.
  Feasibility risk: MEDIUM.
- Test: `test_p07`
  Checks: fresh mixed-origin compaction across all modes plus artifact parsing.
  Valid approaches: 2+.
  Chain-dependent: no for producer ablation; broad system verification follows.
  Feasibility risk: MEDIUM.
- Test: `test_p08`
  Checks: archived dictionary selective/full row equality and fewer reads.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p09`
  Checks: archived batch range/null agreement with row mode.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p10`
  Checks: generated legitimate placeholder-shaped values remain data.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p11`
  Checks: archived neighboring generations remain selectively readable.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_p12`
  Checks: generated dictionary/null row-batch equality plus healthy batch use.
  Valid approaches: 2+.
  Chain-dependent: no for batch ablation.
  Feasibility risk: MEDIUM.
