# Platform feedback — REV-3 re-upload eval (2026-07-20)

Source: `stb submissions fetch-task 4d74fca0-684f-4ace-a1c2-db55737f6c9a`
Eval: `942f4e98-3bb9-4468-8504-a67a166c155e` created 2026-07-20T12:02:18Z outcome=NEEDS_REVISION
Archive: `sudhir_snorkel/inbox/submission_4d74fca0.json`

## What the UI shows
- Summary: **1 Failed to run difficulty check**
- Difficulty download: **No file available**
- Reviewer Feedback sidebar: still the *previous* human rubric send-back (3 negatives + Agent format)
- Quality check: `behavior_in_task_description` FAIL (instruction opacity) — sibling AutoEval; not why difficulty is empty

## Proven root cause (platform JSON)
`difficulty_check` evaluator failed with:

```text
ThrottlingException when calling the BatchGetBuilds operation: Rate exceeded: BatchGetBuilds
```

Same throttle also failed: `codebase_applicability`, `test_quality_judge`, `claude_code_reviewer`.

Fast path that *did* run:
- `long_context_check`: SUCCEEDED — All static checks passed
- `tb_check`: SUCCEEDED — produced the quality_check_summary (including the opacity FAIL)

Form already has the REV-3 rubric (`test_rubrics` starts with `Agent rebuilds /app/bin/forge…`). Difficulty/agent fields are empty because the difficulty job never returned results.

## Do NOT
- Rewrite instruction for profile/preview/constraint disclosure based on this round
- Treat stale rubric revision_notes as proof the REV-3 rubric paste failed
- Hardness-revise (CM-008) with empty agent stats

## Do
- Re-trigger evaluation (re-upload same zip or platform re-eval) when AWS is not throttling
- Keep REV-3 rubric paste + optional branch nudge as already shipped
- CM-019: throttle / empty difficulty ⇒ infra, not task logic
