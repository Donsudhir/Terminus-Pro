# Idea: Lockstep Replay Fray

- Idea ID: `IDEA-0020`
- Slug: `lockstep-replay-fray`
- Category: games
- Languages: TBD (candidate: c++ or rust)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

Recorded matches of a lockstep-simulated game desync on replay at reproducible ticks for some seeds; the ordering and state-consumption contract of the simulation must be repaired so every recording replays exactly.

## Structural archetype

Deterministic ordering repair via a seeded scheduler: the harness exposes explicit tick/seed control (no timing luck), and the verifier grades digest-identical replay across a seed matrix. The solver reasons about ordering contracts and state-stream consumption, not numerical or resource properties. This is the portfolio's single determinism-repair idea (procgen-seed-shear was rejected as its duplicate).

## Novelty fingerprint

- Domain/system: a headless lockstep game simulation — entity system, ability/event system, shared RNG streams, recording/replay harness with per-tick state digests.
- Failure mechanism: entity update order depends on hash-set iteration seeded by allocation address; one ability path consumes a variable number of RNG draws gated on a float comparison compiled differently (fast-math) in the replay build; event-queue ties break by insertion order instead of stable keys.
- Distributed fix topology: entity iteration, RNG-draw discipline in the ability system, and event-queue tie-breaking live in three subsystems; each alone still desyncs a distinct seed class.
- Verifier/invariant surface: per-tick digest equality between record and replay across a seed/entity-count matrix, healthy seeds preserved, and re-recorded sessions replaying under both build profiles.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): no determinism/replay idea in the local active portfolio; robust-predicate-scale-parity touches float semantics but grades geometric topology parity, not replay identity. procgen-seed-shear was rejected specifically to keep this archetype unique.
- Structural differentiator: the invariant is temporal (state trajectory identity under re-execution), and the falsifiers run through divergence-point bisection over recorded trajectories — an investigation style no other idea uses.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must localize the first divergent tick, then discover address-seeded iteration, conditional RNG consumption, and unstable tie-breaking — three ordering contracts violated in different subsystems.
- Synthesize: a desync at tick N is caused by silent state drift many ticks earlier; the solver must build the record/replay comparison tooling mentally (or actually) across entity, ability, and event subsystems.
- Diagnose: symptoms are "some matches desync around mid-game"; the harness gives digests, not causes.
- Navigate coupling: fixing entity iteration changes which entity acts first, which changes RNG draw order globally — recordings made before the fix replay differently, so the solver must reason about what "correct" means across the fix boundary (the verifier's re-record scenarios pin this down).
- Reason beyond training: generic "use a seeded RNG" advice is already satisfied; the bugs are in consumption order and tie-breaking contracts, which require trajectory-level causal reasoning specific to this engine.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Entity update order varies because a hash-set iterates in address order — divergence follows allocation history, not game logic, provable by digest bisection plus per-subsystem state dumps.
2. An ability path draws RNG a variable number of times depending on a float threshold that flips under the replay build's compilation profile — the RNG stream then desynchronizes everywhere downstream.
3. Event-queue ties (same-tick events) resolve by insertion order, which differs once iteration order is fixed — a second-layer bug exposed only after the first fix.
4. Fix locations: entity-system iteration, ability-system RNG discipline, event-queue comparator — three subsystems.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): race conditions and asynchronous ordering (primary, deterministically harnessed); long-horizon causal debugging; recovery from disproven hypotheses.
- Causal chain (4-8 dependent stages): (1) reproduce a desync and bisect to the first divergent tick; (2) dump subsystem states at that tick to attribute divergence to entity order; (3) fix iteration, find desyncs move earlier for other seeds; (4) bisect again to the RNG stream, falsify the "seed differs" hypothesis, discover conditional draws; (5) fix draw discipline, find same-tick event ties still flip; (6) stabilize tie-breaking; (7) sweep the seed/entity matrix and re-record scenarios.
- Heterogeneous evidence surfaces (>= 3): recorded trajectory files, per-tick digest logs, simulation state dumps, build/profile configuration, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "recordings are corrupt" — falsified by checksums and by the same recording replaying cleanly for healthy seeds; H2 "RNG seeding differs between builds" — falsified by logging initial seeds and first draws, which match until the conditional-draw tick.
- Failing scenario and healthy control: specific seed/entity-count classes desync; healthy seeds replay digest-identically and must continue to, including through the fixes (blocks "re-serialize everything every tick" style rewrites that alter healthy trajectories).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (bisections, state dumps, three ordered fixes with re-bisection, matrix sweep).
- Determinism strategy: lockstep tick scheduler with explicit seed control; no threads, no sleeps, no wall clock; the "race" is a deterministic ordering contract violation; single container, offline.
- Domain and why this is not trivia: tests simulation-determinism engineering — ordering contracts, RNG stream discipline, trajectory bisection — a real multiplayer-engine skill, not a trivia lookup.

## Symptoms-only instruction sketch

"Players report replays that stop matching the live match partway through — always the same point for a given recording. QA confirms most recordings are fine. Make every archived recording replay to the exact recorded outcome, and make fresh recordings replay exactly under both shipping build profiles."

## Decision notes

Captured 2026-07-19; confirmed as the sole determinism-repair archetype (procgen duplicate rejected). Step 2a watchpoints: the fix must not be "record more state" (verifier includes fresh-recording scenarios where the recording format is fixed), and digests must cover semantic state so cosmetic-order rewrites cannot fake identity.
