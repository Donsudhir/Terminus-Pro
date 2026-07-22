# Idea: Sanitizer Parser Rift

- Idea ID: `IDEA-0028`
- Slug: `sanitizer-parser-rift`
- Category: security
- Languages: TBD (candidate: c or rust, python)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A markup sanitizer and the downstream renderer in the same codebase parse documents differently, so policied content survives sanitization for specific constructs while some benign content is over-stripped; the differential itself must be eliminated.

## Structural archetype

Parser-differential elimination: two in-repo consumers of the same input disagree about its structure, and the verifier grades *agreement* (tree equivalence on a generated corpus) alongside policy outcomes (bypass corpus neutralized, benign corpus preserved). The graded object is the absence of a differential between two parsers — distinct from the trust-chain idea, which grades verdict correctness of one decision procedure against forgeries.

## Novelty fingerprint

- Domain/system: a document pipeline — tokenizer/tree-builder used by the sanitizer, a second parse path used by the renderer, an entity decoder, a policy table, and bypass/benign corpora.
- Failure mechanism: the sanitizer re-tokenizes after entity decoding while the renderer decodes exactly once (double-decode differential); foreign-content mode transitions (SVG/math-like islands) differ between the two tree builders; the policy table matches raw tag names before case folding on one path only.
- Distributed fix topology: entity-decode sequencing, foreign-content state machine, and policy-match normalization live in three places; each alone leaves either a live bypass class or an over-stripping class.
- Verifier/invariant surface: every bypass-corpus document renders inert; every benign-corpus document renders with its content intact; a differential harness parses generated documents through both paths and requires structural agreement.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): offline-trust-chain-skew (IDEA-0015) is the other security idea but grades acceptance-matrix correctness of a trust decision; here the subject is structural disagreement between two parsers, and half the failures are benign-content losses, not attacks. No markup/parsing idea exists elsewhere in the portfolio.
- Structural differentiator: the fix target is a meta-property (two parsers agree on all inputs), which cannot be reached by patching individual bypass cases — the differential harness generates fresh disagreements until the state machines truly converge.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the decode-order difference, the foreign-content transition divergence, and the case-folding asymmetry by reducing failing documents to minimal differentials — the bypass corpus never labels which mechanism each case exploits.
- Synthesize: understanding one disagreement requires holding both state machines in mind simultaneously; the three mechanisms interact (an entity can smuggle a foreign-content trigger whose case-folding then differs).
- Diagnose: symptoms are "some sanitized documents still execute content, others lose legitimate markup"; the mapping from symptom to mechanism is many-to-many.
- Navigate coupling: fixing double-decode changes what the foreign-content machine sees, shifting (not removing) several bypasses; hardening the policy table alone over-strips more benign content, failing the preservation corpus — the equilibrium requires all three fixes.
- Reason beyond training: parser-differential reasoning on a bespoke pair of state machines is not pattern-matchable; stock sanitizer checklists (allowlists, escaping) do not repair a structural disagreement between two in-house parsers.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The sanitizer decodes entities and then re-tokenizes, so `&lt;` sequences can materialize structure the renderer sees differently — provable by tracing one bypass document through both paths.
2. The two tree builders enter/exit foreign-content mode on different token sets, so islands parse as markup in one and text in the other — provable with a minimal island fixture.
3. Policy matching case-folds on one path only, so mixed-case names slip the table in exactly one parser — provable by a two-document experiment.
4. Fix locations: entity-decode sequencing, foreign-content state machine, policy-match normalization — three roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): security reasoning (primary); log/evidence triage (differential reduction); recovery from disproven hypotheses.
- Causal chain (4-8 dependent stages): (1) reproduce a bypass and an over-strip from the corpora; (2) build/reduce minimal differential documents; (3) attribute the first class to decode ordering; (4) fix it, re-run, observe surviving bypasses shift, attribute to foreign-content transitions; (5) converge the state machines; (6) catch the case-folding asymmetry via residual mixed-case cases; (7) pass bypass, benign, and generated-agreement suites together.
- Heterogeneous evidence surfaces (>= 3): bypass/benign document corpora, parse-tree dumps from both paths, policy configuration, sanitizer/renderer logs, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the policy table is just missing entries" — falsified by a bypass document using only policied names; H2 "the renderer alone is buggy" — falsified by cases where the sanitizer's own tree disagrees with the bytes it emits.
- Failing scenario and healthy control: entity-laden, island-bearing, and mixed-case documents disagree; plain well-formed documents parse identically through both paths and must keep rendering byte-identically (blocks "strip everything ambiguous," which fails the benign-preservation corpus).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (corpus triage, differential reduction, three convergence fixes, tri-suite verification).
- Determinism strategy: static corpora plus a seeded document generator for the agreement harness; no network, no browser — the renderer is an in-repo tree consumer; single container, offline.
- Domain and why this is not trivia: parser-differential analysis is a professional security specialty; the security aura was discounted and the residual state-machine reasoning stands on its own.

## Symptoms-only instruction sketch

"Security review found documents that pass our sanitizer yet still run active content downstream, while the support queue has complaints about legitimate formatting being destroyed. Both lists are in the archive. Make sanitization sound and lossless: archived attack documents must render inert, archived legitimate documents must keep their content, and the pipeline must stop disagreeing with itself about what a document contains."

## Decision notes

Captured 2026-07-19; fingerprinted same day. Step 2a watchpoints: the agreement harness must generate documents (seeded) so case-patching cannot converge it; benign-preservation must be graded on rendered output, not sanitizer exit codes (CM-006).
