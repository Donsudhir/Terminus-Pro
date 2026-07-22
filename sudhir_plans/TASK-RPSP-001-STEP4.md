# TASK-RPSP-001 Step 4 Plan

- Date: 2026-07-18
- Status: Completed with APPROVAL
- Revision: 4
- Canonical task: `sudhir_tasks/active/robust-predicate-scale-parity`
- Final archive: `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`

## Sequence completed

1. Confirmed Step 3b CLEAN, checksum current, gates current, package absent, and no stale task containers.
2. Pruned unused Docker networks before stress without touching active containers.
3. Ran current-tree oracle 10x at full `-k 10 -n 10` concurrency.
4. Required all ten trials to complete with reward 1.0 and zero exceptions.
5. Cleaned all task containers and unused task networks left by the Snap Docker teardown issue.
6. Ran a fresh post-stress NOP and required reward 0.0 with zero exceptions.
7. Built the final zip directly from the canonical task source.
8. Ran standalone zip validation and the authoritative approval gate.
9. Inspected all archive members, required dotfiles, forbidden-file exclusions, fingerprint, and source/zip parity.
10. Ran the full repository regression and recorded final evidence.

## Outcome

- Oracle 10x: 10/10, mean 1.0, zero errors
- Fresh NOP: 0.0, zero errors
- Approval: PASS, approved true, zero warnings and zero blocking failures
- Archive: 42 members, 29,677 bytes
- SHA-256: `17a0eb184ef35e43a0d6474da4ca7367a931de0e456b378534e1d9310bd6797d`
- Source/zip parity: 42/42, no missing, extra, or changed files
- Full repository regression: Ruff PASS, pytest 241 passed and 26 skipped
- Next action: upload the final zip to Snorkel, mark phase submitted, then ingest returned feedback
