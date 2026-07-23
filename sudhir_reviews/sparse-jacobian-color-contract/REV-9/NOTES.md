# REV-9 notes — sparse-jacobian-color-contract

## Latest platform signal (2026-07-22)
NEEDS_REVISION with **only** AutoEval FAILED banners:
- `CodeExecutionEnvironment:18aa29d0-…`
- `CodeExecutionEnvironment:1ecdf6d7-…`

fetch-task eval[16] (2026-07-22T20:16Z):
- Fast/static siblings SUCCEEDED (category, template, long_context, applicability, test_quality)
- `tb_check` + `difficulty_check` → `build_status=FAILED`, **empty logs**
- No new human reviewer prose

## Root cause
**CM-019** — platform CodeExecution environment failed before agents/review ran.
Not a digest/config/content reject. Local REV-8 package already passed Harbor
oracle 10x / NOP.

## History on this submission
`difficulty_check`: about **3 SUCCEEDED / 14 FAILED** across 17 evals. The
image *can* run (SUCCEEDED on 2026-07-18 and 2026-07-21), but CodeExecution
fails most of the time with empty logs. That pattern blocks human review even
when the zip is locally sound.

## Decision recommendation
**Park / deprioritize.** Do not spend another content REV chasing AutoEval.
Optional: at most one unchanged re-upload/re-eval when CodeBuild is quieter.
Resume content work only after `difficulty_check` SUCCEEDS with agent stats.
If that returns EASY again, that is a separate CM-008 problem — not this banner.
