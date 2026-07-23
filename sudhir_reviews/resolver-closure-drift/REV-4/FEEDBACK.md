## Quality Check Results
❌ fail - behavior_in_task_description: The instruction.md describes the lock file format (name version source-id per line, sorted, final newline) and the build-report.json schema (boolean success, integer members). However, several behaviors tested by the test suite are NOT described in the instruction: (1) The concepts of 'alpha', 'beta', 'plain', and 'mixed' profile modes and how they affect which packages are admissible are not explained. (2) The 'preview' and 'withdrawn' package attributes and their semantics under different profiles are not described. (3) The exact constraint format (name:low:high:channel:exact-code) is not explained in instruction.md, despite being used extensively in tests. (4) The instruction vaguely references 'two edge-case behaviors' from branches without identifying what they are (alpha preview selection, beta retained selection). (5) The tests generate new catalog entries and project files dynamically and verify specific selections — these behavioral rules are not spelled out. The instruction is deliberately opaque about the core behaviors that the agent must implement.
✅ pass - behavior_in_tests
✅ pass - informative_test_structure
✅ pass - anti_cheating_measures
✅ pass - structured_data_schema
✅ pass - pinned_dependencies
✅ pass - typos
✅ pass - tests_or_solution_in_image
✅ pass - hardcoded_solution
✅ pass - file_reference_mentioned

Also UI: AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
Build ID: CodeExecutionEnvironment:67fcefd6bb3-4f85-bc03-ccbea4229e43
Uploaded: resolver-closure-drift.zip (20/07/2026, 18:55:11)
UID: 4d74fca0-684f-4ace-a1c2-db55737f6c9a
