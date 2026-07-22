# STEP3B — REV-3 paper review — rowgroup-prune-mirage

- Date: 2026-07-20
- Decision: **ACCEPT WITH NOTES for Step 4**
- Scope: instruction / schema disclosure repair after platform QC Needs Revision

## Evidence reviewed

- Platform QC FAIL axes: `behavior_in_task_description`, `structured_data_schema`,
  `file_reference_mentioned` (captured in `REV-3/FEEDBACK.md`).
- Preflight: PASS after REV-3 edits; checksum rewritten (48 files).
- Collapse: 0 FAIL / 1 WARN (RC2) / 22 PASS — same RC2 shape as REV-2.
- Instruction audit: symptoms-only, 0 families triggered.
- Dockerfile check: PASS. Base image is the sanctioned canonical GCC 13
  bookworm digest from `dockerfile and image best practices.mdc` (C/C++ family);
  Rust/Cargo remain apt-pinned for the dual-language lab. Reviewer “non-canonical”
  warning is incorrect against the current sanctioned list.
- Harbor oracle 1x: `jobs/2026-07-20__00-18-55`, mean 1.0, zero trial exceptions.
- Harbor NOP: `jobs/2026-07-20__00-21-56`, mean 0.0, zero trial exceptions.
- No code/oracle/test changes; ablations from REV-2 remain valid for the fix
  frontier. Disclosure-only edit does not move flipping points.

## What changed

1. Added normative `/app/docs/report-schema.md` documenting top-level and per-case
   JSON keys, ingest output `<store-directory>/data.store`, and faithful
   live-value markers (`low`, `high`, `has_absent`).
2. Expanded `instruction.md` to name those keys and `data.store` inline, cite the
   schema doc as grading reference, and add one symptom sentence on incomplete
   markers / origin lanes across selective vs batch paths.
3. Pointed `format-notes.md` at the schema doc so lagging notes cannot be mistaken
   for the operational contract.
4. Updated `output_contract.toml` and `construction_manifest.json` token lists.
5. Spec Construction Amendment 2 recorded.

Deliberately **not** embedded: fixture-specific tallies such as row_count=4 /
sum=100 (answer-shaped; forbidden).

## RC2 WARN justification (unchanged class)

RC2 WARNs that `rust/src/ember/fold.rs` is predictable via the visible path token
`rust` overlapping instruction/file-name signals. Two of three oracle targets
remain unpredictable. This is the same justified WARN accepted in REV-2 Step 3b;
no new telegraph was introduced by the schema disclosure.

## Instruction honesty

Operational output contract now lives in `instruction.md` (field names +
`data.store`) with `/app/docs/report-schema.md` as the normative grading
reference — matching the maritime/plc/cluster pattern that clears platform
`structured_data_schema`. RC6 remains symptoms-only because field names are not
dense backticked schema clusters. No fix-path symbols, algorithms, or oracle
tallies were disclosed.

## Verdict

ACCEPT WITH NOTES — proceed to Step 4 (oracle 10x + fresh NOP) then package and
re-upload.
