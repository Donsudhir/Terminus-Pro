# Idea: Artifact Trust Chain Skew

- Idea ID: `IDEA-0015`
- Slug: `offline-trust-chain-skew`
- Category: security
- Languages: TBD (candidate: go or rust, shell)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

An offline artifact-signing verifier gives inconsistent verdicts on the same bundle depending on entry point; one general fix must make every verdict correct against a matrix of forged and legitimate bundles.

## Structural archetype

Adversarial acceptance matrix: the verifier grades a single hardened decision procedure against many adversarial variants plus a legitimate set. The solve is judged by verdict correctness across the matrix, not by agreement between components or by any historical artifact. No other portfolio idea grades adversarial-variant robustness.

## Novelty fingerprint

- Domain/system: an offline software-release trust pipeline — a CLI verifier and a service-side verifier sharing (nominally) one trust store, with cross-signed intermediates and revocation snapshots bundled as fixtures.
- Failure mechanism: depth-first versus breadth-first chain building diverging on cross-signed intermediates; name constraints enforced on leaves only in one path; revocation lookups keyed by subject rather than issuer+serial so revoked intermediates are missed.
- Distributed fix topology: chain builder, constraint checker, and revocation matcher must change coherently; fixing any one still accepts at least one forged class or rejects a legitimate class.
- Verifier/invariant surface: verdict matrix — legitimate, cross-signed-legitimate, expired-graft, constraint-violating, revoked-intermediate, and re-signed-payload bundles must all receive the correct verdict from both entry points.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): no PKI/trust-chain idea in the local portfolio. The generic "harden a service against adversarial scenarios" accept-exemplar in `idea-validation.mdc` is the shape ancestor; this instance differs by centering X.509-style path-building semantics rather than input sanitization.
- Structural differentiator: hardness lives in chain-building graph semantics (multiple valid paths, cross-signatures) — a reasoning problem, not a recipe; security-aura discount was applied and the residual reasoning stands.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find that the two entry points build chains in different orders, that constraints skip intermediates on one path, and that revocation keys collide — all only observable by tracing verdict differences across crafted bundles.
- Synthesize: a bundle's fate is decided by the interaction of path selection, constraint scope, and revocation matching; no single function contains the acceptance rule.
- Diagnose: symptoms are two inconsistent verdicts on one bundle; nothing says which of the three subsystems (or how many) is wrong.
- Navigate coupling: making the CLI match the service by copying its path order silently inherits the service's constraint-scope hole; the fix must be correct, not merely consistent.
- Reason beyond training: cross-signed path building with per-path constraint validity is genuinely subtle (real CVE territory), and the repo's bespoke chain model prevents pattern-matching a stock library answer.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The CLI accepts the first depth-first chain while the service scores breadth-first candidates — divergence appears only for bundles with a cross-signed intermediate.
2. Name constraints are checked against the leaf only in the service path; a constraint-violating intermediate passes there and fails in the CLI.
3. The revocation snapshot index is keyed by subject DN, so a revoked cross-signed intermediate with a re-used subject escapes matching.
4. Fix locations: chain-building module, constraint-evaluation module, revocation index/matcher — distinct roots shared by both entry points.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): security reasoning (primary); multi-component reasoning; recovery from disproven hypotheses.
- Causal chain (4-8 dependent stages): (1) reproduce the verdict disagreement on the reported bundle; (2) trace both entry points to find they select different chains; (3) form and falsify the "trust stores differ" hypothesis; (4) discover the constraint-scope hole while unifying path selection; (5) craft a probe bundle proving revoked intermediates escape; (6) repair all three subsystems; (7) sweep the full bundle matrix from both entry points.
- Heterogeneous evidence surfaces (>= 3): verifier trace logs, certificate/bundle fixtures (binary artifacts), trust-store configuration, code, revocation snapshot data.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the two binaries use different trust stores" — falsified by hashing the loaded stores from both paths; H2 "clock/validity skew" — falsified by verifying with the harness's fixed virtual time on a bundle with generous validity.
- Failing scenario and healthy control: cross-signed and revoked-intermediate bundles fail; plain single-chain legitimate bundles verify identically on both paths and must keep verifying (blocks "reject everything unusual" patches).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (dual-path tracing, bundle crafting, three coordinated repairs, matrix sweep).
- Determinism strategy: fixed virtual verification time, pre-generated key material and snapshots, no network; single container.
- Domain and why this is not trivia: tests trust-graph reasoning and adversarial completeness, not recall of an RFC field; every rule is discoverable from bundle behavior.

## Symptoms-only instruction sketch

"Release engineering found that a bundle rejected on developer machines was accepted by the publishing service, and an auditor later showed the service accepted a bundle it should have refused. Make verification give the correct verdict for every bundle in the archive, identically from both tools. Bundles that verify today for good reasons must continue to verify."

## Decision notes

Captured 2026-07-19; sharpened to the adversarial-acceptance-matrix archetype in the same-day template review. Step 2a watchpoints: verdict tests must be behavioral (run the verifiers) not string proxies (CM-006), and the forged-bundle classes must each require a different aspect of the general fix so no single-location patch clears the matrix.
