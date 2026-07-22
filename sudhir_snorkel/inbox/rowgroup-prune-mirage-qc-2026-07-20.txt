# Platform feedback — rowgroup-prune-mirage (UID fac356b4-6394-4023-b296-30308827b30e)
Captured: 2026-07-20
Source: Snorkel Submission UI + Quality Check + Review Report + Test Quality Review
Zip: rowgroup-prune-mirage.zip (uploaded 19/07/2026, 23:11:08)

## AutoEval banner
AutoEval execution failed.
Build status: FAILED.
Build ID: CodeExecutionEnvironment:1eb340faed-48db-a0a5-1339c5109bd5

## Quality Check Results

❌ fail - behavior_in_task_description: The instruction.md describes the task at a high level but omits several key details that the tests verify. Specifically: (1) The JSON report schema is not documented — tests check for 'status', 'cases', 'digest', 'row_count', 'sum_amount', 'pages_total', 'pages_read', 'path', 'skipping', and 'case_id' fields, none of which are specified in the instruction. (2) The instruction mentions 'per-case answer and work counters' but never defines what fields these are. (3) The instruction says the ingest command stores output in a 'store-directory' but does not specify the output filename 'data.store' within that directory. (4) The page marker structure (low, high, has_absent) and what 'faithful value domain' means numerically is not described. (5) The test verifies specific numeric values for mixed.store queries (e.g., row_count=4, sum=100 for range 10–40) — these are not described in the instruction. The instruction only mentions correctness conceptually ('same correct rows and totals'), not what the expected correct values are.

✅ pass - behavior_in_tests
✅ pass - informative_test_structure
✅ pass - anti_cheating_measures

❌ fail - structured_data_schema: The instruction.md only states the JSON output has 'top-level status set to complete, cases, and digest, while preserving the existing per-case answer and work counters.' It does not document the schema for individual case objects within 'cases' — specifically fields like row_count, sum_amount, pages_total, pages_read, path, skipping, and case_id. The tests verify all these fields but they are not documented in the instruction, the architecture docs, or format-notes. The store file format (H|generation header, P|id|gen|low|high|has_absent|region_low|region_high|count page records, R|present|origin|amount|region row records) is only partially described in format-notes.md and that document explicitly states 'These notes may lag the current reader. They are useful background, not an operational contract.'

✅ pass - pinned_dependencies
✅ pass - typos
✅ pass - tests_or_solution_in_image
✅ pass - hardcoded_solution

❌ fail - file_reference_mentioned: The instruction.md says the ingest command takes '<CSV> <store-directory>' and that 'fresh inputs use /app/bin/loam ingest <CSV> <store-directory>'. However, it does not mention that the output file within the store directory is named 'data.store'. The test in _ingest() explicitly checks: target = target_dir / 'data.store' and asserts target.is_file(). An agent would need to determine the output filename by inspecting the source code or by trial and error. The instruction should explicitly state the output filename.

## Review Report (tbench-task)

Status: WARNING / RECOMMENDATION: NEEDS REVISION

Warnings:
1. Non-Canonical Docker Base Image — public.ecr.aws/docker/library/gcc:13-bookworm (digest-pinned). Confirm against canonical t-bench base image list.
2. Instruction Brevity and Implicit Requirements — tested behaviors (origin-aware liveness, legacy marker handling) only implicitly referenced via overall correctness contract. Suggest one clarifying sentence about mixed-generation slabs with incomplete markers and varied origin lanes across the two execution paths.

Test Quality Review: ROBUST / ACCEPT (no test changes required for this rejection mode).

## Local root-cause classification
Primary blockers: QC fails on behavior_in_task_description, structured_data_schema, file_reference_mentioned.
Secondary: review warnings (base image confirmation; one clarifying sentence).
Do NOT put fixture-specific oracle tallies (e.g. row_count=4, sum=100) into instruction.md — that is answer-shaped. Document field schema + semantic correctness contract instead (sibling pattern: normative schema doc referenced from instruction).
