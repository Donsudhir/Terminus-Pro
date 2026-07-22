# rowgroup-prune-mirage Edit Ledger

## 2026-07-19T17:05:37Z — Revision 1

- evidence capture

## 2026-07-19T17:13:18Z — Revision 2

- Step 3b generalization: generated fresh CSVs, removed test-side internal-authority narration, and added repeated-report byte verification.

## 2026-07-19T18:45:00Z — Revision 3

- Platform QC FAIL: behavior_in_task_description + structured_data_schema + file_reference_mentioned (JSON case fields, data.store, marker semantics); review NEEDS REVISION on instruction disclosure / base-image note

## 2026-07-21 — Revision 4

- Platform difficulty run rated REV-3 TRIVIAL (opus-4-8 5/5, gpt5-5 5/5); CM-008
  hardening: removed markers_complete breadcrumb + architecture.md giveaway
  sentence; restructured rill.cpp as lane/mask kernel (store.cpp builds lanes);
  added vault.store incident artifact + 4 drill lines + orders_c.csv; schema doc
  all-non-live marker convention; tests p13-p15; oracle gate now generation<3
  legacy-open. Instruction.md unchanged. Spec Construction Amendment 3;
  manifest flipping contract updated. Preflight PASS, oracle 1x 1.0
  (jobs/2026-07-21__07-08-14), NOP 0.0 (jobs/2026-07-21__07-09-24), ablation
  subsets match contract exactly.

## 2026-07-20 — Revision 3 implementation

- Added environment/docs/report-schema.md (normative JSON + data.store + markers).
- Expanded instruction.md: inline field names, data.store, mixed-gen/origin symptom sentence; cite schema doc.
- format-notes.md points at report-schema; output_contract + construction_manifest updated.
- Spec Construction Amendment 2; base image confirmed canonical GCC.
- No code/oracle/test changes.

## 2026-07-21T00:54:38Z — Revision 4

- Platform difficulty TRIVIAL (both frontier agents 5/5); harden to at least MEDIUM per CM-008
