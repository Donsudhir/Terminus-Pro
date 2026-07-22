# STEP3B — REV-4 paper review — rowgroup-prune-mirage

- Date: 2026-07-21
- Decision: **ACCEPT WITH NOTES for Step 4**
- Scope: CM-008 difficulty hardening after platform difficulty run rated the
  REV-3 zip TRIVIAL (opus-4-8 5/5, gpt5-5 5/5, oracle 3/3, NOP 0/1).

## Collapse diagnosis of REV-3 (why agents passed 10/10)

1. `cpp/src/row.cpp::is_live` contained the exact correct origin-lane liveness
   rule; buggy `lattice/rill.cpp` was a one-glance sibling diff — fix C was
   copy-paste (A7 pre-factored helper collapse).
2. `store.cpp` computed `slab.markers_complete = generation >= 3` into a field
   nothing consumed — a grep-landing breadcrumb for fix B — and
   `architecture.md` stated the conservative-skip rule verbatim ("avoiding a
   read is allowed only when the marker proves that the slab cannot
   contribute").
3. `report-schema.md` marker semantics plus the three-lane `tilt_a` signature
   made fix A transcription.
4. All three fixes were local and independent (A9 orthogonal-checklist fail).

## REV-4 hardening (instruction.md unchanged — QC-passing REV-3 text preserved)

1. **Breadcrumb removal** — `markers_complete` deleted from `types.hpp` /
   `store.cpp`; architecture.md giveaway sentence deleted. The
   generation→marker-trust model must now be reconstructed from artifact
   forensics (mixed.store page 0 declares markers `100|100|1` against live
   rows {10,20}; vault.store page 0 declares `has_absent=0` while holding a
   retired-origin row an origin-blind gen-2 writer could not see).
2. **Sibling-oracle removal** — `store.cpp` now populates per-slab column
   lanes; `rill.cpp` is a lane/mask kernel. The planted defect (mask from
   presence lane only) is unchanged in meaning, but fixing it requires
   translating the liveness rule into mask algebra rather than copying
   `is_live`. `row.cpp` untouched.
3. **New incident artifact `data/archive/vault.store`** (gen 2/3/2) with stale
   `has_absent=0` and stale text markers on gen-2 pages; four cause-neutral
   drill lines added to `incident.case` so the divergence is reproducible.
4. **Producer edge semantics** — all-non-live slab convention added to
   `report-schema.md` (low 0, high 0, has_absent true); practice CSV
   `orders_c.csv` with an all-non-live chunk and a live `-999` row.
5. **Three new tests** p13/p14/p15 covering isnull-with-skipping equivalence,
   text-probe completeness under stale gen-2 text markers, and sparse fresh
   chunk markers + placeholder-live consistency.
6. **Oracle** — gate trust now derives from `generation < 3` (legacy-open);
   unknown-text / unknown-range guards and range normalization retained; batch
   mask built from origin+presence lanes.

Spec Construction Amendment 3 records all of the above; construction manifest
flipping contract updated (A 6, B 7, C 7 of 15 tests; max concentration 7/15).

## Evidence

- Preflight `./scripts/check-task.sh`: PASS (Phase A+B+C, checksum rewritten,
  50 files).
- Gates: static=PASS, dockerfile=PASS, collapse=WARN (0 FAIL / 3→2 WARN after
  GX7 fix; RC2 + GX3 remain), integrity=PASS.
- Harbor oracle 1x: `jobs/2026-07-21__07-08-14`, mean 1.0, 0 exceptions.
- Harbor NOP: `jobs/2026-07-21__07-09-24`, mean 0.0, 0 exceptions.
- Containerized ablation matrix (full/noA/noB/noC oracle variants against the
  built REV-4 image):
  - full: 15/15 passed.
  - noA (fold.rs buggy): fails exactly {p01, p03, p05, p07, p10, p15}.
  - noB (veil.cpp buggy): fails exactly {p02, p03, p06, p08, p11, p13, p14}.
  - noC (rill.cpp buggy): fails exactly {p04, p05, p06, p09, p12, p13, p15}.
  All three subsets match the amended flipping contract verbatim.

## WARN justifications

- **RC2 (same class as REV-2/REV-3):** `rust/src/ember/fold.rs` predictable via
  the path token `rust`. Unavoidable for a dual-language lab; two of three
  targets remain unpredictable. Accepted as before.
- **GX3 61 LOC (borderline band):** the oracle is a precise three-function
  coordination — a marker fold, an admission gate, and a batch mask — where
  each function body is naturally short. Every solve.sh operation is a
  substantive fix (removing any one flips its declared test subset, proven by
  the ablation matrix above); no cosmetic padding was added and none is
  acceptable under the A16 anti-gaming policy.

## Difficulty expectation

The three trivializing channels (sibling copy, dead-field grep breadcrumb,
doc-stated solution rule) are closed. Remaining hardness: reconstructing the
generation trust model from conflicting persisted markers, translating
liveness into lane-mask semantics, and generalizing to verifier-owned CSVs and
probes (isnull-with-skipping, stale text markers, all-non-live chunks,
placeholder-valued live rows) that the bundled drill only hints at. Re-measure
on the platform before claiming MEDIUM/HARD (CM-008).

## Verdict

ACCEPT WITH NOTES — proceed to Step 4 (oracle 10x + fresh NOP), package,
re-upload with fresh form pastes.
