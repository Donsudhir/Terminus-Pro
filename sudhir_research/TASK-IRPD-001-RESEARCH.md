# TASK-IRPD-001 — input-ring-physics-desync — Super-Uniqueness Dossier

- Idea: `input-ring-physics-desync` (IDEA-0034)
- Category: games
- Archetype: long-horizon investigation — fixed-timestep input-ring / physics consumption desync where tick-count overlays stay green, short healthy-control replays stay bit-stable, and long same-seed replays diverge on entity state digests
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** a headless fixed-timestep game simulation with recorded inputs, an input ring/buffer, physics integration, and entity state digests under seed control.
2. **Failure mechanism:** live sessions look fine; replays of the same seed diverge in entity state digests after a few hundred ticks while tick-count overlays remain green; a short healthy-control replay stays bit-stable.
3. **Distributed fix topology:** input-ring enqueue/dequeue vs tick authority, physics step consumption of buffered inputs, and digest/hash sampling must coordinate. Approximate physics or tick-count-only repairs are rejected.
4. **Verifier/invariant surface:** failing long replays must match recorded outcome digests; short healthy controls remain bit-stable; tick-count bait must not be treated as success.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` on 2026-07-23.

Games neighbours:

- `lockstep-replay-fray` (IDEA-0020) — lockstep ordering/RNG/event-queue tie-break contracts across a seed matrix; not input-ring vs physics consumption with tick-count-green / short-control bait.
- `procgen-seed-shear` (IDEA-0029, **rejected**) — structural duplicate of lockstep (deterministic regeneration divergence); slug reserved; world-border RNG/cache invalidation, not input-ring physics.
- `save-lineage-exhume` (IDEA-0031) — legacy save-format migration/recovery; different mechanism.

Differentiation vs IDEA-0020 / rejected IDEA-0029: IRPD’s failure ontology is **input-buffer/ring coupling to fixed-timestep physics** with a **duration-gated healthy control**, not entity-iteration/RNG/event-queue ordering (lockstep) and not procgen border regeneration. Shared “replay digests” surface is not sufficient for collision under the super-uniqueness gate. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: no games / deterministic-replay / input-buffer task. **No collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Strict content scan of `Task_Ready_To_Submit/` and `sudhir_tasks_ready_to_submit/` for `input.?buffer|input.?ring|fixed.?timestep|lockstep|procgen|state.?digest` (2026-07-23): **0 hits**. Loose “deterministic replay” phrasing appears in unrelated audit/heal tasks without game input-ring physics. **No collision.**

### 4. Upstream corpus

Local `tasks/` and prior TB research notes contain no Terminal-Bench public task whose core is input-ring / fixed-timestep physics desync with tick-count bait and short healthy-control parity. **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `Terminal-Bench deterministic replay input buffer fixed timestep physics desync game simulation`
- Industry notes on fixed-timestep replay, input recording, and desync (inspiration only)

External engineering discusses real input-record / fixed-timestep desync modes. No public Terminal-Bench task instance, patch, or test suite was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is a single-player replay harness where the input ring and physics integrator disagree under long traces while short traces and tick counters look healthy. Generic “seed the RNG” or “use fixed timestep” advice does not repair ring/physics consumption contracts graded by digest parity.

## Closest analogue and structural difference

- **Closest analogue:** captured `lockstep-replay-fray` (IDEA-0020); rejected neighbour `procgen-seed-shear` (IDEA-0029) is the same lockstep archetype and is not reused.
- **Structural difference:** this idea’s core is **input-ring buffering vs fixed-timestep physics consumption** judged by **long-replay entity digests** with **tick-count-green bait** and a **short bit-stable healthy control** — not lockstep entity/RNG/event ordering, and not procgen world regeneration.

## Result

Uniqueness PASS for `input-ring-physics-desync`. Do not start Step 2a in this session.
