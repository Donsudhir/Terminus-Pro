## 2026-07-21 - RUN-0049 - Synchronization program Slice 8 complete

- Accepted/indexed ADR-0020. Added `ci_policy.py` and the 23-check official
  coverage matrix: 21 deterministic local controls, `typos` and
  `check_task_sizes` explicitly delegated upstream.
- Added exact sanctioned final-image policy (10 canonical images + scratch),
  100 MiB total / 50 MiB file context limits, and symlink-escape rejection.
- Extended dependency checks across pip/npm/Cargo/Go/Maven/Gradle, package locks,
  checksummed downloads, and commit-pinned Git clones.
- Completed unsafe capabilities and reserved mounts (`/oracle` included),
  offline-test network patterns with local-wheel exception, layer-volatility,
  runtime build-tool, and same-stage archive extraction/removal checks.
- Integrated Docker CI parity into `approve_task.py`; Docker FAIL blocks and
  WARN is visible. Approval names delegated checks rather than fabricating PASS.
- Added positive/negative/warning/false-positive fixtures. Repaired the clean
  fixture's CM-001 symlink and duplicate apt transactions.
- Shadow across all six active tasks and six runtime/language families produced
  zero new blocking or warning deltas; existing musl warning is unrelated.
- Ruff PASS; focused suite 75 PASS / 23 skipped; full regression 355 PASS /
  26 skipped. No active task/archive/checksum/registry outcome changed.
- The initial eight-slice compatibility rollout is complete. Net-new
  construction may resume after proposal PASS, eligibility, uniqueness, and
  Step 2a GO; upstream `typos` + `check_task_sizes` must pass before submission.
- Next: Workstream 2.2 deterministic rubric grammar gate.

## 2026-07-21 - RUN-0048 - Synchronization program Slice 7 complete

- Accepted/indexed ADR-0019 and added `root_adapter.py`: configured canonical
  writes, explicit historical reads, `TB3_*` overrides, hard read-only guard,
  and a tested legacy rollback mapping.
- Inventoried all root readers/writers in
  `sudhir_research/ROOT-ADAPTER-INVENTORY-2026-07-21.md`.
- Migrated pipeline, shell env, Step 2a, approval/collapse/requirements,
  similarity reading, and index generation to the adapter.
- Package/revise now atomically refresh the current index and restore the prior
  ZIP on failure. No new write targets historical `Task_Ready_To_Submit/`.
- Moved current index ownership to
  `sudhir_progress/CANONICAL_SUBMISSION_INDEX.json`; retained the independent
  historical 159-archive fixture. Current 6/6 and historical 159/159 validate.
- Three overlapping current/historical archive names are SHA-256 identical; no
  dual-write/copy migration was required.
- BOARD, IDEA_INDEX, and STATUS now share one registry generation digest and a
  grouped replacement rollback. STATUS is generated, not hand-maintained.
- Shadow: six active task sources retain zero static failures; existing warnings
  unchanged. Historical compatibility roots remain readable only.
- Root-focused suite 11 PASS; Ruff PASS; full regression 339 PASS / 26 skipped;
  registry validation 0 errors. CM-023 marked prevented.
- No task source/archive/checksum/platform outcome was rewritten by Slice 7.
- Next: Slice 8 official CI coverage matrix and one check family per isolated
  shadow/activation unit.

## 2026-07-21 - RUN-0047 - Task Idea Proposal becomes lifecycle Gate 0

- Captured the current Snorkel proposal form from user screenshots: Task Idea
  Summary (2–5 sentences), one Idea Category, Associated Skills (5–10), and
  Task Tags (3–6). Check feedback is disabled until all are complete.
- Accepted/indexed ADR-0018. For a selected new candidate, agents now output
  only the four paste-ready fields and stop for platform Check feedback before
  uniqueness, Step 2a, task registration, or file creation.
- Added `idea_proposal.py` plus `sudhir_task.py idea proposal` validation and
  capture: verdict, feedback, evidence, exact fields, normalized category,
  source provenance, and no-copy reuse boundary.
- Proposal PASS gates uniqueness and task registration. BOARD/IDEA_INDEX expose
  the Proposal axis and override stale downstream next actions while pending.
- Added `web/idea-inspiration-sources.md` with the user-directed tier ladder:
  GitHub/SWE-bench/TB papers; AoC/Unix/DevOps; bug trackers/release notes/
  Stack Overflow/Reddit; systems books; recurring model weakness surfaces.
  Current eligibility and six-scope uniqueness override source popularity.
- Updated both byte-identical lifecycle skills, canonical lifecycle, workflow,
  web ideation bundle, Option A/B handoff, command reference, idea-validation
  entry prerequisite, AGENTS routing, proposal template, and WW-013.
- AGENTS is 1,353 bytes. Ruff PASS; focused suite 41 PASS; full regression
  328 PASS / 26 skipped; registry validation 0 errors.
- Canonical index refreshed for external RPM REV-4 package `decd9555…c63132`;
  no task source or archive bytes were edited by this lifecycle change.
- Next action: use proposal-first output on the next selected candidate; Slice 7
  root-adapter planning remains pending.

## 2026-07-21 - RUN-0046 - RPM REV-4 CM-008 difficulty harden (TRIVIAL → remeasure)

- Opened REV-4 for `rowgroup-prune-mirage` (`fac356b4`) after platform
  difficulty TRIVIAL (opus-4-8 5/5, gpt5-5 5/5). Stale AutoEval FAILED banner
  ignored (CM-004); agent stats present so CM-008 applies.
- Hardening (instruction.md unchanged): removed `markers_complete` breadcrumb
  and architecture.md conservative-skip giveaway; restructured `rill.cpp` as
  lane/mask kernel; added `vault.store` + drill lines + `orders_c.csv`; schema
  all-non-live marker convention; tests p13–p15; oracle gate uses
  `generation < 3` legacy-open. Spec Construction Amendment 3.
- Ablations match flipping contract: noA {p01,p03,p05,p07,p10,p15},
  noB {p02,p03,p06,p08,p11,p13,p14}, noC {p04,p05,p06,p09,p12,p13,p15}.
- Harbor: oracle 1x `2026-07-21__07-08-14` mean 1.0; oracle 10x
  `2026-07-21__07-23-14` 10/10; post-stress NOP `2026-07-21__07-27-14` mean 0.0.
- Collapse 0 FAIL / 2 WARN (RC2, GX3) justified in `REV-4/STEP3B.md`.
- Packaged zip SHA-256
  `decd9555517e295ee363f306c35f2e453ee8b8e66f379ff16d6dc6f4c1c63132` (48 members);
  approval PASS. Form pastes in REV-4. CM-008 Seen + prevention text bumped.
- Next: re-upload zip + form pastes; wait for difficulty remeasure (≥MEDIUM).

## 2026-07-21 - RUN-0045 - Synchronization program Slice 6 complete

- Re-verified official Task Subtypes Markdown: UI verification remains Python
  pytest and browser automation uses Playwright Python, not JS/TS Playwright.
- Accepted/indexed ADR-0017: the platform recognizes `ui_building`, while
  TERMINUS separately house-blocks net-new UI; exemptions require durable
  review/revision evidence.
- Registry records now persist `subcategories`; idea/task CLIs capture them;
  task source refresh applies them before shipping eligibility.
- Dual verdicts are profile-specific: synthetic UI is official=eligible /
  house=blocked; evidence-backed in-flight UI is house=exempt-in-flight.
- Deleted the retired 15-file JS/Vitest UI scaffold. Static compatibility now
  requires standard pytest `test.sh`, Playwright Python imports, pinned Python
  dependencies, and image-build browser installation; obsolete JS verifier
  files fail.
- Shadow: 0 UI across 6 active tasks, 5 current ZIPs, and 159 historical ZIPs;
  all active tasks retain zero static failures. Existing warnings are unrelated.
- CM-022 marked prevented. Ruff PASS; focused suite 60 PASS; full repository
  regression 320 PASS / 26 skipped; registry validation 0 errors.
- No active task source or ZIP content changed. Archive indexes were refreshed
  only for an externally regenerated SJCC ZIP present in both roots.
- Next action: Slice 7 canonical-root adapter, historical read-only enforcement,
  transactional index/status generation, and rollback/parity tests.

## 2026-07-21 - RUN-0044 - ERS REV-4 instruction polarity fix

- Opened REV-4 for `envelope-rotation-shear` (`7037bf76`).
- Root content fix: `instruction.md` states public-service namespace-binding
  polarity for generated live reads vs substitutions, and maintain must not
  rewrite active matching-service records (no internal symbol names).
- Spec authoring + reviewer appendices: REV-4 amendment.
- Gates: static/dockerfile/integrity PASS; collapse 0 FAIL / 1 WARN (RC8
  justified in `REV-4/STEP3B.md`).
- Harbor: oracle 1x `2026-07-21__06-31-44` mean 1.0; oracle 10x
  `2026-07-21__06-34-26` 10/10; NOP `2026-07-21__06-36-45` mean 0.0.
- Packaged zip SHA-256
  `95066f6b07081538af232c7d2eb382606105ef6006142b0101b53b45a07dbec1`;
  approval PASS. Phase=package. CM-002 Seen bumped for ERS REV-4.

## 2026-07-21 - RUN-0043 - ERS AutoEval FAILED is tb_check, not difficulty

- Submission `7037bf76` revision_notes: AutoEval FAILED build
  `CodeExecutionEnvironment:f29d2053-a03c-4298-b83c-63785c705b97`.
- Root cause: evaluator `tb_check` FAILED (~374s) with empty
  `quality_check_summary` and empty `full_logs` (infra; not a content QC
  reject). Same eval’s `difficulty_check` SUCCEEDED: MEDIUM, solvable,
  oracle 3/3, agents 60%/60%.
- Not a task-image/Dockerfile failure for agents. Real content signal is
  instruction-sufficiency FAIL (axis convention). Updated CM-004 / CM-019
  Seen notes. Inbox copy: `sudhir_snorkel/inbox/submission_7037bf76.json`.

## 2026-07-21 - RUN-0042 - Synchronization program Slice 4 complete

- Scope: eligibility/exemption registry schema and lifecycle gates only. No task
  source, checker layout, skeleton, root default, or ZIP content changed.
- Added `eligibility_policy.py` reviewed snapshot `terminus-ec-2026-07-21`:
  data-processing/debugging/software-engineering category blocks and the
  net-new milestone block, with official dates/source URLs.
- Registry schema v3 migrated 31 ideas + 12 tasks additively with zero missing
  fields. Pre-schema work is `pre-ADR-0016` / grandfathered-pending-review and
  blocks only at package/submit when current-rule evidence is required.
- New current work is blocked before uniqueness PASS, Step 2a GO, task
  registration, package, and submitted phase. Synthetic fixtures exercised all
  three blocked categories, milestone work, shipping, and missing evidence.
- Added `eligibility` and `exemption-capture`. Exemptions require source,
  revision/review state, evidence references, reason, effective date, and ID;
  empty evidence/bare booleans fail.
- Captured RPM REV-3 `ELIGIBILITY.md`: submission `fac356b4…` is in
  `NEEDS_REVISION`. Idea/task both evaluate `exempt-in-flight`, package
  blocking=false. This does not waive any technical/reviewer gate.
- Updated lifecycle/taxonomy/authoring/idea-generation guidance and command
  reference for the live blocks. Added WW-011.
- Ruff PASS; focused suite 14/14 PASS; full suite 314 PASS / 26 skipped;
  registry validation 0 errors. Next action: Slice 5 shared layout classifier.

## 2026-07-21 - RUN-0041 - Synchronization program Slice 3 complete

- Scope: current frontier-model profile only. No registry schema, task source,
  task verdict, skeleton, root default, or archive changed.
- Added `model_policy.py`: GPT-5.5 + Claude Opus 4.8 current pair effective
  2026-06-12, current agent/quality/SDK flags, explicit legacy GPT-5.2/Opus 4.6
  parser support, and visible model-shaped unknown identifiers.
- `agent_test.py` now runs only the current pair by default, preserves legacy
  job parsing, retains unknown future models in reports, and still excludes
  oracle/NOP keys. Report metadata records the active model profile.
- Updated executable consumers and operational guidance: requirements checker,
  rubric review, QC adjudication, commands, workflow, review rule, CI guide,
  unified specification, conventions, and current feedback examples.
- Difficulty math was not edited. Regression proves identical current/legacy
  pass rates yield identical verdicts. A drift test forbids legacy defaults in
  current operational files while historical evidence remains untouched.
- Dry-run emitted exactly GPT-5.5 and Opus 4.8 commands with no API execution.
  Ruff PASS; focused suite 24 PASS / 6 skipped; full suite 299 PASS / 26 skipped.
- CM-020 remains active because eligibility/policy-snapshot enforcement is the
  next isolated slice. Next action: Slice 4 registry eligibility/exemptions.

## 2026-07-21 - RUN-0040 - Synchronization program Slice 2 complete

- Scope: semantic `tests/test.sh` reward-footer validation only. No model,
  registry schema, task source, skeleton, root, or archive edits.
- Added exact current fixtures for `rc=$?`, inline `$?`, captured/quoted status,
  and WORKDIR `exit 0`; added forbidden fixtures for trailing exit, intervening
  status-clobber command, and reversed rewards.
- Implemented `reward_txt_footer_errors`: consumes verifier status immediately,
  ignores variable casing/quote/indent style, requires success=1/failure=0, and
  rejects any substantive command after the closing `fi`. Preserved the existing
  static-check pass-message API.
- Report-only shadow: active sources 6/6 unchanged PASS; canonical ZIPs 6/6
  unchanged PASS; historical corpus 156 unchanged PASS + 5 old literal false
  negatives corrected, with zero PASS-to-FAIL regressions across 161 scripts.
- Manually inspected all five deltas. Footer semantics are valid. Separate
  historical WORKDIR/reward concerns remain outside this slice and were not
  waived.
- Post-activation: all six active canonical tasks PASS the `test_sh` selector.
  Ruff PASS; focused suite 36/36 PASS; full regression 292 PASS / 26 skipped.
- CM-021 is now prevented. Next action: Slice 3 only, current model-profile
  centralization with no intended task-verdict change.

## 2026-07-21 - RUN-0039 - Synchronization program Slice 1 complete

- Scope was deliberately limited to ADR-0016 and baseline repair. No checker
  verdict, registry schema, task source/status, root default, skeleton, or ZIP
  content changed.
- Accepted and indexed ADR-0016: official-vs-house dual verdicts, reviewed
  policy precedence, evidence-backed in-flight exemptions, additive pre-schema
  defaults, safe root migration, shadow promotion, selective invalidation,
  explicit ACCEPTED-only transitions, generated STATUS, and isolated slices.
- Reduced AGENTS.md from 1,679 to 1,247 bytes by demoting routing/command detail;
  the 1,500-byte cap was not raised.
- Diagnosed the archive drift. The sparse-Jacobian ZIP is valid (43 members) and
  byte-identical in historical and canonical roots, SHA-256 `dcc1c8f4…ffa5`.
  The historical index was stale, not the archive.
- Updated the historical index from 158 to 159 and added an independent
  canonical-current index for all six Sudhir submission archives. Added a
  regression asserting both indexes match their respective directories.
- Evidence: focused cap/index suite 16/16 PASS; changed Python test Ruff PASS;
  full `python3 -m repo_tests` PASS, 285 tests with 26 skipped.
- CM-023 remains active because root adapters and generated STATUS have not
  landed. CM-020/021/022 also remain active. Next action: execute Slice 2 only,
  beginning with official/footer fixtures and report-only shadow comparison.

## 2026-07-21 - RUN-0038 - Policy synchronization and acceptance program plan

- Goal: turn the 2026-07-21 documentation audit into an implementation-ready
  framework program that improves acceptance, accuracy, uniqueness, and
  resilience to future policy changes.
- Added `docs/exec-plans/terminus-ec-policy-sync-and-acceptance-program.md`.
  The plan defines the four-ahead loop: detect source drift, normalize a
  reviewed policy snapshot, impact-simulate every tracked artifact, then
  shadow/migrate with checksum-aware rollback.
- Architecture separates PLATFORM COMPATIBLE from HOUSE EXCELLENCE verdicts;
  preserves Step 2a evidence v3, collapse checks, checksums, dossiers, and the
  CM ledger; and adds explicit acceptance-transition evidence so evaluation is
  never inferred as acceptance.
- Program phases: restore baseline; repair the current compatibility kernel;
  close official CI/rubric/contract/solvability/uniqueness gaps; add reviewed
  policy sync and dual verdicts; integrate documented `stb` lifecycle data;
  then add predictive impact/migration and selective evidence invalidation.
- Adversarial plan review found the initial implementation batch too broad and
  the root-role migration unsafe. The plan now starts with three isolated
  slices: ADR+baseline only, semantic `test.sh` only with report-only shadow,
  then current model constants only. Registry, milestone, UI, and root changes
  land separately with grandfathering and rollback.
- No checker, registry schema, task source, task status, skeleton, archive, or
  submission package changed. Next action: execute Slice 1 only after user GO.

## 2026-07-21 - RUN-0037 - Complete Terminus EC documentation gap audit

- Scope: read all 44 docs-navigation pages plus the linked live Category Status
  and Changelog; 339,085 bytes, zero fetch failures.
- Compared official July 2026 policy and check contracts against pipeline,
  static/Docker/ZIP gates, model calibration, subtype support, rubric capture,
  solvability analysis, platform ingestion, canonical roots, and repo tests.
- Confirmed critical drift: current official `rc=$?` / no-exit `test.sh` fails
  the local matcher while the forbidden trailing-exit form passes; primary
  preflight still uses deprecated milestone and JS UI layouts; calibration
  still targets GPT-5.2 / Opus 4.6; blocked net-new categories/milestones are
  not exemption-aware mechanical gates.
- Recorded the full prioritized report at
  `sudhir_research/TERMINUS-EC-DOCS-GAP-AUDIT-2026-07-21.md`.
- Added CM-020 through CM-023 and matching knowledge-graph nodes/edges so the
  newly discovered failure modes are not left only in chat.
- Current certification is RED, not PASS: `python3 -m repo_tests` ran 284 tests
  with 2 failures and 26 skips. Failures: AGENTS.md 1,679 > 1,500-byte cap;
  submission index expected 158 but found 159 archives (new unindexed
  `sparse-jacobian-color-contract.zip`).
- Additional state drift: generated BOARD is newer than hand-maintained STATUS;
  legacy Task_Ready_To_Submit has 159 archives while canonical
  sudhir_tasks_ready_to_submit has 6.
- No task source, checker, skeleton, archive, registry status, or package was
  changed. Next action: repair Phase 0 in the audit before trusting local
  compatibility verdicts; preserve `rowgroup-prune-mirage` as an exempt
  in-flight data-processing revision.

## 2026-07-20 - RUN-0036 - SJCC REV-6 AutoEval env-build failure (CM-019)

- Task: `sparse-jacobian-color-contract` (UID `d9082cd8`); UI Needs Revision
  with “system code did not run” / empty difficulty artifact.
- Root cause: latest eval AutoEval CodeExecution builds FAILED×2 (IDs
  `983991d8…`, `c49b6cb7…`) with empty `full_logs`; Fast static PASS;
  difficulty/quality never populated. Not an EASY (CM-008) verdict this round.
- Local: `docker build --no-cache` PASS; `dockerfile_check` PASS;
  `validate_submission_zip` PASS. Captured in REV-6/FEEDBACK.md.
- Ledger: CM-019 + FAILURE-CM-019 + EVIDENCE-SJCC-011.
- Next: re-upload / re-eval (optional `build_timeout_sec` bump); do not
  hardness-revise until agent stats exist.

## 2026-07-20 - RUN-0035 - RPM REV-3 schema disclosure repair + package

- Task: `rowgroup-prune-mirage` (UID `fac356b4`); platform Needs Revision on
  QC `behavior_in_task_description`, `structured_data_schema`,
  `file_reference_mentioned`.
- REV-3: added normative `environment/docs/report-schema.md`; expanded
  `instruction.md` with inline JSON keys, `data.store`, marker semantics, and
  one mixed-generation/origin symptom sentence; pointed format-notes at the
  schema; confirmed base image is the sanctioned GCC 13 bookworm digest.
- No code/oracle/test changes. Did not embed fixture oracle tallies.
- Gates: static PASS; dockerfile PASS; collapse 0 FAIL / 1 justified RC2 WARN;
  preflight checksum 48 files.
- Harbor: oracle 1x `2026-07-20__00-18-55` mean 1.0; oracle 10x
  `2026-07-20__00-22-56` 10/10 mean 1.0; post-stress NOP
  `2026-07-20__00-26-25` mean 0.0.
- Package approval PASS (mechanical WARN only for justified RC2): 46 members,
  SHA-256 `1962af627a865f420475c013b88e536fa2e6394c6350a2f2de5454254ed1f549`.
- Ledger: CM-002 Seen bumped; CM-018 + WW-010; FAILURE-CM-018; EVIDENCE-RPM-010+.
- Next: re-upload zip, paste REV-3 form fields, `phase submitted`, ingest result.

## 2026-07-19 - RUN-0034 - ERS REV-3 Go classification + paired read contract

- Task: `envelope-rotation-shear`; trigger: platform rated MEDIUM but applied
  the Python HARD threshold because verifier-only pytest was listed as a task
  language. Agent failures also exposed a missing positive contract for direct
  reads of valid generated namespaces.
- Opened REV-3 and captured the platform feedback. Corrected `task.toml` and the
  registry to Go-only agent-facing metadata; amended the authoring spec and idea
  record consistently.
- Clarified `instruction.md` at observable level: valid live records for newly
  introduced service namespaces read without recovery, while intact
  cross-namespace substitutions still fail without recovery. No internal scope,
  cache, fallback, algorithm, or patch location was disclosed.
- Independent review found the platform's `AxisFor` prescription incomplete:
  that check already exists and an internally coherent copied source frame still
  passes it. The current strict canonicalizing oracle is a second valid design,
  so the verifier remains behavior-based rather than locking one fallback.
- Gates: spec lint PASS; static PASS; Dockerfile PASS; integrity PASS; collapse
  0 FAIL / 2 justified WARN / 21 PASS. REV-3 Step 3b verdict ACCEPT WITH NOTES.
- Harbor: oracle 1x `2026-07-19__23-51-22` mean 1.0; pre-review NOP
  `2026-07-19__23-52-55` mean 0.0. First 10x attempt hit two CM-003 Docker
  address-pool setup exceptions with eight completed trials at 1.0; after cleanup,
  `2026-07-19__23-56-00` passed 10/10 at controlled concurrency with zero
  exceptions. Fresh NOP `2026-07-19__23-58-50` scored 0.0.
- Package approval PASS with no blockers: 55 members, exact source parity,
  SHA-256 `670cac18709eecf34f899ce83125694e6fb93701940ec77453a40b5c65c50e4e`.
- CM-002 and CM-011 were extended; knowledge graph and STATUS were updated.
- Next: re-upload the REV-3 archive, paste stored REV-3 form fields, and select
  Go as the platform Language. Ingest the new result before any acceptance claim.

## 2026-07-19 - RUN-0033 - ERS REV-2 from Snorkel reviewer + CM-015/016/017

- Task: `envelope-rotation-shear` (submission `7037bf76`); outcome needs-revision.
- Lessons logged same session: CM-015 (UI rubric `Agent…, ±N` + severity tiers),
  CM-016 (initial `reward.txt` write after mkdir), CM-017 (do not brittle-pin apt
  Go toolchain); CM-002 Seen bumped for grading-only instruction gaps; WW-009 +
  PATTERN-RUBRIC-UI-001; `TASK_PROPOSAL_RUBRIC.md` got canonical/wrong examples.
- Task fixes: instruction contracts (get-fail-without-recover, maintain
  re-encrypts older, recover-with-history); unpinned `golang-go`; early reward
  write; REV-2 form fields with 27-point severity-tiered rubric.
- Prevention surfaces: Default skeleton `test.sh` + task-creation template.
- Harbor post-edit: oracle 1x `2026-07-19__22-29-43` 1.0; NOP
  `2026-07-19__22-31-21` 0.0; oracle 10x `2026-07-19__22-31-51` 10/10.
- Package: sha256 `2b36c843d8c0e602c4aed178e2533f022300f6908aa60b1cea3b9dfac7aecb90`
  (collapse RC8 WARN unchanged).
- Next: re-upload zip; paste REV-2 form fields.

## 2026-07-19 - RUN-0032 - Columnar Prune Mirage next-task build

- Task candidate: `rowgroup-prune-mirage`; phase: uniqueness / Step 2a; goal:
  create the next complete hard task as a genuine mixed Rust/C++ columnar-engine
  investigation, then validate and package it only if every lifecycle gate passes.
- Baseline: `main` already contains extensive user-owned modified and untracked
  harness/task work. No baseline file will be reverted, cleaned, or committed.
- Selection rationale: data-processing is absent from the recognized task
  portfolio, while scientific-computing is already concentrated. The candidate
  centers plan-independent query correctness rather than another numerical
  parity, replay, or generic reconciliation task.
- Initial attack: reframe the preliminary three-bug sketch around one historical
  null-representation contract spanning the Rust storage writer, C++ planner,
  and C++ execution kernels. Independently test CM-010 substitutability and
  stage-skipping before accepting mechanical Step 2a output.
- Intended commands: six-scope local collision audit; sourced `validate_loop.py`
  init/record/status; `sudhir_task.py idea uniqueness` and `idea validation`;
  construction only after both PASS/GO; then task gates, oracle 1x, NOP, paper
  review, oracle 10x, final package, and board validation.
- Offline rule: no network access. External-domain claims will use already
  captured repository sources and reproducible local behavior; lack of current
  web evidence will be stated rather than invented.
- Six-scope uniqueness: PASS. Closest analogue is `hybrid-search-latency`, but
  its graded object is retrieval quality/resource behavior rather than
  plan-independent columnar answers across archived and newly produced stores.
- Step 2a: attempt 1 returned 0 FAIL / 0 WARN under evidence contract v3;
  strict v2 spec lint PASS; ADR-0015 accepted the Rust producer + C++ planner +
  C++ batch topology.
- Construction: 47 canonical source files, 41 meaningful environment files,
  digest-pinned GCC runtime with offline Rust/C++/pytest toolchains, 12 opaque
  behavioral tests, and a 142-LOC three-location oracle.
- REV-2 review removed test-side narration of the internal authority, generated
  fresh CSV inputs per test, and added repeated audit-byte verification.
- Behavioral evidence: untouched baseline 0/12; oracle 12/12; exact ablations
  A=`p01,p03,p05,p07,p10`, B=`p02,p03,p06,p08,p11`,
  C=`p04,p05,p06,p09,p12`.
- Step 2b: preflight PASS; Harbor oracle 1x `2026-07-19__22-43-53` mean 1.0;
  NOP `2026-07-19__22-44-37` mean 0.0. Collapse has one justified RC2 WARN
  caused solely by the visible `rust/` language-directory token; 22 checks PASS.
- Step 4: oracle `2026-07-19__22-47-29` passed 10/10 with zero exceptions;
  fresh NOP `2026-07-19__22-50-35` scored 0.0. Zip validation, manifest,
  45/45 source parity, and `approve_task.py` PASS.
- Final archive: `sudhir_tasks_ready_to_submit/rowgroup-prune-mirage.zip`,
  SHA-256 `276d2d003d75ccc374e1888fad3c52cd3001980da81d4d3e9f5071c17e235047`.
- Repository regression excluding two confirmed pre-existing workspace baseline
  failures: 268 passed, 26 skipped, 2 deselected. Docker cleanup completed.
- Next: manually upload the approved zip, paste REV-2 form fields, and ingest
  direct platform feedback without treating evaluation as acceptance.

# Sudhir Task-System Changelog

Append-only. Never store secrets or raw credentials.

## 2026-07-19 - RUN-0031 - SJCC REV-5 anti-EASY (quill_tint + groups + gauge)

- Task: sparse-jacobian-color-contract (`d9082cd8`)
- Trigger: REV-4 still EASY; agents clear structural bugs; soft k05/k11 only
- Actions: move row tint to `quill_tint`; compound gauge ∞-norm+sticky;
  Euclidean + ledger.groups contracts; chromatic group asserts
- Harbor: oracle 10x `2026-07-19__20-42-41` mean 1.0; NOP `2026-07-19__20-47-48` 0.0
- Package: sha256 `c59ef678453a5b65755ab5d0ab3dfdcc7ad842587d4e980e7f36f2376c7b101a`
- Next: re-upload; platform remeasures (≥ MEDIUM)

## 2026-07-19 - RUN-0030 - ADR-0014 no Python-primary agent languages

- Trigger: Sudhir after SJCC `d9082cd8` still EASY; directive to avoid Python
  projects (models already strong; prefer niche languages)
- Added ADR-0014, CM-011, WW-008; wired into TASK_LIFECYCLE, AGENTS.md,
  idea-validation, task-creation, KNOWLEDGE_GRAPH
- Note: SJCC itself is Rust/C/Fortran — Snorkel Language=Python was form label
- Next: on new ideas enforce niche stacks; SJCC REV-5 only if Sudhir asks

## 2026-07-19 - RUN-0029 - SJCC REV-4 still-EASY → operator-weight harden

- Task: sparse-jacobian-color-contract (`d9082cd8`)
- Trigger: REV-3 platform EASY (opus 100%/gpt5 80%); agents copy term coeffs
- Actions: ridge row-weight; instruction operator-sensitivity contract; bury
  span_scratch/vault carry; tighten k04; CM-008 Seen bump
- Harbor: oracle 10x `2026-07-19__18-26-24` mean 1.0; post-10x NOP
  `2026-07-19__18-30-55` mean 0.0
- Package: sha256 `381c8ccf8263dc1bfb9fc889ec474a6c3c2e69abed60d87b40046dce7f62d00d`
- Next: re-upload; platform remeasures difficulty (target MEDIUM)

## 2026-07-19 - RUN-0028 - ERS/RCD uniqueness + Step 2a semantic reopen

- Selected `envelope-rotation-shear` and `resolver-closure-drift` from the new
  portfolio for full preparation.
- Completed six-scope uniqueness dossiers and recorded uniqueness PASS:
  `sudhir_research/TASK-ERS-001-RESEARCH.md` and
  `sudhir_research/TASK-RCD-001-RESEARCH.md`.
- Both first drafts mechanically validated at 0 FAIL / 0 WARN. RCD attempt 1
  was recorded/finalized before an independent semantic review found
  construction-blocking defects; its GO and construct phase were reopened.
- New failure mode CM-010: schema 0/0 did not detect substitutable fix
  signatures, skippable causal stages, incomplete noun extraction, or hidden
  verifier contracts.
- ERS defects caught before `record`: invalid subcategory, incomplete noun
  provenance, underspecified recovery report, artificial causal chain, and
  cause-revealing test descriptions.
- RCD defects caught before valid construction: A/B authorities could absorb
  one another, formatter issue was orthogonal, exact public contracts were
  missing, and the proposed history/build substrate was incomplete.
- Corrected Step 2a drafts are in progress; construction and submission status
  remain blocked until independent semantic review and managed-loop GO.

## 2026-07-19 - RUN-0027 - SJCC REV-3 EASY→MEDIUM harden

- Task: sparse-jacobian-color-contract (`d9082cd8`)
- Trigger: platform EASY after REV-2 gauge contracts; CM-008
- Actions: structural-coeff instruction contract; de-stick gauge; harden
  lane.c / knit.f90; denser k02 cluster family; task.toml medium
- Harbor: oracle 10x `2026-07-19__17-19-54` mean 1.0; post-10x NOP
  `2026-07-19__17-24-16` mean 0.0
- Package: sha256 `d0e134cc42f4af1b290500a6141f013fa9e349c2eb693460301cf0f118fd0b3a`; approve PASS
- Next: re-upload to Snorkel; platform re-measures difficulty

## 2026-07-19 - RUN-0026 - Idea portfolio expansion (18 new, archetype-unique)

- Scope: idea capture only; no task execution, no Step 2a claims
- Captured IDEA-0013…IDEA-0028, IDEA-0030 via `idea new`; first batch was
  template-cloned (metamorphic parity across N modules), caught in-session
- Corrective pass: assigned every idea a distinct structural archetype
  (graded object differs per idea: coherence, restatement, adversarial matrix,
  misleading docs, plan forensics, reproducibility, perf-under-bit-exactness,
  replay determinism, exactly-once accounting, recover-then-fix,
  crash-resume convergence, leakage audit, history archaeology,
  refactor-under-invariance, round-trip fidelity, parser differential,
  format archaeology, boot-graph diagnosis)
- Rejected IDEA-0029 procgen-seed-shear (duplicate of lockstep-replay-fray);
  minted IDEA-0031 save-lineage-exhume as archetype-distinct replacement
- Full dossiers written in `sudhir_ideas/records/` (fingerprint, five axes,
  > =3 discoveries, >=3 fix locations, v3 investigation profile, symptoms
  > sketch); collision audits are local-scan-only — full six-scope uniqueness
  > research remains TODO per idea before any Step 2a
- Registry summaries synced (`scripts/sync_idea_summaries_2026_07_19.py`);
  `idea validate` 0 errors / 24 uniqueness-pending warnings (expected);
  board rendered 31 ideas / 9 tasks
- Knowledge graph: PATTERN-ARCHETYPE-001, FAILURE-PORTFOLIO-001,
  EVIDENCE-PORTFOLIO-001
- Next: pick 1-2 candidates, run super-uniqueness dossiers, then Step 2a loops

## 2026-07-19 - RUN-0025 - SJCC REV-2 CM-006 contracts/coverage/rubric

- Task: sparse-jacobian-color-contract (`d9082cd8`)
- Actions: clarified gauge isolation / run order / ledger / scale-summary contracts;
  absolute span_info + ids + malformed test_k13; domain output-based rubric
- Harbor: oracle 10x `2026-07-19__16-04-34` mean 1.0; post-10x NOP
  `2026-07-19__16-09-08` mean 0.0
- Package: sha256 `1fb0d85bf896f02c08042a6c7c33a9006b46c1f206a8e13426ba6de84cf47e41`
- Next: re-upload zip to Snorkel and paste REV-2 form fields

## 2026-07-19 - RUN-0024 - RPSP REV-7 TRIVIAL→MEDIUM harden

- Task: robust-predicate-scale-parity (`fcee6e2e`)
- Trigger: platform Difficulty TRIVIAL (opus/gpt5 100%); CM-008 logged
- Actions: close always-refine escape (cancel raw==2 + well-conditioned exact raw);
  bury plate/frame greppable loci; keep inspect CLI + conservatism (CM-002);
  instruction notes well-conditioned certification
- Harbor: oracle 1x `2026-07-19__15-29-41` mean 1.0; oracle 10x `2026-07-19__15-31-05`
  mean 1.0; post-10x NOP `2026-07-19__15-35-48` mean 0.0
- Package: sha256 `60a22f1ef62971a2bc48cfddc8129433e6c81128b742430ab1d6634c725d1e66`
- Next: re-upload zip to Snorkel; platform will re-measure difficulty band

## 2026-07-19 - RUN-0023 - musl-sysroot-splice REV-2 packaged

- Task: musl-sysroot-splice
- Harbor: oracle 10x mean 1.0 (`jobs/2026-07-19__14-58-38`); post-10x NOP mean 0.0 (`jobs/2026-07-19__15-03-08`)
- Package: `sudhir_tasks_ready_to_submit/musl-sysroot-splice.zip` sha256 `5739b009e19f822817ceb48fa98f7142b9f41928a0b14d68016a02450ecc9ee6` (46 members); approve PASS (mechanical WARN only)
- Next action: re-upload zip to Snorkel `29a821f1` and paste REV-2 form fields

## 2026-07-19 - RUN-0022 - musl-sysroot-splice REV-2 (CM-006 verifier)

- Task: musl-sysroot-splice (submission `29a821f1`)
- Phase: Needs Revision → verifier repair (Step 2b green; Step 4 blocked)
- Goal: prove fully static musl built through knit/pack/seal, not `No INTERP` /
  helper-name string proxies
- Actions:
  - opened `sudhir_reviews/musl-sysroot-splice/REV-2/` with feedback + form pastes;
  - replaced weak entrypoint string checks with stubbed-helper execution,
    stage↔live helper equality, and staged musl identity (`libc.a` digest +
    `strings` musl + `-static` seal);
  - hardened `tests/test.sh` for CM-007;
  - symlinked `sudhir_tasks/active/musl-sysroot-splice` → `tasks/musl-sysroot-splice`
- Harbor: oracle 1x mean 1.0 (`jobs/2026-07-19__14-50-19`); NOP mean 0.0
  (`jobs/2026-07-19__14-50-58`); oracle 10x blocked by unkillable leftover
  containers / exhausted Docker address pools (needs privileged daemon restart)
- Next action: restart Docker, re-run oracle 10x `-n 1`, `evidence --oracle-10x`,
  then `package` and re-upload to Snorkel

## 2026-07-18 - RUN-0001 - Repository governance

- Task: repository-wide
- Phase: governance and planning
- Goal: encode the reusable lifecycle, namespace personal artifacts, and select the first task
- Actions:
  - audited the existing harness, task corpus, regression health, and toolchain;
  - researched mathematically deep task white space;
  - selected Robust Predicate Scale Parity;
  - created Sudhir-owned folders;
  - saved the lifecycle, master plan, status, ADRs, research index, idea index, templates, and knowledge graph;
  - added Cursor and agent skill adapters.
- Result: governance layer created; task construction remains blocked by the red harness baseline
- Evidence: `sudhir_plans/TERMINUS_DIAMOND_PLAN.md`, `sudhir_progress/STATUS.md`, `sudhir_decisions/`, and `sudhir_knowledge/`
- Decision: use one canonical task source under `sudhir_tasks/active/`
- Next action: Phase 2 Gold Harness Repair plan and baseline preservation

## 2026-07-18 - RUN-0002 - Gold Harness Repair

- Task: repository-wide
- Phase: baseline repair
- Goal: make Step 2a, regression tests, lint, packaging validation, and canonical Sudhir paths trustworthy
- Preservation:
  - hashed eight pre-existing untracked artifacts before editing;
  - found no recoverable copies of the missing historical fixture tasks;
  - did not delete or overwrite existing task sources or archives.
- Repairs:
  - anchored root ignore rules and made the schema plus nested fixtures trackable;
  - standardized all workflow references on `workflow.md`;
  - standardized Step 2b on oracle 1x + NOP and Step 4 on oracle 10x;
  - compressed always-on policy documents under tested context limits;
  - created a recoverable clean task fixture and focused detector fixtures;
  - replaced archive-directory parity with a SHA-256 submission index;
  - added canonical milestone archive validation;
  - added Python 3.12 project metadata, `uv.lock`, Ruff, and pytest configuration;
  - added configurable roots and a Zsh/Bash-compatible Sudhir environment script;
  - added Git text normalization and whitespace policy through `.gitattributes`;
  - cleaned the tracked harness to a green Ruff baseline.
- Certification:
  - Step 2a schema smoke: PASS;
  - `uv sync --frozen`: PASS;
  - Ruff: PASS;
  - pytest: 239 passed, 26 skipped;
  - canonical unittest: 264 tests, OK, 26 skipped;
  - submission index: current for 157 archives;
  - archive validation: 157/157 PASS;
  - canonical Sudhir task-path preflight: exit 0, temporary probe removed.
- Decisions: ADR-0003, ADR-0004, and ADR-0005
- Next action: TASK-RPSP-001 Step 2a validation

## 2026-07-18 - RUN-0003 - TASK-RPSP-001 Step 2a

- Task: TASK-RPSP-001 `robust-predicate-scale-parity`
- Phase: research, uniqueness, and idea validation
- Goal: obtain a mechanically defensible GO before constructing task source
- Research:
  - audited 157 submission archives and active tasks with no semantic collision;
  - reviewed Shewchuk robust predicates, CGAL exact-predicate guidance, GCC floating-point semantics, Rust FFI, and Fortran/C interoperability;
  - selected exact rational signs, affine-equivalent connectivity, handedness, adjacency, incidence, topology, and byte determinism as verifier surfaces.
- Design:
  - committed four hidden discoveries and three distributed candidate topologies;
  - selected four locations across C, Rust, and Fortran;
  - planned twelve opaque tests with each location controlling 4/12, below cap 0.34;
  - mechanically classified the 163-word public instruction as symptoms-only with zero causal-connective signals.
- Validation:
  - evidence schema: PASS;
  - attempt 1: 0 FAIL, 0 WARN;
  - topology and construction manifest persisted in normalized evidence;
  - strict v2 authoring-spec lint: PASS;
  - finalize: exit 0.
- Final certification:
  - the full suite first detected one changed untracked archive hash for `musl-sysroot-splice.zip`;
  - the changed archive independently passed structural validation;
  - refreshed only that archive's content record in the submission index;
  - submission index current for 157 archives, Ruff PASS, pytest 239 passed and 26 skipped, and `git diff --check` PASS.
- Corrections during the run:
  - retried `record` with its required task name and `--evidence` argument after an initial CLI usage error;
  - added the mandatory v2 triviality ledger, per-gate pitfall inventory, and initial-draft commitments after strict lint identified their absence.
- Decision: ADR-0006 accepts the selected topology and unblocks construction.
- Next action: Step 2b construction plan and complete initial task snapshot.

## 2026-07-18 - RUN-0004 - TASK-RPSP-001 Step 2b

- Task: TASK-RPSP-001 `robust-predicate-scale-parity`
- Phase: construction, preflight, oracle 1x, and NOP
- Goal: create the approved mixed-language task and complete the Step 2b gate chain without entering Step 3b or Step 4
- Starting state:
  - branch `main` at `3384fcb`;
  - 81 existing changed or untracked worktree entries;
  - canonical task root absent;
  - Docker, Harbor, and uv available.
- Rules loaded: lifecycle, approved spec, ADR-0006, task creation, Docker, difficulty, review, workflow, commands, taxonomy, templates, and reference task.
- Planned construction: one deterministic offline container, C + Rust + Fortran, four approved fix locations, twelve opaque exact/property tests, substantive oracle, and local construction manifest.
- Construction:
  - created 47 task files with 36 substantive environment files excluding Dockerfile/compose;
  - implemented the complete dyadic parser, exact native refinement, bounded tetrahedral enumeration, host lifecycle, Fortran row fold, deterministic report, twelve tests, and four-target oracle;
  - kept the 163-word public instruction unchanged and symptoms-only.
- Verification:
  - static PASS with no warning;
  - Dockerfile PASS;
  - collapse 0 FAIL, 0 WARN, 23 PASS;
  - packaging preview and 44-file checksum PASS;
  - local oracle 12/12 and untouched baseline 0/12;
  - each selected-location ablation fails exactly its declared four-test subset;
  - Harbor oracle 1x mean 1.0, zero errors;
  - Harbor NOP mean 0.0, zero errors.
- Harness improvements:
  - added Rust scoped-visibility and Fortran procedure extraction to the construction-manifest gate with regression coverage;
  - made registry revision invalidation remove stale final-only archives;
  - preserved new registry routing while returning `AGENTS.md` below its hard byte cap.
- Infrastructure note: the Snap Docker daemon denied Harbor compose teardown after completed trials; internal process-tree cleanup removed all stale task containers.
- Registry: revision 2, phase `review`; no final submission zip exists.
- Final repository certification: Ruff PASS, pytest 240 passed and 26 skipped, current task checksum, 157-archive index current, no stale task containers, and whitespace PASS.
- Evidence: `sudhir_reviews/robust-predicate-scale-parity/STEP2B.md`.
- Next action: Step 3b paper review; do not package or run oracle 10x yet.

## 2026-07-18 - RUN-0005 - Pipeline driver, status board, and Snorkel ingestion

- Task: repository-wide, plus a full end-to-end drive of TASK-RPSP-001
- Phase: tooling and integration test
- Goal: give every chat one systematic pipeline, make task create/revise easy,
  and surface Snorkel platform feedback automatically without re-prompting
- Actions:
  - added `sudhir_task.py` (stdlib) with new/status/board/phase/revise/gates/
    package/ingest/sync-snorkel/backfill subcommands;
  - established `sudhir_progress/registry.json` as the single source of truth and
    `sudhir_progress/BOARD.md` as its rendered view;
  - added a Snorkel export parser and `sudhir_snorkel/inbox/` -> `archive/`
    ingest flow that extracts difficulty, solvability, static outcome, upload
    time, and per-agent pass rates from platform blobs;
  - backfilled the registry from active tasks and the five root
    `submission_*.json` exports;
  - wired the pipeline contract into the always-on `sudhir-task-lifecycle`
    skill (both copies) and `AGENTS.md`;
  - registered `reproducible-reduction-parity` as a new idea through the driver
    and initialized its Step 2a loop to exercise create ergonomics;
  - accepted ADR-0007.
- Certification (real command output, not claims):
  - `ruff check sudhir_task.py`: PASS;
  - RPSP cheap gates via driver: static PASS, dockerfile PASS, collapse PASS,
    integrity PASS;
  - RPSP oracle 1x: mean 1.0 (job `2026-07-18__22-31-07`);
  - RPSP NOP: mean 0.0 (job `2026-07-18__22-35-19`);
  - RPSP oracle 10x (`-k 10 -n 2`): 10/10 reward 1.0, 0 exceptions
    (job `2026-07-18__22-50-52`);
  - RPSP packaged + approved via driver: `validate_submission_zip` PASS,
    `approve_task` mechanical gate PASS.
- Notes:
  - an early 10x at full concurrency threw 10 RuntimeErrors from Docker
    "all predefined address pools have been fully subnetted"; pruned networks
    and reran throttled to reach a clean 10/10;
  - no unattended Snorkel API exists; the network pull is a documented
    extension point in `cmd_sync_snorkel`;
  - a concurrent session edited the same registry/status files during this run;
    kept the shared registry and reconciled with its RUN-0004 record.
- Next action: Step 3b paper review for RPSP, then `phase submitted` after the
  platform upload; ingest the returned export to close the loop.

## 2026-07-18 - RUN-0006 - TASK-RPSP-001 Step 3b

- Task: TASK-RPSP-001 `robust-predicate-scale-parity`
- Phase: structural, honest-instruction, collapse, scientific, and per-test feasibility review
- Lifecycle correction:
  - registry showed Package/approve from RUN-0005 before Step 3b completed;
  - invalidated that package and removed its zip through revision 3;
  - marked RUN-0005's oracle 10x and approval stale after review edits.
- Confirmed findings:
  - exact host sentinel was unnecessarily pinned;
  - one lex-least-even cell representation was unnecessarily pinned;
  - verifier parsed binary symbols to police implementation;
  - all nine bundled batches were not directly protected from replacement;
  - architecture prose pointed at reusable host state.
- Revision 4 repairs:
  - accepted any distinct non-sign refinement state;
  - made cell, adjacency, and topology checks representation-agnostic while retaining positive exact orientation;
  - removed binary symbol-table inspection;
  - exercised all three bundled families and their actual nine variant names;
  - removed cause-adjacent state wording.
- Independent validation:
  - alternate always-refine C, alternate Rust sentinel, and lex-greatest-even Fortran implementation passed all twelve tests;
  - each selected location still fails exactly its declared four tests;
  - static, Dockerfile, collapse 23/23, packaging preview, and checksum PASS;
  - current Harbor oracle `2026-07-18__23-21-05`: mean 1.0, zero errors;
  - current Harbor NOP `2026-07-18__23-22-00`: mean 0.0, zero errors;
  - full repository regression: Ruff PASS, pytest 240 passed and 26 skipped.
- Review disposition:
  - unsupported request to copy repository policy `.mdc` files into the task was rejected;
  - no verifier-health or quality-check escalation was justified;
  - final verdict CLEAN, hard, no HIGH or MEDIUM task defect remains.
- Evidence: `sudhir_reviews/robust-predicate-scale-parity/STEP3B.md`.
- Registry: revision 4, phase `review`, final package absent.
- Next action: Step 4 oracle 10x, fresh NOP, package, archive parity inspection, and approval.

## 2026-07-18 - RUN-0007 - TASK-RPSP-001 Step 4

- Task: TASK-RPSP-001 `robust-predicate-scale-parity`
- Phase: oracle stress, fresh NOP, final package, parity, and approval
- Prerequisites: revision 4, Step 3b CLEAN, checksum current, cheap gates PASS, no package
- Docker preparation: pruned unused networks from 29 to 17 before full concurrency.
- Oracle 10x:
  - job `2026-07-18__23-30-19`;
  - full `-k 10 -n 10` concurrency;
  - 10/10 completed with reward 1.0;
  - mean 1.0, zero errors, zero retries, all pass-at-k values 1.0.
- Fresh NOP:
  - job `2026-07-18__23-31-33`;
  - mean 0.0, zero errors.
- Package:
  - `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`;
  - SHA-256 `17a0eb184ef35e43a0d6474da4ca7367a931de0e456b378534e1d9310bd6797d`;
  - 29,677 bytes, 42 members;
  - required dotfile present, forbidden and AI-scaffolding files absent.
- Approval:
  - checksum, static, collapse, zip validation, manifest, and source/zip parity PASS;
  - source/zip files 42/42, no missing, extra, or content mismatch;
  - machine decision PASS, approved true, zero warnings, zero blocking failures;
  - verifier-health explicitly skipped on the clean routine path; quality adjudication not required.
- Harness repair: pipeline subprocesses now propagate canonical task/spec/submission/review/job roots; added focused regression and emitted validation metrics to the canonical spec log.
- Infrastructure: Snap Docker compose teardown still denied cleanup after successful trials; all RPSP containers and unused networks were removed manually without task impact.
- Final repository certification: Ruff PASS, pytest 241 passed and 26 skipped, task checksum current, 157-archive index current, whitespace PASS.
- Evidence: `sudhir_reviews/robust-predicate-scale-parity/STEP4.md`.
- Decision: APPROVED and ready to upload; no task or archive edits permitted before upload.
- Next action: upload the zip, mark phase submitted, then ingest platform feedback.

## 2026-07-19 - RUN-0008 - musl-sysroot-splice platform-rejection triage and fix

- Trigger: Snorkel submission `29a821f1-da07-442d-986a-1e681631abdc`
  (musl-sysroot-splice) stuck in NEEDS_REVISION. Revision notes: "AutoEval
  execution failed. Build status: FAILED. Build ID:
  CodeExecutionEnvironment:f53a7114-9b90-46e2-b0e4-4b4734f7deff." Difficulty
  summary: "not tested with any agents as the Oracle solution failed."
- Evidence pulled with `stb submissions feedback/fetch-task`: fast static
  checks on the 21:33 IST upload SUCCEEDED (build 97e66d03, 6 warnings); the
  AutoEval difficulty build is what FAILED. The 20:56 IST difficulty artifact
  showed oracle 1.0 x3 and NOP 0.0 but 5/10 Terminus agent trials errored with
  AgentSetupTimeoutError after "asciinema installation verification failed".
- Root cause (reproduced locally in the built image): the Dockerfile ran
  `ln -sf /usr/local/bin/python3.13 /usr/bin/python3` AFTER apt installed
  asciinema. Debian's asciinema shebang is `#!/usr/bin/python3` and its module
  lives in python3.11 dist-packages, so the symlink made asciinema fail with
  ModuleNotFoundError at runtime. The Dockerfile's own `asciinema --version`
  checks ran BEFORE the symlink layer, so builds passed. Agent setup then tried
  `apt-get install asciinema` offline (allow_internet=false) and timed out.
- Fix: dropped both `ln -sf` lines (PATH already resolves python/python3 to
  /usr/local/bin 3.13) and added `asciinema --version` to the final pip RUN so
  a broken asciinema now fails the image build.
- Regate after fix: check-task.sh preflight PASS (known WARNs), oracle 1x 1.0
  (`jobs/2026-07-19__00-00-15`), NOP 0.0 (`jobs/2026-07-19__00-00-46`), oracle
  10x 10/10 (`jobs/2026-07-19__00-01-39`), zip rebuilt and validated,
  `approve_task.py` exit 0 with `--skip-verifier-health`.
- Registry: registered musl-sysroot-splice, phase package, next action
  re-upload via `stb submissions update 29a821f1-...`.
- Sweep: same symlink+asciinema pattern found in 5 other ready zips —
  ephemeris-maneuver-window-bind, grid-inertia-rocof-estimate,
  hetero-sketch-rank-reconcile, rf-handoff-hysteresis-band,
  split-brain-ownership-audit. They will hit the same AgentSetupTimeoutError
  and must be fixed before upload.

## 2026-07-19 - RUN-0009 - RPSP rev5 instruction grounding for fcee6e2e

- Trigger: submission `fcee6e2e-1c89-476f-aa10-5932a474ef97` uploaded as
  `robust-predicate-scale-parity.zip`. Platform: HARD, solvable=false.
  Agents 0/10. Oracle 3/3. Universal miss: `eval_band` conservatism via
  `--inspect-series` (r01/r02 0/10). Quality check fail
  `behavior_in_task_description`. Recommendation: document conservatism +
  inspect CLI in `instruction.md`.
- Fix: rewrite instruction (conservatism, GEOMLAB\_\*, --inspect-series,
  --inspect-status, schema/order/digest); rename `--inspect-state` →
  `--inspect-status` so CR1 does not collide with `map_state`.
- Mechanical: collapse 0 FAIL / 2 WARN (RC6, GX9 justified in
  `sudhir_reviews/robust-predicate-scale-parity/STEP3B-REV5.md`);
  `check-task.sh` PASS; zip validated at
  `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`.
- Blocked: Harbor oracle/NOP/10x cannot run — Docker address pools fully
  subnetted; snap-docker containers refuse kill without sudo.
- Next: user runs sudo docker cleanup, then finish oracle 1x/NOP/10x +
  approve_task and `stb submissions update fcee6e2e-…`.

## 2026-07-19 - RUN-0010 - RPSP rev5 Harbor gates complete

- Docker pools cleared after user restart; removed 58 exited containers and
  leftover harbor networks.
- Fresh evidence: oracle 1x 1.0 (`jobs/2026-07-19__02-08-51`), NOP 0.0
  (`jobs/2026-07-19__02-09-36`), oracle 10x 10/10
  (`jobs/2026-07-19__02-10-13`, `-k 10 -n 2`).
- `approve_task.py` PASS; zip SHA-256
  `7f3d02666e02dd9ac6a8ab1b461600d1889592f773f3e1a0f2ab1d95172d84ea`.
- Next: `stb submissions update fcee6e2e-1c89-476f-aa10-5932a474ef97
sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`.

## 2026-07-19 - RUN-0011 - Idea portfolio and super-uniqueness gate

- Trigger: the user required one clean idea list that always shows whether each
  concept is approved, executed, submitted, and accepted, while keeping future
  ideas structurally unique.
- Governance:
  - accepted ADR-0008;
  - upgraded the single registry to schema v2 with separate `ideas` and `tasks` maps;
  - made the idea index and task board generated views of that registry;
  - separated idea gate, uniqueness, execution, submission, and platform outcome;
  - made `evaluation-passed` explicitly weaker than final `accepted`.
- Novelty enforcement:
  - every new idea receives a permanent `IDEA-NNNN` ID and append-only history;
  - uniqueness PASS requires a domain/mechanism/topology/verifier fingerprint,
    all six collision-search scopes, evidence, closest analogue, and structural difference;
  - non-legacy phase advancement, gates, and packaging are blocked until uniqueness
    PASS plus Step 2a GO with evidence;
  - rejected slugs remain reserved and cannot be silently recycled.
- Workflow:
  - added `idea new`, `idea status`, `idea uniqueness`, `idea validation`,
    `idea list`, `idea backfill`, `idea validate`, and explicit `outcome` commands;
  - made platform ingest idempotent by submission/source hash and protected
    explicit outcomes from inferred export status;
  - added a process lock plus atomic registry replacement for concurrent sessions.
- Migration:
  - initialized 11 pre-existing concepts: RPSP approved with its real research and
    Step 2a evidence, reproducible reduction validating, three alternatives reserved,
    and six historical tasks marked legacy without fabricated uniqueness proof;
  - a concurrent session added Sparse Jacobian Color Contract as IDEA-0012; it is
    uniqueness-passed but still validating, demonstrating that execution remains blocked.
- Baseline repair: refreshed only the stale byte count and SHA-256 for the already
  rebuilt `musl-sysroot-splice.zip` regression-index entry; no archive was edited.
- Certification:
  - Ruff: PASS;
  - pytest: 247 passed, 26 skipped;
  - registry JSON parse: PASS;
  - idea registry: 0 errors, 10 intentional warnings (pending/reserved or honest legacy);
  - unchanged platform exports: 0 ingested, 5 unchanged on repeated runs;
  - construction-block probe: pending Reproducible Reduction Parity correctly refused;
  - `AGENTS.md`: 1499 bytes under the binding 1500-byte cap.
- Next action: every future concept starts with `idea new`; update the exact registry
  transition at each GO/STOP, execution, upload, revision, acceptance, or rejection.

## 2026-07-19 - RUN-0013 - SJCC idea uniqueness + Step 2a GO

- Task: `sparse-jacobian-color-contract` (TASK-SJCC-001)
- Registered via `sudhir_task.py new`; uniqueness PASS across idea-registry,
  active/archived tasks, 157 submission archives, upstream `tasks/`, and
  external CPR/Coleman–Moré sources.
- Step 2a attempt 1: `validate_loop.py record` → 0 FAIL / 0 WARN, ACTION GO;
  strict `finalize` PASS.
- Artifacts: research dossier, authoring spec, reviewer appendix, attempt-1
  evidence JSON, ADR-0009 freezing the four-location topology.
- Selected locations: `native/lane.c::mix_cols`, `host/vault.rs::bind_slot`,
  `host/gauge.rs::reset_span`, `analysis/knit.f90::merge_slots` (4/12 each).
- Next: Step 2b construction under `sudhir_tasks/active/sparse-jacobian-color-contract/`.

## 2026-07-19 - RUN-0014 - SJCC Step 2b cheap gates PASS

- Constructed `sudhir_tasks/active/sparse-jacobian-color-contract/` from ADR-0009
  and the approved authoring spec (C/Rust/Fortran, four seeded locations).
- Docker behavioral evidence (agent session, recorded in STEP2B.md): oracle
  12/12; NOP 10 failed / 2 passed.
- Fresh `sudhir_task.py gates`: static=PASS, dockerfile=PASS, collapse=PASS
  (0 FAIL / 0 WARN / 23 PASS), integrity=PASS (checksum verified).
- Next: Step 3b paper review, then Harbor oracle 1x + NOP.

## 2026-07-19 - RUN-0017 - SJCC Step 4 COMPLETE (10x + package APPROVED)

- Docker recovered; oracle 10x `-k 10 -n 1` → mean 1.0, 0 exceptions
  (`jobs/2026-07-19__03-05-27`). Fresh NOP mean 0.0
  (`jobs/2026-07-19__03-10-32`).
- First package FAIL: root-owned `tests/.pytest_cache` leaked into zip.
  Removed via alpine container mount; added `.pytest_cache` to
  `sudhir_task.py` `_ZIP_EXCLUDE_DIRS`.
- `sudhir_task.py package` → validate PASS, approve_task PASS.
  Zip: `sudhir_tasks_ready_to_submit/sparse-jacobian-color-contract.zip`
  SHA-256 `9c5b0e5e6658fc95cc4eb854eeffb8f3ff04afa60f2458b759e6e789c04c63f2`
  (43 members).
- STEP4.md APPROVED. Next: upload to Snorkel + phase submitted + ingest.

## 2026-07-19 - RUN-0016 - SJCC Step 4 oracle 10x BLOCKED (CM-003)

- Attempted `harbor run … -a oracle -k 10 -n 1` after cleanup script;
  stuck snap containers refused non-root `docker rm -f` (sudo password
  required in this environment).
- Job `jobs/2026-07-19__03-02-26`: 1/10 reward 1.0, 9 exceptions
  (AddTestsDirError ×1, RuntimeError ×8). Docker socket vanished mid-run.
- Did **not** package or approve. STEP4.md records BLOCKED + recovery cmds.
- Next: user `sudo snap restart docker` + kill stuck containers, then re-run
  10x / NOP / `sudhir_task.py package`.

## 2026-07-19 - RUN-0015 - SJCC Step 3b CLEAN + Harbor oracle/NOP

- Task: `sparse-jacobian-color-contract` revision 1
- Paper review found CM-002 gap (`--resume-check` / SENSLAB\_\* under-documented),
  CR1 risk (`span_info` vs `reset_span`), and `leaked` tell in `vault.rs`.
- Fixes: rename CLI to `--mode-echo`, document env overrides without backtick
  schema dumps, rename local `carry`, regenerate checksum.
- Cheap gates re-PASS; Docker oracle 12/12; Docker NOP 10 fail / 2 pass.
- Harbor: oracle 1x mean 1.0 (`jobs/2026-07-19__02-58-38`); NOP mean 0.0
  (`jobs/2026-07-19__02-59-20`); 0 exceptions each. Compose down hit snap
  permission denied (CM-003) after successful rewards.
- Review: `sudhir_reviews/sparse-jacobian-color-contract/STEP3B.md` CLEAN.
- Next: Step 4 oracle 10x (after docker pool/cleanup), then package/approve.

## 2026-07-19 - RUN-0011 - Common mistakes ledger (ADR-0010)

- Created `sudhir_knowledge/COMMON_MISTAKES.md` with CM-001…CM-005 covering
  asciinema/python3 symlink, instruction probe discoverability, Docker address
  pools, stale AutoEval banners, and CR1 CLI/symbol stem collisions.
- Accepted ADR-0010; wired ledger into lifecycle skill (`.cursor` + `.agents`),
  `AGENTS.md`, and `TASK_LIFECYCLE.md` Phase 7 / start-of-chat.
- Added `dockerfile_check.py` rule `python_interpreter_hygiene` (CM-001 FAIL on
  `/usr/bin/python3` repoint when asciinema is installed) plus unit tests.
- Knowledge graph: DECISION-0010, RULE-MISTAKES-001, FAILURE-CM-\* nodes/edges.

## 2026-07-19 - RUN-0021 - Task dossier and learning loop (ADR-0012)

- Accepted ADR-0012: per-revision dossier under `sudhir_reviews/<slug>/REV-<n>/`,
  registry `evidence` / `revisions` / `learning`, and capture commands.
- Added `sudhir_dossier.py` plus driver commands: `evidence`, `feedback-capture`,
  `form-capture` (DIFFICULTY/SOLUTION/VERIFICATION/RUBRIC), `rubric-capture`,
  `learn-check`; `revise` opens the workspace; `package` stores zip SHA-256 and
  requires PREUPLOAD (or `--force`); `ingest` writes PLATFORM.md + CM suggestions.
- Encoded CM-007 in `run_static_checks.py`; updated skeletons + SJCC/RPSP fixtures;
  CM-007 status → prevented.
- Added `sudhir_knowledge/WHAT_WORKED.md`; wired lifecycle skill + `AGENTS.md`.
- Backfilled RPSP REV-6 (feedback, form paste fields, rubric, evidence, PREUPLOAD)
  and musl/SJCC REV-1 feedback stubs.
- Regression: `repo_tests/test_sudhir_dossier.py` (revise, form-capture, CM-007).

## 2026-07-19 - RUN-0020 - RPSP revision 6 Step 4 package

- Harbor oracle 10x (`-k 10 -n 2`): `jobs/2026-07-19__13-29-21` mean 1.0,
  10/10, 0 errors.
- Fresh NOP: `jobs/2026-07-19__13-31-57` mean 0.0.
- `sudhir_task.py package robust-predicate-scale-parity`: validate PASS,
  approve_task PASS (collapse WARN only).
- Zip SHA-256 `002571487962e397b1123130703819916a52e67e53d5c0cb2302bb27d999c9a8`
  at `sudhir_tasks_ready_to_submit/robust-predicate-scale-parity.zip`
  (mirrored to `Task_Ready_To_Submit/`).
- Notes: `sudhir_reviews/robust-predicate-scale-parity/STEP4-REV6.md`.
- Next: re-upload to `fcee6e2e`; then musl / SJCC CM-006.

## 2026-07-19 - RUN-0019 - RPSP revision 6 (CM-007)

- Opened revision 6 for `robust-predicate-scale-parity`.
- Closed grading-integrity hole: `tests/test.sh` now
  `cd /tests && PYTHONSAFEPATH=1 python -m pytest … --confcutdir=/tests`.
- `task.toml`: difficulty medium; dropped `mcp_servers`.
- Dockerfile: `asciinema --version` final-layer check.
- Evidence: check-task PASS; Harbor oracle
  `jobs/2026-07-19__13-23-56` mean 1.0; NOP
  `jobs/2026-07-19__13-24-49` mean 0.0; Docker shadow probe PASS
  (vuln rc=0, fixed reward=0 under attack, oracle+attack reward=1).
- Notes: `sudhir_reviews/robust-predicate-scale-parity/STEP2B-REV6.md`.
- Next: Step 4 oracle 10x + package + re-upload `fcee6e2e`.

## 2026-07-19 - RUN-0018 - CM-006 / CM-007 verifier-contract cluster

- Trigger: platform Needs Revision feedback on three submissions
  (musl `29a821f1`, SJCC `d9082cd8`, RPSP `fcee6e2e`), pasted in chat.
- Pattern: task bodies largely solvable; graders failed to lock the claimed
  contract (weak proxies / under-coverage / off-domain rubric) or were
  bypassable (`python -m pytest` from agent-writable `/app`).
- Appended `CM-006` (weak proxy / coverage / rubric drift) and `CM-007`
  (pytest cwd/`sys.path` + `/conftest.py` shadow) to
  `sudhir_knowledge/COMMON_MISTAKES.md` with matching pre-upload checks.
- Knowledge graph: `FAILURE-CM-006`, `FAILURE-CM-007`,
  `EVIDENCE-PLATFORM-2026-07-19`, plus HIT / CONFIRMED_BY / DOCUMENTED_AS edges.
- No task source edits in this run; revisions still pending.

## 2026-07-19 - RUN-0017 - Active portfolio reconciliation and import quarantine

- Trigger: user corrected three live states and did not recognize five records
  shown as legacy ideas.
- Authoritative check: `stb submissions list -p
bfe79c33-8ab0-4061-9849-08d3207c9927` returned six current submissions:
  Musl Sysroot Splice was `REVIEW_PENDING` and Robust Predicate Scale Parity was
  `EVALUATION_PENDING`; SJCC remained local development and was not submitted.
- Origin finding: the five unknown records came from root-level May 2026
  `submission_*.json` exports automatically backfilled on 2026-07-18. Their JSON
  names the same project ID but older assignment IDs. Their submission IDs are
  absent from the current six-submission listing.
- Decision: accepted ADR-0011. Known old work may be `grandfathered`; stale or
  unrecognized imports move to a provenance-only quarantine and are excluded
  from active idea/task totals without deleting history.
- Corrected active states:
  - Musl Sysroot Splice: grandfathered, submitted, `IN REVIEW`;
  - Robust Predicate Scale Parity: approved, submitted, `IN EVALUATION`;
  - Sparse Jacobian Color Contract: approved, `IN DEVELOPMENT / PACKAGE`, not submitted.
- Quarantined: Cluster Green Tail Red, FFmpeg Filtergraph Regression Lab,
  Hazard Evac Flow Lab, Legacy PLC Wire Restore, and Maritime Lane Weather Weave.
  Each record retains source filename, project/assignment/submission IDs, upload
  timestamp, evidence, and quarantine reason.
- Hardened behavior: normal export ingestion refreshes provenance but cannot
  reactivate quarantine; linked task next actions drive the portfolio; pre-upload
  construction/gates/review/package all remain visibly in development; current
  review/evaluation stages suppress contradictory stale feedback summaries.
- Concurrent baseline repair: updated the compliant Dockerfile test fixture for
  CM-001 and removed one unused local introduced with that test.
- Certification: Ruff PASS; pytest 252 passed / 26 skipped; idea registry 0
  errors / 5 intentional active warnings; repeated ingest 0 changed / 5 unchanged;
  `AGENTS.md` 1428 bytes under its 1500-byte cap.
- Result: active portfolio contains seven recognized ideas; five historical
  imports remain visible only in the quarantine table.

## 2026-07-19 - RUN-0022 - Long-horizon investigation profile (ADR-0013)

- Goal: make future idea generation and task creation target coherent,
  production-like investigations without forcing all weakness dimensions into
  every task or grading solver process.
- Accepted ADR-0013 and added
  `sudhir_knowledge/LONG_HORIZON_TASK_PHILOSOPHY.md` plus the scoped rollout
  plan under `docs/exec-plans/`.
- Added an additive Step 2a `investigation_profile` schema and evidence-contract
  v3 marker for newly initialized loops. Existing state without the marker is
  grandfathered and remains recordable.
- New profile requires 2-4 weakness areas, 4-8 causal stages, 3+ distinct
  evidence surfaces, 2+ hypotheses with falsifiers, failing and healthy-control
  scenarios, deterministic reproduction, domain non-trivia, and a 20-100
  meaningful-action estimate. Action count is explicitly not a task reward.
- Updated Step 1 web prompts, workflow copy, Step 2a authoring/reviewer format,
  Step 2b preservation guidance, taxonomy routing, lifecycle, and strategic
  idea guidance. `debugging` and `software-engineering` remain blocked primary
  categories.
- First focused test run exposed CM-009: sourced canonical spec roots redirected
  temporary test state into `sudhir_ideas/specs/`. Removed the generated demo
  artifacts and made validate-loop tests rebind and restore module roots.
- Evidence: sourced-environment focused regression PASS, 46 tests in 0.69s
  (`test_validate_loop`, finalize, naming pass, lint spec, web bundle).
- Directly affected suite after driver/template coverage: 57 passed; Ruff PASS.
- Full certification after CM-009 isolation and reconciliation of the already
  present RPSP/musl compatibility archives with the generated submission index:
  Ruff PASS; 266 passed / 26 skipped.
- No active task source or submission archive changed; existing gate/package
  evidence remains valid.
- Next: use the v3 profile on the next new idea and collect pilot evidence
  before adding any runtime substrate or trajectory gate.

## 2026-07-19 - RUN-0027 - Envelope Rotation Shear construction

- Task: `envelope-rotation-shear`; phase: construction; goal: build the approved
  exhaustive authoring inventory under the canonical Sudhir task root.
- Baseline: the canonical task root and compatibility `tasks/` copy were absent;
  the registry records uniqueness PASS, Step 2a approval, and construction phase.
- Inputs: canonical Authoring Brief and construction manifest, CM-010 independent
  topology checks, CM-007 verifier hardening, and the current Docker discipline.
- Intended commands: focused local Go/Python tests, untouched-baseline NOP-style
  run, four exact single-location ablations, static checks, Dockerfile checks,
  collapse checks, and `scripts/check-task.sh`.
- Constraints: no Harbor, no package, no oracle 10x, no commit, and no repo-level
  checker edits. Next: construct the task, then record exact local evidence.

## 2026-07-21 — SJCC REV-7 CM-019 hedge

- Diagnosed empty difficulty as CM-019 (CodeExecution FAILED + BatchGetBuilds throttle), not non-canonical rust base.
- Raised build/verifier timeout to 1200s and memory to 8192; CM-016 test.sh early reward.
- Harbor oracle 1x/NOP/10x PASS; packaged zip sha256 `50ba0424…` for re-upload.
