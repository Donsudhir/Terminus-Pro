### Decision
GO — Attempt 2.

- One history-led policy incident replaces the independent formatter defect.
- Three intrinsically different typed authorities replace duplicate candidate-list signatures.
- Public operation, output, historical evidence, actual package builds, and overlapping ablations are now explicit.

### Metadata
- Task name: resolver-closure-drift
- Title: Resolver Closure Drift
- Category: build-and-dependency-management
- Languages: [rust, python]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excl. Docker files)
- Subcategories: []
- Tags: [dependency-resolution, semantic-merge, reproducible-builds, git-history, transitive-closure]
- Milestones: 0

### Investigation profile

**Weakness areas:** `git_reasoning` is primary. `multi_component_reasoning` and `mistake_recovery` reinforce the same merged-policy incident.

**Dependent causal chain:**

1. Current-head runs establish that only the combined project fails while both parent controls and an ordinary control remain healthy. Deterministic archive permutations alter graph identity, public bytes, and downstream outcome.
2. The reconstructed DAG shows alpha and beta as sibling children of one base. Each parent’s committed check and note states a distinct unique selection, so either revert is invalid.
3. Replaying base, alpha, beta, merge, and current proves the true two-parent merge is the first semantic failure. This falsifies damaged archive content and later unrelated changes.
4. Cause-neutral traces show raw source/request information disappears before policy eligibility and that raw traversal identity later reaches the graph.
5. Partial repairs prove A can preserve raw distinctions but lacks policy state, while B has policy state but cannot reconstruct evidence discarded before `Vane`.
6. Once A and B agree, C must validate the admitted transitive graph and commit semantic identity/order into `Trellis`. The healthy writer then emits that plan verbatim.
7. Parent controls, generated neighbors, pairwise cross tests, deterministic permutations, repeated clean runs, and real offline Cargo builds verify the complete repair.

Stages 2–6 are causally dependent: parent history defines what cannot be reverted; replay identifies composition rather than one parent; traces reveal the typed loss; partial runs force the A/B split; and only admitted decisions provide the graph C can commit. Git commands are useful but never graded.

**Evidence surfaces:**

- Git history: real base → alpha/beta siblings → two-parent merge → current DAG.
- Documentation: exact parent checks and release notes, each scoped to one branch contract.
- Logs: raw, constrained, admitted, and graph trace rows without fix locations.
- Code: three typed boundaries plus healthy surrounding modules.
- Build artifacts: public lock bytes and actual offline Cargo compilation reports.
- Tests: parent controls, generated policy cases, pairwise ablations, and deterministic permutations.

**Competing hypotheses and deterministic falsifiers:**

- Writer-only nondeterminism: falsified because the writer serializes `Trellis` unchanged and an output-only reorder leaves membership/build failures.
- One bad parent: falsified by that sibling parent’s unique passing selection and committed compatibility artifact.
- Damaged archive: falsified by identical payload hashes, successful parent builds, and merged-only decision divergence over equivalent copies.

**Conditional matrix:**

- Failing: combined parent behaviors over a transitive payload graph.
- Failing: equivalent archive/root encodings of that graph.
- Healthy: alpha and beta independently.
- Healthy: ordinary unique-closure project across every history point.

**Meaningful-action estimate:** 46 evidence-producing reads, history queries, replays, trace comparisons, partial patches, generated checks, and builds.

**Determinism:** fixed descriptor metadata and explicit parent arrays; `git commit-tree`; immutable manifests and Rust crate payloads; fixed input permutations; offline single-container execution; no timing, randomness, filesystem-order dependence, or network.

**Domain reasoning:** the solver must compose historical dependency-selection contracts, preserve source/request context, apply contextual eligibility, commit transitive semantic identity, and prove actual payload compatibility. This is not one package-standard lookup or a sorting recipe.

### Discovery budget

- Discovery: Alpha and beta are sibling parent commits with different uniquely supported selections.
  Planned location: reconstructed Git DAG, `tests/parent_alpha.rs`, `tests/parent_beta.rs`, and branch release notes.
  Why instruction must not reveal it: naming either policy or commit would turn contract reconstruction into direct search.
- Discovery: Raw source/request evidence is collapsed before eligibility can compose both contracts.
  Planned location: `src/aero/veil.rs`, type definitions, and trace rows.
  Why instruction must not reveal it: the lost distinction identifies A and nearly states its repair.
- Discovery: Eligibility needs both constrained evidence and separate policy state, so it cannot be folded into A or reconstructed later.
  Planned location: `src/cairn/sill.rs`, `PolicyFrame`, and parent/cross replays.
  Why instruction must not reveal it: the exception rule is the central merged-policy diagnosis.
- Discovery: Stable lock bytes require graph commitment over admitted semantic identity rather than archive/traversal identity.
  Planned location: `src/quill/quay.rs`, `Cairn`, `Trellis`, traces, and payload builds.
  Why instruction must not reveal it: naming this identity rule would make C transcription.

### Anti-trivialization verdict

1. **Disclosure-collapse — PASS.** Operational and output disclosure does not reveal the sibling policies, lost typed evidence, or semantic graph identity.
2. **Hidden-instance — PASS.** Generated names, ranges, graphs, policy frames, and payloads require general behavior.
3. **Single-artifact repair — PASS.** Distinct typed inputs/outputs and three pairwise cross tests prevent one manifest, fixture, or writer patch.
4. **Generalization — PASS.** Deterministic generators vary package identities, ranges, edges, archive order, and root order.
5. **Prompt-honesty — PASS.** One rebuild command, one entrypoint, exact public format, output path, offline boundary, compatibility, requirements, builds, and byte identity are stated.
6. **Cheating-vs-difficulty — PASS.** Fresh generated projects and real compilation block handwritten lockfiles without creating the reasoning burden.
7. **Mechanical-fix filter — PASS.** The core is project Rust behavior, not harness or metadata repair.
8. **Localized-fix — PASS.** Three non-substitutable authorities each control 5/12 tests; no location controls a majority.
9. **Oracle-locality — PASS.** The 95–130 line target is genuine validation/conversion/policy/graph logic, not whole-file copying.
10. **Small declarative-cluster — PASS.** No policy table or config block can express the generated typed behavior.
11. **Grep-collapse — PASS.** Every selected path, symbol, parameter, signature type, and test name is clean against the exact noun set.
12. **Pre-factored-helper — PASS.** Opaque symbols do not mirror public concepts.
13. **Recipe-discount — PASS.** Generic range comparison and sorting cannot derive both parent contracts or admitted graph identity.
14. **Security-aura discount — PASS.** No security language is used.
15. **Orthogonal-checklist — PASS.** Byte stability is downstream of the same semantic decisions; there is no independent formatter bug.
16. **Harness-discount — PASS.** History reconstruction and payload compilation provide substrate, not hardness.
17. **One-pass solvability — PASS.** Current code alone does not explain both valid parents or their merged typed mismatch.
18. **Hard-only gate — PASS.** The bounded work requires senior history, policy, type-boundary, graph, and build reasoning.
19. **Discovery budget test — PASS.** Four non-trivial facts have distinct homes and legitimate non-disclosure reasons.
20. **Instruction specificity test — PASS.** Causes, algorithms, commits, policies, files, and symbols remain undisclosed.
21. **Topology distribution test — PASS.** Three plausible topologies each require three typed locations; the selected topology is structurally non-collapsible.

### Topology enumeration (3 candidate fix topologies)

1. **Selected typed pipeline**
   - `src/aero/veil.rs::cast_vane`
   - `src/cairn/sill.rs::turn_sill`
   - `src/quill/quay.rs::lace_quay`
   - No single location suffices because A lacks policy state, B lacks raw/request evidence, and C sees only accepted graph nodes.
2. **Query-partition topology**
   - `src/store/pane.rs::read_cell`
   - `src/model/hinge.rs::reduce_frame`
   - `src/graph/berth.rs::make_mesh`
   - No single location suffices because decoding, request-policy reduction, and complete graph materialization have disjoint information.
3. **Decision-journal topology**
   - `src/input/reed.rs::shape_leaf`
   - `src/policy/keel.rs::mark_turn`
   - `src/closure/spool.rs::replay_mesh`
   - No single location suffices because normalization lacks policy, journal entries are local, and replay has no raw metadata.

### Rubric axes

- **Verifiable — PASS.** Public parsing, exact parent contracts, independently derived constraints, deterministic bytes, and real Cargo builds are programmatic.
- **Well-specified — PASS.** All operational and observable requirements have a single public source of truth.
- **Solvable — PASS.** The true DAG, parent artifacts, traces, types, fixtures, and payloads bound the investigation.
- **Difficult — PASS.** The union of two project-specific contracts and its typed propagation remain undisclosed.
- **Interesting — PASS.** This models real dependency resolver and reproducible-build regression work.
- **Outcome-verified — PASS.** Any implementation producing valid closures, bytes, compatibility, and builds passes.

### Hardness axes

- **Discover — PASS.** Four required facts live in history, traces, code, and build outcomes rather than the prompt.
- **Synthesize — PASS.** Raw classification, policy eligibility, and graph commitment exchange constrained values.
- **Diagnose — PASS.** The prompt gives symptoms and contracts, not causes.
- **Navigate coupling — PASS.** Parent reverts, one-boundary fixes, and output-only fixes each violate distant invariants.
- **Reason beyond training — PASS.** Project-specific historical contract composition dominates generic resolver knowledge.

### Instruction completeness test

Can the task be solved from `instruction.md` alone? **No — PASS.** The instruction is sufficient to rebuild, invoke, parse, and judge the tool, but it contains no parent selection rule, raw-context classification, eligibility exception, or graph identity diagnosis.

## Reviewer Appendix

### Implementation plan

Build a dependency-free Rust resolver under a reconstructed repository. The history builder consumes five descriptors: base has no parent; alpha and beta each have base as their only parent; merge has `[alpha, beta]`; current has merge. Descriptors include fixed identity/time/message/tree metadata, while deterministic patch payloads create the sibling features, branch-local checks/notes, merge integration, and current fixture. `rebuild_repo.py` uses `git commit-tree`, verifies parent counts and tree hashes, creates branch refs, and leaves current checked out at `/app/repo`.

The baseline must keep alpha and beta independently green while failing the merged interaction. `RawRecord + QueryFrame -> Vane` is the only raw-context conversion. `Vane + PolicyFrame -> Admitted` is the only eligibility decision. `Cairn<Admitted> + Wick -> Trellis` is the only complete-graph commitment. The writer accepts `Trellis` and emits the public lines without deciding policy. This shape makes output reproducibility part of semantic closure identity.

The package archive contains actual Rust crate sources. Tests and the tool assemble selected crates into a temporary path-dependency workspace and run `cargo build --offline --locked`. Wrong transitive selections fail compilation through genuine API incompatibility, not a metadata sentinel.

### Proposed file inventory

Task root:

- `instruction.md` — exact two-paragraph public contract.
- `task.toml` — anonymous v2 hard/offline metadata.
- `output_contract.toml` — local declaration of the public lock target and schema checks.
- `construction_manifest.json` — local mirror of exact symbols and ablations.
- `tests/test.sh` — CM-007-safe offline pytest runner.
- `tests/test_outputs.py` — twelve isolated behavioral tests.
- `solution/solve.sh` — deterministic patch/rebuild oracle limited to three function bodies.

Environment control:

- `environment/Dockerfile` — digest-pinned build and runtime setup.
- `environment/.dockerignore` — excludes task tests, solution, caches, `.git`, build products, and local manifests.
- `environment/Makefile` — deterministic authoring build/check targets.
- `environment/verifier-requirements.txt` — pinned verifier dependencies installed during image build.
- `environment/bin/rebuild-forge` — rebuilds `/app/repo` and atomically installs `/app/bin/forge`.

History reconstruction:

- `environment/bootstrap/rebuild_repo.py` — validates and materializes the DAG.
- `environment/bootstrap/history/descriptors/base.json` — no parents; fixed base commit metadata.
- `environment/bootstrap/history/descriptors/alpha.json` — parent `[base]`; alpha patch.
- `environment/bootstrap/history/descriptors/beta.json` — parent `[base]`; beta patch.
- `environment/bootstrap/history/descriptors/merge.json` — parents `[alpha, beta]`; two-parent integration tree.
- `environment/bootstrap/history/descriptors/current.json` — parent `[merge]`; combined fixture and neutral cleanup.
- `environment/bootstrap/history/patches/alpha.patch` — feature plus `tests/parent_alpha.rs` and `docs/releases/alpha.md`.
- `environment/bootstrap/history/patches/beta.patch` — feature plus `tests/parent_beta.rs` and `docs/releases/beta.md`.
- `environment/bootstrap/history/patches/merge.patch` — integration tree preserving both parent artifacts.
- `environment/bootstrap/history/patches/current.patch` — current fixture and cause-neutral cleanup.

Base Rust project:

- `environment/bootstrap/base/Cargo.toml`, `Cargo.lock` — dependency-free offline package.
- `environment/bootstrap/base/src/main.rs`, `lib.rs` — binary and library assembly.
- `environment/bootstrap/base/src/model/{mod,raw,frame,vane,admitted,cairn,trellis}.rs` — constrained model types.
- `environment/bootstrap/base/src/aero/{mod,veil,pale}.rs` — A and real diagnostic decoy.
- `environment/bootstrap/base/src/cairn/{mod,sill,rill}.rs` — B and real advisory decoy.
- `environment/bootstrap/base/src/quill/{mod,quay,bay}.rs` — C and real compiler-summary decoy.
- `environment/bootstrap/base/src/store/{mod,catalog,payload}.rs` — archive and payload loading.
- `environment/bootstrap/base/src/graph/{mod,walk}.rs` — healthy graph expansion.
- `environment/bootstrap/base/src/cli/{mod,session}.rs` — one supported solve path.
- `environment/bootstrap/base/src/build/{mod,workspace}.rs` — materializes and compiles selected payload crates.
- `environment/bootstrap/base/src/wire/{mod,lock}.rs` — healthy `Trellis` serializer.
- `environment/bootstrap/base/src/trace.rs` — cause-neutral typed events.
- `environment/bootstrap/base/docs/architecture.md` — component responsibilities, no merged cause.
- `environment/bootstrap/base/conf/defaults.toml` — ordinary non-fix defaults.

Offline archive and projects:

- `environment/bootstrap/base/archive/catalog.json` — source identities, versions, requirements, payload roots.
- `archive/alder/{1.0.0,1.1.0-alpha.1,1.1.0}/{Cargo.toml,src/lib.rs}` — three API-compatible/incompatible variants needed by alpha and generated neighbors.
- `archive/birch/{2.0.0,2.1.0}/{Cargo.toml,src/lib.rs}` — beta alternatives and policy controls.
- `archive/cedar/{3.0.0,3.1.0}/{Cargo.toml,src/lib.rs}` — transitive API boundary.
- `archive/elm/4.0.0/{Cargo.toml,src/lib.rs}` — downstream root payload.
- `environment/bootstrap/base/projects/{ash,beech,cypress,dogwood,hawthorn,spruce}.toml` — ordinary, parent, combined, permutation, and build controls.

Every payload source exports real Rust APIs used by dependents. The inventory contains no expected final lockfile, merged-answer commit, hidden verifier input, or metadata-only build sentinel.

### Oracle notes

`solution/solve.sh` edits only:

- `cast_vane`: validate raw source metadata and request-local evidence; reject contradictory combinations; preserve only the constrained distinctions B legitimately needs; produce `Vane`. Expected 28–38 changed lines.
- `turn_sill`: combine `Vane` with `PolicyFrame`; preserve alpha’s and beta’s unique parent outcomes; scope exceptional admission to its valid context; produce immutable `Admitted` or an explicit rejection. Expected 30–42 changed lines.
- `lace_quay`: validate all accepted nodes and edges, detect missing/duplicate semantic identities, bind root intent, commit deterministic semantic tuple traversal, and produce `Trellis`. Expected 37–50 changed lines.

The 95–130 total is plausible because each function performs mandatory validation, conversion, and failure handling over a distinct type boundary. These are not three large conditionals that could move into one function: A lacks policy data, B lacks raw evidence and full graph, and C lacks both.

The writer is unchanged. The oracle may not modify signatures/types, parent artifacts, descriptors, fixtures, payloads, tests, writer, decoys, or build runner. It must rebuild via `/app/bin/rebuild-forge`.

A second valid implementation may use different internal local data structures inside each committed body, recompute safe local ordering, or use iterators instead of temporary vectors. It may not change the externally committed typed boundaries. Tests grade behavior rather than local source form.

### Collapse audit

Stage: implementation-plan

Smallest plausible successful patch:

A 95–130 line patch across `cast_vane`, `turn_sill`, and `lace_quay`. A preserves raw/request distinctions in `Vane`; B applies the union of parent contracts using separate `PolicyFrame`; C validates and commits the complete `Cairn<Admitted>` under semantic identity and deterministic traversal. The healthy writer serializes `Trellis`.

Likely editable frontier:

- `src/aero/veil.rs::cast_vane`
- `src/cairn/sill.rs::turn_sill`
- `src/quill/quay.rs::lace_quay`

Requirement-to-file map:

- Alpha compatibility → A plus healthy B, verified by parent artifact and `test_r01`.
- Beta compatibility → B plus healthy A, verified by parent artifact and `test_r02`.
- Merged/general policy → A+B and generated cross/neighbor checks.
- Complete transitive semantic identity → A+C and B+C cross checks.
- Public byte identity → C’s `Trellis`; healthy writer only emits it.
- Actual buildability → selected graph plus real payload compiler, not one fix destination.

Oracle estimated complexity: 95–130 comment-stripped semantic changed lines; GX3 target at least 80.

Discoverability:

The public instruction exposes operation and output but not diagnosis. Exact parent values are honestly visible in sibling history and verifier expectations, but neither value states how to compose both contracts. The current writer is visibly simple, preventing a misleading output-only answer. Types reveal available information without narrating the correct conversion. Opaque selected names and real decoys resist direct noun grep.

Red flags:

- Construction must stop if any selected type gains enough information to absorb another authority.
- Construction must stop if parent artifacts mention the sibling or merged failure.
- Construction must stop if actual compilation is replaced with metadata validation.
- Construction must stop if isolated reversions do not match the overlapping five-test declarations.
- Construction must stop if real semantic edit distance is below 80.

Residual hardness:

After all files are visible, the solver must still use sibling history to understand non-revertable behavior, identify where raw evidence becomes too weak, reconcile policy using only the allowed typed data, and commit the resulting transitive graph so both semantics and bytes remain invariant over generated equivalent inputs.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**

dependency workspace, dependency, workspace, app, repo, source, bin, rebuild-forge, rebuild command, command, edited binary, binary, forge, single supported entrypoint, supported entrypoint, entrypoint, solve, projects, project, workspace.toml, output, workspace.lock, UTF-8 text, text, lock line, lines, line, name, version, source-id, id, one ASCII space, ASCII space, space, fields, field, ascending bytewise tuple order, bytewise tuple order, tuple order, tuple, order, duplicate tuples, duplicate tuple, tuples, one final newline, final newline, newline, bundled project, nearby generated input, generated input, input, dependency set, set, declared direct and transitive requirements, direct and transitive requirements, declared direct requirements, direct requirements, declared direct requirement, direct requirement, direct, declared transitive requirements, transitive requirements, declared transitive requirement, transitive requirement, transitive, declared requirements, requirements, declared requirement, requirement, bundled downstream build, downstream build, build, equivalent package archive orderings, package archive orderings, package archive ordering, package archive, archive orderings, archive ordering, package, archive, orderings, ordering, clean repeated runs, clean repeated run, repeated runs, repeated run, runs, run, byte-identical lockfiles, byte-identical lockfile, lockfiles, lockfile, established edge-case behaviors, edge-case behaviors, edge-case behavior, behaviors, behavior, existing consumers, existing consumer, consumers, consumer, committed parent checks and release notes, parent checks and release notes, committed parent checks, committed parent check, parent checks, parent check, parents, parent, checks, check, release notes, release note, notes, note, repository history, repository, history, expected selections, expected selection, selections, selection, merged failure, failure, valid repair, repair, new package names and ranges, new package names, new package name, package names and ranges, package names, package name, package ranges, package range, names, ranges, range, work, bundled data, data, network requests, network request, network, requests, request, project inputs, project input, inputs, hand, tool, clean state, state

The list is de-duplicated in first-occurrence order. It includes exact surface plurals, normalized singulars, path and CLI tokens (`app`, `repo`, `bin`, `rebuild-forge`, `forge`, `solve`, `projects`, `workspace.toml`, `output`, `workspace.lock`), standalone coordinated terms (`direct`, `transitive`), and meaningful compounds such as `dependency workspace`, `direct and transitive requirements`, `committed parent checks`, `release notes`, `network requests`, `package archive orderings`, `repository history`, and `clean state`.

**Renames during drafting:**

- `src/source/classify.rs::classify_source` → `src/aero/veil.rs::cast_vane`: removed public source vocabulary and classification intent.
- `src/policy/eligibility.rs::decide_requirement` → `src/cairn/sill.rs::turn_sill`: removed public requirement vocabulary and policy intent.
- `src/closure/identity.rs::commit_lock_order` → `src/quill/quay.rs::lace_quay`: removed public lock/order vocabulary.
- `test_archive_order_bytes` → `test_shuffle_equivalence`: removed public archive/order/byte vocabulary while retaining a behavioral name.
- `test_parent_alpha` → `test_r01`: removed parent and scenario identity.
- `test_parent_beta` → `test_r02`: removed parent and scenario identity.
- `test_cross_pair` → `test_r03`: removed pairwise topology disclosure.
- `test_neighbor_matrix` → `test_r04`: removed generated-scenario shape.
- `test_shuffle_equivalence` → `test_r05`: removed ordering and equivalence hints.
- `test_repeat_equivalence` → `test_r06`: removed repeated-run and equivalence hints.
- `test_direct_frontier` → `test_r07`: removed direct-boundary vocabulary.
- `test_negative_neighbor` → `test_r08`: removed polarity and neighborhood shape.
- `test_root_permutation` → `test_r09`: removed root-ordering topology.
- `test_transitive_frontier` → `test_r10`: removed transitive-boundary vocabulary.
- `test_payload_compile` → `test_r11`: removed payload-build scenario disclosure.
- `test_beta_matrix` → `test_r12`: removed branch and matrix identity.

**Test names audited:**

- `test_r01`
- `test_r02`
- `test_r03`
- `test_r04`
- `test_r05`
- `test_r06`
- `test_r07`
- `test_r08`
- `test_r09`
- `test_r10`
- `test_r11`
- `test_r12`

**Decoy declarations audited:**

- `src/aero/pale.rs::cast_fane(a: &SampleRow, b: &DisplayFrame) -> Result<Fane, SampleError>`
- `src/cairn/rill.rs::turn_rill(a: Fane, b: &AdvisoryFrame) -> Result<Shown, DropCode>`
- `src/quill/bay.rs::lace_bay(a: Batch<Shown>, b: &Gauge) -> Result<Tally, TallyError>`

All selected paths, function names, parameter names, signature type names, exact decoy paths/symbols/signatures, and final test names were checked case-insensitively against every token. No final substring hit remains.

**Concentration math:**

- Union: 12 tests.
- A: 5/12 = `0.4166666666666667`.
- B: 5/12 = `0.4166666666666667`.
- C: 5/12 = `0.4166666666666667`.
- Memberships: 15 because `test_r03`, `test_r10`, and `test_r11` are pairwise overlaps.
- Cap: `0.5`.
- Status: PASS.

### Per-test feasibility pre-check

- Test: `test_r01`
  Checks: alpha’s unique historical selection, complete requirements, and actual payload build.
  Valid approaches: 2+; any typed policy preserving the documented outcome passes.
  Chain-dependent: no; isolated project/archive/build.
  Exact-value assertions: yes; uniquely documented in alpha parent check/note and independently embedded in verifier code.
  Feasibility risk: LOW.
- Test: `test_r02`
  Checks: beta’s unique historical selection, complete requirements, and actual payload build.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: yes; uniquely documented in beta parent check/note and verifier.
  Feasibility risk: LOW.
- Test: `test_r03`
  Checks: both parent outcomes coexist in one merged graph and compile.
  Valid approaches: 2+.
  Chain-dependent: self-contained A+B behavior, not another test.
  Exact-value assertions: only the two uniquely documented parent outcomes; graph/build assertions are derived.
  Feasibility risk: LOW.
- Test: `test_r04`
  Checks: generated raw/request neighbors preserve or reject distinctions correctly.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: property-based from generated manifests.
  Feasibility risk: LOW.
- Test: `test_r05`
  Checks: public byte equality and builds over explicit equivalent archive permutations.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: public line grammar plus pairwise equality, no golden lock.
  Feasibility risk: LOW.
- Test: `test_r06`
  Checks: clean semantically equivalent runs produce identical bytes and exact final-newline grammar.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: only public format; no golden closure.
  Feasibility risk: LOW.
- Test: `test_r07`
  Checks: generated direct-request boundaries retain required evidence through classification.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: derived from request and archive manifests.
  Feasibility risk: LOW.
- Test: `test_r08`
  Checks: the supported beta context does not become broad admission for nearby cases.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: beta’s documented positive value plus property-based negative neighbors.
  Feasibility risk: LOW.
- Test: `test_r09`
  Checks: equivalent root/traversal permutations yield one tuple set, order, bytes, and build.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: public grammar and equality only.
  Feasibility risk: LOW.
- Test: `test_r10`
  Checks: generated transitive nodes retain classified semantic identity through graph commitment.
  Valid approaches: 2+.
  Chain-dependent: self-contained A+C cross behavior.
  Exact-value assertions: requirement-derived membership, not an oracle lockfile.
  Feasibility risk: LOW.
- Test: `test_r11`
  Checks: policy-sensitive admitted nodes form a complete closure whose real Rust payload workspace compiles.
  Valid approaches: 2+.
  Chain-dependent: self-contained B+C policy/graph/build chain.
  Exact-value assertions: uniquely required API-compatible member plus compiler success.
  Feasibility risk: LOW.
- Test: `test_r12`
  Checks: generated beta policy frames preserve the branch contract only in valid contexts.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: documented positive value; other outcomes derived from manifests.
  Feasibility risk: LOW.

No test depends on another test, mutable expected files, execution order, randomness, timing, network, a Git command, or the oracle’s textual implementation. The pairwise cross tests intentionally require two typed locations but remain independently set up and behaviorally verifiable.

### Final score

- Hardness axes: 5 PASS, 0 WARN, 0 FAIL
- Anti-trivialization checks: 21 PASS, 0 WARN, 0 FAIL
- Rubric axes: 6 PASS, 0 WARN, 0 FAIL
- Instruction completeness: PASS
- Investigation profile: complete and semantically dependent
- Collapse audit: PASS
- Evidence-contract target: 0 FAIL / 0 WARN, subject to read-only validator output
