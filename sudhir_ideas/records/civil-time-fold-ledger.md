# Idea: Recurring Billing Fold Drift

- Idea ID: `IDEA-0014`
- Slug: `civil-time-fold-ledger`
- Category: data-processing
- Languages: TBD (candidate: python, sql)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

A recurring billing engine mischarges subscribers on specific local dates; the deliverable is both a repaired engine and a restated correction ledger for a year of already-issued invoices.

## Structural archetype

Repair-plus-restatement: the solver must fix forward behavior AND back-compute a historically correct restatement artifact from stored records. The verifier grades the restatement ledger and future invoices together; no other portfolio idea requires reconstructing corrected history as an output.

## Novelty fingerprint

- Domain/system: subscription billing and scheduling over civil time — recurrence expander, proration module, shared timezone loader, and an invoice database with a year of issued invoices.
- Failure mechanism: DST fold instants collapsed by a UTC round-trip in recurrence anchoring; proration that divides by fixed 86400-second days; two components pinned to different tzdata snapshots so recently-changed zones disagree.
- Distributed fix topology: recurrence expander, proration arithmetic, tz snapshot unification, and the restatement generator must agree; fixing only forward behavior leaves the restatement wrong, and vice versa.
- Verifier/invariant surface: restated ledger balances to the corrected amounts per subscriber-month; future invoices correct across DST folds, gaps, and zone-rule changes; untouched-control subscribers restate to zero delta.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): no civil-time or billing idea exists in the local portfolio; nearest internal shape is generic pipeline-parity work, which this differs from by grading a reconstructed historical artifact rather than agreement between two computations.
- Structural differentiator: the hard half is deriving what *should have been billed* from stored evidence — an inverse computation the engine never implemented.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must find the UTC round-trip that collapses fold-time anchors, the fixed-86400 proration divisor, and the tzdata version skew — none named anywhere.
- Synthesize: correct restatement requires composing recurrence semantics, proration arithmetic, and zone-rule history; no module contains the whole billing meaning.
- Diagnose: symptoms are finance complaints ("some customers double-charged in autumn, some unbilled in spring"); nothing mentions DST, tzdata, or proration.
- Navigate coupling: repairing recurrence anchors changes which periods exist, which changes proration inputs, which changes the restatement; each partial fix produces a *differently wrong* ledger.
- Reason beyond training: fold/gap disambiguation interacting with proration and version-skewed zone rules is not a textbook datetime exercise; the restatement inverse has no library recipe.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. Recurrence anchors pass through a naive UTC round-trip that picks the first fold occurrence regardless of the subscription's anchor policy — visible only by correlating invoice timestamps with zone transition tables.
2. Proration divides by 86400 seconds, so 23h/25h local days mis-prorate — visible from invoice line deltas on transition days only.
3. The scheduler and the invoice renderer load different tzdata snapshots; a zone whose rules changed mid-year drifts only after the change date.
4. Fix locations: recurrence expander, proration module, shared tz loader, restatement generator — distinct roots.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): rare and conditional failures (primary); SQL and data-state investigation; long-context state retention.
- Causal chain (4-8 dependent stages): (1) query the invoice DB to characterize which subscriber-dates are wrong; (2) correlate wrong dates with zone transition tables to form the DST hypothesis; (3) reproduce one wrong invoice through the engine to isolate the anchor collapse; (4) fix anchors, find transition-day amounts still wrong, isolate proration; (5) fix proration, find one zone still drifting after a mid-year rule change, isolate tzdata skew; (6) unify snapshots; (7) build the restatement from stored records and reconcile totals.
- Heterogeneous evidence surfaces (>= 3): invoice database state, scheduler logs, tzdata artifacts, engine configuration, code.
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "decimal rounding bug" — falsified by exact recomputation on non-transition days matching stored invoices; H2 "corrupted subscriber records" — falsified by replaying a clean subscriber fixture through the failing date and reproducing the error.
- Failing scenario and healthy control: fold/gap dates and the rule-changed zone fail; UTC-anchored subscribers and non-transition dates are correct and must restate to zero delta (blocks blanket recomputation hacks).
- Meaningful-action estimate (20-100, no busywork): ~45-75 (DB queries, transition-table correlation, three isolations, restatement construction, reconciliation).
- Determinism strategy: all invoices, clocks, and tz snapshots are fixtures; the engine runs on a virtual "today"; offline, single container.
- Domain and why this is not trivia: tests temporal-semantics engineering and inverse reconstruction over real money artifacts, not recall of one tzdata fact; every rule is discoverable from the data.

## Symptoms-only instruction sketch

"Finance flagged a year of invoices: some subscribers were double-charged on certain autumn dates and others missed a charge in spring, and one region drifts by an hour since mid-year. Produce a restatement ledger with the correct amounts for every issued invoice, and make the engine bill correctly going forward. Subscribers that were billed correctly must show zero restatement delta."

## Decision notes

Captured 2026-07-19; reshaped same day to the repair-plus-restatement archetype after the portfolio-template review. Step 2a watchpoints: the restatement must not be derivable by re-running the fixed engine alone (stored records include manual adjustments the engine never saw), and instruction nouns (fold, proration, tzdata) must not name fix-path symbols.
