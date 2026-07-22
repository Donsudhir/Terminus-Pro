# ADR-0016: Policy Synchronization, Dual Verdicts, and Safe Migration

- Status: Accepted
- Date: 2026-07-21
- Task ID: Repository-wide
- Related: ADR-0001, ADR-0004, ADR-0007, ADR-0008, ADR-0010, ADR-0011, ADR-0012, CM-020, CM-021, CM-022, CM-023

## Context

The complete July 2026 Terminus EC documentation audit found that the local
framework is strong on idea validation, anti-collapse review, evidence capture,
checksums, and package parity, but is not synchronized with the current platform
contract. Exact official examples receive incorrect local verdicts, model IDs
are stale, current policy blocks are not exemption-aware, and compatibility and
house rules are mixed together.

The audit also found operational ambiguity. `sudhir_config.toml` names Sudhir
roots as canonical while legacy task and submission directories remain
independently writable and are still used by some tools and tests. The generated
BOARD and hand-maintained STATUS can disagree. Evaluation evidence is not final
acceptance and must never be promoted to acceptance by inference.

A synchronization program must repair current correctness first, preserve
in-flight work, and then make future policy changes observable without allowing
a fetched document or heuristic parser to mutate tasks or evidence silently.

## Decision

1. **Dual verdicts.** Framework results will distinguish:
   - `PLATFORM COMPATIBLE`: current reviewed official policy and published
     checks;
   - `HOUSE EXCELLENCE`: stricter repository rules for uniqueness, difficulty,
     determinism, and training value.

   House failures must never claim upstream authority. Routine new tasks should
   pass both; any house override requires explicit ADR-backed evidence.

2. **Reviewed policy snapshots.** Official policy is a versioned, hashed,
   human-reviewed dependency. Detection and byte-level diffing may be automatic;
   semantic normalization and promotion are not. Precedence is:
   live dated Category Status/Changelog, latest Reviewer Checklist, current
   requirements/check topic pages, detailed guides, then FAQ/examples/glossary.
   Unresolved contradictions produce `policy-review-required`.

3. **In-flight exemptions.** A category, subtype, or structure block applies to
   net-new work from its effective date. Work already in review or revision may
   continue only with source-backed exemption evidence. A boolean without the
   platform/source event is insufficient.

4. **Pre-schema compatibility.** New registry policy fields will be additive.
   Existing records remain readable as `pre-ADR-0016` and
   `grandfathered-pending-review`. Missing fields do not break board or ingest;
   they block only a later package/submit decision when required evidence is
   still absent.

5. **Root roles and safe transition.** The intended writable roots remain those
   configured in `sudhir_config.toml`. Legacy roots are historical or
   compatibility surfaces, but this role is not enforced until every writer is
   inventoried, a shared adapter is implemented, current and historical indexes
   are separated, manifest/hash parity is proved, and rollback is tested. Slice
   1 changes no root defaults and deletes no archive.

6. **Shadow promotion.** New or materially changed checks begin in report-only
   mode, receive positive/negative/false-positive fixtures, and are compared
   across relevant task/layout/language families before blocking. Exact P0
   repairs may use an abbreviated window only with official-source evidence,
   result diffs, adjudication, and rollback.

7. **No silent migration.** A policy change first produces an impact report and
   task-specific migration plan. It never rewrites a task, accepted archive,
   checksum, gate record, exemption, or platform outcome automatically. Task
   edits use the existing revision flow and invalidate dependent evidence.

8. **Selective evidence invalidation.** Evidence is invalidated according to
   what changed. Model changes invalidate difficulty/solvability evidence;
   rubric grammar changes invalidate rubric validation; task/layout changes
   invalidate checksum, gates, oracle/NOP, review, and package evidence.

9. **Acceptance-transition guard.** A task may enter `accepted` only from an
   explicit synchronized platform/reviewer event whose state is `ACCEPTED`.
   HARD difficulty, solvable=true, static PASS, evaluation-passed,
   `EVALUATION_PENDING`, `REVIEW_PENDING`, or `OFFERED` cannot infer acceptance.

10. **Generated status views.** `sudhir_progress/registry.json` remains the
    mutable status source. BOARD and STATUS will be generated in one transaction;
    STATUS is never hand-edited after that generator lands.

11. **Implementation isolation.** The program lands in small slices. Slice 1 is
    decision and baseline repair only. Checker verdict, registry schema, task
    source, model, layout, UI, and root-adapter changes land separately with
    focused and full regression evidence.

## Consequences

- New construction remains frozen until the current compatibility kernel is
  trustworthy. Existing evidenced revisions may continue.
- `rowgroup-prune-mirage` remains an in-flight data-processing revision; its
  exemption must be captured before a later package/submit decision.
- Current house rules such as hard-only, no Python-primary solvable core,
  offline-by-default, and oracle 10x remain active unless superseded by another
  ADR, but are labeled as house policy.
- Historical model and policy evidence remains readable but cannot satisfy a
  current-policy claim without an explicit risk decision.
- Policy sync, dual verdict, platform adapter, root migration, and predictive
  migration require subsequent isolated implementation slices.

## Rollback

This ADR is superseded, never edited. Before enforcement code lands, rollback is
simply a new ADR choosing a different architecture. After enforcement lands:

- reactivate the previous policy snapshot;
- demote changed checks to report-only;
- restore previous root defaults through the tested adapter mapping;
- retain all policy history, raw evidence hashes, exemptions, migrations, and
  accepted archives;
- reinstate the manual CM-020 through CM-023 pre-upload controls until repaired
  mechanical gates are active again.

No rollback may delete historical evidence or convert an inferred evaluation
result into acceptance.
