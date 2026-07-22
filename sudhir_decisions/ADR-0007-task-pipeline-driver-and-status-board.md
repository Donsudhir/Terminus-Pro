# ADR-0007: Single Pipeline Driver, Registry, and Snorkel Status Board

- Status: Accepted
- Date: 2026-07-18
- Task ID: Repository-wide
- Related: ADR-0001 (namespace and single source of truth)

## Context

Task work was driven by re-prompting the lifecycle each chat. There was no
single place to see what every task's phase, gate state, or platform verdict
was. Snorkel platform feedback existed only as large `submission_*.json` blobs
at the repository root, never linked to the tasks they described. The user
asked for easy create/revise, automatic ingestion of platform details into a
visible status surface, and one systematic pipeline every chat follows.

Snorkel's "Terminus-2nd-Edition" platform serves feedback behind app auth and
S3 (`daas-blobs`); this repository holds no API credentials, so an unattended
network pull is not currently possible. The realistic automation is to parse
the exports the user downloads.

## Decision

1. Add `sudhir_task.py` as the single pipeline entry point. It is stdlib-only,
   computes paths from `sudhir_config.toml`, and wraps the existing harness
   scripts (`run_static_checks.py`, `dockerfile_check.py`, `collapse_check.py`,
   `task_integrity.py`, `validate_submission_zip.py`, `approve_task.py`).
2. `sudhir_progress/registry.json` is the source of truth for task state.
   `sudhir_progress/BOARD.md` is its rendered view and is never edited by hand.
3. Lifecycle phases are fixed: idea, step2a, construct, gates, review, package,
   submitted, feedback.
4. `revise` bumps a revision counter and invalidates prior gate and package
   evidence, enforcing the lifecycle rule that any edit reruns gates.
5. Snorkel feedback enters through `sudhir_snorkel/inbox/` (or repo-root
   `submission_*.json`); `ingest` parses difficulty, solvability, static
   outcome, upload time, and per-agent pass rates, then archives the blob so it
   is ingested once. Raw blobs stay untracked; only the parsed registry fields
   are committed.
6. The always-on `sudhir-task-lifecycle` skill and `AGENTS.md` require every
   chat to start with `board` + `ingest` and to route work through the driver.

## Consequences

- One command surface replaces repeated lifecycle prompting.
- Platform verdicts are visible next to the tasks they grade.
- If a real Snorkel API and token appear, `cmd_sync_snorkel` is the single
  extension point to fetch exports into the inbox before `ingest` runs.
- The driver never fabricates oracle/NOP results; those still require Docker
  and Harbor and are recorded only from real job output.
