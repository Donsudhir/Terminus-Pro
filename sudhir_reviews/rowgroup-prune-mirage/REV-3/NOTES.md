# REV-3 notes — rowgroup-prune-mirage

Opened: 2026-07-19T18:45:00Z (driver timestamp)
Implemented: 2026-07-20

## Why the submission failed

Three QC fails, all instruction/disclosure — not oracle/test/solution defects.

| QC axis | Gap | REV-3 fix |
| --- | --- | --- |
| `behavior_in_task_description` | High-level totals only | Named counters, markers, `data.store`; mixed-gen/origin symptom sentence |
| `structured_data_schema` | No normative case schema | `/app/docs/report-schema.md` + inline field names |
| `file_reference_mentioned` | Missing ingest filename | Explicit `<store-directory>/data.store` |

## Mistakes remembered

- CM-002 recurrence + **CM-018** (JSON keys + exact filenames).
- Do not paste fixture oracle tallies into instruction.

## Base image

`public.ecr.aws/docker/library/gcc:13-bookworm@sha256:930f2ebe…` is the
sanctioned canonical C/C++ image in `dockerfile and image best practices.mdc`.
No change.

## Gate evidence (disclosure-only edit)

- Preflight PASS; checksum 48 files.
- Collapse 0 FAIL / 1 justified RC2 WARN / 22 PASS.
- Oracle 1x `2026-07-20__00-18-55` mean 1.0.
- NOP `2026-07-20__00-21-56` mean 0.0.
- Step 4 oracle 10x: pending / recorded in STEP4.md when complete.
