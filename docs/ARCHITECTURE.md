# ARCHITECTURE — short codemap for the TB3 harness

This is a one-page map of which file owns which layer. For policy see
`AGENTS.md` and `.cursor/rules/`; for commands see `commands.md`; for
conventions see `REPO_CONVENTIONS.md`. This file is not the place for
any of those.

## Root roles

- `root_adapter.py` — sole resolver for canonical writable roots and historical
  read-only compatibility roots.
- `sudhir_tasks/active/` — canonical writable task source.
- `sudhir_ideas/specs/` — canonical writable Step 2a state/spec evidence.
- `sudhir_tasks_ready_to_submit/` — canonical writable current submissions.
- `Task_Ready_To_Submit/` — immutable historical/reference archive corpus.
- `tasks/` and `specs/` — compatibility/read surfaces only; production writes
  are rejected by the adapter.

## Task spec layer (Step 1 / 2a)

- `sudhir_ideas/specs/<task>.md` — Authoring Brief + Reviewer Appendix +
  Triviality Ledger + Per-gate Pitfall Inventory + Initial Draft
  Commitments. Pre-commitment artifact for the task.
- `sudhir_ideas/specs/<task>-validation-log.md` — attempt history, gate failures,
  dirty-flag triggers, CNI references, draft-commitment drift.
- `sudhir_ideas/specs/.<task>-state.json` — `validate_loop.py` state machine.
- `sudhir_ideas/specs/README.md` — schema documentation for the above.
- `validate_loop.py` — runs Step 2a; new loops use evidence contract v3 and
  require the additive long-horizon `investigation_profile` while legacy state
  remains readable.
- `lint_spec.py` — checks the new mandatory sections.

## Task implementation layer (Step 2b)

- `sudhir_tasks/active/<task>/` — canonical task source.
- Standard layout: `instruction.md`, `task.toml`, `output_contract.toml`,
  `environment/`, `solution/solve.sh`, and pytest under `tests/`.
- Milestone layout: global `task.toml`/`environment/` plus
  `steps/milestone_N/{instruction.md,tests/,solution/}`; no deprecated root
  instruction/tests/solution. Full contract: `task-creation.mdc`.
- `.step2b-checksum` — local generated integrity state; see conventions.

## Static / collapse layer (Step 2b gates)

- `run_static_checks.py` — instruction, dockerfile, test layout,
  output contract, hidden instructions, milestone language.
- `collapse_check.py` — oracle locality, frontier concentration,
  grep resistance.
- `verifier_health.py` — verifier shape sanity.
- `ci_checks/` — focused single-purpose checks (canary, dockerfile
  references, test sanity, etc.) usable independently of the umbrella.
- `task_integrity.py` — shared checksum module used by both
  `scripts/check-task.sh` and `approve_task.py`.

## Packaging / approval layer (Step 4)

- `scripts/check-task.sh` — one-command preflight (static + collapse
  + tmp-zip-validate + checksum stamp). Not Step 2b PASS.
- `validate_submission_zip.py` — validates a built submission zip.
  Owns `FORBIDDEN_ROOT_FILES`, `BANNED_AI_FILENAMES_CI`, and
  `BANNED_AI_DIRECTORY_NAMES_CI`.
- `approve_task.py` — final approval. Verifies `.step2b-checksum`
  before packaging.
- `sudhir_progress/CANONICAL_SUBMISSION_INDEX.json` — generated current ZIP
  index, refreshed by package/revise transactions.
- `repo_tests/fixtures/submission_index.json` — immutable historical-corpus
  regression index.
- `dsv_humanizer.py` — acceptance-safe atomic DSV policy and hash audit.

## Task skeletons

- `skeleton/Default_Task_Skeleton/` — standard offline verifier template.
- `skeleton/milestone_template/` — milestone layout + offline per-step runners.

No UI scaffold is shipped; exempt revisions use pytest + Playwright Python.

## Agent guidance layer

- `AGENTS.md` — only always-on file. Routing + must-fire bullets.
- `docs/ARCHITECTURE.md` — this file.
- `.cursor/rules/00-authoring-critical.mdc` — agent-requested
  expanded discipline.
- `.cursor/rules/{task-creation,idea-validation,
   difficulty-calibration,review-and-submit}.mdc` — deep references.
- `workflow.md` — Step 1–4 process + embedded Ralph discipline.
- `commands.md` — canonical command reference.
- `REPO_CONVENTIONS.md` — durable conventions and waivers.
- `CNI.md` — backlog with promotion + demotion policy.
- `sudhir_knowledge/LONG_HORIZON_TASK_PHILOSOPHY.md` — new-idea causal
  investigation doctrine and anti-overengineering boundary.
- `skills/` (path locked in phase 2) — opt-in workflow macros.
- `.agents/skills/terminus-dsv-humanizer/` — pinned DSV-only model audit.

## Test layer

- `repo_tests/` — regression coverage for every mechanical gate.
- `repo_tests/fixtures/` — fixture tasks with pinned static-check
  results (`COMMON_STATIC_PASS_MESSAGES` in `repo_tests/cases.py`).
