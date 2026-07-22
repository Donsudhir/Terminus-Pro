# AGENTS.md

Edition 2. Read `docs/ARCHITECTURE.md` and `sudhir_knowledge/TASK_LIFECYCLE.md`.

## Pipeline (every chat)

Run `sudhir_task.py board`, then `ingest`; registry JSON is truth. Before
packaging read `COMMON_MISTAKES.md` and `WHAT_WORKED.md`. New work first outputs
the 4 proposal fields and stops for Check feedback,
then run `idea new` + `idea proposal`. Construction needs proposal PASS,
uniqueness + Step 2a GO. `outcome` requires evidence;
evaluation-passed is not acceptance. Inbox: `sudhir_snorkel/inbox/`.

## Routing

Commands/process: `commands.md`, `workflow.md`, `REPO_CONVENTIONS.md`. Author,
review, and communication detail lives under `.cursor/rules/`.

## Always

1. Read commands from files, not memory.
2. Offline only; install dependencies in the Dockerfile.
3. Step 2b: preflight + oracle 1x + NOP. Step 4 only: oracle 10x.
4. Edits invalidate evidence; rerun gates. Never alter checksums.
5. Claim no status without command output.
6. Store every form paste in `REV-<n>/`.
7. Require `.dockerignore`; clean Docker after packaging.
8. Log new failures in `COMMON_MISTAKES.md` immediately.
9. No Python-primary solvable core (ADR-0014); verifier-only pytest is fine.

## Shipping

Follow `validate_submission_zip.py` and `REPO_CONVENTIONS.md`; never ship
authoring metadata, checksums, metrics, rubrics, or AI scaffolding.
