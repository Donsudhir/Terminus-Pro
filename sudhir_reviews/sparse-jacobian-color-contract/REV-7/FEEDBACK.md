# Platform feedback — REV-7 (diagnose “system code did not run”)

Source: `stb submissions feedback` + `fetch-task` for
`d9082cd8-c0ad-4174-a34f-4731f0b63907` (2026-07-21).

## What the UI shows
- Reviewer Feedback: AutoEval FAILED builds
  - `CodeExecutionEnvironment:983991d8-13a0-43b3-9211-38aeb54b5613` (`tb_check`)
  - `CodeExecutionEnvironment:c49b6cb7-d53e-451c-b9b7-0741f032927c` (`difficulty_check`)
- Difficulty / quality artifact fields empty (“No file available”)
- Fast static / long_context / test_quality_judge / claude_code_reviewer: SUCCEEDED
  on sibling AutoEvals (review reports say READY / ROBUST)

## Root cause (from platform JSON)
**CM-019 — platform CodeExecution / rate-limit path, not task logic.**

Latest completed evals (12 = 2026-07-19T18:07Z, 13 = 19:34Z re-poll):
- `difficulty_check` and `tb_check` → `build_status=FAILED`, `full_logs` empty,
  `solvable` / `difficulty` / `text_summary` blank
- Sibling evaluators hit AWS `ThrottlingException` on `BatchGetBuilds`
  (`Rate exceeded`) while fetching CodeBuild results
- Local `docker build`, `dockerfile_check`, and zip validation still PASS

## Not the cause
- **Non-canonical base image warning** in the pasted review report is a
  false positive. `public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe…`
  is on the sanctioned list in `dockerfile and image best practices.mdc` /
  `ci_checks.mdc`.
- PATH / verifier-python shim is intentional CM-007 anti-cheat; not a build fail.
- Prior successful difficulty run (REV-5 / eval 11) already proved the image
  class can run agents: EASY 80/80 — that is a separate CM-008 hardness debt
  that REV-6 content addresses but could not be remeasured under CM-019.

## REV-7 fix
- Raise `build_timeout_sec` 600 → 1200 and `memory_mb` 4096 → 8192 (CM-019 hedge)
- Align `test.sh` with CM-016 early `reward.txt=0` + ctrf dependency comment
- Re-package and re-upload so difficulty/tb_check can remeasure
