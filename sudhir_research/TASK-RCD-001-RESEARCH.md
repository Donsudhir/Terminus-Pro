# TASK-RCD-001 — resolver-closure-drift — Super-Uniqueness Dossier

- Idea: `resolver-closure-drift` (IDEA-0025)
- Category: build-and-dependency-management
- Archetype: history archaeology / semantic-merge reconciliation
- Research date: 2026-07-19
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** a private-index dependency resolver with separate
   prerelease-ordering and yanked-version fallback policies, a canonical
   lockfile writer, fixture indexes, and an offline reconstructed commit
   history carrying two formerly independent feature branches.
2. **Failure mechanism:** two individually correct policy changes compose
   incorrectly after merge: yanked-version fallback can feed a prerelease
   candidate into an ordering policy that ranks it above an eligible stable
   release. A later canonicalization relaxation masks the semantic conflict
   in CI while causing lockfile churn.
3. **Distributed fix topology:** candidate precedence, fallback eligibility,
   and lockfile canonicalization must be reconciled. Reverting either feature
   fails its original scenario; fixing serialization alone exposes but does
   not repair the invalid closure.
4. **Verifier/invariant surface:** both historical feature contracts continue
   to pass; interaction fixtures choose valid closures; repeated runs and both
   build entry points emit canonical byte-identical lockfiles; downstream
   fixture builds succeed.

## Collision audit — all six scopes

### 1. Idea registry (31 ideas)

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` 2026-07-19.
`bitwise-rebuild-drift` is the nearest build-category idea, but it audits
entropy in a code-generation/archive/link pipeline and grades bitwise build
reproducibility. `musl-sysroot-splice` stages a static toolchain. Neither
involves dependency-resolution semantics, feature-contract interaction, or
history archaeology. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: robust-predicate-scale-parity, sparse-jacobian-color-
contract, musl-sysroot-splice. `tasks/` also contains
journal-compaction-replay, mothlight-courier-replay-triage, and
driftlens-calibrate-api. No resolver, lockfile, version-policy, yanked-release,
or semantic-merge task. **No collision.**

### 3. Archived tasks / submission archives (159 zips)

Extracted every `instruction.md` (`/tmp/subm_instr`, 2026-07-19). Searches for
`lockfile|dependency resolver|prerelease|yanked|package index|semver|version
constraint|version range|registry mirror|git history|bisect|merge conflict`
returned no semantic match. Two broad `resolution` hits
(`tensor-retention-gate`, `magnetometer-kalman-residual-debug`) use unrelated
meanings. **No collision.**

### 4. Upstream corpus

The closest public benchmark result is Alibaba terminal-bench-pro's
`implement-depgraph-dependency-resolver`. Its instruction is spec-complete:
implement a `DependencyResolver` class, listed comparison operators,
topological sort, explicit exception types, output JSON schema, and test
cases. It is a blank-canvas implementation task and would fail this
repository's disclosure-collapse and instruction-specificity gates.

This idea instead starts with a working resolver whose two feature branches
each remain correct in isolation. The hard work is reconstructing their
contracts from history, proving their emergent interaction, and designing a
policy that preserves both while restoring canonical output. Topological sort
and ordinary constraint intersection are already healthy controls. **No
semantic collision.**

### 5. Current external research

Searches performed 2026-07-19:

- `"terminal-bench" task git bisect semantic conflict two merged changes
  dependency resolver repair benchmark 2026`
- `Terminal-Bench 2026 dependency resolver lockfile task benchmark agent
  version resolution semantic merge conflict`

Results found general Terminal-Bench documentation, the spec-complete Alibaba
task above, and GitBench. GitBench separately grades mechanical Git operations
such as `git_bisect`, `merge_conflicts`, and `cherry_pick`; it does not combine
history evidence with a domain-specific semantic policy repair, nor does it
grade preserving both branch contracts. **No collision found in current
public search.**

### 6. Structural-neighbour check

Package-manager bug reports commonly involve prereleases, yanked releases, or
lockfile churn separately. That shared vocabulary is not a collision. The
defining structure here is an emergent semantic conflict between two
individually correct historical changes, with a third change that becomes a
plausible but incomplete first bisect result. The solution must preserve the
union of prior contracts rather than revert history or implement a fresh
resolver.

## Closest analogue and structural difference

- **Closest analogue:** Alibaba terminal-bench-pro
  `implement-depgraph-dependency-resolver`.
- **Structural difference:** the analogue implements an explicitly specified
  resolver from scratch. This task investigates an existing resolver through
  reconstructed history, recovers two independent feature contracts, and
  repairs their merged semantics plus serialization without regressing either
  feature.
- **Why GitBench is not the closer analogue:** Git commands are optional
  investigation tools, not the graded outcome. Tests grade resolver closure
  and lockfile properties; an expert could inspect bundled commits manually
  and still pass.

## Authoritative technical grounding

### Python packaging version ordering

Source: PEP 440, *Version Identification and Dependency Specification*,
https://peps.python.org/pep-0440/ (retrieved 2026-07-19).

Pre-releases have defined ordering and are normally excluded unless explicitly
requested or no final/post release satisfies the requirement. The task uses a
small project-owned policy modeled on these ideas, not a requirement to recall
PEP text. Fixture behavior and historical tests expose the contracts.

### Yanked releases

Source: PEP 592, *Adding "Yank" Support to the Simple API*,
https://peps.python.org/pep-0592/ (retrieved 2026-07-19).

Yanking permits an index to discourage new selection of a release without
deleting it and breaking already pinned installations. This creates a real
policy seam between fallback eligibility, exact pins, and candidate ordering.

### Reproducible lockfiles

Source: PEP 665, *A file format to list Python dependencies for reproducibility
of an application* (withdrawn, but its reproducibility analysis remains
informative), https://peps.python.org/pep-0665/ (retrieved 2026-07-19).

Lockfiles exist to make dependency choices reproducible. Canonical
serialization and stable ordering are therefore behavioral supply-chain
properties, not formatting trivia.

## History construction policy

The task package must not ship `.git` metadata. Per
`LONG_HORIZON_TASK_PHILOSOPHY.md`, Step 2b will bundle offline patches/commit
descriptors and reconstruct a local repository during image build. The
solver-visible runtime may contain that reconstructed history because history
is a legitimate evidence surface; packaging still excludes authoring
metadata. Commit messages and historical tests explain each feature's intent
without naming the merged fix.

## Construction feasibility and anti-collapse risks

- Current-state code must contain several plausible policy paths and decoy
  helpers; prompt nouns must not grep directly to fix symbols.
- The interaction must be impossible to repair by reverting either branch:
  original branch scenarios remain scored healthy controls.
- The misleading canonicalization commit is genuine: it relaxed output order
  to make a flaky test pass, thereby masking closure changes. It is not an
  arbitrary decoy and fixing it alone must still fail interaction scenarios.
- The public instruction reports lockfile churn and downstream breakage. It
  does not name prereleases, yanks, fallback, precedence, canonicalization, or
  commits.
- Tests derive closure properties from fixture indexes and build results; they
  must not encode one expected answer table or inspect Git commands.
- Three distinct roots remain necessary: ordering policy, fallback policy, and
  writer. An oracle under 80 substantive changed lines would need careful
  review because this topology could otherwise collapse to three short
  conditionals.

## Uniqueness verdict

**PASS for the super-uniqueness gate.** Six required scopes were searched.
The nearest analogue is recorded and differs in failure mechanism,
investigation, distributed topology, and verifier surface. This permits Step
2a validation only; it is not Step 2a GO and does not permit construction.
