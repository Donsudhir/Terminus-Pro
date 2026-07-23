# Platform snapshot (sanitized)

Captured: 2026-07-23T13:16:08Z

## Scalars
- difficulty: HARD
- solvable: False
- status_line: ❌ Some tests not passed by any agent run
- static_outcome: PASS
- submission_id: ecea3323-138e-4636-a02c-ea96f9505840
- zip_filename: cluster-green-tail-red.zip
- uploaded_at: 2026-05-30T17:24:13.086Z
- source_file: submission_ecea3323.json

## Agent performance
- terminus-claude-opus-4-6: 0.0%
- terminus-gpt5-2: 0.0%

## text_summary

```
Difficulty: ✅ HARD

Status: ❌ Some tests not passed by any agent run

Agent Performance:
  • terminus-claude-opus-4-6: 0.0% (0/5 runs)
  • terminus-gpt5-2: 0.0% (0/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-6: 5 other
  • terminus-gpt5-2: 5 other

Unit Tests Results:
  • verifier_did_not_run: 0 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ➖ NOT_APPLICABLE, ## Job Summary

### 1. Overall Results

**0/10 trials succeeded. 10/10 failed.** No agent completed any task work — every single trial was terminated by the same infrastructure error before execution began. Reward across the board: **0**.

### 2. Common Failure Pattern (100% of trials)

All 10 trials share an identical failure mode:

> **`AgentSetupTimeoutError`** — terminus-2's `_attempt_tmux_installation` step hung inside the Daytona sandbox exec API, triggering an `asyncio.CancelledError` after the 360-second setup budget expired.

The Daytona Docker environment itself built quickly (~3–4 seconds) every time. The failure is consistently in the **post-build agent session initialization** step (tmux install), not in the environment build or task execution. This points squarely at a systemic infrastructure bug in the terminus-2 ↔ Daytona sandbox polling loop — likely a hung `environment.exec()` call that never returns or times out gracefully.

### 3. Hack Check

**No hacking — not applicable.** Since no agent ever reached execution, there was nothing to hack. All `reward_hacking` checks pass trivially (9 `pass`, 1 `not_applicable` for tbench-task__nPNt4J3). No trajectory files exist, no test files were modified, no `reward.txt` was written, and no `solution/` directory was accessed across any trial.

### 4. Debug: Instruction/Specification Issues

**Cannot assess** — all 10 `task_specification` checks are `not_applicable` due to pre-execution failure. The task (fixing a Go `cluster_lab` binary to compute latency/simulation metrics and output a precise JSON report) was never attempted.

A few analysts noted the specification *appears* reasonably complete where they could partially assess it (e.g., tbench-task__nPNt4J3 noted that `instruction.md` covers all 8 `PUBLIC_KEYS` fields, median bounds, fixture packs, and distinct-medians requirements; tbench-task__Q5NgFEu noted references to `cluster-schema.md`, `guardrails.toml`, and fixture packs), but this is speculative — no agent ran to validate it.

### 5. Agent Progress

**0% progress across all trials.** No agent steps were executed in any trial. There are no trajectory files, no code modifications, no binary rebuilds, and no verifier runs. This is a hard zero with no gradient to analyze.

### 6. Agent/Model Differences

Minimal signal here:
- **9/10 trials**: terminus-2 + `claude-opus-4-6`
- **1/10 trial** (tbench-task__TyAbosJ): terminus-2 + `GPT-5.2`

Both hit the exact same failure. The bottleneck is entirely in the terminus-2 agent framework's Daytona sandbox integration, not in the underlying model — model choice is irrelevant when setup never completes.

---

### Bottom Line

This job produced **zero useful signal** about task difficulty, agent capability, or specification quality. The entire run was consumed by a single reproducible infrastructure bug: **terminus-2 cannot successfully initialize a tmux session in the Daytona sandbox within 360 seconds**. Fix the sandbox exec polling/timeout handling in terminus-2 before re-running this job.
```

## quality_check_summary

```
## Quality Check Results
✅ pass - behavior_in_task_description: The instruction.md covers all major test behaviors: (1) binary path, no CLI args, input/output paths, and CLUSTER_LAB_OUT env var; (2) references /app/docs/cluster-schema.md as the normative JSON contract listing all 8 fields; (3) explicitly names schema_tag, median_ms, p99_band, io_wait_share, proxy_retry_heat, serving_ok, primary_ok, policy_kind; (4) states the median range (at most 25 ms below / 35 ms above catalog target); (5) describes fixture grading with both fixture names and their output directories; (6) requires distinct median_ms values across all three packs; (7) describes policy_kind=reschedule condition and the 'cleared guardrails' requirement tested by tests s02–s08.
✅ pass - behavior_in_tests: Tests cover every behavior described in the instruction: schema_tag value (s01), median_ms match and catalog range (s02), p99_band (s03), proxy_retry_heat (s04), io_wait_share (s05), primary_ok (s06), serving_ok (s07), policy_kind (s08), proxy_retry_storm fixture full recomputation (s09), neighbor_flood fixture full recomputation (s10), exact public key set (s11), distinct medians across all three packs (s12). The 'reconcile Go with catalog guardrails, rebuild, and rerun' process is implicit in the binary test setup.
✅ pass - informative_test_structure: The test file is clearly organized: module-level constants define simulation parameters, well-named helpers (run_lab, run_lab_with_pack, reference_report, assert_report_matches_pack) encapsulate repeated logic, each test function has a descriptive docstring stating exactly what it checks, and tests are numbered s01–s12 making progression clear. The Python reference_report function mirrors the intended Go algorithm, making correctness reasoning transparent.
✅ pass - anti_cheating_measures: The environment deliberately ships broken op implementations: op_a.go multiplies holdTicks by ThrottleUnitMs (45) instead of adding holdTicks; op_b.go returns streak*3 with no MaxProxyRounds guard instead of returning 0 or 1; op_c.go has the lane logic inverted (depth*4 for primary, depth for noisy); sim/driver.go accumulates io_wait for all lanes instead of only the noisy lane, iterates bg before fg (wrong order), and omits the streak reset to 0. These require genuine algorithmic analysis to fix. Tests are not copied into the Docker image. No expected output values appear in data files; fixtures contain only input parameters.
✅ pass - structured_data_schema: The instruction explicitly cites /app/docs/cluster-schema.md as the normative contract. That file provides a clear table listing all 8 fields with name, type, and precise meaning (e.g., policy_kind values 'none'/'reschedule' and their conditions). The guardrails.toml supplies the numeric thresholds (median_target_ms=50, p99_runaway_ms=3000, io_wait_cap=20, throughput_floor=4). Together these constitute an explicit, machine-readable schema.
✅ pass - pinned_dependencies: The Dockerfile pins the Python base image by SHA256 digest, Go to version 1.22.12 with SHA256 checksum verification, uv to version 0.9.5, and apt packages with explicit versions (ca-certificates=20230311+deb12u1, curl=7.88.1-10+deb12u14, tmux=3.3a-3). The test runner uses uvx with explicit -w pytest==8.4.1 and -w pytest-json-ctrf==0.3.5 flags plus pre-downloaded wheels in tests/wheels/ covering all transitive dependencies.
✅ pass - typos: All file paths, field names, environment variable names, and commands are consistent across instruction.md, cluster-schema.md, Dockerfile, test code, and source files. CLUSTER_LAB_OUT, cluster_report.json, fixture directories (fixture_neighbor, fixture_proxy), and all 8 JSON field names match exactly between instruction.md, cluster-schema.md, and test_outputs.py. No discrepancies found.
✅ pass - tests_or_solution_in_image: The Dockerfile does not COPY tests/ or solution/ into the image. It copies only Go source packages (blk, proxy, cgroup, net, pool, trace, sim, metrics, config, util, decoy, cmd), data/, catalog/, deploy/, docs/, ci/, bench/, go.mod, and Makefile. Tests are mounted separately at /tests at grading time; solution/solve.sh is never referenced in the Dockerfile.
✅ pass - hardcoded_solution: solve.sh writes correct Go source for op_a.go (lane-aware hold logic), op_b.go (MaxProxyRounds guard), op_c.go (corrected lane multipliers), and a fully rewritten sim/driver.go with correct fg-before-bg ordering, noisy-only io_wait accumulation, and streak reset. It then compiles with go build and runs the binary. The solution derives all output values through the simulation process rather than echoing pre-computed answers.
✅ pass - file_reference_mentioned: The instruction explicitly names all relevant output files: /app/output/cluster_report.json as the primary output, CLUSTER_LAB_OUT as the override directory, and /app/output/fixture_neighbor/ and /app/output/fixture_proxy/ as the fixture run output paths. These match what the tests look for in run_lab() and run_lab_with_pack().
```

## test_review

```
================================================================================
                         REVIEW REPORT: tbench-task
================================================================================

Status:        ❌ FAIL
Task Location: /root/harbor_tasks/tbench-task

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------

This task requires the agent to debug a Go-based cluster simulation lab whose
operator functions (op_a, op_b, op_c) and simulation driver contain logic bugs
that produce incorrect report output. The agent must reconcile the broken
implementations against the catalog guardrails and schema documentation, fix
the bugs, rebuild the binary, and rerun it to produce a correct cluster report.
The test suite contains 12 test functions that verify every outward JSON field
against a reference implementation and validate correct behavior across multiple
fixture scenario packs.

================================================================================
                            CRITICAL ISSUES ❌
================================================================================

--------------------------------------------------------------------------------
1. Missing asciinema in Dockerfile
--------------------------------------------------------------------------------

File:    tbench-task/environment/Dockerfile (line 5-8)
Problem: The Dockerfile uses a custom base image (python:3.13-slim-bookworm)
         which does not include asciinema. Only tmux is installed explicitly.
         The platform requires both tmux AND asciinema for terminal session
         logging. Without asciinema the session fails silently with
         verifier_did_not_run.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN apt-get update && apt-get install -y --no-install-recommends \          │
│      ca-certificates=20230311+deb12u1 \                                     │
│      curl=7.88.1-10+deb12u14 \                                              │
│      tmux=3.3a-3 \                                                          │
│      && rm -rf /var/lib/apt/lists/*                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Required fix:
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN apt-get update && apt-get install -y --no-install-recommends \          │
│      ca-certificates=20230311+deb12u1 \                                     │
│      curl=7.88.1-10+deb12u14 \                                              │
│      tmux=3.3a-3 \                                                          │
│      asciinema \                                                            │
│      && rm -rf /var/lib/apt/lists/*                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Explanation: The base image is python:3.13-slim-bookworm, not a t-bench base
image. Both tmux and asciinema must be explicitly installed for the platform's
terminal session recording to function. Without asciinema, agent sessions will
fail silently and the verifier will never run.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is a well-crafted hard debugging task that tests deep code comprehension
across multiple interacting Go packages. The bugs are subtle (inverted lane
logic, wrong accumulation variables, missing streak resets, wrong unit ordering)
and require the agent to reason about simulation semantics. The single critical
issue — missing asciinema — is a straightforward Dockerfile fix.

Key Strengths:
  ✓ Excellent anti-cheating: bugs require holistic understanding of operator
    interactions, not pattern-matching on isolated functions
  ✓ Thorough test suite with reference implementation that validates all
    report fields across three distinct scenario packs
  ✓ Well-designed decoy files and red herrings that test agent focus

Key Weaknesses:
  ✗ Missing mandatory asciinema dependency prevents session recording

Evaluates: Go debugging, cross-module reasoning, simulation logic comprehension,
           build system familiarity

================================================================================
  RECOMMENDATION: ❌ REQUIRES FIXES

  Add asciinema to the Dockerfile apt-get install line. Once fixed, the task
  is ready to use — all other aspects meet Terminal-Bench 2.0 standards.
================================================================================
```

## test_rubrics (from platform export)

```
Agent reads /app/docs/cluster-schema.md or /app/docs/architecture.md to learn the outward report contract before editing code, +2
Agent inspects at least two of the Rust crates under /app (blk, proxy, cgroup, sim) visible in the trace, +3
Agent runs /app/bin/cluster_lab on the bundled pack before or after edits and cites p99_band, proxy_retry_heat, or io_wait_share from the trace output, +2
Agent repairs block-throttle wait logic in blk/ (OpA primary vs noisy hold behavior), +5
Agent repairs proxy retry amplification logic in proxy/ (OpB rounds, streak, or limit handling), +5
Agent repairs cgroup queue wait logic in cgroup/ (OpC depth scaling per lane), +5
Agent repairs sim/driver.rs dispatch ordering, I/O wait fold, or proxy-streak reset when driver edits are visible in the trace, +3
Agent rebuilds /app/bin/cluster_lab after source changes (cargo build or make visible in the trace), +3
Agent runs /app/bin/cluster_lab and produces or refreshes /app/output/cluster_report.json, +3
Agent re-runs the lab or exercises fixture packs under /app/data/fixtures/ (neighbor_flood.json, proxy_retry_storm.json) after a fix attempt, +2
Agent consults /app/catalog/guardrails.toml for median or serving-floor expectations, +1
Agent coordinates fixes across at least two module roots (blk/, proxy/, cgroup/, or sim/) rather than patching a single file while leaving other tail symptoms, +3
Agent writes cluster_report.json by hand without running cluster_lab, -5
Agent changes only scenario_pack.json or fixture JSON without reconciling Rust behavior, -3
Agent patches tests/ or deletes verifier files instead of fixing /app sources, -5
Agent changes only policy_kind or fold thresholds in sim/driver.rs without editing wait logic under blk/, proxy/, or cgroup/, -3
Agent adds unbounded retry loops or busy-wait sleeps in application code, -3
Agent claims success while p99_band or proxy_retry_heat in the trace still show runaway or hot on the bundled pack, -2
```

