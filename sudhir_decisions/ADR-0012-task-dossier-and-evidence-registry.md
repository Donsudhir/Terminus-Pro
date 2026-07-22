# ADR-0012: Task Dossier and Evidence Registry

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Related: ADR-0007, ADR-0010, ADR-0011

## Context

The pipeline driver tracks phase, cheap gates, and a zip path, while
COMMON_MISTAKES captures lessons by hand. Platform revisions still left
reviewer prose, rubrics, Harbor job IDs, and zip hashes in chat or STATUS.md.
`revise` invalidated gates but did not open a durable revision workspace, so
the next chat had to rediscover why the revision existed.

## Decision

1. **Per-revision dossier** under `sudhir_reviews/<slug>/REV-<n>/` holds
   human-readable artifacts for that revision:
   - `NOTES.md` — why the revision opened
   - `FEEDBACK.md` — pasted or captured reviewer text
   - `PLATFORM.md` — sanitized ingest snapshot (no raw Snorkel blob)
   - `DIFFICULTY.md`, `SOLUTION.md`, `VERIFICATION.md` — Snorkel form paste
     fields submitted with the task (exact text we uploaded)
   - `RUBRIC.md` — UI rubric paste for that revision
   - `PREUPLOAD.md` — CM / evidence checklist; required before `package`
   - `EVIDENCE.md` — Harbor job pointers recorded by the driver
   - `CM-SUGGESTIONS.md` — keyword-proposed CM ids from feedback/ingest

2. **Registry extensions** (backward-compatible) on each task entry:
   - `package.sha256`, `package.member_count`
   - `evidence.oracle_1x|nop|oracle_10x` → `{job, mean, at, path}`
   - `revisions[]` → `{n, reason, opened_at, feedback_ref, rubric_ref, zip_sha, cm_ids}`
   - `learning.cm_hits[]`, `learning.patterns_applied[]`

3. **Driver commands** (stdlib, in `sudhir_task.py`):
   - `revise` creates `REV-<n>/` and appends `EDIT_LEDGER.md`
   - `evidence` records Harbor `result.json` means into registry + dossier
   - `feedback-capture` / `rubric-capture` / `form-capture` write dossier files
     (including difficulty/solution/verification/rubric paste fields) and
     suggest CM ids
   - `learn-check` prints applicable CM preventions; fails if PREUPLOAD incomplete
   - `package` stores zip SHA-256 and refuses unless PREUPLOAD has no unchecked
     `- [ ]` items (override with `--force`)
   - `ingest` writes `PLATFORM.md` + `CM-SUGGESTIONS.md` under the current REV;
     when the export carries `test_rubrics`, copy into `RUBRIC.md` if empty

4. **Mechanical learning**: encode file-checkable CM rows as gate FAILs (CM-007
   in `run_static_checks.py`). Advisory CMs remain checklist items in
   PREUPLOAD and COMMON_MISTAKES.

5. **Success surface**: `sudhir_knowledge/WHAT_WORKED.md` is loaded at chat
   start beside COMMON_MISTAKES.

Raw Snorkel exports stay untracked (ADR-0007). Harbor jobs are never invented;
`evidence` only records parsed `jobs/<id>/result.json` output.

## Consequences

- Every revision has a stable path for feedback, rubric, and proof jobs.
- Package cannot ship without a conscious pre-upload walk (or explicit `--force`).
- Repeat pytest cwd-shadow failures fail static checks before upload.
- Agents still must not claim PASS without command evidence.
