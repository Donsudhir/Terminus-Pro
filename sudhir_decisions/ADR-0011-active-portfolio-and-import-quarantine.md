# ADR-0011: Active Portfolio and Import Quarantine

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Supersedes: the assumption in ADR-0008 that every backfilled export belongs in the active portfolio

## Context

The first idea-registry backfill treated every root-level `submission_*.json` export as an active historical idea. Five May 2026 exports were therefore shown beside current work even though the user did not recognize them. Their JSON provenance points to the same platform project ID but older assignment IDs, and none of their submission IDs appears in the authoritative six-submission listing returned on 2026-07-19.

The same reconciliation confirmed three known current states: Musl Sysroot Splice is `REVIEW_PENDING`, Robust Predicate Scale Parity is `EVALUATION_PENDING`, and Sparse Jacobian Color Contract remains under local development.

## Decision

1. The default idea portfolio and pipeline show only recognized active work.
2. Unrecognized or stale imports are never deleted. They move to `portfolio_scope = quarantined`, their idea status becomes `retired`, and their source export, project/assignment/submission IDs, upload date, evidence, and reason remain in the registry.
3. Generated views place quarantined imports in a separate provenance table and exclude them from active idea/task totals.
4. `grandfathered` means a user-recognized active task that predates the structured uniqueness dossier. It may continue through its existing lifecycle but carries an explicit warning rather than fabricated retrospective proof.
5. Live platform stages include `in-evaluation` and `in-review`. Direct project-list evidence overrides stale feedback embedded in an older export.
6. Work at construction, gates, internal review, or pre-submission packaging remains labeled `IN DEVELOPMENT`; packaging is not execution completion until a submission exists.
7. Re-ingesting a quarantined root export may refresh its provenance but must never reactivate it.

## Reconciled records

- Musl Sysroot Splice: grandfathered, submitted, in review.
- Robust Predicate Scale Parity: approved, submitted, in evaluation.
- Sparse Jacobian Color Contract: approved, in development, not submitted.
- Cluster Green Tail Red, FFmpeg Filtergraph Regression Lab, Hazard Evac Flow Lab, Legacy PLC Wire Restore, and Maritime Lane Weather Weave: quarantined historical imports.

## Consequences

The main portfolio now answers “what are we actually working on?” without losing the audit trail explaining how stray records appeared. Unknown imports cannot silently influence active counts or next actions, and current platform stages remain evidence-backed.
