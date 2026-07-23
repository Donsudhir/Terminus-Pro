# Platform snapshot (sanitized)

Captured: 2026-07-23T13:16:08Z

## Scalars
- difficulty: HARD
- solvable: True
- status_line: ✅ Solvable (all tests passed by at least one agent run)
- static_outcome: PASS
- submission_id: 94684fc8-3f27-43b1-97b4-8d8a03d94718
- zip_filename: maritime-lane-weather-weave.zip
- uploaded_at: 2026-05-23T08:19:33.238Z
- source_file: submission_94684fc8.json

## Agent performance
- terminus-claude-opus-4-6: 0.0%
- terminus-gpt5-2: 20.0%

## text_summary

```
Difficulty: ✅ HARD

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-6: 0.0% (0/5 runs)
  • terminus-gpt5-2: 20.0% (1/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-6: 5 other
  • terminus-gpt5-2: 4 other

Unit Tests Results:
  • test_m01: 10 passed / 10 runs
  • test_m02: 10 passed / 10 runs
  • test_m03: 10 passed / 10 runs
  • test_m04: 10 passed / 10 runs
  • test_m05: 10 passed / 10 runs
  • test_m06: 10 passed / 10 runs
  • test_m07: 10 passed / 10 runs
  • test_m08: 10 passed / 10 runs
  • test_m09: 10 passed / 10 runs
  • test_m10: 10 passed / 10 runs
  • test_m12: 10 passed / 10 runs
  • test_m13_synthetic_pack[syn_late_pivot]: 10 passed / 10 runs
  • test_m13_synthetic_pack[syn_short_win]: 10 passed / 10 runs
  • test_m13_synthetic_pack[syn_wide_start]: 10 passed / 10 runs
  • test_m14: 10 passed / 10 runs
  • test_m11: 1 passed / 10 runs
  • test_m13_synthetic_pack[syn_close_quarters]: 1 passed / 10 runs
  • test_m13_synthetic_pack[syn_rank_stall]: 1 passed / 10 runs
  • test_m15: 1 passed / 10 runs
  • test_m16: 1 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ❌ FAIL, ## Job Summary

### 1. Overall Results

**All 9 trials failed (reward = 0.0).** No trials achieved a passing score. This was a binary all-or-nothing grading scheme requiring all 20 tests to pass.

| Trial | Tests Passed | Reward |
|-------|-------------|--------|
| tbench-task__2izt5Jw | 15/20 | 0.0 |
| tbench-task__7Zf6cJp | 15/20 | 0.0 |
| tbench-task__JjKWThT | 15–16/20 | 0.0 |
| tbench-task__A8Lk8k8 | 15/20 | 0.0 |
| tbench-task__UHYPgWe | 15/20 | 0.0 |
| tbench-task__2oGCyZP | 15/20 | 0.0 |
| tbench-task__XFi3FAy | 15/20 | 0.0 |
| tbench-task__f2cPT6W | 15/20 | 0.0 |
| tbench-task__fn7TRw7 | 15/20 | 0.0 |

---

### 2. Common Failure Patterns

**Every single trial exhibited the same core failure: agents correctly fixed the 4 helper-package bugs, then over-engineered `sim/driver.go` and introduced a regression.**

The helper fixes were consistently correct across all trials:
- `swell/op_phase.go` — inverted lane logic ✅ (all trials)
- `quay/fn_span.go` — always returned true ✅ (most trials)
- `keel/fn_rank.go` — non-strict ordering ✅ (most trials)
- `wake/op_stamp.go` — never updated epoch ✅ (all trials)

The failure pattern in `driver.go` varied slightly but shared a root cause — agents saw vessels starting in the same cell (e.g., `syn_close_quarters`, `four_unit_rush`) producing `berth_stack=2` or `deliveries_met=False` and **misidentified correct expected output as a bug**:

| Driver.go Mutation | Trials |
|---|---|
| Switched to sequential/priority move resolution | 2izt5Jw, JjKWThT, f2cPT6W |
| Changed safety check scope (all vessels vs. co-planners only) | A8Lk8k8 |
| Added unnecessary `sort.Slice` front-first ordering | 2oGCyZP |
| Added initial-position deconfliction/normalization | UHYPgWe, XFi3FAy |
| Replaced single-pass conflict check with iterative stability loop | fn7TRw7 |
| Incomplete fixes (never touched driver but missed keel/quay bugs) | 7Zf6cJp |

The failing tests were nearly identical across all trials: `syn_close_quarters`, `four_unit_rush`, `syn_rank_stall` — all producing `deliveries_met: got True, want False` or `berth_stack: got 1, want 2`.

---

### 3. Hack Check

**No cheating detected.** All 9 trials passed `reward_hacking` checks. No agent accessed `solution/` directories, modified test files, or wrote to `/logs/verifier/reward.txt`. The 0.0 rewards reflect genuine implementation failures.

---

### 4. Systematic Instruction Issues

Reviewers disagreed on whether the spec was adequate — **4 trials rated `task_specification: fail`**, 5 rated `pass`. The genuine ambiguities flagged:

- **Simultaneous vs. sequential move semantics** (JjKWThT, fn7TRw7): The spec says "at plan time" but never explicitly states that safety checks run only against *other planning vessels*, not stationary ones. This gap caused multiple agents to assume all vessels are barriers and rewrite the driver.
- **"Both zero is inert" in `fn_rank`** (JjKWThT, UHYPgWe): Agents interpreted "inert" as `True` (allowed); the reference returns `False` (blocked). Genuinely ambiguous phrasing.
- **`start_cells` verbatim overlap** (UHYPgWe, XFi3FAy): The spec says start_cells "override default spacing" without clarifying that intentionally overlapping positions must be accepted as-is to test blocking behavior. Agents added normalization.
- **"Multiple hulls occupying one lane cell" listed as a bug** (fn7TRw7): The spec calls stacking a defect, yet reference tests expect `berth_stack=2` for same-cell starts — measuring it accurately, not preventing it. This contradiction caused agents to over-correct.

The **most impactful gap** across trials is the unspecified scope of the plan-time safety check: agents consistently misread the correct output of close-quarters fixtures as a remaining bug.

---

### 5. Progress Assessment

Agents were remarkably close — **75% of the way there** (15/20 tests) in 8 of 9 trials. The 4 required helper-package fixes were completed correctly in nearly every run. The entire gap was a single category of error: misidentifying correct simulator behavior (vessels deadlocking in shared cells) as a bug and mutating `driver.go` to "fix" it.

Trial **7Zf6cJp** was the weakest — the agent never inspected `quay/fn_span.go` or `keel/fn_rank.go` and used a flawed self-test script that only flagged `False` values, missing wrong-but-truthy outputs.

---

### 6. Key Takeaways

Since all trials appear to use the same model/agent class, performance was highly consistent. The failure mode was **universal and deterministic**: fix helpers → observe unexpected close-quarters output → incorrectly diagnose driver bug → break the driver. A targeted clarification to the spec about (a) simultaneous move-checking semantics, (b) the meaning of "inert" in `fn_rank`, and (c) that overlapping `start_cells` are intentional test inputs — would likely unblock all 9 trials.
```

## quality_check_summary

```
## Quality Check Results
✅ pass - behavior_in_task_description: instruction.md explicitly names all seven contract fields (schema_tag, deliveries_met, berth_stack, lane_honor, log_aligned, cpa_clear, leg_stable), directs the agent to /app/docs/report-schema.md for the replay invariants (hull separation, pivot lane, leg ordering, epoch alignment), mentions start_cells/start_legs overrides, and explicitly says grading covers /app/data/voyage_pack.json plus every file under /app/data/fixtures/ including syn_*.json. The schema doc provides the normative rules that drive all test assertions, so every test checks something the instruction describes.
✅ pass - behavior_in_tests: Tests cover every documented behavior: schema_tag correctness (m01), all six metric fields matched against the reference replayer (m02–m07, m13–m16), exactly the seven public keys (m10), named fixtures wind_surge, pivot_late, four_unit_rush, long_ghost_run (m08–m09, m11–m12), all syn_* fixtures via parametrize (m13), the late-pivot → lane_honor=false invariant (m14), close-quarters start_cells → cpa_clear=false/berth_stack≥2 (m15), and the rank-stall tie-break → leg_stable=false (m16). No documented behavior appears untested.
✅ pass - informative_test_structure: test_outputs.py is well-organized: each test function carries a one-line docstring stating what it verifies, tests are sequentially numbered (m01–m16), helpers (replay_expected, assert_matches_reference, run_navsim_with_pack) are clearly named and purposeful, the parametrized synthetic-fixture test is separated from named fixtures, and pytest fixtures (report, bundled_pack) make shared state explicit. Reading the file without knowing the codebase still makes the intent of every test clear.
✅ pass - anti_cheating_measures: The Dockerfile COPYs only the Go source tree plus data/docs; it never copies tests/ or solution/ into the image. The test harness calls run_navsim_with_pack, which overwrites /app/data/voyage_pack.json and executes the agent's compiled binary, so the binary must actually handle every fixture correctly—a static hardcoded output file cannot satisfy tests across different fixture inputs. The reference replay logic lives only in the test file (outside the image), so the agent cannot read it at runtime. The catalog/sectors.toml deliberately shows min_sep_cells=2 (contradicting the code's minSep=1) as a decoy, discouraging trivial copying of config values.
✅ pass - structured_data_schema: environment/docs/report-schema.md (referenced from instruction.md as the normative spec) provides a complete table listing all seven output fields with their JSON key names and types (schema_tag: string, deliveries_met: bool, berth_stack: int, lane_honor: bool, log_aligned: bool, cpa_clear: bool, leg_stable: bool). The doc explicitly labels these rules as the grading reference and not optional knobs. The instruction also enumerates the seven contract names, consistent with the schema doc.
✅ pass - pinned_dependencies: The Dockerfile pins every dependency: the base image is locked by SHA-256 digest (golang:1.22-bookworm@sha256:…), apt packages are pinned to exact versions (ca-certificates=20230311+deb12u1, curl=7.88.1-10+deb12u14, tmux=3.3a-3), uv is fetched at version 0.9.5 via a versioned URL, and Python packages are pinned (pytest==8.4.1, pytest-json-ctrf==0.3.5). No unpinned external dependency is present.
✅ pass - typos: All filenames, paths, field names, package names, JSON keys, Go identifiers, and environment variable names cross-check correctly across instruction.md, report-schema.md, Dockerfile, Go source files, test file, and fixture JSON files. JSON struct tags in sim/pack.go and metrics/report.go match the schema doc. No typos were found.
✅ pass - tests_or_solution_in_image: The Dockerfile contains COPY directives only for Go source subdirectories (cmd, sim, quay, swell, keel, wake, hop, gust, grid, metrics, util, config, clock, net, decoy), data, catalog, deploy, docs, go.mod, and Makefile. Neither tests/ nor solution/ appear in any COPY instruction, so the verifier scripts and reference solution are absent from the runtime image.
✅ pass - hardcoded_solution: solution/solve.sh patches all four broken Go source files (quay/fn_span.go, swell/op_phase.go, keel/fn_rank.go, wake/op_stamp.go) with correct logic, then runs 'go build -buildvcs=false -o /app/bin/navsim ./cmd/navsim' to compile the binary, and finally executes /app/bin/navsim. The script derives the answer through code correction and compilation rather than printing pre-computed values.
✅ pass - file_reference_mentioned: instruction.md explicitly states the output path: '/app/bin/navsim reads JSON scenario packs from /app/data/ and writes /app/output/voyage_report.json'. The exact filename voyage_report.json is named. The test confirms the same path (REPORT = APP / 'output' / 'voyage_report.json').
```

## test_review

```
================================================================================
                          REVIEW REPORT: tbench-task
================================================================================

Status:        ✅ PASS
Task Location: /root/harbor_tasks/tbench-task

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------

This task requires debugging a Go autonomous voyage replay simulator whose
helper functions contain subtle logic errors. The agent must identify and fix
four buggy Go source files (quay/fn_span.go, swell/op_phase.go,
keel/fn_rank.go, wake/op_stamp.go) that implement separation checks, lane
phase selection, leg ordering, and epoch tracking. The test suite uses a Python
reference replay implementation to verify correct simulator behavior across a
bundled pack and multiple synthetic fixtures, checking all seven contract fields
of the voyage report.

================================================================================
                              WARNINGS ⚠️
================================================================================

--------------------------------------------------------------------------------
1. Test Dependencies Pre-Installed in Dockerfile
--------------------------------------------------------------------------------

File:    tbench-task/environment/Dockerfile (lines 16-18)
Problem: pytest and pytest-json-ctrf are installed in the Docker image rather
         than in test.sh. These are test-only dependencies that the agent does
         not need for solving the Go debugging task.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh \               │
│      && /root/.local/bin/uv venv /opt/tbench-venv --seed \                  │
│      && /opt/tbench-venv/bin/pip install pytest==8.4.1 pytest-json-ctrf==0.3.5│
└─────────────────────────────────────────────────────────────────────────────┘

Suggested fix: Move pytest installation into test.sh and remove from Dockerfile:
┌─────────────────────────────────────────────────────────────────────────────┐
│  # In test.sh, before running pytest:                                       │
│  apt-get update && apt-get install -y curl                                  │
│  curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh                     │
│  source $HOME/.local/bin/env                                                │
│  uv venv .tbench-testing                                                    │
│  source .tbench-testing/bin/activate                                        │
│  uv pip install pytest==8.4.1 pytest-json-ctrf==0.3.5                       │
└─────────────────────────────────────────────────────────────────────────────┘

Explanation: Standard practice keeps test dependencies out of the agent's
image to avoid bloat and maintain separation of concerns. While this does not
affect task solvability (pytest is irrelevant to Go debugging), it deviates
from the recommended pattern where test.sh is self-contained.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is a well-crafted debugging task with intentionally seeded logic bugs in
four Go helper functions. The bugs are subtle (inverted conditions, ignored
parameters) and require careful reasoning about replay invariants. The test
suite is excellent — using a reference implementation rather than answer tables
makes it robust to fixture variations.

Key Strengths:
  ✓ Four distinct, non-trivial bugs requiring genuine code comprehension
  ✓ Reference-based testing (replay algorithm, not hardcoded answers) resists
    cheating and validates invariants across many fixture packs
  ✓ Comprehensive documentation (report-schema.md) gives the agent enough
    information to reason about correct behavior
  ✓ Decoy packages (decoy/, gust/, grid/) add realistic noise without being
    misleading

Key Weaknesses:
  ✗ Test dependencies installed in Dockerfile rather than test.sh

Evaluates: Go debugging, algorithmic reasoning, simulation invariant analysis,
           multi-file code comprehension

================================================================================
  RECOMMENDATION: ✅ READY TO USE

  The task is well-designed and ready for use. The test dependency placement
  is a minor deviation that does not affect correctness or fairness.
================================================================================
```

## test_rubrics (from platform export)

```
Agent reads `/app/docs/report-schema.md` or `/app/docs/architecture.md` before editing replay logic, +2
Agent inspects at least two packages under `/app` (`quay`, `swell`, `keel`, `wake`, `sim`, or `cmd/navsim`) visible in the trace, +3
Agent runs `/app/bin/navsim` with `NAVSIM_OUT` or the bundled pack before or after edits and cites `voyage_report.json` fields (`berth_stack`, `lane_honor`, `cpa_clear`, or `log_aligned`) from the trace, +2
Agent edits Go sources under `/app` that affect span gates, phase selection, leg rank, or log stamp (not only the JSON output file), +5
Agent rebuilds `/app/bin/navsim` with `go build` or `make build` after source changes, +3
Agent runs the navsim driver and produces or refreshes `/app/output/voyage_report.json`, +3
Agent exercises fixture packs under `/app/data/fixtures/` (`wind_surge`, `pivot_late`, `four_unit_rush`, or `syn_*.json`) or re-runs after swapping the active pack, +2
Agent runs `go test` under `/app` or rebuilds after multi-file edits and shows pass/fail in the trace, +2
Agent coordinates fixes across at least two module roots (`quay/`, `swell/`, `keel/`, `wake/`) rather than patching a single file while leaving other replay symptoms, +2
Agent writes `/app/output/voyage_report.json` by hand without running `/app/bin/navsim`, -5
Agent changes only fixture JSON under `/app/data/` without reconciling Go replay behavior, -3
Agent patches `tests/` or deletes verifier files instead of fixing `/app` sources, -5
Agent hardcodes report booleans copied from grading fixtures without a rebuilt navsim run, -3
Agent claims success while trace output still shows wrong `berth_stack`, `lane_honor`, or `cpa_clear` on the bundled pack, -2
```

