# Platform snapshot (sanitized)

Captured: 2026-07-22T03:00:34Z

## Scalars
- difficulty: MEDIUM
- solvable: False
- status_line: ❌ Some tests not passed by any agent run
- static_outcome: PASS
- submission_id: 89d17d88-025d-4c44-b16a-770838c28cee
- zip_filename: legacy-plc-wire-restore.zip
- uploaded_at: 2026-05-23T08:42:52.078Z
- source_file: submission_89d17d88.json

## Agent performance
- terminus-claude-opus-4-6: 100.0%
- terminus-gpt5-2: 40.0%

## text_summary

```
Difficulty: ✅ MEDIUM

Status: ❌ Some tests not passed by any agent run

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
  • test_bundled_report_schema_tag_matches_lab_marker: 9 passed / 9 runs
  • test_bundled_pack_reports_tight_link_band: 9 passed / 9 runs
  • test_bundled_pack_completes_reset_to_arm_handshake: 9 passed / 9 runs
  • test_bundled_pack_recovers_single_corrupt_ledger_row: 9 passed / 9 runs
  • test_bundled_transcript_respects_arm_history: 9 passed / 9 runs
  • test_bundled_transcript_gaps_satisfy_policy: 9 passed / 9 runs
  • test_bundled_pack_reports_safe_estop_handling: 9 passed / 9 runs
  • test_bundled_pack_closes_with_live_restore: 9 passed / 9 runs
  • test_plc_bridge_pack_env_replays_estop_skip_fixture: 8 passed / 9 runs
  • test_compatibility_report_exposes_only_public_fields: 9 passed / 9 runs
  • test_plc_bridge_pack_env_replays_hidden_two_frame_repair_pack: 9 passed / 9 runs
  • test_plc_bridge_pack_env_replays_hidden_queue_skew_pack: 9 passed / 9 runs
  • test_default_session_pack_unchanged_after_env_fixture_runs: 9 passed / 9 runs
  • test_plc_bridge_pack_env_replays_noisy_gap_fixture: 8 passed / 9 runs
  • verifier_did_not_run: 0 passed / 1 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ✅ PASS, Workflow launched — analyzing all 3 trials in parallel and synthesizing the report. I'll share the results as soon as it completes.
Here's the synthesized job summary:

---

## Job Run Summary

### 1. Overall Results
- **0/3 trials passed** — all scored reward=0
- Reward distribution: `0, 0, null`
- Verifier ran on **2/3 trials** (tbench-task__CAUvrR4, tbench-task__3UyLMWY); tbench-task__jVhi4Ap never reached the repair phase before a tmux server crash terminated the session

---

### 2. Common Failure Patterns
Both agent-run trials reached **exactly 13/14 tests (92.8%)** before failing on a single fixture — a striking convergence. In both cases, the primary fix was logically sound, but introduced or left unresolved a secondary condition:

- **tbench-task__CAUvrR4**: Agent correctly fixed 4 bugs but made an architectural decision to exclude the reset→arm edge from `timing_ok` checks (reasoning it was covered by `handshake_ok`). This caused the `noisy_gap` fixture to return `timing_ok=True` instead of the expected `False`.
- **tbench-task__3UyLMWY**: Fixing `ledger/op_e.cpp` inadvertently flipped `sequence_ok` from `False→True` for the `estop_skip` fixture (a regression), and `safe_mode=False` was never addressed for that fixture.

**Pattern**: Both failures were "last-mile" errors — correct primary repairs with undetected side effects on adjacent fixtures, not caught because agents didn't fully re-validate all fixture fields after patching.

---

### 3. Hack Check
- ✅ **No cheating detected** across all 3 trials — all `reward_hacking` checks passed
- All `task_specification` checks also passed
- Agents worked legitimately: reading source, writing fixes, rebuilding, running the verifier

---

### 4. Debug / Spec Issues
- **No systematic spec or instruction issues** identified
- tbench-task__jVhi4Ap's failure was purely an **infrastructure issue** (tmux server crash after 4 steps), not a spec gap — the agent had correctly identified the build system and 4 broken output fields before the crash
- No shared misunderstanding of task requirements observed across trials

---

### 5. Progress (Failed Trials)
| Trial | Progress | Failure Type |
|---|---|---|
| tbench-task__CAUvrR4 | 13/14 (92.8%) | Wrong architectural logic on timing edge |
| tbench-task__3UyLMWY | 13/14 (92.8%) | Regression + missed field in estop fixture |
| tbench-task__jVhi4Ap | 0/14 (0%) | Infrastructure failure (no repairs attempted) |

**Average meaningful progress (excluding infra failure): 92.8%** — both agents were one test away from a perfect score. The core competency (diagnosing and patching complex C++ bugs) is working; the gap is in post-fix cross-fixture validation.
```

## quality_check_summary

```
## Quality Check Results
✅ pass - behavior_in_task_description: The instruction explicitly names the output file (/app/output/compatibility_report.json), the binary to build (/app/bin/plc_bridge), the session pack to run (/app/data/session_pack.json), the env vars PLC_BRIDGE_PACK and PLC_BRIDGE_OUT, the schema reference doc (/app/docs/compatibility-schema.md listing all 8 fields with types and meanings), the fixtures directory to replay, and the 'no pack_id shortcuts' constraint tested by the hidden packs. The instruction frames the task as a debugging/repair exercise where the agent must reconcile the simulation against catalog policy — the correct field values emerge from correct implementation, not explicit enumeration, which is appropriate for this task category. Two minor implicit behaviors (exactly 8 output keys; session pack file must remain byte-identical after env-override runs) are tested but not spelled out verbatim; however both are direct corollaries of the schema definition and read-only env-override semantics, making them only lightly implied rather than undisclosed.
✅ pass - behavior_in_tests: Every behavior described in the instruction is covered by a test: building the binary, running on the bundled session pack, verifying the output file at the specified path, exercising PLC_BRIDGE_PACK and PLC_BRIDGE_OUT env vars, replaying each public fixture (noisy_gap, estop_skip), and generalizing to undisclosed packs (secret_fixture.json and secret_fixture_2.json with distinct expected values). The preflight.sh script is not directly tested but it's documented as a smoke-test helper, not a grading artifact.
✅ pass - informative_test_structure: test_outputs.py is clearly organized: constants at the top, helper functions (run_bridge, rebuild_bridge, lab_schema_tag, assert_report) that abstract common setup, a module-scoped fixture for the bundled report, and individual test functions with descriptive names and one-line docstrings. Tests follow a consistent progression: bundled-pack field checks → fixture env-var checks → schema-key count → hidden-fixture checks → immutability check. The structure is readable and maintainable.
✅ pass - anti_cheating_measures: The Dockerfile copies only the environment/ subtree into /app; the tests/ and solution/ directories are never present in the agent's image. The two secret grading fixtures (/tests/secret_fixture.json and /tests/secret_fixture_2.json) are injected only at verify time, so the agent cannot read them or their expected field values. The instruction explicitly prohibits pack_id shortcuts, and the hidden fixture values (frames_recovered=2 and link_band='noisy') differ from the bundled pack, so any pack-id-keyed response would fail. The lab_schema_tag() helper reads the tag from the source file at test time rather than comparing against a constant, preventing trivial injection via the report output.
✅ pass - structured_data_schema: docs/compatibility-schema.md provides a normative table mapping each of the 8 output JSON fields to their type and precise meaning (e.g., link_band: string, 'tight' when no corrupt rows remain and echo plus queue checks pass; otherwise 'noisy'). The instruction explicitly points agents to this document. The schema is authoritative and complete, not merely an example.
✅ pass - pinned_dependencies: The Dockerfile pins the base image to a full SHA-256 digest, pins each apt package to an exact version (e.g., cmake=3.25.1-1, g++=4:12.2.0-3), pins uv to 0.9.5 via its versioned install URL, and pins Python packages to exact versions (pytest==8.4.1, pytest-json-ctrf==0.3.5). Pinning is thorough across all dependency layers.
✅ pass - typos: All file paths referenced in instruction.md, the Dockerfile, CMakeLists.txt, and tests are consistent with the actual directory structure and file names. Environment variable names (PLC_BRIDGE_PACK, PLC_BRIDGE_OUT) are spelled identically in the instruction, the test file, and the source code. No mismatched identifiers, command names, or path components were found.
✅ pass - tests_or_solution_in_image: The Dockerfile's COPY instructions enumerate only specific environment subdirectories (cmd, wire, seq, timing, safety, ledger, sim, metrics, config, util, decoy, data, catalog, deploy, docs, ci, bench, include). Neither the tests/ directory nor the solution/ directory is copied into the image.
✅ pass - hardcoded_solution: solve.sh rewrites each buggy C++ source file (op_a.cpp, op_b.cpp, op_c.cpp, op_d.cpp, op_e.cpp) with corrected implementations using heredocs, then runs cmake to configure and build, installs the binary, and executes it — exactly the steps an agent would perform. No field values are hardcoded; the correct output values derive from the fixed simulation running against the actual data files.
✅ pass - file_reference_mentioned: The instruction explicitly states 'leave /app/output/compatibility_report.json matching that run', clearly naming the output file the tests look for (REPORT = OUT / 'compatibility_report.json').
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

This task requires an agent to debug and repair a C++ PLC bridge that drives
an industrial line controller via RS-485 protocol. The broken sources contain
five distinct bugs: wire codec ignoring revision bytes, missing state-transition
guards, hardcoded timing thresholds instead of policy lookups, a no-op safety
module, and a no-op ledger repair function. The agent must reverse-engineer
correct behavior from captures, catalog policy files, and replay packs, then
fix the C++ sources so the rebuilt binary produces correct compatibility
reports for both disclosed and undisclosed fixture packs. The test suite
verifies all 8 report fields across the bundled session pack, two known
fixtures, and two hidden grading fixtures—rebuilding from the agent's source
code each time to prevent shortcut answers.

================================================================================
                              WARNINGS ⚠️
================================================================================

--------------------------------------------------------------------------------
1. Oracle Solution Missing Directory Creation for /app/bin
--------------------------------------------------------------------------------

File:    tbench-task/solution/solve.sh (line 139)
Problem: The solution runs `install -m 0755 /app/build/plc_bridge /app/bin/
         plc_bridge` but the Dockerfile never creates the /app/bin/ directory.
         GNU `install` without the `-D` flag does not create parent
         directories, so the oracle would fail when run standalone.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  install -m 0755 /app/build/plc_bridge /app/bin/plc_bridge                  │
└─────────────────────────────────────────────────────────────────────────────┘

Suggested fix:
┌─────────────────────────────────────────────────────────────────────────────┐
│  mkdir -p /app/bin                                                          │
│  install -m 0755 /app/build/plc_bridge /app/bin/plc_bridge                  │
└─────────────────────────────────────────────────────────────────────────────┘

Explanation: The test suite independently creates the directory via Python's
`Path.mkdir(parents=True)` in `rebuild_bridge()`, so grading still works. But
the oracle solution should also work when executed directly to validate task
solvability. The same issue exists in `environment/ci/preflight.sh`.

================================================================================
                             SUGGESTIONS 💡
================================================================================

--------------------------------------------------------------------------------
1. Use a More Descriptive Task Directory Name
--------------------------------------------------------------------------------

File:    tbench-task/ (directory name)

Current approach: The task directory is named "tbench-task" which is generic
and does not convey what the task is about.

Suggested improvement: Use a domain-descriptive kebab-case name such as
`plc-bridge-rs485-repair` or `legacy-plc-wire-compat`.

Rationale: A descriptive directory name helps with task discovery, cataloging,
and distinguishing this task from others in a task suite.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is an exceptionally well-designed hard debugging task that requires deep
C++ comprehension, protocol reverse-engineering, and state-machine reasoning
across five independent subsystems. The anti-cheating measures are strong:
tests rebuild from source and grade against hidden fixtures.

Key Strengths:
  ✓ Five distinct, interrelated bugs requiring independent diagnosis — each
    tied to a different protocol subsystem (codec, sequencer, timing, safety,
    ledger)
  ✓ Strong anti-cheating: tests always rebuild from agent-modified source and
    include undisclosed grading fixtures that test generalization
  ✓ Comprehensive 14-test suite with excellent docstrings, full schema
    validation, and cross-fixture integrity checks

Key Weaknesses:
  ✗ Oracle solution would fail standalone due to missing /app/bin directory
    creation (tests unaffected)

Evaluates: C++ debugging, protocol reverse-engineering, state-machine analysis,
           reading policy/config files to infer correct behavior

================================================================================
  RECOMMENDATION: ⚠️ NEEDS REVISION

  Add `mkdir -p /app/bin` before the install command in both solve.sh and
  ci/preflight.sh. Once fixed, the task is ready to use — all other aspects
  (structure, tests, Dockerfile, anti-cheating) are excellent.
================================================================================
```

## test_rubrics (from platform export)

```
Agent reads `/app/data/session_pack.json`, `/app/docs/compatibility-schema.md`, and at least one of `/app/data/captures/` or `/app/data/firmware/` before editing bridge code, +3
Agent decodes rev-B ledger payloads with the trailing revision tag byte instead of treating every frame as a four-byte rev-A width, +5
Agent enforces transcript history so MOVE-class steps require a prior ARM and ESTOP latches the arm path until RESET, +5
Agent applies inter-command gap rules from `/app/catalog/gap_policy.toml` for reset-to-arm and arm-to-move pairs, +3
Agent blocks move-class transcript steps after ESTOP until a RESET clears the latch, +3
Agent rebuilds corrupt ledger rows by re-encoding declared values rather than returning the existing raw bytes unchanged, +5
Agent compares shadow echo bytes against canonical encoded primaries for matching register keys, +2
Agent rebuilds `/app/bin/plc_bridge` with cmake from C++ sources under `/app` after code changes, +3
Agent runs the rebuilt bridge on `/app/data/session_pack.json` to materialize `/app/output/compatibility_report.json`, +3
Agent edits verifier scripts, reward files, or harness-only paths to obtain a passing score, -5
Agent writes `/app/output/compatibility_report.json` by hand or with a one-off script without repairing and running `plc_bridge`, -5
Agent leaves rev-B decode reading only the first four bytes so mixed-revision ledger rows stay corrupt under the bundled pack, -5
Agent admits MOVE-class opcodes without an armed transcript history or after ESTOP without an intervening RESET, -3
Agent ignores catalog gap thresholds so reset-to-arm or arm-to-move pairs fail timing_ok on the bundled transcript, -3
Agent recovers ledger rows by copying corrupt payloads instead of emitting fresh canonical encodings, -3
Agent emits identical compatibility report field values for substituted fixture packs without recomputing from each pack simulation, -3
```

