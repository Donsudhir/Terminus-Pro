# ADR-0019: Canonical Root Adapter and Historical Read-Only Enforcement

- Status: Accepted
- Date: 2026-07-21
- Task ID: Repository-wide
- Related: ADR-0001, ADR-0004, ADR-0007, ADR-0016, CM-023

## Context

ADR-0016 defined root roles but deferred enforcement until every writer was
inventoried, current and historical indexes were separated, parity was proved,
and rollback was tested. The inventory found one production task/package driver
and several compatibility defaults or manual commands. The largest operational
risk was documentation that still instructed authors to write new archives into
`Task_Ready_To_Submit/`, leaving a stale historical copy beside a newer canonical
archive.

The registry is the status source of truth, but BOARD, IDEA_INDEX, and STATUS
were not generated as one grouped view update. The current submission index was
stored as a regression fixture and required manual refresh after packaging.

## Decision

1. `root_adapter.py` is the only production resolver for canonical and
   historical workspace roots.
2. Canonical writable roots are loaded from `sudhir_config.toml`, with explicit
   `TB3_*` environment overrides:
   - `sudhir_tasks/active/`;
   - `sudhir_ideas/specs/`;
   - `sudhir_tasks_ready_to_submit/`;
   - `sudhir_reviews/`;
   - `sudhir_logs/jobs/`.
3. `tasks/`, `specs/`, and `Task_Ready_To_Submit/` are compatibility or
   historical read surfaces. Production writes through those accessors raise
   `HistoricalRootWriteError`.
4. The tracked Step 2a validation schema remains an explicit read-only input at
   `specs/validation_schema.json`; generated Step 2a state and specs write only
   to the canonical spec root.
5. Current and historical indexes have distinct ownership:
   - current: `sudhir_progress/CANONICAL_SUBMISSION_INDEX.json`, refreshed
     atomically by package/revise transactions;
   - historical: `repo_tests/fixtures/submission_index.json`, changed only by an
     explicit historical-index command.
6. Package creation writes only to the canonical root. A package or index
   failure restores the previous canonical ZIP. Revision invalidation removes
   only the canonical current ZIP and refreshes the current index; historical
   evidence is never deleted.
7. BOARD, IDEA_INDEX, and STATUS are generated from one registry snapshot with
   one generation digest. Their grouped replacement restores prior bytes if any
   replacement fails.
8. Active command/rule/workflow guidance uses canonical environment variables or
   `sudhir_task.py package`. Historical archive examples are explicitly
   read-only reference usage.
9. No task source, accepted archive, historical archive, checksum, or platform
   outcome is migrated or deleted automatically.

## Rollback

`legacy_rollback_roots()` provides the pre-migration mapping for an explicit code
rollback. Rollback may restore old defaults but must not delete either archive
population or overwrite current/historical indexes with each other. Re-enable
CM-023 manual controls until the adapter is repaired.

## Consequences

- New writes cannot silently create a second mutable task/spec/archive copy.
- Current index drift is repaired in the same package/revise operation that
  changed the current archive population.
- Historical uniqueness and regression reads remain available.
- Generated STATUS can no longer disagree with BOARD by being hand-maintained.
