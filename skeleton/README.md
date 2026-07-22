# Task skeletons (offline verifier)

Canonical starting points for new tasks. Each skeleton sets
`[environment].allow_internet = false` and installs verifier dependencies
in `environment/Dockerfile` instead of at runtime in `test.sh`.

| Skeleton | Use when |
|----------|----------|
| `Default_Task_Skeleton/` | Standard single-step Python/pytest task |
| `milestone_template/` | Multi-milestone task (`steps/milestone_N/`, `[[steps]]` in `task.toml`) |

Copy the matching skeleton into `tasks/<task-name>/` and edit from there.
See `.cursor/rules/task-creation.mdc` for full construction rules.

There is intentionally no UI scaffold. Net-new `ui_building` work is blocked
by the repository's house eligibility rule. An evidence-backed in-flight UI
revision must use the official Python pytest + Playwright Python contract and
pass the focused compatibility branch in `run_static_checks.py`; it must never
restore or copy the retired JavaScript/Vitest verifier stack.
