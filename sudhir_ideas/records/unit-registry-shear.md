# Idea: Unit Registry Shear

- Idea ID: `IDEA-0026`
- Slug: `unit-registry-shear`
- Category: scientific-computing
- Languages: TBD (candidate: fortran, python, c)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

Three simulation modules must migrate onto a shared physical-quantity exchange layer without changing any published result bit-for-bit — and the naive migration changes results, because each module's private unit handling hides load-bearing numerical behavior.

## Structural archetype

Cross-system refactoring under an output-invariance contract: nothing is "broken" at the start; the mandate is architectural, and the difficulty is that a semantically-faithful unification requires discovering why mathematically-equivalent conversions are not numerically equivalent here. The verifier grades new cross-module capabilities *and* bit-stability of legacy outputs. No other portfolio idea grades a refactor.

## Novelty fingerprint

- Domain/system: a coupled multi-physics simulation — three modules with private unit registries (thermal, kinematics, radiative), an exchange/coupling layer, golden output archives, and new cross-module scenarios that fail today.
- Failure mechanism (of naive migration): module A stores temperatures as affine-offset values and relies on exact cancellation in differences (centralizing to Kelvin changes results); module B treats angles as dimensionless with a deferred scale factor applied post-hoc; module C serializes through a unit-dependent quantization that rounds differently after conversion reordering.
- Distributed fix topology: the exchange-layer design plus targeted adaptations in each module's boundary; a correct solution coordinates all four places — centralizing conversions without per-module semantic adapters fails bit-stability, and adapters without a real shared layer fail the new cross-module scenarios.
- Verifier/invariant surface: legacy scenario outputs bit-identical to golden archives; new cross-module exchange scenarios produce correct physical results; round-trip conversion properties hold on the exchange layer.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): certified-enclosure-drift (IDEA-0009, reserved) is interval-certification divergence — different mechanism (certified enclosures) and different deliverable (repair, not refactor). reproducible-reduction-parity grades reduction agreement. Neither is unit semantics or refactor-shaped.
- Structural differentiator: the task's tension — unify semantics while forbidden from changing outputs — makes "just convert everything to SI" (the training-data answer) the canonical failing move.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must discover each module's hidden numerical dependency on its private representation (affine cancellation, deferred angle scaling, unit-coupled quantization) — visible only by diffing pilot-migration outputs against goldens and tracing the discrepancy to its mechanism.
- Synthesize: the exchange layer's design must reconcile three incompatible internal conventions plus the coupling semantics between them; the correct architecture emerges only from understanding all three modules.
- Diagnose: when the naive migration diverges, nothing says why — the solver gets an output diff and must attribute it across conversion order, representation, and serialization.
- Navigate coupling: fixing module A's adapter changes coupled quantities flowing into B and C, shifting their diffs; the bit-stability gate forces a specific, discoverable order of semantic preservation rather than any plausible-looking refactor.
- Reason beyond training: unit libraries are common; preserving exact floating-point behavior across a representation migration is specialist numerical-software engineering with no stock recipe.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Module A computes temperature differences whose affine offsets cancel exactly in its private representation; premature conversion to absolute scale loses the cancellation — provable by a two-line numerical experiment once suspected.
2. Module B's angle quantities carry a deferred scale factor applied at serialization, not at computation — provable from golden-file forensics on rotational scenarios.
3. Module C quantizes through a grid defined in its native unit; converting before quantization lands values on a different grid — provable by comparing quantization residues.
4. Fix locations: exchange-layer core, plus boundary adapters in modules A, B, and C — four coordinated sites.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): cross-system refactoring (primary); investigate-plan-implement-verify discipline; long-context state retention.
- Causal chain (4-8 dependent stages): (1) run legacy scenarios and pin goldens; (2) pilot-migrate one module, observe bit drift, isolate the affine-cancellation dependency; (3) design the adapter preserving A's semantics; (4) migrate B, catch the deferred-angle-scale discrepancy from rotational goldens; (5) migrate C, catch the quantization-grid discrepancy; (6) implement the shared exchange contract across all boundaries; (7) verify legacy bit-stability plus the new cross-module scenarios.
- Heterogeneous evidence surfaces (>= 3): golden output archives, module source in multiple languages, coupling configuration, numerical experiment outputs, serialization artifacts.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the drift is compiler/flag noise" — falsified because unmigrated modules rebuild bit-identically under the same flags; H2 "goldens are stale" — falsified by regenerating goldens from the untouched tree.
- Failing scenario and healthy control: naive unification diverges on thermal-difference, rotational, and serialization scenarios; scalar SI-native quantities migrate cleanly and their paths must remain bit-stable throughout (blocks wrapping everything in double-conversion shims, which fail the round-trip property checks).
- Meaningful-action estimate (20-100, no busywork): ~50-90 (golden pinning, three pilot migrations with forensic isolation, layer design, full verification).
- Determinism strategy: fixed inputs, single-threaded numerics, pinned toolchain; bit-stability is itself the graded property; single container, offline.
- Domain and why this is not trivia: tests numerical-preserving architecture migration — the kind of refactor scientific-software teams fear most — not unit-conversion arithmetic.

## Symptoms-only instruction sketch

"Management requires the three simulation modules to exchange physical quantities through one shared layer so the new coupled scenarios in the archive can run. A previous attempt was abandoned because validation outputs changed. Deliver the shared layer with the new scenarios working, while every archived legacy scenario reproduces its published output exactly."

## Decision notes

Captured 2026-07-19; reshaped to the refactor-under-invariance archetype in the same-day template review. Step 2a watchpoints: new-scenario tests must be impossible to satisfy with per-pair ad-hoc conversion shims (round-trip and associativity properties on the layer), and golden bit-stability must span enough scenario diversity that "recompute goldens" is not an available move.
