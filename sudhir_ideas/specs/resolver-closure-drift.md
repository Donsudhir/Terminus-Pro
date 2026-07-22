### Decision
GO — Attempt 2.

- Replaced the formatter side issue with one history-led policy incident whose stable bytes come from semantic graph commitment.
- Replaced duplicate candidate-list signatures with three information-narrowing typed authorities.
- Made the public contract operationally complete and committed a real two-parent history plus compilable offline package payloads.

### Metadata
- version: 2
- Task name: resolver-closure-drift
- Title: Resolver Closure Drift
- Category: build-and-dependency-management
- Languages: [rust, python]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [dependency-resolution, semantic-merge, reproducible-builds, git-history, transitive-closure]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. The public prose, typed construction manifest, history DAG, file inventory, and overlapping ablations are binding. Any change to them requires a Step 2a amendment.

### Public contract

Use these two paragraphs verbatim as `instruction.md`:

The dependency workspace is `/app/repo`. After changing its source, run `/app/bin/rebuild-forge`; this rebuild command installs the edited binary at `/app/bin/forge`. The single supported entrypoint is `/app/bin/forge solve /app/projects/workspace.toml`. It writes `/app/output/workspace.lock` as UTF-8 text. Each lock line is `<name> <version> <source-id>` with one ASCII space between fields. Lines use ascending bytewise `(name, version, source-id)` tuple order, contain no duplicate tuples, and end with one final newline.

For every bundled project and nearby generated input, the dependency set must satisfy all declared direct and transitive requirements and complete the bundled downstream build. Equivalent package archive orderings and clean repeated runs must produce byte-identical lockfiles. Preserve both established edge-case behaviors relied on by existing consumers; committed parent checks and release notes in the repository history define their expected selections independently without describing the merged failure. A valid repair must also handle new package names and ranges created by the checks. Keep all work offline, use bundled data, and make no network requests. Do not replace project inputs or write the lockfile by hand; the checks rebuild and run the tool from clean state.

The corresponding local `output_contract.toml` is precommitted as:

- `user_visible_outputs = ["/app/output/workspace.lock"]`
- `internal_harness_files = ["/app/output/resolve.log", "/app/output/build-report.json"]`
- `structured_outputs.lock.target = "/app/output/workspace.lock"`
- `structured_outputs.lock.format = "utf8-line-records"`
- `structured_outputs.lock.instruction_checks = ["<name> <version> <source-id>", "ASCII space", "ascending bytewise", "no duplicate tuples", "one final newline"]`

### Failure topology

The reconstructed repository has a common base, two sibling feature parents, a true two-parent merge, and a current child. Each parent introduces a legitimate package-selection behavior with an exact expected selection documented by a branch-local check and release note. Both parent projects remain healthy. The merge fails only when one project activates both contracts across a transitive dependency graph.

The incident crosses three information-narrowing authorities. A converts raw package and request evidence into a constrained type but has no policy state. B consumes that constrained type plus policy state and emits an immutable accepted decision but cannot recover raw evidence. C receives a complete graph of accepted decisions and root intent, validates edge closure, and commits semantic identity and deterministic traversal into a `Trellis`; it has neither raw records nor policy state. The existing writer merely serializes `Trellis` in the public line format. Thus byte stability is a consequence of correct semantic closure identity, not a separate formatter repair.

### Investigation architecture

The selected weakness areas are Git/history reasoning (primary), multi-component reasoning, and recovery from partial diagnoses. The dependent seven-stage progression is:

1. Reproduce the merged-only build and byte symptoms while both parent controls remain healthy.
2. Inspect the real sibling-parent DAG and recover each exact compatibility contract.
3. Replay base, both parents, the two-parent merge, and current child to prove composition is the first semantic failure.
4. Compare cause-neutral traces to locate raw-context loss and traversal identity entering the graph.
5. Use partial runs to prove A lacks policy state and B lacks discarded raw evidence, forcing a typed handoff.
6. Commit the admitted graph under semantic identity so the same policy incident yields one complete buildable closure and one byte representation.
7. Verify parent controls, cross cases, generated neighbors, deterministic permutations, clean rebuilds, and actual offline payload compilation.

Evidence spans Git history, committed documentation, traces, current Rust code, lock/build artifacts, and behavioral checks. Competing hypotheses are a writer-only bug, a bad parent that should be reverted, and damaged archive content; each has a deterministic falsifier. The meaningful-action estimate is 46. No command history or investigative tool is graded.

### Environment shape

- `bootstrap/base/` is a compilable Rust resolver with healthy parsing, range handling, CLI dispatch, lock-line writing, tracing, and downstream workspace assembly.
- `bootstrap/history/descriptors/` declares commit identity, fixed author/time/message, and explicit parent arrays. Alpha and beta both name base; merge names alpha and beta; current names merge.
- `bootstrap/history/patches/` contains deterministic unified patches. Alpha and beta each add one feature, one exact parent check, and one release note. Merge contains only the integration tree needed to combine both parents and preserve their artifacts; current adds the combined fixture and neutral cleanup.
- `bootstrap/rebuild_repo.py` validates the DAG, applies patches in topological order, creates commits with `git commit-tree`, verifies the merge has two parents, and installs branch refs plus current `HEAD`.
- `archive/` contains manifests and substantive Rust crate payloads. The downstream builder assembles the selected payloads into a clean Cargo workspace and runs `cargo build --offline --locked`; metadata-only proxies are forbidden.
- `src/aero/`, `src/cairn/`, and `src/quill/` contain the selected typed authorities and one real decoy each.
- `src/store/`, `src/model/`, `src/graph/`, `src/cli/`, `src/build/`, and `src/wire/` provide healthy surrounding machinery.
- `projects/` contains ordinary, alpha, beta, combined, archive-permutation, and transitive-build projects with neutral names.
- The Docker build reconstructs `/app/repo/.git`, installs `/app/bin/forge` and `/app/bin/rebuild-forge`, stages `/app/archive` and `/app/projects`, and removes descriptor material from the runtime filesystem. No `.git` metadata ships in the task archive.

### Required artifacts

Create a standard single-step, single-container, non-UI, offline task with `instruction.md`, `task.toml`, local-only `output_contract.toml`, local-only `construction_manifest.json`, `environment/Dockerfile`, `environment/.dockerignore`, the committed environment inventory below, `tests/test.sh`, `tests/test_outputs.py`, and `solution/solve.sh`.

`task.toml` uses `version = "2.0"`, anonymous author fields, `difficulty = "hard"`, `category = "build-and-dependency-management"`, `languages = ["rust", "python"]`, `codebase_size = "small"`, `number_of_milestones = 0`, `allow_internet = false`, and coherent timeouts no greater than 1800 seconds. The Dockerfile pins every base stage by digest, installs all verifier tools at build time, and verifies the final Python/asciinema environment after any path changes.

`/app/bin/rebuild-forge` must rebuild `/app/repo` and atomically install the resulting binary at `/app/bin/forge`; it takes no network action. Tests invoke this command after source edits. The healthy lock writer accepts only `Trellis` and emits the public schema without policy logic.

### Test plan

Create exactly twelve pytest functions with the following names and behavior. Every function creates isolated inputs and output directories, invokes `/app/bin/rebuild-forge`, runs the one documented entrypoint, parses the public line format, and uses immutable expectations embedded in test code or independently computed from project manifests and package payloads. Historical exact values must also appear in their corresponding committed parent check/note, but verifier expectations must not be read from agent-writable files.

1. `test_r01` — Assert alpha’s uniquely documented parent selection, direct/transitive requirements, and real payload build. Valid approaches: 2+. Chain-dependent: no. Controlled by A only.
2. `test_r02` — Assert beta’s uniquely documented parent selection, direct/transitive requirements, and real payload build. Valid approaches: 2+. Chain-dependent: no. Controlled by B only.
3. `test_r03` — Exercise the smallest merged interaction and require both parent outcomes plus a complete payload build. Valid approaches: 2+. Chain-dependent: self-contained A+B cross test.
4. `test_r04` — Generate nearby source/request combinations and require correct constrained classification without a merged-policy shortcut. Valid approaches: 2+. Chain-dependent: no. Controlled by A only.
5. `test_r05` — Directly satisfy the public archive-order requirement: fixed equivalent archive-record permutations must produce byte-identical public files and buildable closures. Valid approaches: 2+. Chain-dependent: no. Controlled by C only.
6. `test_r06` — Run a fixed sequence of clean, semantically equivalent invocations and require identical bytes and one final newline. Valid approaches: 2+. Chain-dependent: no. Controlled by C only.
7. `test_r07` — Generate direct-request boundaries and verify the classifier preserves the distinctions consumed downstream without asserting implementation shape. Valid approaches: 2+. Chain-dependent: no. Controlled by A only.
8. `test_r08` — Pair one supported beta case with nearby excluded cases so broad admission fails. Valid approaches: 2+. Chain-dependent: no. Controlled by B only.
9. `test_r09` — Permute root declarations and traversal seeds while requiring one semantic tuple set, one order, and identical bytes. Valid approaches: 2+. Chain-dependent: no. Controlled by C only.
10. `test_r10` — Generate graphs where raw classification changes a transitive node’s semantic identity and require deterministic complete closure. Valid approaches: 2+. Chain-dependent: self-contained A+C cross test.
11. `test_r11` — Generate a policy-sensitive transitive selection whose wrong admitted node has an incompatible Rust API; require exact closure and actual offline Cargo success. Valid approaches: 2+. Chain-dependent: self-contained B+C cross test.
12. `test_r12` — Generate beta-side policy frames over several names and ranges and require the documented behavior only in its valid context. Valid approaches: 2+. Chain-dependent: no. Controlled by B only.

The overlapping flipping memberships are:

- A: `test_r01`, `test_r03`, `test_r04`, `test_r07`, `test_r10`.
- B: `test_r02`, `test_r03`, `test_r08`, `test_r11`, `test_r12`.
- C: `test_r05`, `test_r06`, `test_r09`, `test_r10`, `test_r11`.

The union is twelve tests and each location controls `5/12 = 0.4166666666666667`, below the cap `0.5`. `test_r03` is the A+B overlap, `test_r10` the A+C overlap, and `test_r11` the B+C overlap. Reverting a location must flip its declared five tests; overlaps are expected to flip under either participating reversion.

### Drafting guardrails

Do not place the merged diagnosis in instructions, fixture names, test names, current comments, commit messages, or traces. Parent checks and notes must state their own exact selection and rationale independently; neither may mention the sibling policy or future merge. The verifier may embed those exact values because they have an honest historical home, but it must not implement the merged policy as a test-side oracle. Do not read expected results from mutable environment files. Do not add a second entrypoint, hidden output field, provenance record, process requirement, expected lockfile, or source-inspection assertion.

### Triviality Ledger

- **Revert alpha or beta:** blocked by `test_r01` and `test_r02`, each backed by its sibling-parent history.
- **Implement all policy in A:** impossible without `PolicyFrame`; generated beta and negative-neighbor cases fail.
- **Implement all policy in B:** impossible because B receives `Vane`, not `RawRecord` or `QueryFrame`; discarded context cannot be recovered.
- **Implement all policy in C:** impossible because C sees only `Cairn<Admitted>` and `Wick`; parent classification and eligibility decisions are no longer available.
- **Sort output bytes only:** the writer already emits `Trellis`; wrong admitted graph membership still fails cross cases and real payload compilation.
- **Hardcode bundled projects:** blocked by generated names, ranges, graph edges, policy frames, archive permutations, and real crate payload builds.
- **Copy expectations from history into a table:** parent values alone do not determine the merged rule; cross and neighboring cases require general typed composition.
- **Pad the oracle:** forbidden. The 95-130 changed lines are required validation, conversion, policy reconciliation, edge validation, semantic deduplication, and deterministic graph commitment inside the three declared symbols.

### Per-gate Pitfall Inventory

- **RC1 — Oracle simplification:** preserve both parent contracts with additive typed reconciliation; no revert, delete, or old-tree reset.
- **RC2 — Oracle predictability:** use only committed opaque paths/symbols/test names and cause-neutral traces; parent artifacts describe outcomes, not the merged seam.
- **RC3 — Verifier shallowness:** parse every public line, derive requirements, build selected payload crates, verify parent values, and compare deterministic semantic/byte outcomes.
- **RC4 — Tamper surface:** keep expected parent selections in verifier code and independently in Git history; never load verifier expectations from editable notes, manifests, or lockfiles.
- **RC5 — Reference artifacts:** ship no final lockfile, merged-answer patch, expected graph, or answer commit.
- **RC6 — Instruction specificity:** preserve the exact public paragraphs; the line schema and rebuild command are operational contracts, while all diagnostic causes remain absent.
- **RC7 — Oracle triviality:** require 95-130 genuine changed lines across three exact symbols; stop and reopen Step 2a if real GX3 edit distance is below 80.
- **GX1 — Comment leakage:** no correctional or intent comments near changed lines; mechanics-only comments are allowed.
- **GX3 — Edit distance:** count comment-stripped semantic additions/removals only; no whole-file, whitespace, marker, or no-op inflation.
- **GX9 — Contract saturation:** public prose states properties and format, not scenario/version answer triples; exact parent values live in separate parent history and verifier code.
- **GX10 — Polarity contradiction:** do not place opposing status words for one scenario in the same public scope.
- **Static checks:** use anonymous v2 metadata, the declared output contract, absolute paths, CM-007-safe pytest invocation, offline dependencies, `.dockerignore`, digest-pinned images, LF scripts, and resolved Docker copies.

### Initial Draft Commitments

No path outside this list may be added without amending Step 2a.

- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `construction_manifest.json`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Makefile`
- `environment/verifier-requirements.txt`
- `environment/bin/rebuild-forge`
- `environment/bootstrap/rebuild_repo.py`
- `environment/bootstrap/history/descriptors/base.json`
- `environment/bootstrap/history/descriptors/alpha.json`
- `environment/bootstrap/history/descriptors/beta.json`
- `environment/bootstrap/history/descriptors/merge.json`
- `environment/bootstrap/history/descriptors/current.json`
- `environment/bootstrap/history/patches/alpha.patch`
- `environment/bootstrap/history/patches/beta.patch`
- `environment/bootstrap/history/patches/merge.patch`
- `environment/bootstrap/history/patches/current.patch`
- `environment/bootstrap/base/Cargo.toml`
- `environment/bootstrap/base/Cargo.lock`
- `environment/bootstrap/base/src/main.rs`
- `environment/bootstrap/base/src/lib.rs`
- `environment/bootstrap/base/src/model/mod.rs`
- `environment/bootstrap/base/src/model/raw.rs`
- `environment/bootstrap/base/src/model/frame.rs`
- `environment/bootstrap/base/src/model/vane.rs`
- `environment/bootstrap/base/src/model/admitted.rs`
- `environment/bootstrap/base/src/model/cairn.rs`
- `environment/bootstrap/base/src/model/trellis.rs`
- `environment/bootstrap/base/src/aero/mod.rs`
- `environment/bootstrap/base/src/aero/veil.rs`
- `environment/bootstrap/base/src/aero/pale.rs`
- `environment/bootstrap/base/src/cairn/mod.rs`
- `environment/bootstrap/base/src/cairn/sill.rs`
- `environment/bootstrap/base/src/cairn/rill.rs`
- `environment/bootstrap/base/src/quill/mod.rs`
- `environment/bootstrap/base/src/quill/quay.rs`
- `environment/bootstrap/base/src/quill/bay.rs`
- `environment/bootstrap/base/src/store/mod.rs`
- `environment/bootstrap/base/src/store/catalog.rs`
- `environment/bootstrap/base/src/store/payload.rs`
- `environment/bootstrap/base/src/graph/mod.rs`
- `environment/bootstrap/base/src/graph/walk.rs`
- `environment/bootstrap/base/src/cli/mod.rs`
- `environment/bootstrap/base/src/cli/session.rs`
- `environment/bootstrap/base/src/build/mod.rs`
- `environment/bootstrap/base/src/build/workspace.rs`
- `environment/bootstrap/base/src/wire/mod.rs`
- `environment/bootstrap/base/src/wire/lock.rs`
- `environment/bootstrap/base/src/trace.rs`
- `environment/bootstrap/base/docs/architecture.md`
- `environment/bootstrap/base/conf/defaults.toml`
- `environment/bootstrap/base/archive/catalog.json`
- `environment/bootstrap/base/archive/alder/1.0.0/Cargo.toml`
- `environment/bootstrap/base/archive/alder/1.0.0/src/lib.rs`
- `environment/bootstrap/base/archive/alder/1.1.0-alpha.1/Cargo.toml`
- `environment/bootstrap/base/archive/alder/1.1.0-alpha.1/src/lib.rs`
- `environment/bootstrap/base/archive/alder/1.1.0/Cargo.toml`
- `environment/bootstrap/base/archive/alder/1.1.0/src/lib.rs`
- `environment/bootstrap/base/archive/birch/2.0.0/Cargo.toml`
- `environment/bootstrap/base/archive/birch/2.0.0/src/lib.rs`
- `environment/bootstrap/base/archive/birch/2.1.0/Cargo.toml`
- `environment/bootstrap/base/archive/birch/2.1.0/src/lib.rs`
- `environment/bootstrap/base/archive/cedar/3.0.0/Cargo.toml`
- `environment/bootstrap/base/archive/cedar/3.0.0/src/lib.rs`
- `environment/bootstrap/base/archive/cedar/3.1.0/Cargo.toml`
- `environment/bootstrap/base/archive/cedar/3.1.0/src/lib.rs`
- `environment/bootstrap/base/archive/elm/4.0.0/Cargo.toml`
- `environment/bootstrap/base/archive/elm/4.0.0/src/lib.rs`
- `environment/bootstrap/base/projects/ash.toml`
- `environment/bootstrap/base/projects/beech.toml`
- `environment/bootstrap/base/projects/cypress.toml`
- `environment/bootstrap/base/projects/dogwood.toml`
- `environment/bootstrap/base/projects/hawthorn.toml`
- `environment/bootstrap/base/projects/spruce.toml`
- `tests/test.sh`
- `tests/test_outputs.py`
- `solution/solve.sh`

The alpha patch creates `tests/parent_alpha.rs` and `docs/releases/alpha.md` in the alpha commit; beta creates `tests/parent_beta.rs` and `docs/releases/beta.md` in the beta commit. Both files remain in the merge/current trees. Their exact selections and independent rationales are solver-visible through `/app/repo` and Git history, but neither artifact mentions the sibling branch or merged diagnosis.

Every package payload is a substantive compileable Rust crate. Catalog entries bind versions, source identities, transitive requirements, and payload directories. The build module materializes the selected crates into a clean path-dependency workspace and runs Cargo offline; it may not replace compilation with metadata comparison.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```yaml
- path: src/aero/veil.rs
  symbol: cast_vane
  kind: function
  signature: pub(crate) fn cast_vane(a: &RawRecord, b: &QueryFrame) -> Result<Vane, ClassError>
  purpose: Validates and converts one raw candidate plus request-local evidence into a constrained value.

- path: src/cairn/sill.rs
  symbol: turn_sill
  kind: function
  signature: pub(crate) fn turn_sill(a: Vane, b: &PolicyFrame) -> Result<Admitted, RejectCode>
  purpose: Applies contextual policy to a constrained value and returns an immutable accepted decision.

- path: src/quill/quay.rs
  symbol: lace_quay
  kind: function
  signature: pub(crate) fn lace_quay(a: Cairn<Admitted>, b: &Wick) -> Result<Trellis, GraphError>
  purpose: Validates a complete accepted graph and commits its semantic identities and deterministic traversal.
```

The oracle may change only these three function bodies. Exact signatures, types, paths, and parameter names are fixed. A has raw/request evidence but no policy state; B has policy state and a `Vane` but no raw record; C has the complete admitted graph but no raw/request/policy evidence. Surrounding code must not expose a bypass with all three inputs.

The expected genuine semantic delta is:

- `cast_vane`: 28-38 changed lines for validation, normalization, contradictory-evidence rejection, and constrained conversion.
- `turn_sill`: 30-42 changed lines for the union of parent contracts, context-limited exceptions, and explicit rejection paths.
- `lace_quay`: 37-50 changed lines for edge validation, semantic identity, deduplication, complete-graph checks, and deterministic `Trellis` construction.

Total target: 95-130 comment-stripped semantic changed lines. These operations are independently demanded by tests; no comments, formatting, no-op writes, or whole-file replacement count.

#### flipping_point_contract

```yaml
locations:
  - id: A
    path: src/aero/veil.rs
    controls_tests: [test_r01, test_r03, test_r04, test_r07, test_r10]
  - id: B
    path: src/cairn/sill.rs
    controls_tests: [test_r02, test_r03, test_r08, test_r11, test_r12]
  - id: C
    path: src/quill/quay.rs
    controls_tests: [test_r05, test_r06, test_r09, test_r10, test_r11]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

The three pairwise overlaps are intentional and semantic:

- A+B: `test_r03`
- A+C: `test_r10`
- B+C: `test_r11`

Each isolated reversion must flip its five declared tests for behavioral reasons. Other tests must remain green. A reversion may not be simulated by disabling code, changing tests, or using scenario-specific guards.

#### decoy_manifest

```yaml
- path: src/aero/pale.rs
  kind: helper
  rhymes_with: cast_vane
  non_fix_purpose: cast_fane(a: &SampleRow, b: &DisplayFrame) -> Result<Fane, SampleError> converts diagnostic sampling rows into a bounded display value.

- path: src/cairn/rill.rs
  kind: helper
  rhymes_with: turn_sill
  non_fix_purpose: turn_rill(a: Fane, b: &AdvisoryFrame) -> Result<Shown, DropCode> applies display filtering to optional advisory events.

- path: src/quill/bay.rs
  kind: helper
  rhymes_with: lace_quay
  non_fix_purpose: lace_bay(a: Batch<Shown>, b: &Gauge) -> Result<Tally, TallyError> assembles deterministic compiler-summary rows from completed jobs.
```

Decoys must compile, execute in ordinary diagnostics, use signatures structurally similar to their selected neighbor, and remain untouched by the oracle. They must not describe themselves as decoys or healthy paths.

#### code_forbidden_tokens

```yaml
code_forbidden_tokens: [dependency workspace, dependency, workspace, app, repo, source, bin, rebuild-forge, rebuild command, command, edited binary, binary, forge, single supported entrypoint, supported entrypoint, entrypoint, solve, projects, project, workspace.toml, output, workspace.lock, UTF-8 text, text, lock line, lines, line, name, version, source-id, id, one ASCII space, ASCII space, space, fields, field, ascending bytewise tuple order, bytewise tuple order, tuple order, tuple, order, duplicate tuples, duplicate tuple, tuples, one final newline, final newline, newline, bundled project, nearby generated input, generated input, input, dependency set, set, declared direct and transitive requirements, direct and transitive requirements, declared direct requirements, direct requirements, declared direct requirement, direct requirement, direct, declared transitive requirements, transitive requirements, declared transitive requirement, transitive requirement, transitive, declared requirements, requirements, declared requirement, requirement, bundled downstream build, downstream build, build, equivalent package archive orderings, package archive orderings, package archive ordering, package archive, archive orderings, archive ordering, package, archive, orderings, ordering, clean repeated runs, clean repeated run, repeated runs, repeated run, runs, run, byte-identical lockfiles, byte-identical lockfile, lockfiles, lockfile, established edge-case behaviors, edge-case behaviors, edge-case behavior, behaviors, behavior, existing consumers, existing consumer, consumers, consumer, committed parent checks and release notes, parent checks and release notes, committed parent checks, committed parent check, parent checks, parent check, parents, parent, checks, check, release notes, release note, notes, note, repository history, repository, history, expected selections, expected selection, selections, selection, merged failure, failure, valid repair, repair, new package names and ranges, new package names, new package name, package names and ranges, package names, package name, package ranges, package range, names, ranges, range, work, bundled data, data, network requests, network request, network, requests, request, project inputs, project input, inputs, hand, tool, clean state, state]
```

This list is the first-occurrence, de-duplicated extraction of exact surface plurals, normalized singulars, standalone coordinated terms, path/CLI tokens, and domain-meaningful compounds from the exact public instruction. It applies to fix-path file/directory tokens, function/class/constant names, parameter names, and committed signature type names. It does not restrict public prose or ordinary documentation.
