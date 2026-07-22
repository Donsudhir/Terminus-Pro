# ADR-0001: Sudhir Namespace and Source of Truth

- Status: Accepted
- Date: 2026-07-18
- Decision owners: Sudhir and the repository task agent

## Context

Task sources, submission archives, prompts, reviews, and personal artifacts are currently mixed with upstream repository paths. Some upstream paths are ignored or hardcoded by tools, and maintaining copied task trees would create drift. The repository needs a durable personal namespace without breaking Terminal-Bench and Harbor compatibility.

## Decision

Use top-level `sudhir_` folders as the canonical ownership boundary for personal task development, research, decisions, logs, plans, reviews, knowledge, and final archives. Canonical editable task source lives under `sudhir_tasks/active/<task-name>/`. Upstream paths are compatibility surfaces only and must never become independently editable duplicates.

Existing tools will be extended or wrapped to accept the canonical paths. If temporary staging under an upstream path is unavoidable, it must be generated, traceable, and deleted or regenerated from canonical source rather than edited directly.

## Consequences

### Positive

- Personal work is easy to identify and preserve.
- One source of truth prevents source and zip drift.
- Logs, research, decisions, and final artifacts have explicit owners.
- Future automation can index a stable namespace.

### Negative

- Existing skills and scripts that hardcode `tasks/`, `specs/`, or `Task_Ready_To_Submit/` need adapters.
- The regression suite must be updated carefully so namespacing does not hide upstream defects.

## Follow-up

- Implement path adapters during the Gold Harness Repair phase.
- Add ignore rules for generated checksums, metrics, caches, and temporary staging under `sudhir_tasks/`.
- Do not move historical artifacts until they have been indexed and preserved.
