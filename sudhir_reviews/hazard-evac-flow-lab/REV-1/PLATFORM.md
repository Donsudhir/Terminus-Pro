# Platform snapshot (sanitized)

Captured: 2026-07-22T03:00:34Z

## Scalars
- difficulty: MEDIUM
- solvable: True
- status_line: ✅ Solvable (all tests passed by at least one agent run)
- static_outcome: PASS
- submission_id: 49eb874f-b79a-4477-94f2-135a089b58cd
- zip_filename: hazard-evac-flow-lab.zip
- uploaded_at: 2026-05-26T01:23:55.203Z
- source_file: submission_49eb874f.json

## Agent performance
- terminus-claude-opus-4-6: 100.0%
- terminus-gpt5-2: 40.0%

## text_summary

```
Difficulty: ✅ MEDIUM

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-6: 100.0% (5/5 runs)
  • terminus-gpt5-2: 40.0% (2/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-gpt5-2: 3 other

Unit Tests Results:
  • test_subsystem_unit[./graph]: 10 passed / 10 runs
  • test_subsystem_unit[./flow]: 10 passed / 10 runs
  • test_subsystem_unit[./wave]: 10 passed / 10 runs
  • test_subsystem_unit[./prior]: 10 passed / 10 runs
  • test_p01: 10 passed / 10 runs
  • test_p02: 10 passed / 10 runs
  • test_p03: 10 passed / 10 runs
  • test_p04: 10 passed / 10 runs
  • test_p05: 10 passed / 10 runs
  • test_p06: 10 passed / 10 runs
  • test_p07: 9 passed / 10 runs
  • test_p08: 9 passed / 10 runs
  • test_p09: 10 passed / 10 runs
  • test_p10: 10 passed / 10 runs
  • test_p11: 10 passed / 10 runs
  • test_h01: 8 passed / 10 runs
  • test_h02: 10 passed / 10 runs
  • test_h03: 7 passed / 10 runs
  • test_h04: 7 passed / 10 runs
  • test_h05: 7 passed / 10 runs
  • test_h06: 8 passed / 10 runs
  • test_h07: 10 passed / 10 runs
  • test_h08: 10 passed / 10 runs
  • test_h09: 10 passed / 10 runs
  • test_h10: 7 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ✅ PASS, ## Job Summary: Go Simulator Repair Task

### 1. Overall Results
**0/3 trials passed** (all received reward 0.0). No agent successfully completed the task. All three trials used the same general approach pattern, suggesting a single model/agent configuration was tested.

---

### 2. Common Failure Patterns

All three trials converged on the **same root failure**: after correctly fixing the four operator stubs, agents over-engineered a fix to `sim/driver.go` that broke congestion modeling for fixture packs.

| Phase | Result |
|-------|--------|
| Fix 4 operator stubs (op_path, op_split, op_rank, op_phase) | ✅ All 3 agents succeeded |
| Pass unit tests | ✅ All 3 agents passed subsystem tests |
| Fix peak_ratio/jam_band computation | ❌ All 3 agents failed |

**The exact failure mode was identical across all trials**: agents introduced a "time-spreading" or "cumulative division" model in `driver.go` to bring `peak_ratio` down for the bundled pack, but this over-smoothed congestion — causing fixture packs explicitly designed to show congestion (`dual_bottleneck`, `shelter_tight`, `priority_stress`) to incorrectly report `jam_band="clear"`. Test failure counts were 6/25 (tbench-task__4h5rPQc), 7/25 (tbench-task__qP5aY9M), and 5/25 (tbench-task__ozTTDc8).

**Secondary failure** in tbench-task__qP5aY9M only: `late_hazard` fixture failed because the agent did not implement hazard-avoiding route selection — convoys were still routed through the blocked bridge edge.

---

### 3. Hack Check
**No cheating detected.** All three trials passed `reward_hacking` checks. Agents worked through legitimate code edits, shell commands, and binary rebuilds. No access to `solution/` directories, no writes to `reward.txt`, no manipulation of test files.

---

### 4. Systematic Instruction Issues

**No instruction defects** — all three trials passed `task_specification` checks. The spec was clear:
- `plan-schema.md` explicitly defines `peak_ratio` as **maximum per-tick edge utilization** (not cumulative)
- Jam band thresholds (`clear < 0.65`, `tight < peak_cap`, else `severe`) were documented

The failures were agent reasoning errors: agents saw `peak_ratio=1.0` or `0.821` on the bundled pack and incorrectly concluded the load model needed redesigning, rather than recognizing the operators alone were the source of the bug. A minimal operator-only fix would have produced correct fixture outputs without touching `driver.go`.

---

### 5. Progress on Failed Trials

Agents were **consistently ~76–80% complete**:
- 19/25 tests passed (tbench-task__4h5rPQc)
- 18/25 tests passed (tbench-task__qP5aY9M)  
- 20/25 tests passed (tbench-task__ozTTDc8)

The gap was entirely concentrated in congestion-sensitive fixture tests. The hardest sub-task — recognizing that `driver.go` should be left alone after fixing the operators — was missed every time.

---

### 6. Key Differences Between Agents

All three trials appear to be the same model configuration. Differences were marginal:
- **tbench-task__ozTTDc8** performed best (20/25), failing only 5 tests
- **tbench-task__qP5aY9M** performed worst (18/25) and was the only trial with an additional unique failure (hazard routing)
- **tbench-task__4h5rPQc** was the only trial to explicitly note the `all-or-nothing` grading insight, suggesting slightly better task meta-awareness

**The core fix needed** — computing peak utilization as a per-tick maximum rather than a cumulative average — was misidentified by all agents as a load-spreading problem rather than a measurement problem.
```

## quality_check_summary

```
## Quality Check Results
❌ fail - behavior_in_task_description: The instruction covers the bundled-pack pass conditions and the fixture file names but leaves several hardened-test behaviors undescribed. test_h03–h06 expect specific jam_band values (tight/severe) and numeric peak_ratio ranges for each fixture (e.g., test_h06 requires 0.95 ≤ peak_ratio ≤ 0.99 for priority_stress). test_h07 requires determinism across back-to-back runs, which is never mentioned. test_h10 manipulates phase_count=1 and expects jam_band='severe' with peak_ratio≥1.0, a behavior not described anywhere in instruction.md or plan-schema.md. An agent reading only instruction.md would not know these properties are graded.
✅ pass - behavior_in_tests: Every behavior the instruction explicitly describes is covered by at least one test: binary presence (plan fixture), bundled-pack field values (test_p01–p06), exact key set (test_p11), fixture replays (test_p07–p10, test_h03–h06), unit-test passage for all four subsystem packages (test_subsystem_unit), and field recomputation rather than copying (test_h08/h09).
✅ pass - informative_test_structure: The test file is well-organised: helper functions are clearly named (run_planner, assert_jam_peak_coherent, assert_bundled_completion), every test function has a one-sentence docstring explaining what it checks, and test IDs follow a two-tier scheme (test_p* for public/basic checks, test_h* for hardened/edge-case checks), making the intent of each test immediately clear.
✅ pass - anti_cheating_measures: The Dockerfile copies only source packages plus data into the image; neither tests/ nor solution/ is included. Expected output values are entirely derived at runtime from the simulation execution. The schema_tag is read dynamically from labels.go rather than hardcoded in the test. The decoy/ package contains plausible-looking but unused functions (LaneHint, SpreadScore) that could distract an agent looking for shortcuts. No ground-truth output files are planted in the image.
✅ pass - structured_data_schema: plan-schema.md (referenced explicitly in instruction.md) documents all six output fields with their JSON keys, Go types, and exact band thresholds (clear < 0.65, tight < peak_cap, severe ≥ peak_cap). The schema is normative and complete, not merely illustrative.
✅ pass - pinned_dependencies: The base image is pinned by SHA-256 digest (golang:1.22-bookworm@sha256:…). All apt packages carry explicit version strings (ca-certificates=20230311+deb12u1, curl=7.88.1-10+deb12u14, python3=3.11.2-1+b1, tmux=3.3a-3). uv is installed at version 0.9.5 via a versioned URL. Python packages are pinned (pytest==8.4.1, pytest-json-ctrf==0.3.5). No unversioned external dependencies are present.
✅ pass - typos: All file paths in instruction.md (/app/bin/evac_planner, /app/data/evac_pack.json, /app/output/evac_plan.json, /app/docs/plan-schema.md, fixture filenames) match the actual files in the environment. Variable names, package imports, and JSON field names are consistent across source, schema docs, and tests. No typos were found.
✅ pass - tests_or_solution_in_image: The Dockerfile contains no COPY instruction for tests/ or solution/. The verifier runs from /tests/ which is mounted at grading time, separate from the build image.
✅ pass - hardcoded_solution: solve.sh implements corrected algorithms for op_path.go (k-shortest paths via edge deletion), op_split.go (capacity-weighted flow distribution), op_phase.go (modular phase assignment), and op_rank.go (vulnerability-ratio ordering), then rebuilds the binary with go build and runs it. The answer is derived entirely through computation, not by echoing a pre-computed result.
✅ pass - file_reference_mentioned: instruction.md explicitly names the output file: 'writes /app/output/evac_plan.json'. The tests confirm this path as PLAN = APP / 'output' / 'evac_plan.json', matching the instruction.
```

## test_review

```
================================================================================
                         REVIEW REPORT: tbench-task
================================================================================

Status:        ⚠️ WARNING
Task Location: /root/harbor_tasks/tbench-task

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------

This task presents a broken Go-based city evacuation simulator where the agent
must diagnose and repair four subsystem packages (graph routing, flow
splitting, wave phasing, and priority ranking) so that the planner binary
produces correct evacuation plans. The solution fixes algorithmic bugs in
op_path.go (adds k-shortest-path via edge removal), op_split.go (capacity-
weighted distribution), op_phase.go (modulo staggering), and op_rank.go
(vulnerability-ratio sorting). The test suite contains 23+ test cases
validating subsystem unit tests, bundled pack output, fixture generalization,
mutation robustness, and determinism.

================================================================================
                              WARNINGS ⚠️
================================================================================

--------------------------------------------------------------------------------
1. Test Dependencies Installed in Dockerfile Instead of test.sh
--------------------------------------------------------------------------------

File:    tbench-task/environment/Dockerfile (lines 21-23)
Problem: pytest==8.4.1 and pytest-json-ctrf==0.3.5 are installed in the Docker
         image rather than in test.sh. The standard pattern installs test
         dependencies in test.sh to keep the agent environment clean and make
         test.sh self-contained.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh \               │
│      && /root/.local/bin/uv venv /opt/tbench-venv --seed \                  │
│      && /opt/tbench-venv/bin/pip install pytest==8.4.1 pytest-json-ctrf==0.  │
│  3.5                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘

Suggested fix: Move pytest installation into test.sh and remove the venv
setup from the Dockerfile:
┌─────────────────────────────────────────────────────────────────────────────┐
│  # In test.sh, before running pytest:                                       │
│  curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh                     │
│  source $HOME/.local/bin/env                                                │
│  uv venv .tbench-testing                                                    │
│  source .tbench-testing/bin/activate                                        │
│  uv pip install pytest==8.4.1 pytest-json-ctrf==0.3.5                       │
└─────────────────────────────────────────────────────────────────────────────┘

Explanation: Installing test-only dependencies in the Dockerfile makes test.sh
dependent on the image build and deviates from the standard self-contained
test runner pattern. The agent does not need pytest to solve the task.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is an excellent debugging/optimization task that effectively evaluates an
agent's ability to read, understand, and fix algorithmic Go code within a
realistic multi-package simulator. The broken implementations are carefully
designed to fail unit tests and produce incorrect outputs while remaining
plausible enough to require genuine comprehension.

Key Strengths:
  ✓ Well-designed bug seeding — each broken subsystem has a distinct flaw
    (single-path only, no-split, constant-phase, alphabetical-not-vuln sort)
  ✓ Strong anti-cheating: mutation tests (test_h01, test_h10) and multiple
    fixture replays prevent hardcoded answers
  ✓ Comprehensive test coverage with clear docstrings and determinism checks

Key Weaknesses:
  ✗ Test dependencies baked into Docker image rather than test.sh

Evaluates: Go debugging, graph algorithm implementation, multi-package code
           comprehension, simulation correctness reasoning

================================================================================
  RECOMMENDATION: ⚠️ NEEDS REVISION

  The task is high-quality and nearly ready. Move pytest installation from the
  Dockerfile into test.sh to follow the standard self-contained test runner
  pattern, then the task is ready to use.
================================================================================
```

## test_rubrics (from platform export)

```
Agent reads `/app/docs/plan-schema.md` or `/app/docs/architecture.md` before editing routing or replay logic, +2
Agent inspects at least two of `graph/`, `flow/`, `wave/`, `prior/`, and `sim/` packages visible in the trace, +3
Agent runs `/app/bin/evac_planner` with `EVAC_PLANNER_OUT` or default output path and cites `evac_plan.json` fields in the trace, +2
Agent edits Go sources under `/app` (not only JSON output), +5
Agent rebuilds `/app/bin/evac_planner` with `go build` after source changes, +3
Agent exercises `/app/data/evac_pack.json` or a swapped fixture pack and compares plan fields, +2
Agent coordinates fixes across at least two package roots rather than one file only, +2
Agent runs `go test` under `/app` after substantive edits and shows pass/fail in the trace, +2
Agent writes `/app/output/evac_plan.json` by hand without running `/app/bin/evac_planner`, -5
Agent patches `tests/` or deletes verifier files instead of fixing `/app` sources, -5
Agent changes only `/app/data/` fixtures without reconciling Go replay logic, -3
Agent hardcodes plan field literals copied from grading packs without a rebuilt planner run, -3
Agent claims success while trace still shows severe jam_band or false hazard_ok on the bundled pack, -2
```

