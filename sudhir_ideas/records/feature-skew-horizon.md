# Idea: Feature Horizon Skew

- Idea ID: `IDEA-0024`
- Slug: `feature-skew-horizon`
- Category: machine-learning
- Languages: TBD (candidate: python, sql)
- Created: 2026-07-19T10:58:41Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A feature store's offline backtests look impossibly good and the deployed model underperforms; the solver must prove where future information leaks into training features and rebuild the pipeline so its backtest is honest.

## Structural archetype

Temporal-leakage audit: the deliverable is a *proof-shaped* repair — the verifier checks that every training feature value is reproducible using only data timestamped before its cutoff (leak-freedom as a checkable property), that offline and online computations agree on frozen fixtures, and that the honest backtest metric lands in a realistic band. Grading a negative information-flow property is unlike any other portfolio idea.

## Novelty fingerprint

- Domain/system: an ML feature platform — event-history store, offline batch feature builder, online serving computation, point-in-time backtest harness, and model training artifacts.
- Failure mechanism: one source joins on record load-time instead of event-time (future data enters features); window buckets are right-inclusive offline but left-inclusive online; a "latest value" feature reads the mutable current row during backfill instead of the as-of snapshot.
- Distributed fix topology: the join semantics, the window bucketing contract (both sides), and the as-of snapshot resolution live in separate components; each alone leaves a measurable leak or an offline/online disagreement.
- Verifier/invariant surface: leak detectors (recompute features with the post-cutoff data removed; values must not change), offline/online parity on frozen entities, and backtest metrics within an honest band established by the leak-free reference.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): tokenizer-serving-rift (IDEA-0016) shares the ML category but is documentation-falsification about preprocessing; this grades an information-flow property over time-indexed data. No feature-store or leakage idea exists elsewhere in the portfolio.
- Structural differentiator: hardness centers on temporal-join semantics and constructing the leak proof, not on artifact forensics or parity per se.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must localize which of dozens of features leak, then find the load-time join, the inclusivity mismatch, and the mutable-row read — none of which throw errors and all of which *improve* offline metrics, hiding in plain sight.
- Synthesize: leakage is a property of the composition of ingestion timestamps, join keys, window arithmetic, and snapshot resolution; the solver needs a causal model of time in the whole platform.
- Diagnose: symptoms are "offline AUC 0.97, production complaints"; suspiciously good is the only signal, and the leading hypothesis space is large (drift, serving bugs, label errors, leakage).
- Navigate coupling: fixing the join drops backtest metrics, which makes the remaining leaks look "fine" relative to the new baseline — the solver must keep auditing past the first fix; aligning window inclusivity changes online values too, so parity fixtures constrain which side must move.
- Reason beyond training: point-in-time correctness over a bespoke event store with mixed timestamp vocabularies (event, load, effective) requires careful original reasoning; generic "avoid leakage" advice does not locate three distinct mechanisms.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. One upstream source's join uses load-time, letting late-arriving records inject future knowledge into past feature rows — provable by the cutoff-ablation detector flagging exactly those features.
2. Offline windows include the right endpoint while the online path excludes it, so boundary events count differently — provable on frozen-entity fixtures at bucket edges.
3. The backfill path for "latest value" features reads the live row, not the as-of snapshot — provable by mutating a row post-cutoff and watching a historical feature change.
4. Fix locations: join resolution in the offline builder, window arithmetic (shared contract), snapshot/as-of resolution in backfill — three components.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): ambiguous production symptoms (primary); SQL/data-state investigation; investigate-plan-implement-verify discipline.
- Causal chain (4-8 dependent stages): (1) reproduce the offline/production gap and rank leakage among competing hypotheses; (2) build/run the cutoff-ablation experiment to prove leakage exists; (3) attribute the first leak to the load-time join; (4) fix it, re-audit, find boundary-event discrepancies, isolate window inclusivity; (5) align the window contract under parity fixtures; (6) re-audit, catch the mutable-row backfill read; (7) rebuild features, verify leak-freedom, parity, and an honest metric band.
- Heterogeneous evidence surfaces (>= 3): event-history database, feature snapshot files, offline builder logs, online computation outputs, training/backtest metric artifacts.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "production traffic drifted from training distribution" — falsified by replaying archived production windows through the offline pipeline and still seeing inflated metrics; H2 "label quality differs" — falsified by label audits on the frozen fixture set.
- Failing scenario and healthy control: time-sensitive features leak; purely static features (and one correctly-joined source) are leak-free and must produce identical values after the fix (blocks nuking the feature set or shifting all timestamps wholesale).
- Meaningful-action estimate (20-100, no busywork): ~45-75 (hypothesis triage, ablation tooling, three isolations with re-audits, rebuild and verification).
- Determinism strategy: frozen event history, fixed cutoffs, deterministic model evaluation (no retraining randomness — fixed seeds or closed-form metric checks); single container, offline.
- Domain and why this is not trivia: temporal-correctness engineering in ML platforms is a paid specialty; the task tests constructing leakage proofs, not reciting the definition of leakage.

## Symptoms-only instruction sketch

"The fraud model backtests at near-perfect discrimination but performs badly in production, and retraining on fresher data makes backtests look even better. Find out why the offline numbers cannot be trusted, make the platform produce features whose backtest honestly predicts production behavior, and keep the historical feature values that are already trustworthy unchanged."

## Decision notes

Captured 2026-07-19; reshaped to the temporal-leakage-audit archetype in the same-day template review. Step 2a watchpoints: the honest-metric band must be derived from the leak-free reference (not a magic number), and leak detectors must be behavioral recomputation, not string/schema proxies (CM-006).
