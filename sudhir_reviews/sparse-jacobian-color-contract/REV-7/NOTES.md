# REV-7 notes — sparse-jacobian-color-contract

## Why
Platform UI: “system code did not run” / empty difficulty artifact after REV-6
upload. Not an EASY content reject this round.

## Diagnosis
CM-019: `difficulty_check` + `tb_check` CodeExecution builds FAILED with empty
logs; sibling AutoEvals hit `ThrottlingException` on `BatchGetBuilds`. Fast
static and quality/review judges still SUCCEEDED. Canonical Rust base image is
already correct (reviewer “non-canonical” warning is wrong).

## Changes
- `task.toml`: `build_timeout_sec=1200`, `verifier.timeout_sec=1200`,
  `memory_mb=8192` (agent stays at platform cap 1800; 2x-verifier is WARN-only)
- `tests/test.sh`: CM-016 early `reward.txt=0`; note ctrf comes from Dockerfile
- No instruction / source / test-logic edits (REV-6 hardness still unmeasured)

## Next
Re-run gates + oracle evidence, package, re-upload. After difficulty populates,
if still EASY apply CM-008; do not treat this banner as hardness feedback.
