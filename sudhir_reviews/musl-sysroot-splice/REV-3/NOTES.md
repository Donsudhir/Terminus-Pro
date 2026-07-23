# REV-3 notes — musl-sysroot-splice

Opened: 2026-07-22T18:55:51Z

Reason: CM-002: clarify LANE_TAG is stdout-only; ledger is exactly marker/thread/errno (platform Needs Revision)

## Reviewer asks

1. Stop saying "lane-tag rows." Ledger is exactly `marker`, `thread`, `errno`.
   `LANE_TAG=BRAVO` is runtime stdout only.
2. Remove trailing "cc" / "testing on rubric artifact" from the rubric paste.
   Local REV-2/REV-3 rubric Agent lines already omit that; re-pasted unchanged.

## Change set (minimal)

- `instruction.md` only: symptoms wording + explicit ledger vs stdout distinction.
- No tests, solution, Dockerfile, or environment logic edits.
- DSV re-captured under Humanizer gate; rubric Agent lines unchanged from REV-2.

## Harbor

See `EVIDENCE.md` after oracle/NOP/10x.
