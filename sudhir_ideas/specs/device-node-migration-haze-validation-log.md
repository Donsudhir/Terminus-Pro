# Validation Log: device-node-migration-haze

## Attempt 1
- Derived score: 1 FAILs, 0 WARNs
- Evidence: device-node-migration-haze-attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)
- Blocking evidence failures:
  - Schema validation failed at $.naming_pass: Additional properties are not allowed ('recomputed_concentration' was unexpected)

## Attempt 2
- Derived score: 0 FAILs, 0 WARNs
- Evidence: device-node-migration-haze-attempt-2-evidence.json

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 2
- count of run_static_checks.py WARN-only exits before approval: 8
- count of collapse_check.py FAIL exits before first PASS: 3
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 383.88s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 520.92s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null
