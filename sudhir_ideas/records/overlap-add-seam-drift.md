# Idea: Streaming Convolution Seam Drift

- Idea ID: `IDEA-0019`
- Slug: `overlap-add-seam-drift`
- Category: scientific-computing
- Languages: TBD (candidate: c, python)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A streaming signal-processing engine that is numerically correct on short runs degrades on long runs — state and memory grow without bound and throughput collapses — and it must be repaired without changing a single output bit.

## Structural archetype

Performance-and-memory regression under a bit-exactness handcuff: the verifier grades stable work metrics (allocation counts, state-size bounds, operation ratios) alongside bit-identical outputs. The tension — improve the resource profile while forbidden from touching numerics — is the core difficulty. No other portfolio idea grades resource behavior as the outcome.

## Novelty fingerprint

- Domain/system: a chunked streaming convolution/filtering engine — block scheduler, boundary-state ring buffer, transform-plan cache, and normalization stage — processing long fixture streams.
- Failure mechanism: the ring buffer's retirement condition compares against the wrong epoch counter for block sizes that do not divide the kernel span, so boundary state accretes; the plan cache key omits stride so incompatible plans accumulate; a normalization rescan is quadratic because an earlier refactor broke a partial-sum invariant (the refactor is visible in bundled patch-history artifacts).
- Distributed fix topology: retirement logic, cache keying, and the partial-sum invariant restoration live in three modules; each alone leaves a different unbounded-growth or quadratic term.
- Verifier/invariant surface: bit-exact equality with current outputs on all fixtures; bounded state size across long streams; allocation and operation counts within generous ratio envelopes; no wall-clock one-shot thresholds.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): reproducible-reduction-parity (IDEA-0007) shares the numerical-streaming domain but grades cross-implementation numerical parity; this idea grades resource behavior with numerics frozen — opposite constraint direction. The quarantined ffmpeg import is provenance-only; no semantic reuse.
- Structural differentiator: the solver's enemy is asymptotic behavior, not wrongness; every naive "optimization" that changes summation order fails the bit-exactness gate.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the wrong-epoch comparison (only for non-divisor block sizes), the incomplete cache key, and the broken partial-sum invariant — the last one recoverable only by reading bundled patch history to learn what the invariant used to be.
- Synthesize: the growth curve observed at the top is the sum of three independent leaks with different growth rates; separating them requires instrumented experiments across configurations.
- Diagnose: symptoms are "long jobs slow down and get OOM-killed"; nothing names the ring buffer, the cache, or normalization.
- Navigate coupling: restoring the partial-sum invariant is only bit-safe if accumulation order is preserved exactly; fixing retirement changes which states exist for the cache to key, so fixes interact and must be sequenced with re-measurement.
- Reason beyond training: generic "profile and cache" advice fails against the bit-exactness handcuff; the engine's bespoke epoch/segment bookkeeping is not a library pattern.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Boundary-state retirement compares segment epochs against the block counter, which only coincide when the block size divides the kernel span — provable by state-size instrumentation across block-size configs.
2. The plan cache key omits stride, so plans for every distinct stride accumulate and thrash — provable from cache statistics counters.
3. Normalization was O(n) via partial sums until a bundled historical patch dropped the running-sum update on one code path; the invariant must be reconstructed from that history to restore it bit-safely.
4. Fix locations: ring-buffer retirement, plan-cache keying, normalization partial-sum path — three modules.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): measured performance and memory work (primary); long-horizon causal debugging; Git/history reasoning.
- Causal chain (4-8 dependent stages): (1) reproduce degradation with the bundled long-stream driver and metric counters; (2) separate memory growth from compute growth by config sweeps; (3) attribute state growth to non-divisor block sizes, isolate the epoch comparison; (4) fix retirement, re-measure, find allocation churn persists, isolate cache keying; (5) fix keying, re-measure, find quadratic time remains, trace normalization; (6) recover the lost invariant from patch history and restore it order-exactly; (7) verify bit-exactness plus all metric envelopes.
- Heterogeneous evidence surfaces (>= 3): runtime metric counters, memory/state instrumentation, patch-history artifacts, configuration matrix, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "input fixtures grow harder over time" — falsified by re-running an early chunk window late in the stream and seeing identical per-chunk cost; H2 "allocator fragmentation" — falsified by counter evidence that live state itself grows.
- Failing scenario and healthy control: non-divisor block sizes and multi-stride jobs degrade; divisor-block single-stride jobs are already bounded and must keep identical outputs and metrics (blocks "rewrite the engine" approaches).
- Meaningful-action estimate (20-100, no busywork): ~45-75 (instrumented sweeps, three isolations with re-measurement, history recovery, final verification).
- Determinism strategy: fixed fixtures and seeds; metrics are counted work (allocations, operations, state sizes), never wall-clock; single container, offline.
- Domain and why this is not trivia: tests performance engineering under numerical-stability constraints — a real HPC/DSP discipline — not knowledge of one FFT fact.

## Symptoms-only instruction sketch

"Production streaming jobs start fast and end crawling; the longest ones get OOM-killed around hour six, and ops noticed memory climbing roughly with the number of distinct job shapes. Short validation runs are numerically perfect. Make long runs sustain their early resource profile. Outputs must remain bit-for-bit identical to today's on every archived fixture."

## Decision notes

Captured 2026-07-19; reshaped to the performance/memory archetype in the same-day template review. Step 2a watchpoints: metric envelopes must be generous ratios per the philosophy doc (no fragile thresholds), and the bit-exactness gate must cover enough fixture diversity that reordering-based "optimizations" reliably fail.
