# Idea: Changefeed Splice Skew

- Idea ID: `IDEA-0023`
- Slug: `changefeed-splice-skew`
- Category: data-processing
- Languages: TBD (candidate: python, sql, c)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A change-data-capture applier must reach the exact source state even when killed at any point and resumed; today, resume from several injection points diverges, and for some feeds even a clean run is wrong.

## Structural archetype

Crash-consistency convergence: the harness provides deterministic kill-point injection hooks, and the verifier grades that resume-from-every-injection-point converges to the same correct final state. The graded object is an invariant over the set of all interrupted executions — a shape no other portfolio idea has.

## Novelty fingerprint

- Domain/system: a CDC pipeline — captured transactional change feed, an applier with checkpointing and side-effect emission, a replica database with constraints, and a deterministic fault-injection harness.
- Failure mechanism: the applier checkpoints after emitting side effects but before committing the transaction (resume double-applies non-idempotent operations); primary-key updates are decomposed into delete+insert that can straddle a batch boundary, violating constraint-ordered apply; idempotence keys derive from LSN+table without the statement index, colliding for multi-statement transactions.
- Distributed fix topology: checkpoint/commit ordering, PK-update decomposition/batching, and idempotence-key construction sit in three modules; each alone leaves a divergence class reachable from some injection point.
- Verifier/invariant surface: for every injection point in the schedule matrix, kill+resume ends byte-equal to the uninterrupted correct state; constraint violations never occur mid-apply; a healthy feed applies identically before and after the fix.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): the archived journal-compaction-replay task (single-store WAL compaction) is the nearest neighbor in the submission archive; this idea differs structurally — cross-system apply semantics (transaction splitting, PK identity, idempotence) graded under exhaustive kill-point injection rather than one store's log replay. rowgroup-prune-mirage shares the database domain but grades plan-independent answers.
- Structural differentiator: the universally-quantified resume property ("from *every* kill point") forces reasoning about atomicity boundaries rather than fixing one repro.
- Evidence paths and retrieval dates: local registry + active-task + submission-stem scan 2026-07-19 (journal-compaction-replay noted as distinct). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the checkpoint-before-commit window, the batch-straddling PK decomposition, and the colliding idempotence keys — each reachable only from particular injection points or feed shapes.
- Synthesize: correctness is a property of the applier's atomicity protocol as a whole; the three bugs interact (a fixed checkpoint order changes which operations the idempotence key must cover).
- Diagnose: symptoms are "replicas drift after incidents, and one feed is wrong even without incidents"; nothing names checkpointing, decomposition, or key construction.
- Navigate coupling: moving the checkpoint after commit without fixing idempotence keys converts double-apply bugs into skipped-apply bugs from other injection points; batching PK updates atomically changes transaction boundaries, which changes the injection schedule the keys must survive — the fixes must be designed as one protocol.
- Reason beyond training: exactly-once apply protocols are well-known *as goals*, but this store's specific checkpoint format, constraint ordering, and feed encoding require original protocol reasoning, not a copied pattern.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The checkpoint record is written in the emission path, before the replica transaction commits — provable by inspecting checkpoint/commit interleaving at an injection point that reliably double-applies.
2. A PK update becomes delete+insert split across batches, so a kill between batches leaves the row absent and a resume violates a foreign-key ordering — provable from the feed encoding plus a specific injection point.
3. Idempotence keys collide for multi-statement transactions (LSN+table only) — provable by finding two statements sharing a key in the feed dump.
4. Fix locations: checkpoint/commit sequencing, feed decomposition/batching, idempotence-key builder — three modules.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): rare and conditional failures (primary); long-horizon causal debugging; SQL/data-state investigation.
- Causal chain (4-8 dependent stages): (1) reproduce clean-run divergence on the multi-statement feed and isolate the key collision; (2) fix keys, run injection matrix, find double-applies, trace checkpoint/commit ordering; (3) reorder the protocol, rerun, find missing-row divergence at batch boundaries; (4) decode the feed to find PK-update decomposition; (5) redesign batching to preserve transaction atomicity; (6) revisit key coverage under the new boundaries; (7) pass the full matrix plus healthy-feed control.
- Heterogeneous evidence surfaces (>= 3): replica database state, checkpoint files, feed dumps (binary/structured), applier logs, injection-schedule configuration.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "the feed itself is corrupt/incomplete" — falsified by a reference sequential apply (slow path) reaching the correct state; H2 "replica constraints reject valid data" — falsified by constraint logs showing violations only under specific interleavings.
- Failing scenario and healthy control: multi-statement and PK-update feeds diverge under injection; a simple insert-only feed converges from every kill point already and must keep doing so with unchanged final state (blocks "truncate and re-apply from scratch" — the harness counts that as a distinct final state via replica-local sequence counters).
- Meaningful-action estimate (20-100, no busywork): ~50-85 (feed decoding, injection-matrix runs, protocol redesign across three modules, convergence sweeps).
- Determinism strategy: kill points are named hooks in the applier reached deterministically by the schedule; no signals, timers, or real crashes; single container, offline.
- Domain and why this is not trivia: tests atomicity-protocol design under interruption — core data-infrastructure engineering — not recall of one database fact.

## Symptoms-only instruction sketch

"After any incident that restarts the sync worker, replicas drift from the source, and one feed disagrees even on clean runs. Ops needs the worker to be kill-safe: however and whenever it is stopped through the archived schedules, resuming must land the replica in exactly the source state, and feeds that sync correctly today must be unaffected."

## Decision notes

Captured 2026-07-19; reshaped to the crash-consistency archetype in the same-day template review. Step 2a watchpoints: injection hooks must be infrastructure (named schedule points), never test-only backdoors that reveal fix sites; the insert-only control plus sequence counters must make wholesale re-apply detectable.
