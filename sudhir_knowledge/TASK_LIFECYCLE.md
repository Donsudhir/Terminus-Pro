# Sudhir Terminal-Bench Task Lifecycle

## Purpose

This is the reusable operating contract for every Terminal-Bench task created in this repository. Load it whenever the request includes creating, validating, reviewing, packaging, submitting, revising, or researching a task. The goal is to avoid repeating instructions while preserving every decision, command result, review finding, and lesson.

## Source-of-truth order

When instructions conflict, use this order and record the conflict in an ADR:

1. The user's explicit instruction in the current task.
2. Accepted ADRs in `sudhir_decisions/`.
3. This lifecycle.
4. `task-type-taxonomy.md` and `.cursor/rules/`.
5. `workflow.md`, Docker guidance, reviewer guidance, and CI guidance.
6. Historical examples and old submission archives.

Never silently choose between conflicting rules. Stop, write the conflict and proposed resolution, then continue only when one source clearly wins.

## Canonical Sudhir workspace

- `sudhir_ideas/` - per-idea dossiers, generated idea index, uniqueness notes, and Step 2a records.
- `sudhir_decisions/` - immutable ADRs and the decision index.
- `sudhir_research/` - official sources, community findings, and source-quality notes.
- `sudhir_tasks/active/<task-name>/` - canonical editable task source.
- `sudhir_tasks/archived/<task-name>/` - retired or rejected task sources.
- `sudhir_reviews/<task-name>/` - review summaries and evidence pointers.
- `sudhir_tasks_ready_to_submit/` - validated final archives only.
- `sudhir_logs/` - append-only repository and task activity logs.
- `sudhir_knowledge/` - lifecycle rules, common-mistakes ledger, and knowledge graph.
- `sudhir_plans/` - current and historical execution plans.
- `sudhir_progress/` - current status, blockers, next action, and future scope.
- `sudhir_templates/` - reusable submission-output templates.

The upstream `tasks/`, `specs/`, and `Task_Ready_To_Submit/` paths are compatibility surfaces, not duplicate sources of truth. If an existing tool hardcodes an upstream path, create or repair one adapter. Never keep two independently editable copies of the same task.

## Non-negotiable task policy

- Net-new tasks cannot use `data-processing`, `debugging`, or `software-engineering` as their primary category. Evidence-backed in-flight review/revision work is exempt from later blocks.
- Net-new milestone tasks are blocked. Current `steps/milestone_N/` guidance remains for evidence-backed in-flight revisions only.
- Net-new `ui_building` tasks are blocked by house policy even though the
    platform still recognizes the subtype. In-flight UI revisions require
    source-backed exemption evidence and Python pytest + Playwright Python;
    JavaScript/Vitest verifier layouts are not grandfathered.
- Do not disguise a repair task with a category label. The core intellectual work must genuinely belong to the selected category.
- Avoid CSV, routine ETL, generic replay/reconciliation, scheduling, dispatch, ANN, embeddings, and other saturated families unless the mathematical core is demonstrably new.
- New tasks are single-container, offline, deterministic, and non-UI.
- Prefer at least two genuinely necessary low-level languages. Decorative language mixing does not count.
- Do not create Python-primary agent tasks (ADR-0014 / CM-011). Models are already strong on Python; prefer niche, difficult, less-common languages (C/C++/Rust/Fortran/Zig/Ada/Haskell/OCaml, etc.). Pytest under `tests/` for the verifier is allowed; solvable core must not be Python.
- The environment must contain a realistic existing system. Do not create blank-canvas algorithm exercises.
- The public instruction stays symptoms-only. It must be honest and complete about observable outcomes without naming causes, algorithms, thresholds, fix locations, or implementation steps.
- The task must force at least three non-trivial discoveries and at least three coordinated fix locations. No location may control a majority of tests.
- New validation loops must satisfy `LONG_HORIZON_TASK_PHILOSOPHY.md`: 2-4
    reinforcing weakness areas, a 4-8 stage causal chain, heterogeneous evidence,
    falsifiable hypotheses, failing and healthy-control scenarios, deterministic
    reproduction, domain non-trivia, and a credible 20-100 meaningful-action
    estimate. The action estimate is never part of task reward.
- Do not claim PASS, READY, APPROVED, or SUBMITTABLE without fresh command output.

## Idea portfolio contract

`sudhir_progress/registry.json` is the single mutable source for both ideas and
tasks. `sudhir_ideas/IDEA_INDEX.md` and `sudhir_progress/BOARD.md` are generated
views; never edit their statuses by hand. Every concept receives a permanent
idea ID and remains visible even when reserved or rejected, so names and failed
families are not accidentally recycled.

Track these facts separately because they answer different questions:

1. proposal check: pending, passed, failed, or honestly not recorded for old work;
2. idea gate: captured, researching, reserved, validating, approved,
    grandfathered, rejected, retired, or legacy;
3. uniqueness: pending, passed, failed, or honestly not recorded for old work;
4. execution: not started, in development, executed, or executed/revising;
5. submission: not submitted, ready, or submitted;
6. platform outcome: pending, in evaluation, in review, evaluation passed,
    needs revision, accepted, or rejected.

An evaluation pass is not final acceptance. Set `accepted` or `rejected` only
from direct platform/reviewer evidence. Do not invent retrospective uniqueness
proof for legacy tasks.

`grandfathered` is reserved for user-recognized active work that predates the
structured uniqueness dossier. Unrecognized imports are never mixed into the
active portfolio: quarantine them with their raw source, identifiers, dates,
evidence, and reason intact. Re-ingestion may refresh quarantined provenance but
must not reactivate it.

For every new idea, record a novelty fingerprint covering its domain, failure
mechanism, distributed fix topology, and verifier/invariant surface. Search the
idea registry, active tasks, archived tasks, submission archives, upstream task
corpus, and current external research. Name the closest analogue and explain a
structural difference; changing only names, languages, fixtures, or surface
domain is not unique. New non-grandfathered construction is mechanically blocked
until that dossier is PASS and Step 2a is GO with evidence.

## Lifecycle

### Phase -1 - Task Idea Proposal check

This is the first step for every candidate selected for actual task creation.
Read `web/idea-inspiration-sources.md` before generating the candidate. Use the
source ladder for inspiration, but never copy issue text, benchmark instances,
patches, tests, or book exercises.

Generate exactly these paste-ready fields first:

1. **Task Idea Summary** — 2–5 sentences;
2. **Idea Category** — one exact platform display label;
3. **Associated Skills** — 5–10 skills;
4. **Task Tags** — 3–6 tags.

Stop while the user runs **Check feedback** in the Snorkel Task Idea Proposal
form. Do not perform uniqueness research, initialize Step 2a, register a task,
or create task files yet.

When the result returns, capture the idea permanently with `idea new`, then
store the exact form fields and platform evidence with:

`python3 sudhir_task.py idea proposal <slug> passed|failed ...`

If the check fails, revise the four fields and recheck or retain the idea as
rejected. Only proposal=`passed` may enter uniqueness. This early check does not
replace eligibility, six-scope uniqueness, Step 2a, or empirical difficulty.

### Phase 0 - Load context and open a run log

Before changing anything:

1. Run `python3 sudhir_task.py board` and `python3 sudhir_task.py ingest`, then
	read `sudhir_progress/STATUS.md` and the generated idea portfolio.
2. Read the current plan in `sudhir_plans/`.
3. Read the ADR index and all ADRs relevant to the task.
4. Read the task's idea record, research record, and knowledge-graph nodes.
5. Read `task-type-taxonomy.md`, the applicable `.cursor/rules/`, and the canonical command references.
6. Record the task name, phase, goal, current Git state, and intended commands in `sudhir_logs/CHANGELOG.md`.

If the repository baseline is red, distinguish pre-existing failures from task-caused failures before editing.

### Phase 1 - Research, uniqueness, and Step 2a

1. Confirm the Task Idea Proposal check is captured as PASSED. Historical
    established work may be labeled honestly as not recorded.
2. Complete the novelty fingerprint and search every required collision scope.
3. Research official technical sources and current Terminal-Bench or Harbor guidance. Record source URL, retrieval date, claim, confidence, and implication.
4. Treat social or community reports as signals, not policy. Verify important claims against official docs or reproducible local behavior.
5. Record uniqueness PASS only with evidence, a closest analogue, and a structural differentiator.
6. Choose the primary category from `task-type-taxonomy.md` based on the actual work.
7. Run all hard-only idea checks, including the five hardness axes, discovery budget, symptoms-only test, and three-topology test.
8. For newly initialized loops, complete the evidence-contract-v3
    `investigation_profile` before accepting GO. Reject unrelated bug bundles,
    volume-based action estimates, nondeterministic races, and process-graded
    verifier designs.
9. Create the authoring spec and reviewer appendix only after the idea survives uniqueness and feasibility review.
10. Run the Step 2a validator and record GO or STOP in the idea registry. Do not create task files before a GO verdict.

### Phase 2 - Construct the task

1. Read the approved authoring spec only. Reviewer-only details must not leak into the task.
2. Create exactly the committed files under `sudhir_tasks/active/<task-name>/`.
3. Use `version = "2.0"`, anonymous author fields, `difficulty = "hard"`, the selected allowed category, and `[environment].allow_internet = false`.
4. Use 20 or more meaningful environment files for a small task. Do not pad the tree.
5. Every fix-path symbol and path must follow the construction manifest and naming pass.
6. Keep answer-shaped references, golden files, explicit bug comments, walkthroughs, AI scaffolding, and solution hints off solver-visible surfaces.
7. Write tests around mathematical invariants and observable properties. Tests must allow every valid implementation, not only the oracle's exact method.
8. Maintain an edit ledger. Any divergence from the approved spec requires an ADR or spec amendment before continuing.

### Phase 3 - Docker and build discipline

1. Read `docker environment.mdc` and `dockerfile and image best practices.mdc` before writing the Dockerfile.
2. Every `FROM` line must use an immutable SHA-256 digest.
3. The final runtime stage must use an approved canonical image or a recorded, explicitly approved exemption.
4. For C, C++, Fortran, and Rust tasks, prefer the canonical GCC and Rust image families documented by the repository. Use multi-stage builds only when they reduce the runtime surface without hiding required source.
5. Pin package versions and downloaded artifacts. Verify downloaded artifacts by checksum.
6. Install all agent and verifier dependencies at image-build time. Runtime installation is forbidden because internet access is disabled.
7. Do not copy solution files, tests, reviewer material, or hidden answers into the image.
8. Keep the build context below repository limits and include `environment/.dockerignore`.
9. Build from a clean context and record image digest, build duration, and warnings.

### Phase 4 - Cheap gates and review loop

Run in this order, stopping on the first failure:

1. Static checks.
2. Dockerfile checks.
3. Collapse and difficulty checks.
4. Packaging preview.
5. Oracle 1x.
6. NOP.
7. Full paper review against `writing_tests.mdc`, `reviewer_checklist.mdc`, `instructions_prompt.mdc`, `ci_checks.mdc`, `review-and-submit.mdc`, and `difficulty-calibration.mdc`.

For every finding:

- record the exact evidence and governing rule;
- classify it as task defect, convention conflict, unsupported finding, warning, or infrastructure issue;
- apply the smallest correct fix;
- update the edit ledger and knowledge graph;
- rerun every invalidated cheap gate;
- rerun oracle 1x and NOP after any task-file edit.

Do not inflate oracle size with comments, cosmetic rewrites, padding, dead code, or no-op edits.

### Phase 5 - Final validation and packaging

1. Confirm the task integrity checksum matches the current tree.
2. Run oracle 10x only after construction and review are stable. All ten runs must score 1.0.
3. Run NOP and require 0.0.
4. Remove legacy or accidental canary strings from the task and archive. If a current upstream rule explicitly requires one, stop and record the conflict instead of silently violating either policy.
5. Reconfirm every Docker stage uses an approved digest-pinned image.
6. Build the archive directly from the canonical Sudhir task source into `sudhir_tasks_ready_to_submit/<task-name>.zip`.
7. Exclude authoring metadata, checksums, metrics, reviewer files, AI scaffolding, caches, and hidden solution material.
8. Run submission-zip validation and the approval gate. Both must exit 0.
9. Confirm source-to-zip parity and inspect the archive listing manually.
10. Save command outputs or compact evidence summaries in the task review record. Do not store secrets or huge raw logs in Git.

### Phase 6 - Chat-only submission outputs

After final approval, emit the UI submission rubric in chat inside one code block. Follow `TASK_PROPOSAL_RUBRIC.md`. Do not write the generated rubric into the task tree or submission archive.

Also persist every Snorkel form paste into the current revision dossier with
`sudhir_task.py form-capture` (and `rubric-capture` if needed):
`DIFFICULTY.md`, `SOLUTION.md`, `VERIFICATION.md`, `RUBRIC.md` under
`sudhir_reviews/<slug>/REV-<n>/` (ADR-0012). Chat emission is for the UI;
the dossier is the durable copy.

Then emit these three paste-ready sections in chat:

#### Difficulty Explanation

- Must start exactly with `This task is hard because`.
- Four or five sentences.
- Explain the real coupled reasoning based on the finished task.

#### Solution Explanation

- Four or five sentences.
- Explain the overall approach and central idea without unsupported claims.

#### Verification Explanation

- Must start exactly with `The tests checks`.
- Four or five sentences.
- Explain the actual mathematical properties and failure modes exercised by the tests.

Writing requirements for all three:

- sound like the builder explaining completed work to another engineer;
- use simple English, varied sentence lengths, and a slightly informal voice;
- include natural observations such as `I found` or `At first I thought` only when supported;
- include two or three small natural grammar mistakes across the entire output;
- avoid polished transition phrases, buzzwords, academic tone, em dashes, en dashes, semicolons, and excessive commas;
- do not repeat wording across sections;
- do not name files, functions, paths, or repository structure unless necessary;
- never invent details not supported by the solution and tests.

### Phase 7 - Close the loop

Before ending a task session:

1. Append the action, evidence, outcome, and next action to the changelog.
2. Update the idea/task registry and regenerate both status views. After upload,
   mark submission; after feedback, record the exact platform outcome without
   upgrading an evaluation signal to acceptance.
3. Run `sudhir_task.py board`; BOARD, IDEA_INDEX, and STATUS regenerate from one
    registry snapshot. Never edit STATUS by hand.
4. Add or update ADRs for durable decisions.
5. Add new knowledge-graph nodes and edges for concepts, failures, rules, evidence, and reusable patterns.
6. Record which instruction, test, or gate prevented each defect.
7. If the session diagnosed a platform rejection or a surprising local failure,
   append `sudhir_knowledge/COMMON_MISTAKES.md` (ADR-0010) and link a
   `FAILURE-*` graph node. Walk the ledger’s pre-upload checklist before any
   “ready to upload” claim.
8. Capture unresolved risks and future experiments.
9. Leave one explicit next action so another session can resume without reconstructing context.

## Logging contract

Every meaningful log entry includes:

- timestamp;
- task and phase;
- action or command;
- result and exit code;
- evidence location;
- decision or lesson;
- next action.

ADRs are immutable after acceptance. Supersede an ADR with a new ADR rather than rewriting history. Logs may summarize command output but must never contain passwords, tokens, cookies, API keys, or private credentials.

## Current first task

- Task: `robust-predicate-scale-parity`
- Primary category: `scientific-computing`
- Planned languages: C, Rust, and Fortran
- Environment: deterministic, offline, single-container
- Status: APPROVED; final zip ready for platform upload
- Current evidence: revision-4 oracle 10/10, fresh NOP 0.0, zip/parity/approval PASS, repository pytest 241 passed and 26 skipped
- Rule: do not edit task or archive before upload; after upload mark submitted and ingest platform feedback
