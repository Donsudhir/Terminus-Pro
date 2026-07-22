# Gold Harness Repair Execution Plan

- Status: Completed
- Started: 2026-07-18
- Owner: Sudhir task lifecycle
- Scope: restore a trustworthy, reproducible baseline before TASK-RPSP-001 Step 2a

## Safety constraints

- Do not delete or overwrite existing task sources, zips, specs, or user artifacts.
- Hash and index untracked artifacts before moving or adapting them.
- Do not fabricate historical regression evidence.
- Prefer current synthetic fixtures and generated parity mirrors over pretending lost fixture trees were recovered.
- Keep each repair slice independently testable.
- Record every changed contract in an ADR when behavior changes.

## Baseline

- `pytest`: 262 collected, 192 passed, 44 failed, 26 skipped.
- Canonical unittest runner: 262 run, 177 failures, 35 errors, 26 skipped.
- Step 2a schema exists locally but is ignored by Git.
- Historical full regression tasks named by `repo_tests/cases.py` are absent from local files, Git history, remote branches, and submission archives.
- Current branch matches remote main before repair.

## Repair slices

### Slice A - Preservation and tracking

1. Save a SHA-256 manifest for pre-existing untracked artifacts.
2. Anchor ignore rules to root workspaces instead of suppressing nested fixture paths.
3. Explicitly track the Step 2a schema while keeping generated specs ignored.
4. Add ignore rules for generated state under the Sudhir namespace.

Acceptance:

- artifact hashes are recorded;
- schema appears as trackable;
- nested fixture paths are not ignored;
- active task workspaces remain protected from accidental bulk commits.

### Slice B - Documentation and policy consistency

1. Standardize references on `workflow.md`.
2. Resolve Step 2b oracle 1x versus Step 4 oracle 10x wording.
3. Bring always-on agent/rule documents under their tested size limits without deleting policy ownership.
4. Record any canary-policy conflict rather than silently choosing.

Acceptance:

- no broken workflow-document references;
- oracle timing is consistent across docs, skills, and approval help;
- document-cap tests pass.

### Slice C - Regression fixture modernization

The lost historical full fixtures cannot be honestly reconstructed. Replace dependence on them using two fixture classes:

1. Synthetic fixtures committed under explicit, non-ignored paths for checker behavior.
2. Generated submission parity mirrors containing only task metadata and instructions extracted from current archives.

Update tests so:

- checker behavior is pinned by purpose-built synthetic fixtures;
- archive-name parity is pinned by generated mirrors;
- no test claims a shipping archive is the missing historical full source.

Acceptance:

- no FileNotFoundError for historical fixtures;
- static, collapse, approval, instrumentation, and sentinel tests use recoverable fixtures;
- parity mirrors cover every current submission archive.

### Slice D - Milestone-aware packaging

1. Detect standard versus milestone layout from `task.toml` and archive members.
2. Validate standard tasks using root instruction, solution, and tests.
3. Validate milestone tasks using `steps/milestone_N/` content and forbid deprecated mixed layouts.
4. Add regression tests for both shapes.

Acceptance:

- all valid standard archives pass;
- the tracked FFmpeg milestone archive passes for the right structural reason;
- malformed standard and milestone archives fail with precise messages.

### Slice E - Reproducible local toolchain

1. Add project metadata and a lock file.
2. Standardize on Python 3.12 for the current host and tests.
3. Install pinned pytest, pytest-json-ctrf, PyYAML, Ruff, and jsonschema in `.venv`.
4. Record Harbor, Docker client, daemon, and Compose versions.
5. Do not migrate Docker storage inside this repair unless a harness run proves it necessary.

Acceptance:

- `uv sync --frozen` succeeds;
- lint and tests use `.venv` rather than Conda base;
- setup documentation names the real file and command.

### Slice F - Sudhir path adapter

1. Parameterize canonical task, spec, review, and output roots.
2. Keep existing defaults for upstream compatibility.
3. Add a thin command or configuration used by the lifecycle skill.
4. Test source-to-staging and source-to-zip parity without mutable duplication.

Acceptance:

- a fixture task under `sudhir_tasks/active/` can run cheap gates;
- final archive targets `sudhir_tasks_ready_to_submit/`;
- no second mutable task source is introduced.

## Final gate

Before advancing TASK-RPSP-001:

1. Run the canonical regression suite in the locked environment.
2. Run Ruff.
3. Run schema validation on a synthetic Step 2a evidence document.
4. Run one synthetic task through preflight.
5. Record command versions, exit codes, and hashes.
6. Update current status and knowledge graph.

Required result: green baseline or a narrowly scoped accepted baseline ADR with no missing-file errors and no false claims of recovered history.

## Completion evidence

- Step 2a current-schema smoke fixture: PASS, score `[0, 0]`.
- Frozen dependency synchronization: PASS.
- Ruff: PASS.
- Pytest: 239 passed, 26 skipped.
- Canonical unittest runner: 264 tests, OK, 26 skipped.
- Submission index: current for 157 archives.
- Archive validation: 157 of 157 PASS, including one canonical milestone archive.
- Canonical Sudhir task-path preflight: exit 0; temporary probe removed.
- Skill frontmatter and lifecycle links: PASS.

Decisions are recorded in ADR-0003 and ADR-0004. No pre-existing user artifact was deleted or overwritten.
