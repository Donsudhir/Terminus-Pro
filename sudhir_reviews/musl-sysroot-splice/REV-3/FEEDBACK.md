# REV-3 reviewer feedback — musl-sysroot-splice

Reviewer Feedback (platform Needs Revision):

The prompt says "lane-tag rows," but the required JSON ledger is exactly 3 rows: marker, thread, and errno. LANE_TAG=BRAVO is a runtime stdout requirement, not a ledger row. Make that distinction explicit, and also remove the trailing "cc" testing on rubric artifact — that isn't counted as a blocker anymore.

Quality / agent analysis (HARD, solvable): primary failure across 9/9 trials was adding a 4th lane_tag row to probe_report.json, failing test_summary_count and test_seal_json_derives_live_ledger. Fix: instruction.md must distinguish stdout probe requirements from ledger schema (exactly marker, thread, errno).
