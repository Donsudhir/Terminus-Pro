# Platform snapshot (sanitized)

Captured: 2026-07-23T13:16:08Z

## Scalars
- difficulty: None
- solvable: None
- status_line: None
- static_outcome: PASS
- submission_id: 4d74fca0-684f-4ace-a1c2-db55737f6c9a
- zip_filename: resolver-closure-drift.zip
- uploaded_at: 2026-07-20T11:58:53.558Z
- source_file: submission_4d74fca0.json

## Agent performance
- (none parsed)

## text_summary

```
Failed to run difficulty check
```

## quality_check_summary

```
## Quality Check Results
❌ fail - behavior_in_task_description: The instruction.md describes the lock file format (name version source-id per line, sorted, final newline) and the build-report.json schema (boolean success, integer members). However, several behaviors tested by the test suite are NOT described in the instruction: (1) The concepts of 'alpha', 'beta', 'plain', and 'mixed' profile modes and how they affect which packages are admissible are not explained. (2) The 'preview' and 'withdrawn' package attributes and their semantics under different profiles are not described. (3) The exact constraint format (name:low:high:channel:exact-code) is not explained in instruction.md, despite being used extensively in tests. (4) The instruction vaguely references 'two edge-case behaviors' from branches without identifying what they are (alpha preview selection, beta retained selection). (5) The tests generate new catalog entries and project files dynamically and verify specific selections — these behavioral rules are not spelled out. The instruction is deliberately opaque about the core behaviors that the agent must implement.
✅ pass - behavior_in_tests: The tests cover all behaviors mentioned in instruction.md: the lock file is written to /app/output/workspace.lock (checked), build-report.json is written with boolean 'success' and integer 'members' (checked), lines use ascending bytewise tuple order (checked via sorted() assertion), no duplicate tuples (checked via set comparison), ends with one final newline (checked), byte-identical on equivalent runs (test_r05, test_r06, test_r09), transitive closure completeness is validated (validate_closure). The tests also check the two edge-case behaviors (alpha/beta preservation) and new generated package names. Overall test coverage is thorough and consistent with what instruction.md describes.
✅ pass - informative_test_structure: Each test function has a docstring (one-line description) that names what is being checked (e.g., 'Keep the alpha parent selection and compile its closure'). Test IDs are sequential (test_r01 through test_r12). The helper functions are clearly named (run_case, run_failure, parse_lock, validate_closure, write_archive, write_project). The test file includes inline data (BASE_ROWS) and a constraint/generated helper that makes the test assertions readable. The overall structure is clear and maintainable.
✅ pass - anti_cheating_measures: Several measures prevent trivial shortcuts: (1) The test suite rebuilds forge from source before every test case, so the agent cannot plant a script at /app/bin/forge. (2) Tests run in /tests with confcutdir=/tests and PYTHONSAFEPATH=1, preventing the agent from planting conftest.py or pytest.py to manipulate scoring. (3) Each test writes its own temporary archive and project file to a tmp_path directory, so the agent cannot pre-stage answers in the archive. (4) Tests dynamically generate package entries with random-ish names ('juniper', 'larch') and check specific selections, preventing hardcoded catalog manipulations. (5) The solution cannot just write the lockfile by hand since tests rebuild the binary and run it against fresh inputs each time. (6) Internet access is disabled (allow_internet = false). The environment is well-designed against cheating.
✅ pass - structured_data_schema: The instruction explicitly describes the lock file schema: 'Each lock line is <name> <version> <source-id> with one ASCII space between fields.' The instruction also specifies the build-report.json schema: 'a JSON object with boolean success and integer members equal to the lock tuple count.' The field names, types, and semantics are all normatively defined in instruction.md, not just implied by examples.
✅ pass - pinned_dependencies: Python pip packages in verifier-requirements.txt are pinned: pytest==8.4.1 and pytest-json-ctrf==0.3.5. The Dockerfile uses a pinned Rust base image by digest (rust:1.85-slim@sha256:9f841bbe...). Apt packages include version-pinned installs (e.g., git=1:2.39.5-0+deb12u3, python3=3.11.2-1+b1, tmux=3.3a-3). The Rust codebase uses Cargo.lock for reproducible builds. Pinning is thorough.
✅ pass - typos: No typos found in filenames, paths, commands, or variable names across instruction.md, tests/test_outputs.py, tests/test.sh, solution/solve.sh, or the environment files. File paths like /app/output/workspace.lock, /app/bin/forge, /app/bin/rebuild-forge are consistent throughout. The constraint format and API naming conventions are consistent.
✅ pass - tests_or_solution_in_image: The Dockerfile copies only: Makefile, bin/rebuild-forge, and bootstrap/. It does not copy tests/ or solution/ into the image. The COPY commands are explicit and limited: 'COPY Makefile /app/Makefile', 'COPY bin/rebuild-forge /opt/rebuild-forge', 'COPY bootstrap/ /opt/bootstrap/'. No tests or solution files are included in the runtime build.
✅ pass - hardcoded_solution: The solution in solve.sh writes correct implementations to three source files (src/aero/veil.rs, src/cairn/sill.rs, src/quill/quay.rs) that constitute meaningful business logic: veil.rs implements a classification function with proper policy mode handling, sill.rs implements an admission/priority function, and quay.rs implements a graph validation and lock-serialization function. These are non-trivial code transformations that derive the correct behavior through computation rather than hardcoding answers. The solution does not echo or cat any final lockfile.
✅ pass - file_reference_mentioned: Both output files are explicitly named in instruction.md: '/app/output/workspace.lock' and '/app/output/build-report.json'. The instruction also specifies the exact path for the entrypoint ('/app/bin/forge solve /app/projects/workspace.toml') and the output directory. All file references that tests check are mentioned in the instruction.
```

## test_rubrics (from platform export)

```
Agent rebuilds `/app/bin/forge` via `/app/bin/rebuild-forge` and emits `/app/output/workspace.lock` only through `/app/bin/forge solve` with exact `<name> <version> <source-id>` lines, +5
Agent produces lock lines in ascending bytewise (name, version, source-id) order with no duplicate tuples and one final newline, +3
Agent solves a set that satisfies all direct and transitive requirements for bundled and generated projects, +3
Agent preserves both established parent edge-case selections after the merge repair, +5
Agent produces byte-identical lockfiles under equivalent package archive orderings, +2
Agent produces byte-identical lockfiles on clean repeated solves, +1
Agent writes `/app/output/build-report.json` with success true and members equal to the lock tuple count, +2
Agent completes the bundled downstream build offline using the solved lock, +2
Agent hand-writes `/app/output/workspace.lock` or bypasses rebuild-forge, -5
Agent tampers with tests, verifier, or reward files, -5
Agent makes network calls or fetches remote packages instead of using bundled offline data, -3
Agent hardcodes expected lock tuples or report fields instead of repairing the solver, -3
```

