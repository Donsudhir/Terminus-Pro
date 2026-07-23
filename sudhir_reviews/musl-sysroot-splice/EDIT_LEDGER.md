# musl-sysroot-splice Edit Ledger

## 2026-07-22T18:55:51Z — Revision 3

- CM-002: `instruction.md` no longer says "lane-tag rows"; ledger is exactly
  marker/thread/errno; LANE_TAG is runtime stdout only (not a ledger row).
- Rubric: unchanged Agent lines from REV-2 (already separates ledger rows from
  LANE_TAG stdout; no trailing "cc"/rubric-artifact line present).
- No test, solution, Dockerfile, or environment logic edits.

## 2026-07-19T09:16:54Z — Revision 2

- CM-006: behavioral checks for staged musl + live knit/pack/seal pipeline

## 2026-07-22T18:55:51Z — Revision 3

- CM-002: clarify LANE_TAG is stdout-only; ledger is exactly marker/thread/errno (platform Needs Revision)
