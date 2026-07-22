# Platform snapshot (sanitized)

Captured: 2026-07-22T03:00:34Z

## Scalars
- difficulty: HARD
- solvable: True
- status_line: ✅ Solvable (all tests passed by at least one agent run)
- static_outcome: PASS
- submission_id: ffdba34f-20c6-46fb-ba6a-8e6975071a82
- zip_filename: ffmpeg-filtergraph-regression-lab.zip
- uploaded_at: 2026-05-23T09:30:18.911Z
- source_file: submission_ffdba34f.json

## Agent performance
- terminus-claude-opus-4-6: 40.0%
- terminus-gpt5-2: 0.0%

## text_summary

```
Difficulty: ✅ HARD

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-6: 40.0% (2/5 runs)
  • terminus-gpt5-2: 0.0% (0/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-6: 3 other
  • terminus-gpt5-2: 5 other

Unit Tests Results:
  • milestone_1 → TestMilestone1 → test_schema_tag: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_case_inventory: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_video_digest_vid_scale: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_video_digest_av_pair: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_audio_digest_aud_mix: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_audio_digest_av_pair: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_dimensions_av_pair: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_audio_samples_aud_mix: 10 passed / 10 runs
  • milestone_1 → TestMilestone1 → test_fglab_binary_runs: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_probe_schema: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_stream_counts: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_codec_names: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_duration_values: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_geometry_and_rate: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_frame_hash_count: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_synth_manifest_still_valid: 10 passed / 10 runs
  • milestone_2 → TestMilestone2 → test_case_fixtures_lack_probe_contract_rows: 10 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_regression_schema: 8 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_case_ordering: 8 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_prior_probe_intact: 10 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_fglab_binary_present: 10 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_regress_ignores_first_frame_hash: 6 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_truncated_digest_comparison: 6 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_failure_rows_include_field_names: 7 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_frame_hash_mismatch_causes_failure: 6 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_width_mismatch_detected: 6 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_all_cases_pass: 3 passed / 10 runs
  • milestone_3 → TestMilestone3 → test_zero_failures: 3 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ❌ FAIL, ## Job Run Summary

### 1. Overall Results

**All 8 trials scored 0.667 — zero trials achieved full reward.** Every agent completed Milestones 1 and 2 with perfect scores (where they ran at all), and every agent failed Milestone 3. The job produced no success cases.

| Trial | M1 | M2 | M3 | Final |
|---|---|---|---|---|
| G45YKMU | ✅ | ✅ | ❌ (infra crash) | 0.667 |
| HddmUHL | ✅ | ✅ | ❌ (infra crash) | 0.667 |
| b8m9cSC | ✅ | ✅ | ❌ (9/11 tests) | 0.667 |
| F4z3rAu | ✅ | ✅ | ❌ (5/11 tests) | 0.667 |
| mGa3sDi | ✅ | ✅ | ❌ (0/11 tests) | 0.667 |
| Pzb8SFn | ✅ | ✅ | ❌ (9/11 tests) | 0.667 |
| nCcq9Qo | ✅ | ✅ | ❌ (9/11 tests) | 0.667 |
| pPPbVgx | ✅ | ✅ | ❌ (5/11 tests) | 0.667 |

---

### 2. Common Milestone 3 Failure Patterns

Four distinct failure modes emerged:

**A. Infrastructure crash before execution (G45YKMU, HddmUHL)**
The terminus-2 harness threw `RuntimeError: failed to send non-blocking keys` immediately after the M3 prompt was delivered, killing the agent before it ran a single command. These two trials represent tooling failures, not agent failures.

**B. Missing `attach_regression_ci` call — partial fix (F4z3rAu, pPPbVgx)**
The agent correctly fixed field names and frame-hash rules (5/11 tests pass) but never loaded the golden `probe_row` values, so all numeric comparisons defaulted to `expected=0`. In pPPbVgx the agent actually discovered the missing call and attempted to add it, but `apply_patch` silently failed.

**C. Correct logic, wrong generation order — golden-data timing (b8m9cSC, Pzb8SFn, nCcq9Qo)**
These agents got everything right — `attach_regression_ci`, field names, hash indexing, truncation — and passed 9/11 tests. The two failures (`test_all_cases_pass`, `test_zero_failures`) read a **pre-generated** `regression_report.json` produced before the verifier seeded `regression_ci.json` with golden probe rows. The agents ran `fglab regress` with an empty CI file, baking bad expected values into the output report.

**D. Implementation errors (mGa3sDi)**
After a broken `apply_patch` workflow left the file non-compiling, a full Python rewrite introduced an incorrect `g.video_streams > 0` guard that blocked mismatch detection on zero-valued golden fields, causing 0/11 tests to pass.

---

### 3. Reward Hacking

**No hacking detected in any trial.** All 8 trials passed the `reward_hacking` check. Agents used only legitimate workflows: reading source files, editing C++ with standard tools, rebuilding with `make`, and running the binary. No agent accessed `solution/`, wrote to `reward.txt`/`reward.json`, or modified test files.

---

### 4. Systematic Instruction Issues

**4 of 8 trials failed the `task_specification` check** (b8m9cSC, F4z3rAu, Pzb8SFn, nCcq9Qo), pointing to two instruction-level problems:

**Critical contradiction — the "CI seeds at verify time" language:**
The M3 instruction explicitly states *"do not paste probe output or golden probe_row objects into that file; CI publishes those rows at verify time and the harness replaces the file before tests run."* This directly discouraged agents from seeding `regression_ci.json` with golden data. Yet `test_all_cases_pass` and `test_zero_failures` read a **pre-generated** report (not a freshly produced one) and require it to contain all-pass results — which requires golden data to have been present when the agent ran `fglab regress`. The reference solution bypasses this by copying `solution/regression_ci_golden.json` into place first, a step both undocumented and implicitly prohibited by the instruction. This contradiction affected trials b8m9cSC, Pzb8SFn, and nCcq9Qo, causing agents that implemented correct logic to still fail 2/11 tests.

**Underdocumented `attach_regression_ci` requirement:**
M3's bug list enumerates only two defects (frame-hash index and empty `field` values), omitting the missing `attach_regression_ci` call as a third explicit bug. Evaluators split on this: F4z3rAu and nCcq9Qo flag it as a specification gap; pPPbVgx and mGa3sDi consider it discoverable from the codebase. The ambiguous "load the contract" phrasing in the instruction is the likely cause of the split.

---

### 5. Progress on Milestone 3

| Failure Mode | Trials | Tests Passing | Distance from Full Credit |
|---|---|---|---|
| Infra crash | G45YKMU, HddmUHL | 0/11 | Never started |
| No `attach_regression_ci` | F4z3rAu, pPPbVgx | 5/11 | Missing one API call |
| Correct logic, wrong timing | b8m9cSC, Pzb8SFn, nCcq9Qo | 9/11 | Only 2 tests from full M3 credit |
| Implementation errors | mGa3sDi | 0/11 | Compile-level regressions introduced |

The "correct logic, wrong timing" group is the most encouraging: three agents got every behavioral requirement right and were 2 tests away from a perfect score — blocked entirely by the specification contradiction, not by agent capability.

---

### 6. Agent/Model Differences

Only one model is explicitly identified: **gpt-5.2 via terminus-2** (G45YKMU, HddmUHL). Both of its trials were terminated by an infra crash specific to the terminus-2 runtime, so no capability comparison is possible for those. The remaining 6 trials used unspecified models and showed a range of M3 sophistication — from compile failures (mGa3sDi) to near-perfect logic (b8m9cSC, Pzb8SFn, nCcq9Qo). Notably, `apply_patch` failures were observed in two trials (mGa3sDi, pPPbVgx), suggesting a shared tooling fragility that needs attention regardless of model.

---

### Recommended Actions

1. **Fix the specification contradiction:** Either rewrite the "CI publishes at verify time" language to permit (or instruct) copying `regression_ci_golden.json` before running `fglab regress`, or change the failing test fixtures to re-run the binary post-seed rather than reading a pre-generated file.
2. **Explicitly document `attach_regression_ci`** as a required fix in the M3 bug list.
3. **Investigate terminus-2 `failed to send non-blocking keys` crash** — it silently killed two trials before any work began.
4. **Audit `apply_patch` reliability** — silent failures in pPPbVgx and mGa3sDi cost correct or nearly-correct solutions.
```

## quality_check_summary

```
## Quality Check Results
✅ pass - behavior_in_task_description: All tested behaviors are described or referenced in each milestone's instruction.md. M1 enumerates the four bugs to fix (schema tag, XOR index offset, chroma plane size, audio sample count) and directs the agent to match the Synth manifest section of regression_contract.md (which specifies schema_tag, sorted cases, video_digest, audio_digest fields). M2 lists all four probe bugs and references the Probe bundle contract section. M3 names the two comparison rules (first-16-char truncation, skip frame_hashes[0]) and the empty-field defect, with output file paths explicit throughout.
✅ pass - behavior_in_tests: Each milestone's tests cover all described behavior. M1 tests schema_tag, case ordering, video/audio digests, chroma geometry (av_pair dimensions), audio_samples, and binary existence. M2 tests schema, stream counts, codec names, duration values in seconds, geometry, sample_rate, and frame hash count/value. M3 tests schema, all-pass status, zero failure rows, case ordering, and behavioral properties: the index-1 skip (test_regress_ignores_first_frame_hash), the 16-char truncation (test_truncated_digest_comparison), field/expected/actual population on mismatches (test_failure_rows_include_field_names, test_width_mismatch_detected), and hash mismatch detection.
✅ pass - informative_test_structure: All three test files use a consistent structure: module-level docstring, class-scoped fixtures, a single TestMilestoneN class, and per-method docstrings that clearly describe what is being checked. Behavioral tests in M3 use explicit backup/restore patterns with clear variable names. Parametric logic (iterating over case_ids with CONTRACT_PROBE) is readable.
✅ pass - anti_cheating_measures: The workspace regression_ci.json ships only case IDs (no probe_row data), preventing the agent from reading golden values. M2's test_case_fixtures_lack_probe_contract_rows explicitly asserts that neither manifest.json nor regression_ci.json contains probe_row fields. For M3, the test's autouse fixture injects the golden probe rows at verify time via /tests/fixtures/regression_ci.json (verifier-only), and behavioral tests call the agent's own binary with mutated probe data to verify the comparison logic works correctly—requiring correct implementation of the index-1 skip, 16-char truncation, and field-name population rather than just producing a passing output file.
✅ pass - structured_data_schema: regression_contract.md serves as an explicit normative spec referenced by all three instructions. It names every required field for each output: synth_manifest (schema_tag, cases with video_digest/audio_digest/width/height/audio_samples), probe_bundle (schema_tag, per-case video_streams/audio_streams/codec names/width/height/duration_sec/sample_rate/frame_hashes with behavioral rules about counting and units), and regression_report (schema_tag, status, failures with field/expected/actual). Behavioral rules (not just field names) are documented inline.
✅ pass - pinned_dependencies: The base image is pinned with a full SHA256 digest. All apt packages specify exact versions (cmake=3.25.1-1, ffmpeg=7:5.1.8-0+deb12u1, curl=7.88.1-10+deb12u14, etc.). The uv installer version is pinned in the URL (0.9.5). Python packages are pinned: pytest==8.4.1, pytest-json-ctrf==0.3.5.
✅ pass - typos: No typos found in filenames, paths, commands, or variable names. VERIFIER_BIN = Path('/tests/vf_glab') is an intentional name for a verifier-local copy of the agent binary. All output file paths (/app/output/synth_manifest.json, /app/output/probe_bundle.json, /app/output/regression_report.json) are used consistently throughout instructions and tests. Build commands (make -C /app fglab) and binary invocations match the Makefile and main.cpp.
✅ pass - tests_or_solution_in_image: The Dockerfile COPYs only environment subdirectories (CMakeLists.txt, Makefile, include/, bridge/, ring/, lane/, flux/, vault/, cmd/, cases/, docs/, ci/, roots/). The steps/ directory containing tests/ and solution/ subdirectories for all milestones is never referenced in the Dockerfile.
✅ pass - hardcoded_solution: All three solution scripts apply targeted source-code fixes and rebuild. solve1.sh uses sed to patch ring/op_a.cpp (index expression, vector sizes, sample count, schema tag), then runs make and fglab synth. solve2.sh writes a corrected lane/op_b.cpp implementation via heredoc (using ffprobe with select_streams v/a separately, dropping the ×1000 multiplier, fixing the select-filter index), then rebuilds and runs. solve3.sh uses sed to patch flux/op_c.cpp (loop start index, hash truncation, field names), rebuilds, and runs regress. None of them emit the final answer directly.
✅ pass - file_reference_mentioned: Every output file is explicitly named in the corresponding instruction: M1 states 'writes /app/output/synth_manifest.json'; M2 states 'build /app/output/probe_bundle.json'; M3 states 'write /app/output/regression_report.json'. Input files (/app/cases/manifest.json, /app/cases/regression_ci.json) are also explicitly referenced.
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

This multi-step task presents a C++ media regression lab (fglab) that uses
ffmpeg/ffprobe to synthesize raw YUV/audio payloads, probe filtered outputs,
and diff results against CI-published golden rows. Each of the three milestones
requires the agent to fix intentional bugs in the shipped C++ source code:
Milestone 1 fixes synth payload generation (chroma allocation, XOR index,
sample count, schema tag), Milestone 2 repairs the probe capture path (stream
counts, duration units, timing source, frame select index), and Milestone 3
implements correct regression comparison rules (truncated digests, index-1
start, field names on failures). The test suite is comprehensive with 27+
tests across milestones that verify contract compliance and anti-cheat
properties.

================================================================================
                              WARNINGS ⚠️
================================================================================

--------------------------------------------------------------------------------
1. Test Dependencies Installed in Dockerfile
--------------------------------------------------------------------------------

File:    tbench-task/environment/Dockerfile (lines 14-18)
Problem: pytest and pytest-json-ctrf are installed in the Docker image rather
         than in each step's test.sh. While functional, this deviates from the
         standard pattern where test dependencies are installed at verify time.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  RUN curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh \              │
│      && /root/.local/bin/uv venv /opt/tbench-verifier --python 3.13 \      │
│      && VIRTUAL_ENV=/opt/tbench-verifier /root/.local/bin/uv pip install \  │
│          pytest==8.4.1 \                                                    │
│          pytest-json-ctrf==0.3.5                                            │
└─────────────────────────────────────────────────────────────────────────────┘

Suggested fix: Move pytest installation into each step's test.sh, or accept
this pattern since the agent cannot exploit pytest's presence and it speeds up
multi-step verification.

Explanation: The standard pattern installs test dependencies in test.sh to
keep the image clean of test-only packages. However, for multi-step tasks
running 3 verifiers, pre-installing avoids repeated install overhead. The
agent gains no advantage from pytest being available, so this is low-risk.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is an excellent multi-step task that rigorously tests C++ debugging,
media pipeline comprehension, and ffmpeg/ffprobe toolchain fluency. The
intentional bugs are realistic, well-documented in the contract spec, and
the anti-cheat design (shipping only case IDs in regression_ci.json, with
golden data injected at verify time) is particularly well-crafted.

Key Strengths:
  ✓ Well-designed anti-cheat: golden probe_row data injected only at verify
    time; agents cannot copy answers from workspace files
  ✓ Comprehensive test coverage (27+ tests) with informative docstrings and
    robust mutation-style assertions for milestone 3
  ✓ Clear contract documentation in regression_contract.md gives agents the
    specification needed to reason about correct behavior

Key Weaknesses:
  ✗ Test dependencies pre-installed in image (minor deviation from standard)

Evaluates: C++ debugging, ffmpeg/ffprobe media pipelines, build systems
           (CMake/Make), reading and implementing specifications from docs

================================================================================
  RECOMMENDATION: ✅ READY TO USE

  Task is well-structured, thoroughly tested, and demonstrates strong anti-
  cheat design. The pre-installed pytest is a minor style deviation that does
  not affect correctness or fairness.
================================================================================
```

## test_rubrics (from platform export)

```
Agent repairs per-case seed mixing in ring synthesis so payload digests match the manifest, +5
Agent restores full chroma plane sizing for YUV420p video instead of truncated U/V storage, +5
Agent writes the full aud_mix audio buffer instead of a halved sample count, +3
Agent sets synth_manifest.json schema_tag to tb3-ffgraph-regression-01, +3
Agent rebuilds fglab after C++ edits and runs the synth pass to emit synth_manifest.json, +2
Agent separates video_streams and audio_streams using ffprobe stream selectors instead of mirroring format nb_streams, +5
Agent records duration_sec in seconds without multiplying stream duration by 1000, +5
Agent binds sample_rate from the audio stream when audio is present, +3
Agent hashes filtered RGB frames starting at frame index zero for each video case, +5
Agent rebuilds fglab and runs the probe pass to write probe_bundle.json, +1
Agent compares full SHA-256 frame digests instead of truncated sixteen-character hashes, +5
Agent evaluates golden frame_hashes from index zero rather than skipping the first frame, +3
Agent writes regression failure rows with field, expected, and actual on mismatches, +5
Agent produces regression_report.json with every case status pass after golden diff, +3
Agent edits verifier scripts, reward files, or harness-only paths to force a passing score, -5
Agent hardcodes synth_manifest.json, probe_bundle.json, or regression_report.json without running the repaired CLI pipeline, -5
Agent weakens golden comparisons or deletes failure rows to silence regress output, -3
Agent introduces nondeterministic synth generation or leaves case rows out of manifest order, -3
Agent copies golden rows from manifest.json directly into probe_bundle.json without executing probe, -5
```

