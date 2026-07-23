# Step 3b Paper Review — resolver-closure-drift REV-4

- **REV:** REV-4
- **Task path:** `sudhir_tasks/active/resolver-closure-drift`
- **Date:** 2026-07-22
- **Task files edited:** yes — `instruction.md`, `environment/bootstrap/base/docs/architecture.md`
- **Harbor evidence:** oracle 1x `2026-07-22__08-46-44` mean=1.0; nop `2026-07-22__08-48-12` mean=0.0; oracle 10x pending

## Why reopen

QC `behavior_in_task_description` FAIL (CM-002): instruction omitted profile modes, preview/withdrawn semantics, constraint syntax, named edge cases, and generated-package generalization.

## Instruction honesty (post-fix)

| Check | Result |
| --- | --- |
| Observable contracts for all graded behaviors | PASS — profiles, preview/withdrawn, constraint form, edge cases, generated neighbors |
| Cited grading reference | PASS — `/app/repo/docs/architecture.md` |
| No fix-file / symbol leak | PASS — RC2/CR1/CR7 clean |
| RC6 / GX6 | PASS — symptoms-only; 0 causal connectives |
| No fixture lock tuples | PASS — GX9 clean |

## Mechanical

`check-task.sh` PASS (0 FAIL / 0 WARN collapse; static PASS with length WARN only; dockerfile PASS; checksum written).

## Verdict

**ACCEPT for packaging after oracle 10x.** Content fix is disclosure-only relative to solver behavior; residual hardness remains typed merge composition across three authorities.
