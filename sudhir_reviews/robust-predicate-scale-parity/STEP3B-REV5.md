# TASK-RPSP-001 Step 3b — Revision 5 (instruction + probe CLI)

- Date: 2026-07-19
- Submission: `fcee6e2e-1c89-476f-aa10-5932a474ef97`
- Platform status: HARD, `solvable=false` (r01/r02 0/10; r06/r10 1/10)

## Why the platform rejected it

Oracle 3/3 and NOP 0/1 were healthy. All 10 agent trials scored 0.0 because
they never cleared the cancellation-heavy numeric cluster. Best agent hit
10/12 and still missed `eval_band` conservatism. Platform analysis and quality
check both called out a spec gap: `instruction.md` never named the laboratory
probe CLI or the conservatism contract, so agents treated `series.c` as correct.

## Edits (rev 5)

1. **`instruction.md`** — grounded:
   - conservatism: cancellation-heavy floating sums must escalate to exact
     refinement rather than certify the opposite exact sign;
   - `GEOMLAB_INPUT` / `GEOMLAB_OUTPUT`;
   - `/app/bin/geomlab --inspect-series …` and `--inspect-status …`;
   - report schema (`schema_version`, lexical batch order, 9 bundled batches,
     16-hex digest, sorted cells / positive handedness);
   - strict alternate build, byte-stability, malformed fail-closed.
2. **CLI rename** — `--inspect-state` → `--inspect-status` in
   `environment/host/router.rs` and `tests/test_outputs.py`. The old name
   collided with oracle symbol `map_state` under CR1 when mentioned in the
   instruction. `--inspect-series` kept (platform-recommended entry point).

## Collapse residual (justified WARN)

- Verdict: **0 FAIL / 2 WARN / 21 PASS**
- **RC6 cause-revealing** — schema cluster + ALL_CAPS env tokens + CLI flags.
  Accepted: minimum surface to clear platform `behavior_in_task_description`
  and agent discoverability of the numeric probe path. Not `spec-complete`.
- **GX9 50% saturation** — borderline. Accepted: documents contracts without
  enumerating per-test answer triples (no `final=1` / `refine=True` recital).

## Gates remaining

Blocked locally by Docker address-pool exhaustion (stuck snap-docker containers
require `sudo` to kill). After cleanup, rerun oracle 1x, NOP, oracle 10x, then
`approve_task.py`.
