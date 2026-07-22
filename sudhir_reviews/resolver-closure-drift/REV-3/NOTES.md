# REV-3 notes — resolver-closure-drift

Opened: 2026-07-20T11:48:42Z

Reason: Rubric CM-015: Agent format + third negative; optional branch nudge in instruction

## Applied

- Rewrote UI rubric to `Agent …, ±N` with 8 positives (sum 23) and 4 negatives (−5/−5/−3/−3).
- Softened instruction discovery: “the repository branches hold independently valid compatibility lines for those two behaviors.”
- Did **not** name `wire/lock.rs` or declare sorting as a second known defect (keeps GPT 3/5 discrimination).
- CM-015 Seen bumped for RCD `4d74fca0` REV-2; KNOWLEDGE_GRAPH HIT edge added.

## Upload paste

Use `REV-3/RUBRIC.md` body lines (without the `#` header) in the Snorkel rubric field.

## Platform status 2026-07-20

- Submission `4d74fca0` → EVALUATION ran → NEEDS_REVISION
- **Cause:** CM-019 — `difficulty_check` hit AWS `ThrottlingException` / `BatchGetBuilds` Rate exceeded (agents never ran; “No file available”)
- Rubric in form already REV-3 `Agent …, ±N` — prior human rubric notes are leftover sidebar text
- QC `behavior_in_task_description` FAIL is advisory here; do **not** rewrite instruction for this round
- Next: re-upload / re-eval same package only — see `PLATFORM_EVAL_2026-07-20.md`
