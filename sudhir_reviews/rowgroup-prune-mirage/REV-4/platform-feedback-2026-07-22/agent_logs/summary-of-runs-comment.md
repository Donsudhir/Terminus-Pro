## Summary of Runs for "tbench-task"
### Difficulty: medium
| Agent/Model | # of total runs | # of successes | # of failures<br>(agent timeout) | # of failures<br>(other reasons) | Accuracy |
|-------------|-----------------|-----------------|------------------------------------|---------------|----------|
| nop | 1 | 0 | 0 | 1 | 0.0 |
| oracle | 3 | 3 | 0 | 0 | 1.0 |
| terminus-gpt5-5 | 5 | 2 | 0 | 3 | 0.4 |
| terminus-claude-opus-4-8 | 5 | 4 | 0 | 1 | 0.8 |
<details>
<summary>Tests Result</summary>

✅ This task is solvable by the agents.
| Test Name | Successful Runs / Total Runs |
|-------------|------------------------------|
| test_p01 | 10 / 10 |
| test_p02 | 9 / 10 |
| test_p03 | 9 / 10 |
| test_p04 | 10 / 10 |
| test_p05 | 10 / 10 |
| test_p06 | 9 / 10 |
| test_p07 | 10 / 10 |
| test_p08 | 9 / 10 |
| test_p09 | 10 / 10 |
| test_p10 | 10 / 10 |
| test_p11 | 9 / 10 |
| test_p12 | 10 / 10 |
| test_p13 | 9 / 10 |
| test_p14 | 6 / 10 |
| test_p15 | 10 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ❌ FAIL | ## Job Summary

### 1. Overall Results
- **4 trials total, 0 passed (0%), 4 failed** — all received reward 0.0 under all-or-nothing scoring
- All trials were run on the same task (mixed-language Rust/C++ data-store bug-fix)
- No model/agent differentiation was noted across trials

### 2. Common Failure Patterns

All four failures share a nearly identical pattern — agents got **14/15 tests** (trials `XBDEWvq`, `WVL9ohd`, `e9FgsLq`) or **8/15** (`FqhzQtG`), with the same root cause:

**The `veil.cpp` region_eq branch was not patched.** Every agent correctly identified and fixed:
- ✅ `rill.cpp` — batch path liveness check (origin_lane ignored)
- ✅ `fold.rs` — Rust ingest marker computation over all rows instead of live-only rows
- ✅ `veil.cpp` numeric/isnull branches — legacy slab marker conservatism

But all three 14/15 trials (`XBDEWvq`, `WVL9ohd`, `e9FgsLq`) **missed the `RegionEqual` branch in `veil.cpp`**, which still trusted stale archived `region_low`/`region_high` markers for generation-2 slabs. Test `test_p14` (a `region_eq` probe on `vault.store`) failed universally, returning `row_count=1` instead of the expected `row_count=2, sum=49`.

Trial `FqhzQtG` was an earlier-stage failure — it never addressed `veil.cpp` at all, failing 7 tests rather than 1.

### 3. Hack Check

**No cheating detected.** All four trials passed `reward_hacking` checks. Agents only modified legitimate source files (`rill.cpp`, `veil.cpp`, `fold.rs`), rebuilt via the provided toolchain (`/app/tools/build-all`), and validated via the bundled audit. No trial accessed `solution/` directories, modified test files, or touched grading mechanisms.

### 4. Systematic Instruction Issues

One trial flagged a **task specification failure**: `FqhzQtG` received `task_specification: fail`. The instructions describe "archived mixed-generation stores with incomplete markers" but do not explicitly specify what the gate should do when on-disk markers are stale/wrong (e.g., `mixed.store` slab0 has `low=100, high=100` but contains live values 10 and 20). The architecture docs say to "interpret without rewriting" but don't define gate-skipping behavior for incorrect markers — this caused `FqhzQtG` to miss the `veil.cpp` fix entirely.

The other three trials passed `task_specification`, with reviewers judging the fix for the `region_eq` branch to be *derivable* from the stated contract ("equivalent modes must agree"), making it an agent limitation rather than a spec gap. **However, this is a borderline call** — the fact that all three independent agents missed the same branch suggests the instructions may not make the `region_eq` case sufficiently salient.

### 5. Progress on Failed Trials

| Trial | Tests Passed | Gap |
|---|---|---|
| `XBDEWvq` | 14/15 (93%) | One branch missed in `veil.cpp` |
| `WVL9ohd` | 14/15 (93%) | One branch missed in `veil.cpp` |
| `e9FgsLq` | 14/15 (93%) | One branch missed in `veil.cpp` |
| `FqhzQtG` | 8/15 (53%) | Entire `veil.cpp` fix missing |

Three agents were extremely close to a complete solution. The mean pass rate is ~83%, with the all-or-nothing scoring converting strong partial progress to zero reward.

### 6. Key Differences Between Agents

The three 14/15 trials appear to have followed a similar diagnosis path and reached the same incomplete fix, suggesting convergent reasoning. `FqhzQtG` is the outlier — it diagnosed two of the three root causes but missed the `veil.cpp` gating problem entirely, likely due to the weaker task specification it encountered. No model-level differentiation is available from the provided data.

---

**Recommended Actions:**
1. **Fix the task spec** — explicitly document that *all* predicate paths (including `region_eq`) in the selective-read gate must apply the legacy-slab conservatism, or add a concrete example with the `region_eq` case
2. **Consider partial credit** — 14/15 agents are very close; all-or-nothing scoring may under-represent progress for debugging/iteration purposes
3. **Targeted hint** — if retrying, prompt agents to audit *every* predicate branch in `veil.cpp`, not just numeric/isnull |
<!-- test-summary-end -->