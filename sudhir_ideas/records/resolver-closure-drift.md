# Idea: Resolver Closure Drift

- Idea ID: `IDEA-0025`
- Slug: `resolver-closure-drift`
- Category: build-and-dependency-management
- Languages: TBD (candidate: python or rust)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A dependency resolver regressed during a merge window and the lockfile now churns and breaks downstream builds; the solver must reconstruct from offline commit history which two individually-correct changes semantically conflict, then repair the resolver honoring both changes' contracts.

## Structural archetype

History archaeology / semantic-merge reasoning: the primary evidence surface is reconstructed Git history (bundled offline commits applied at image build), and the core insight is that two merged changes are each correct alone but wrong together. The verifier grades resolution properties, but the *investigation* is inherently historical — no other portfolio idea makes commit-lineage reasoning the spine.

## Novelty fingerprint

- Domain/system: a private-index dependency resolver — version-range solver, prerelease/yank policy modules, lockfile writer, and a reconstructed repository history containing the merge window plus test fixtures for several package indexes.
- Failure mechanism: branch A changed prerelease-precedence handling (correct per its issue); branch B added yanked-version fallback (correct per its issue); merged, the fallback can select a prerelease that A's ordering now ranks above a stable version, violating both features' guarantees. A third commit relaxed lockfile canonicalization, masking the conflict in CI and adding nondeterministic churn.
- Distributed fix topology: precedence policy, yank-fallback policy, and lockfile canonicalization must be reconciled; reverting any single commit breaks that commit's legitimately-fixed behavior (the verifier tests both original issues' scenarios).
- Verifier/invariant surface: resolution correctness across fixture indexes covering both original issues and the interaction cases; deterministic, canonical lockfiles across repeated runs; downstream fixture builds succeed.

## Collision audit

All six required scopes were searched on 2026-07-19: idea registry, active
tasks, archived tasks, 159 submission archives (content-level instruction
scan), upstream task corpora, and current external research.

- Closest analogue: Alibaba terminal-bench-pro
  `implement-depgraph-dependency-resolver`, a spec-complete blank-canvas
  resolver implementation.
- Structural differentiator: this task investigates an existing resolver
  through reconstructed history, recovers two independently valid feature
  contracts, and repairs their emergent merged semantics plus canonical
  serialization without reverting either feature. Git commands are not graded.
- Internal neighbours: `bitwise-rebuild-drift` grades build-pipeline entropy;
  `musl-sysroot-splice` grades toolchain staging. Neither uses history
  archaeology or dependency-resolution policy.
- Evidence: `sudhir_research/TASK-RCD-001-RESEARCH.md`, PEP 440, PEP 592,
  PEP 665's reproducibility analysis, the cited Alibaba task, and GitBench.
- Result: no semantic collision found; uniqueness PASS is recorded in the
  registry. This does not imply Step 2a GO.

## Why it is hard (five hardness axes)

- Discover: the solver must bisect reconstructed history to the merge, understand each branch's intent from its commits/tests/issue notes, and find the masking canonicalization change — three historical facts absent from current-state reading.
- Synthesize: the correct repair is a policy that satisfies two contracts simultaneously (prerelease ordering and yank fallback) plus determinism; it exists only at the intersection, not in either branch.
- Diagnose: symptoms are churn and intermittent downstream failures; naive bisection misleads because the canonicalization commit shifts where failures appear.
- Navigate coupling: reverting A or B fails their scenario tests; fixing only canonicalization exposes rather than resolves the semantic conflict; the repair must change resolution policy while keeping every historical guarantee.
- Reason beyond training: SAT-style resolver lore is common, but reasoning about the *composition* of two policy changes against their historical contracts is genuine engineering judgment that cannot be pattern-matched.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The regression window contains a merge of two branches whose tests both still pass — the failure is emergent interaction, provable by constructing the cross-case (yank fallback under new precedence).
2. Lockfile canonicalization was relaxed in a separate commit, which both masks the conflict in CI and causes the observed churn — provable by diffing lockfile serialization across the window.
3. Each branch's contract is documented in its issue/test artifacts; the repair must satisfy the union, discoverable only by reading the history.
4. Fix locations: precedence policy module, yank-fallback module, lockfile writer/canonicalizer — three roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): Git and history reasoning (primary); multi-component reasoning; recovery from disproven hypotheses.
- Causal chain (4-8 dependent stages): (1) reproduce churn and a downstream failure; (2) bisect history — hit the misleading canonicalization commit first and falsify it as root cause; (3) locate the merge and characterize each branch's contract from its artifacts; (4) construct the interaction case proving emergent conflict; (5) design the reconciled policy; (6) restore strict canonicalization; (7) verify both original issues' scenarios, interaction cases, determinism, and downstream builds.
- Heterogeneous evidence surfaces (>= 3): reconstructed commit history (messages, diffs, branch tests), issue/changelog artifacts, lockfiles, package-index fixtures, resolver logs.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the index mirror served different data" — falsified by content-hashing the fixture indexes; H2 "the canonicalization commit is the whole bug" — falsified by re-strictening it on the pre-merge tree and seeing correct behavior, then on post-merge and still failing the interaction case.
- Failing scenario and healthy control: interaction cases and churn fail; each branch's original scenario passes today and must keep passing (blocks revert-based "fixes" — the verifier runs both branches' regression suites).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (bisection, contract reading, interaction-case construction, policy repair, full verification).
- Determinism strategy: history is reconstructed at image build from bundled patches (per philosophy doc: no shipped repo metadata); indexes are static fixtures; single container, offline.
- Domain and why this is not trivia: tests dependency-resolution semantics and historical contract reconciliation — senior build-engineering work, not one packaging fact.

## Symptoms-only instruction sketch

"Since sometime last quarter, regenerating the lockfile gives a different file almost every run, and downstream teams intermittently get broken dependency sets that used to be stable. Two recent 'fixes' in this area are both considered load-bearing and must keep working. Make resolution correct and deterministic again without regressing either of those behaviors."

## Decision notes

Captured 2026-07-19; reshaped to the history-archaeology archetype in the same-day template review. Step 2a watchpoints: history must be reconstructed at build time from bundled patches (packaging excludes .git), and the misleading first-bisect hit must be honestly explainable, not a planted decoy without purpose.
