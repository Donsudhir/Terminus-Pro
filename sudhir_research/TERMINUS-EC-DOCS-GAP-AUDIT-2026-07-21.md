# Terminus EC Documentation Gap Audit

**Audit date:** 2026-07-21  
**Official source:** [Terminus EC Training documentation](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs)  
**Repository:** TERMINUS  
**Method:** Read all 44 pages exposed by the documentation navigation, then read the linked live [Task Category Status](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/category-status.md) and [Changelog](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/changelog.md). Compared those requirements against executable gates, task skeletons, lifecycle state, package validation, platform ingestion, and regression tests.

## Executive verdict

The repository is strong on custom idea validation, anti-collapse analysis, evidence capture, checksum integrity, and package parity. It is **not currently synchronized with the July 2026 Terminus policy and executable contract**.

The most serious gaps are:

1. the local `test.sh` checker rejects the current official footer and accepts a now-forbidden trailing `exit`;
2. the primary static checker still enforces the deprecated milestone layout and deprecated JavaScript UI verifier stack;
3. model calibration still targets GPT-5.2 and Claude Opus 4.6 instead of GPT-5.5 and Claude Opus 4.8;
4. net-new blocked categories and blocked milestone starts are not mechanically gated or distinguished from exempt in-flight revisions;
5. several upstream blocking CI checks have no local equivalent;
6. the local regression suite is red and the manually maintained status summary disagrees with the generated registry board.

**Current verification result:** `python3 -m repo_tests` ran 284 tests: **2 failed, 26 skipped**. The failures are the always-on AGENTS byte cap and a stale submission archive index. Therefore the repository cannot presently claim a green baseline.

## Scope and coverage

The portal navigation contained 44 Markdown pages in seven sections:

| Section                 |  Pages |
| ----------------------- | -----: |
| Getting Started         |      5 |
| Submission Process      |      3 |
| Understanding Tasks     |     11 |
| Detailed Tasking Guides |      6 |
| Testing & Validation    |      7 |
| Reviewing Tasks         |      5 |
| Reference               |      7 |
| **Total**               | **44** |

The audit also included two current policy sources linked from those pages but omitted from the documentation navigation:

- [Task Category Status](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/category-status.md)
- [Changelog](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/changelog.md)

The 44-page corpus was 339,085 bytes and every page fetched successfully.

## Severity definitions

- **P0 — correctness:** local tooling gives the wrong pass/fail result or routes active work against a currently blocked policy.
- **P1 — submission risk:** likely platform rejection, inaccurate difficulty calibration, or inability to support an allowed/exempt workflow.
- **P2 — operational:** important work remains manual, state drifts, or preventions are not enforced.
- **P3 — strategic divergence:** a deliberate house rule is stricter than the platform. It is not necessarily wrong, but must be labeled and maintained separately.

# P0 findings

## P0-1 — `test.sh` validation is inverted relative to the current official template

**Official contract**

The current [Writing Tests](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/creating-tasks/writing-tests) page and the Jun 3 / May 27 changelog entries require:

- `set -uo pipefail`;
- a defensive `rc=$?` captured immediately after pytest is accepted and preferred;
- the reward `if/else` block is the canonical end of the script;
- no trailing `exit` is required or desired;
- the documented invalid-WORKDIR guard uses `exit 0` after writing reward `0`.

**Local behavior**

- [run_static_checks.py](../run_static_checks.py#L119-L135) accepts only the inline `$?` block or an uppercase `RC` block followed by `exit "$RC"`.
- [run_static_checks.py](../run_static_checks.py#L934-L944) compares the tail literally against those two templates.
- [run_static_checks.py](../run_static_checks.py#L139-L147) allows `exit 1`, not the documented `exit 0`, before pytest.

A direct probe produced:

- official lowercase `rc=$?`, no trailing exit: **rejected**;
- locally accepted uppercase `RC` plus trailing exit: **accepted**;
- official invalid-WORKDIR `exit 0`: reported as an unexpected command.

**Consequence:** a docs-correct task can fail locally, while a current-CI-invalid task can pass locally.

**Smallest fix:** parse the reward footer semantically rather than matching literal lines. Accept inline `$?` or any shell variable captured immediately after pytest; require both binary reward branches; reject every trailing exit after the reward block; accept the documented WORKDIR guard. Add exact regression fixtures copied from the current official page.

---

## P0-2 — the primary static checker enforces the deprecated milestone layout

**Official contract**

The current [Milestones](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/milestones) contract uses:

- `steps/milestone_N/instruction.md`;
- `steps/milestone_N/tests/{test.sh,test_mN.py}`;
- `steps/milestone_N/solution/{solve.sh,solveN.sh}`;
- per-step `[steps.agent]` and `[steps.verifier]` tables;
- no root `instruction.md`, `tests/`, `solution/`, or `milestone_N.md`.

New milestone submissions are blocked, but in-flight revisions are expressly exempt and may continue.

**Local conflicts**

- [run_static_checks.py](../run_static_checks.py#L1015-L1031) unconditionally requires root `instruction.md`, root `solution/solve.sh`, and root `tests/test.sh`.
- [run_static_checks.py](../run_static_checks.py#L1157-L1196) unconditionally requires root `[verifier]` and `[agent]` tables.
- [run_static_checks.py](../run_static_checks.py#L1293-L1334) requires deprecated root `milestone_N.md`, `tests/test_mN.py`, and `solution/solveN.sh`, then requires root `solution/solve.sh` to chain every milestone.
- [scripts/check-task.sh](../scripts/check-task.sh#L12-L14) rejects a task without root `instruction.md` before Python validation begins.

The repository already contains the correct layout in [validate_submission_zip.py](../validate_submission_zip.py#L228-L320) and partially in [requirements_check.py](../requirements_check.py#L164-L214), so two incompatible milestone generations coexist.

**Consequence:** an exempt in-flight milestone revision written to the official contract cannot pass the normal local preflight.

**Smallest fix:** make `scripts/check-task.sh`, `check_required_files()`, `check_task_toml()`, `check_task_structure()`, test discovery, and oracle discovery branch on the canonical `[[steps]]` structure. Delete all root `milestone_N.md` assumptions. Add one full official-layout milestone fixture that must pass the complete preflight, not only ZIP validation.

---

## P0-3 — model calibration is one generation stale

**Official contract**

The Jun 12, 2026 changelog upgraded difficulty evaluation to:

- `@openai/gpt-5.5`;
- `@anthropic/claude-opus-4-8`;
- five runs each.

**Local conflicts**

- [agent_test.py](../agent_test.py#L3-L45) recognizes only GPT-5.2 and Claude Opus 4.6.
- [requirements_check.py](../requirements_check.py#L481-L508) recommends GPT-5.2.
- [commands.md](../commands.md#L385-L400) lists GPT-5.2 and Opus 4.6 as the calibration pair.
- [ci_checks/rubric_review.py](../ci_checks/rubric_review.py#L24-L26) defaults to Claude Opus 4.6.
- workflow and review guidance repeatedly name GPT-5.2.

The repository already contains platform feedback from Opus 4.8, but `agent_test.py` cannot group it under its hard-coded model map.

**Consequence:** local pass-rate estimates are not comparable to current platform difficulty, and stronger-model regressions may be missed until upload.

**Smallest fix:** centralize model identifiers in one policy profile, update both current models, make artifact parsing tolerate future model IDs, and version calibration evidence with the model pair and date.

---

## P0-4 — current category and structure blocks are prose-only

**Official live status**

The live category page currently blocks net-new:

- `data-processing` since 2026-07-10;
- `debugging` since 2026-06-18;
- `software-engineering` since 2026-06-18;
- milestone tasks since 2026-06-29.

Tasks already awaiting review or in a revision queue are exempt.

**Local behavior**

- [run_static_checks.py](../run_static_checks.py#L22-L32) allows all nine categories, including all three blocked categories.
- [task-type-taxonomy.md](../task-type-taxonomy.md#L54-L76) does not mark `data-processing` blocked, although it marks the other two.
- [sudhir_task.py](../sudhir_task.py#L214-L237) stores category and revision state but no policy snapshot, first-submission date, block exemption, or in-flight-at-policy-change evidence.
- [sudhir_progress/BOARD.md](../sudhir_progress/BOARD.md#L61-L68) contains an active `data-processing` task and the idea bank contains additional data-processing concepts.

`rowgroup-prune-mirage` is already in the revision queue and is therefore exempt. It should not be discarded merely because the category is now blocked. The gap is the inability to distinguish this exempt task from a new start.

**Consequence:** the system can approve construction of a net-new task the platform will reject, while a naive block could incorrectly stop an exempt revision.

**Smallest fix:** add a dated policy profile and explicit registry fields such as `policy_snapshot`, `first_submitted_at`, `in_flight_exemption`, and `exemption_evidence`. Block at `idea validation`, `new`, and `package` only when a task is net-new and has no exemption.

---

## P0-5 — the UI verifier path is obsolete

**Official contract**

The current [Task Subtypes](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/task-subtypes) and [Task Requirements](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/task-requirements) pages require UI verifiers to remain Python pytest. Browser automation must use Playwright's Python bindings, not a JavaScript or TypeScript Playwright suite.

**Local behavior**

- [run_static_checks.py](../run_static_checks.py#L1343-L1377) requires `package.json`, `playwright.config.ts`, `vitest.config.ts`, JS unit specs, and JS E2E specs.
- [run_static_checks.py](../run_static_checks.py#L1519-L1529) requires `npm run test` and `npm run test:e2e`.
- [skeleton/UI_Task_Skeleton](../skeleton/UI_Task_Skeleton) is built around the deprecated JS/TS verifier stack.

The repository blocks new UI tasks as a house rule, but also claims the skeleton remains for in-progress tasks. That compatibility path is broken against the current official contract.

**Consequence:** an in-progress UI revision following current official guidance cannot pass locally.

**Smallest fix:** either remove the skeleton and state that no UI work is supported, or replace it with pytest plus Playwright Python and make the UI branch use the same reward/test rules as other pytest tasks.

# P1 findings

## P1-1 — local Docker/CI coverage is incomplete

The repository correctly checks digest pins, `WORKDIR`, direct pip pins, apt hygiene, runtime network installs, tmux/asciinema, reserved paths, hidden test/solution copies, heredocs, recursive permissions, and some archive behavior. The following current upstream checks are missing or incomplete:

| Official check/rule               | Local gap                                                                                                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `check_sanctioned_base_images`    | No canonical 10-image final-stage list or credible non-canonical-justification check.                                                                                      |
| `check_build_context_size`        | No 100 MiB total / 50 MiB per-file gate.                                                                                                                                   |
| `check_task_sizes`                | No platform-aligned per-task-file size gate.                                                                                                                               |
| `pinned_dependencies`             | Direct pip packages are checked; npm, Cargo, Go, Maven/Gradle, lockfile validity, and checksum-pinned downloads are not comprehensively enforced.                          |
| `typos`                           | No equivalent blocking check.                                                                                                                                              |
| `check_privileged_containers`     | Regexes cover `--privileged`, `SYS_ADMIN`, and `docker.sock`, but miss `NET_ADMIN`, `SYS_MODULE`, and similar unsafe capabilities. Compose reserved mounts omit `/oracle`. |
| `check_offline_tests`             | Runtime install regex omits at least `git clone`; local-only wheel installs are not modeled explicitly.                                                                    |
| `check_layer_volatility`          | No equivalent warning.                                                                                                                                                     |
| `check_no_build_tools_in_runtime` | No final-stage build-tool warning.                                                                                                                                         |
| `check_file_extraction`           | Detects an unextracted archive but does not fully require same-stage extraction and deletion.                                                                              |

Relevant local implementations are [run_static_checks.py](../run_static_checks.py#L1546-L1697) and [dockerfile_check.py](../dockerfile_check.py#L118-L536).

**Consequence:** local approval can pass a task that current platform CI blocks.

**Recommendation:** implement official check IDs and severities directly, then pin each against synthetic fixtures copied from official good/bad examples. Keep repository-specific checks additive.

---

## P1-2 — high-severity verifier fairness rules remain manual

Current official rules prohibit:

- oracle-only or agent-only verifier branches;
- hardware latency/performance tests;
- oracle-replication thresholds within roughly 5% of oracle performance;
- non-binary rewards;
- verifier behavior that can be bypassed by editing inputs instead of computing results.

Local static checks enforce binary footer shape and source-grep resistance, while `collapse_check.py` adds useful anti-tamper analysis. There is no dedicated mechanical detector for `/oracle` mode branching, common latency assertion patterns, or near-oracle performance thresholds.

**Consequence:** these high-severity defects depend on paper review and may survive the approval gate.

**Recommendation:** add conservative static signals as blocking where exact (`/oracle` branch) and warnings where semantic (latency and near-oracle thresholds), with mandatory adjudication rather than silent waiver.

---

## P1-3 — `long_context` has an enum but no subtype contract gate

- [run_static_checks.py](../run_static_checks.py#L34-L40) accepts `long_context`.
- It does not enforce the official ≥50,000-token floor, authoritative-use requirement, anti-keyword-search requirement, or immediate-reject patterns from the [Long Context Checklist](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/reviewing-tasks/long-context-checklist).

**Consequence:** a falsely labeled long-context task can pass locally and fail review.

**Recommendation:** add a subtype-specific gate. Mechanically enforce corpus size and obvious format/generated-dump failures; require a reviewer dossier for semantic authority and anti-grep reasoning.

---

## P1-4 — rubric capture is not deterministically validated

The repository has strong rubric prose in [TASK_PROPOSAL_RUBRIC.md](../TASK_PROPOSAL_RUBRIC.md) and captures `RUBRIC.md` through `sudhir_task.py`. The capture path does not validate:

- every criterion starts with `Agent`;
- every criterion ends in `, +1|+2|+3|+5|-1|-2|-3|-5`;
- positive scores carry `+`;
- no score `4`;
- at least three negative criteria for non-milestone tasks;
- milestone `# Rubric N` sequence and at least one negative per block;
- positive maximum totals of 10–40 per task or milestone;
- forbidden references to tests, metadata, instruction, oracle, or NOP.

This is already a recurring local failure class in CM-015.

**Consequence:** malformed rubrics are stored and packaged as “pre-upload complete” even though the platform will request revision.

**Recommendation:** add `validate_rubric.py`, run it during `rubric-capture`, `form-capture`, `learn-check`, and `package`, and include focused regression tests.

---

## P1-5 — local difficulty tooling does not implement official solvability

Official “solvable” means that across 10 real-agent runs, every individual test passes at least once, even if no single run passes the full suite.

- [agent_test.py](../agent_test.py#L560-L611) classifies difficulty from full-suite pass rates.
- Existing trial analysis does not produce a per-test 10-run union matrix from CTRF artifacts.
- `verifier_health.py` tests randomized order and partial-oracle discrimination, which is useful but different.

**Consequence:** the system cannot locally reproduce the platform’s `solvable` field or identify the one test that never passes across 10 runs.

**Recommendation:** aggregate every trial’s `verifier/ctrf.json` into per-test pass counts, report union solvability separately from full-run pass rate, and store both in registry evidence.

---

## P1-6 — platform lifecycle integration is incomplete

The official CLI provides `stb submissions list`, `view`, `download`, `feedback`, `create`, and `update`. Local `sync-snorkel` only explains a manual UI export workflow.

- [sudhir_task.py](../sudhir_task.py#L151-L169) omits official `OFFERED` and `SKIPPED` states.
- [sudhir_task.py](../sudhir_task.py#L532-L559) infers a reduced internal status set.
- [sudhir_task.py](../sudhir_task.py#L938-L989) extracts data from form text with regexes.
- [sudhir_task.py](../sudhir_task.py#L2078-L2101) states that network sync is not configured, despite the supported `stb` CLI path.

Real exported JSON files do not include a simple root lifecycle state, so inference from form fields cannot replace `stb submissions list`.

**Consequence:** current platform state, feedback, offer status, skipped status, revision-queue count, and upload/update eligibility are not reliably synchronized.

**Recommendation:** implement an adapter around official `stb` commands, not an undocumented private API. Store raw response provenance and map all official states without conflating evaluation pass with acceptance.

---

## P1-7 — source-of-truth adapters are still independent mutable copies

The configured canonical roots are [sudhir_config.toml](../sudhir_config.toml):

- `sudhir_tasks/active`;
- `sudhir_ideas/specs`;
- `sudhir_tasks_ready_to_submit`.

However:

- `tasks/` and `sudhir_tasks/active/` are independent directories;
- `Task_Ready_To_Submit/` and `sudhir_tasks_ready_to_submit/` are independent directories;
- the legacy submission directory contains 159 ZIPs while the canonical directory contains 6;
- repository archive regression indexes the legacy directory, not the configured canonical directory.

**Consequence:** tooling can validate, index, or package a different copy from the one the lifecycle calls canonical.

**Recommendation:** replace compatibility paths with generated mirrors or symlinks and make every command resolve roots through one configuration function. Never allow edits in both locations.

---

## P1-8 — the current repository baseline and status views are inconsistent

Current regression failures:

1. [AGENTS.md](../AGENTS.md) is 1,679 bytes while [test_doc_size_caps.py](../repo_tests/test_doc_size_caps.py#L27-L55) caps it at 1,500 bytes.
2. [submission_index.json](../repo_tests/fixtures/submission_index.json) is stale: expected 158 archives, actual 159; the only added archive is `sparse-jacobian-color-contract.zip`.

State drift:

- [sudhir_progress/STATUS.md](../sudhir_progress/STATUS.md#L3-L10) was last updated 2026-07-19 and still describes `rowgroup-prune-mirage` REV-2 as awaiting upload.
- [sudhir_progress/BOARD.md](../sudhir_progress/BOARD.md#L61-L68), generated from the registry on 2026-07-20, shows REV-3, gates FAIL, and Needs Revision.

**Consequence:** “current status” depends on which file is read, and the always-on instruction cap intended to prevent rule skimming is itself violated.

**Recommendation:** generate `STATUS.md` from the registry or remove it from the source-of-truth chain. Make archive-index regeneration part of package/ingest transactions. Restore the regression suite before claiming repository health.

# P2 findings

## P2-1 — no dated policy snapshot or change detector

The portal changed models, category blocks, milestone policy, internet policy, minimal-codebase policy, base-image policy, rubric syntax, and test-runner syntax within weeks. The repository stores no official-doc revision date or hash with an idea, task, gate run, or package.

**Consequence:** a previously green task silently becomes stale, and reviewers cannot tell whether it is exempt under an earlier policy.

**Recommendation:** maintain a machine-readable `official_policy.json` containing source URLs, retrieval time, content hashes, effective dates, model IDs, open/blocked categories, allowed task forms, and check versions. A sync command should diff it and invalidate only affected evidence.

---

## P2-2 — portfolio diversity is not summarized or gated

Official guidance says no category should exceed roughly 30% and at least four categories should each represent at least 10%. The system stores categories but the board does not compute distribution, size mix, language mix, or subtype mix.

**Recommendation:** add a portfolio section to `board` with separate distributions for all ideas, active construction, submitted tasks, and accepted tasks. Warn rather than fail unless a live policy creates a hard block.

---

## P2-3 — daily submission and revision-queue caps are not tracked

Official limits are:

- two net-new tasks per UTC day before two acceptances;
- three per UTC day after two acceptances;
- at most 10 submissions in the revision queue;
- revisions do not count against the daily net-new cap.

The registry has no UTC submission ledger, expert-level derivation, or revision-queue count synchronized from the platform.

**Recommendation:** obtain the data through `stb submissions list`, render remaining daily capacity and queue occupancy, and block only clearly disallowed net-new uploads.

---

## P2-4 — official CI and house gates are not labeled separately

The approval stack mixes upstream compatibility requirements with local research policy. A failure message does not consistently say whether the platform would reject the task or the repository has chosen a stricter bar.

**Consequence:** stale house assumptions can masquerade as platform facts, while maintainers may remove valuable local safeguards thinking they are outdated upstream checks.

**Recommendation:** every check should declare `source = official|house`, `official_check_id`, `effective_date`, and `severity`. Approval should show two independent verdicts: **platform-compatible** and **house-policy-approved**.

# P3 strategic divergences

These are deliberate or potentially deliberate constraints, not automatically defects. They diverge from current official acceptance and should be explicitly marked as house policy.

| Axis          | Current official policy                                                                             | Local policy / implementation                                                                                                                            |
| ------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Difficulty    | Medium and Hard accepted; Easy blocked                                                              | Lifecycle says Hard-only; static code allows Medium but its error text says Hard-only; `agent_test.py` marks Medium unaccepted. Internally inconsistent. |
| Codebase size | Minimal, Small, and Large accepted; Minimal re-allowed May 11                                       | Local static gate rejects Minimal and requires ≥20 files.                                                                                                |
| Internet      | `allow_internet=true` accepted when genuinely required                                              | Local lifecycle and gates require offline/false for every task.                                                                                          |
| Python        | Python tasks accepted if empirically Hard                                                           | ADR-0014 prohibits Python-primary agent work.                                                                                                            |
| Containers    | Multi-container accepted with metadata tags                                                         | Lifecycle says new tasks are single-container, while static checks still support Compose.                                                                |
| UI            | Current official subtype docs define a pytest path and live policy page does not list UI as blocked | Local prose blocks all new UI tasks.                                                                                                                     |
| Languages     | All languages accepted                                                                              | Local policy prefers at least two necessary low-level/niche languages.                                                                                   |
| Oracle repeat | Official CI runs oracle three times                                                                 | Local final gate runs ten times; this is a useful stricter reliability check.                                                                            |

**Recommendation:** keep constraints that serve the training strategy, but move them into a named house profile. Do not encode changing platform claims in their error text. A task should be able to report “officially valid but rejected by house policy” rather than receiving an ambiguous failure.

# Official documentation contradictions found

A policy synchronization layer must account for contradictions inside the portal itself:

1. [Submission Diversity Requirements](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/diversity-requirements) says “Category: No restrictions,” while the later live category page and taxonomy block three categories. The live dated status must win.
2. Task Requirements initially calls the manifest field `task_type`, while its examples, reviewer checklist, and all current schema usage use `category`.
3. The glossary still describes older Hard/Medium/Easy thresholds; current difficulty pages use Hard ≤20%, Medium >20–60%, Easy >60–80%.
4. Some codebase-size prose uses overlapping approximate ranges; the FAQ clarifies Minimal 0–19, Small 20+, Large 200+.
5. The prompt-styling “Absolute Paths” principle contains canary-string body text, a documentation editing error.
6. The FAQ header says it was last updated June 29 even though it contains later July policy content.

**Implication:** blindly copying one page is unsafe. The policy profile needs precedence: live category status and dated changelog, then latest reviewer checklist, then topic pages, then examples/glossary.

# Controls already aligned or stronger than official docs

The audit should not obscure what is working well:

- registry and generated board distinguish idea, uniqueness, execution, submission, evaluation, and acceptance;
- Step 2a evidence contract, discovery budget, causal investigation profile, naming pass, and topology checks exceed official baseline requirements;
- `output_contract.toml` plus vocabulary/path checks mechanically support LLMaJ file/schema alignment;
- instruction checks cover absolute paths, task-name leakage, canaries, excessive structure, and hidden environment hints;
- pytest verifier checks cover discoverability, docstrings, Ruff, source-inspection resistance, runtime-install bans, and cwd-shadow hardening;
- Docker checks cover digest pins, tmux/asciinema, Python interpreter hygiene, apt hygiene, direct pip pins, prohibited test/solution copies, reserved paths, common privilege patterns, `.dockerignore`, heredocs, and broad recursive permissions;
- collapse checks are substantially stronger than the official CI on triviality, discoverability, tamper surface, visible references, and oracle locality;
- package validation excludes local metadata and AI scaffolding, detects wrapping folders, and validates source/ZIP parity;
- checksum invalidation correctly prevents approval after task-file edits;
- revision dossiers preserve platform text, form fields, evidence, and common-mistake links;
- explicit acceptance is not inferred from an evaluation pass.

# Recommended repair sequence

## Phase 0 — stop wrong local verdicts

1. Fix semantic `test.sh` footer validation and add official-snippet regressions.
2. Replace deprecated milestone validation with the `steps/milestone_N` contract; add a complete preflight fixture.
3. Decide whether legacy/in-flight UI work is supported. If yes, replace JS/Vitest verification with Python pytest + Playwright Python; if no, remove the misleading skeleton.
4. Update model IDs to GPT-5.5 and Opus 4.8 through a single policy constant.
5. Add a dated net-new policy gate with explicit in-flight exemptions.

## Phase 1 — close platform rejection holes

6. Implement sanctioned-base, build-context-size, task-file-size, ecosystem dependency, unsafe-capability, and missing Docker warning checks.
7. Add deterministic rubric validation.
8. Add long-context subtype validation.
9. Add per-test 10-run union solvability reporting.
10. Add conservative fairness checks for oracle branching, latency assertions, and oracle-replication thresholds.

## Phase 2 — restore coherent operations

11. Integrate `stb submissions list/feedback/download/update` into the registry adapter and add `OFFERED` / `SKIPPED`.
12. Collapse compatibility directories into generated adapters to the configured canonical roots.
13. Generate all current status views from the registry.
14. Restore the full regression baseline: reduce AGENTS below 1,500 bytes and regenerate the archive index.
15. Add portfolio distribution, daily-cap, and revision-queue reporting.

## Phase 3 — prevent recurrence

16. Add a policy-sync command that fetches and hashes the 44-page docs corpus plus live status/changelog.
17. Record the official policy snapshot on every idea GO, gate run, package, submission, and revision.
18. Tag each gate as official or house and render both verdicts separately.
19. Add a docs-to-check coverage manifest so every official requirement has one of: mechanical gate, mandatory paper-review item, intentional house override, or not-applicable rationale.

# Immediate task-level implications

- **Do not start new `data-processing`, `debugging`, `software-engineering`, or milestone tasks.**
- **Do not discard `rowgroup-prune-mirage` solely because `data-processing` is now blocked.** Its revision-queue status makes it exempt; retain evidence of that exemption.
- Recalibrate any task whose hardness evidence was based only on GPT-5.2 / Opus 4.6 before making a new difficulty claim.
- Do not trust current local `test.sh` acceptance as evidence of current platform compliance until the footer matcher is repaired.
- Do not claim repository-wide green status while the two observed regression failures remain.

# Audit evidence summary

| Evidence                                        | Result                                                  |
| ----------------------------------------------- | ------------------------------------------------------- |
| Official navigation pages read                  | 44 / 44                                                 |
| Linked live policy pages read                   | 2 / 2                                                   |
| Fetch failures                                  | 0                                                       |
| Official corpus size                            | 339,085 bytes                                           |
| Repository regression                           | 284 run; 2 failed; 26 skipped                           |
| Official `rc=$?` footer accepted locally        | No                                                      |
| Forbidden trailing-exit footer accepted locally | Yes                                                     |
| Official WORKDIR `exit 0` accepted locally      | No                                                      |
| Legacy submission archives                      | 159                                                     |
| Canonical Sudhir submission archives            | 6                                                       |
| Archive index drift                             | +1 unindexed ZIP (`sparse-jacobian-color-contract.zip`) |
