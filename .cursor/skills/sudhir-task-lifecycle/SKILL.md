---
name: sudhir-task-lifecycle
description: "Use when Sudhir asks to create, research, validate, review, fix, package, submit, or improve a Terminal-Bench or TERMINUS task. Loads the full namespaced lifecycle, ADR, logging, knowledge-graph, Docker, review, rubric, and submission-output requirements so the user never has to repeat them."
disable-model-invocation: false
---

# Sudhir Task Lifecycle

Every chat that touches task work follows the same pipeline driver. Do not
invent an ad-hoc process; use `sudhir_task.py` so status stays in one place.

## Start of every chat

1. Run `python3 sudhir_task.py board` and read `sudhir_progress/BOARD.md` to see
   every idea and task, including separate uniqueness, execution, submission,
   acceptance, phase, gate, and Snorkel states.
2. Run `python3 sudhir_task.py ingest` to pull any new Snorkel exports from
   `sudhir_snorkel/inbox/` (or repo-root `submission_*.json`) onto the board.
3. Read [the common mistakes ledger](../../../sudhir_knowledge/COMMON_MISTAKES.md)
   and [what worked](../../../sudhir_knowledge/WHAT_WORKED.md); apply every
   matching prevention and reuse pattern (Dockerfile Python/asciinema, pytest
   CM-007, behavioral graders, ablation subsets).
4. Read [the canonical lifecycle](../../../sudhir_knowledge/TASK_LIFECYCLE.md),
   `sudhir_progress/STATUS.md`, the current plan, relevant ADRs, and the idea,
   research, and knowledge-graph records for the task in play.
5. If the task is in feedback/Needs Revision, open
   `sudhir_reviews/<slug>/REV-<n>/` (or run `feedback-capture` / `ingest`) so
   reviewer text and form paste fields are not left only in chat.

## First step for every new task idea: proposal check

Before uniqueness research, Step 2a, task registration, or file creation:

1. Read `web/idea-inspiration-sources.md` and use its source ladder as the
   default inspiration pool. Sources are leads, not task/test/patch content to
   copy; current eligibility and uniqueness rules always win.
2. For the single candidate selected to enter the lifecycle, output only these
   four paste-ready Snorkel fields first:
   - **Task Idea Summary** — 2–5 clear sentences;
   - **Idea Category** — one exact platform display label;
   - **Associated Skills** — 5–10 comma-separated skills;
   - **Task Tags** — 3–6 comma-separated tags.
3. Stop. Ask Sudhir to paste the fields into **Task Idea Proposal** and run
   **Check feedback**. Do not continue merely because the draft sounds strong.
4. After Sudhir returns the platform result, capture the idea permanently and
   record the fields/verdict/evidence with `idea proposal`. Failed proposals
   are revised and rechecked or retained as rejected; they are not silently
   recycled.
5. Only proposal=`passed` may proceed to uniqueness and Step 2a. A proposal
   pass is an early signal, not uniqueness PASS, Step 2a GO, difficulty, or
   acceptance.

## Pipeline driver (`sudhir_task.py`)

The driver is the single entry point; the registry
(`sudhir_progress/registry.json`) is the source of truth and the board is its
rendered view. Common flow:

- `idea new <slug>` — capture a permanent idea before starting work.
- `idea proposal <slug> pending|passed|failed …` — store the four proposal
   fields plus platform Check feedback evidence; PASS gates uniqueness.
- `idea uniqueness <slug> …` — record the novelty fingerprint, collision scopes,
  nearest analogue, structural difference, and evidence.
- `idea validation <slug> go|stop …` — persist Step 2a outcome and evidence.
- `idea list` / `idea validate` — inspect or check the portfolio.
- `new <slug> [--category --languages]` — register a task, scaffold its idea record.
- `phase <slug> <phase> [--next "…"]` — record lifecycle progress.
- `gates <slug>` — run static + dockerfile + collapse + integrity gates and store results.
- `revise <slug> [--reason …]` — open `REV-<n>/` dossier; invalidate gate/package
  evidence (lifecycle rule: any edit reruns gates).
- `evidence` / `feedback-capture` / `form-capture` / `rubric-capture` — store
  Harbor jobs and every Snorkel form paste (difficulty, solution, verification,
   rubric) under the current REV. Difficulty/Solution/Verification are an atomic
   acceptance-safe Humanizer set; platform requirements, task truth, and
   project rules outrank style.
- `learn-check <slug>` — print applicable CM preventions; verify PREUPLOAD.
- `package <slug>` — build zip, store SHA-256; requires PREUPLOAD checklist
  (or `--force`).
- `ingest` / `sync-snorkel` — refresh platform feedback into registry +
  `PLATFORM.md`.
- `outcome <slug> <status>` — record explicit reviewer/platform evidence; an
  evaluation pass is not acceptance.

Phases: idea → step2a → construct → gates → review → package → submitted → feedback.

## Non-negotiables

1. Source `scripts/sudhir-env.sh` before running raw harness commands.
2. Task path is `${TB3_TASKS_DIR}/<task-name>`, spec under `${TB3_SPECS_DIR}`,
   final zip under `${TB3_SUBMISSIONS_DIR}`. `sudhir_` paths are canonical; never
   keep two mutable copies. Substitute these roots for any hardcoded `tasks/`,
   `specs/`, or `Task_Ready_To_Submit/` example in legacy `tb3-*` skills.
3. Stop before construction unless the category is allowed, the baseline is
   trustworthy, the full super-uniqueness dossier passed, and Step 2a returned GO.
4. Never claim a gate passed without current command evidence.
5. Before ending a session, update the exact idea/task transition, run
   `sudhir_task.py idea validate` and `sudhir_task.py board`, then update the
   changelog, STATUS, ADRs, and knowledge graph.
6. New platform rejection or local surprise: append
   `sudhir_knowledge/COMMON_MISTAKES.md` and a `FAILURE-*` graph node in the
   same session (ADR-0010). Do not leave the lesson only in chat.
7. Before upload: load `terminus-dsv-humanizer`, preserve acceptance semantics,
   and capture all three DSV fields together so the audit is created. Capture
   the rubric, record Harbor
   `evidence`, tick PREUPLOAD, then `package`. Direct DSV pastes do not satisfy
   the gate.
