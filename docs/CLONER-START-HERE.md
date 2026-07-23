# Clone and Adapt Terminus-Pro Safely

**Use this guide when cloning Sudhir's enhanced TERMINUS repository to create your own task-generation and lifecycle framework with less setup work.**

This is the companion to `docs/TERMINUS-FRAMEWORK-BUILD-GUIDE.md`. That document explains how the framework is designed. This document explains how to clone the existing implementation without corrupting Sudhir's portfolio, claiming someone else's work, or creating ideas and tasks that collide with existing ones.

**Critical rule:** cloning the repository gives you framework code **and** an existing body of ideas, tasks, reviews, evidence, submissions, and failure history. It is a live workbench, not a blank starter template.

---

## 1. What cloning gives you

A clone includes two different assets:

1. **Reusable framework:** lifecycle driver, root adapter, validation loops, task skeletons, static/Docker/collapse checks, approval, revision dossiers, policy modules, tests, and documentation.
2. **Sudhir's portfolio/history:** idea slugs, proposal results, uniqueness records, active and archived tasks, platform exports, review dossiers, current ZIPs, lessons, and decisions.

The first asset is intended to reduce setup effort. The second is provenance and collision evidence. It must not be silently adopted as the new maintainer's work.

### Never assume

- that an existing idea is unowned because it is unfinished;
- that a rejected or retired idea is free to reuse;
- that a quarantined idea may be renamed and submitted;
- that changing language, domain nouns, fixtures, or file names creates novelty;
- that a platform evaluation result means final acceptance;
- that deleting the registry removes the underlying conflict;
- that a public repository or task archive may be redistributed without checking its license.

---

## 2. Choose a clone mode before running lifecycle mutations

There are three safe operating modes. Pick exactly one before creating an idea.

| Mode | Use when | Existing registry and tasks | New work |
| --- | --- | --- | --- |
| **A. Contributor clone** | You are helping Sudhir in the same portfolio | Preserve exactly; pull before every mutation | Add only coordinated work under the existing lifecycle |
| **B. Independent fork with collision memory** | You want your own framework and portfolio | Preserve Sudhir's records as read-only collision/provenance corpus | Use a new remote, new branch policy, new slugs, and explicit ownership |
| **C. Framework-only distribution** | You are preparing a clean reusable template | Remove operational/task data only after creating a durable upstream collision snapshot | Start an empty active registry while still searching the snapshot during conflict checks |

### Commands that must wait until mode selection

Do not run these merely because the clone completed:

```text
sudhir_task.py backfill
sudhir_task.py new
sudhir_task.py idea new
sudhir_task.py revise
sudhir_task.py package
sudhir_task.py outcome
```

First establish ownership, baseline state, and collision sources.

---

## 3. Clone and pin the source

The current local remote is:

```text
git@github.com:Donsudhir/Terminus-Pro.git
```

Use the URL for which the owner has granted access. Do not assume anonymous HTTPS access works if the repository is private.

```bash
git clone git@github.com:Donsudhir/Terminus-Pro.git
cd Terminus-Pro
git rev-parse HEAD
git remote -v
git status --short
```

Record the source commit before changing anything:

```bash
mkdir -p origin_reference
git rev-parse HEAD > origin_reference/TERMINUS_PRO_SOURCE_COMMIT.txt
git remote -v > origin_reference/TERMINUS_PRO_SOURCE_REMOTES.txt
cp sudhir_progress/registry.json origin_reference/TERMINUS_PRO_REGISTRY_SNAPSHOT.json
cp sudhir_ideas/FOREIGN_WORK_DO_NOT_REUSE.md origin_reference/ 2>/dev/null || true
```

For an independent fork, preserve Sudhir's repository as `upstream` and use a different `origin`:

```bash
git remote rename origin upstream
git remote add origin <your-new-repository-url>
git checkout -b fork/bootstrap-<owner-or-team>
```

The snapshot is a collision source, not an active registry. Do not edit it after creation. Commit its source SHA and hash if the fork's license and privacy policy allow retaining it.

---

## 4. Reproduce the environment

The framework uses a locked Python 3.12 environment.

```bash
uv sync --frozen
.venv/bin/python -m repo_tests
.venv/bin/ruff check .
```

Do not install harness dependencies into Conda base or global Python.

Confirm external tools separately:

```bash
harbor --version
docker version
docker compose version
git --version
```

Read `AGENT SETUP MANIFEST.txt` for the versions verified by the repository owner. Different versions are not automatically wrong, but they must be recorded before comparing results.

### Establish the clone baseline

```bash
.venv/bin/python sudhir_task.py board
.venv/bin/python sudhir_task.py ingest
.venv/bin/python sudhir_task.py idea validate
.venv/bin/python scripts/build_submission_index.py --check
.venv/bin/python scripts/build_submission_index.py --historical --check
```

Classify failures as:

- framework defect;
- missing local dependency;
- unavailable Docker/Harbor infrastructure;
- stale generated state;
- expected portfolio warning;
- owner-specific data unavailable in this clone.

Never begin by "fixing" a task because a clone-wide test failed. First prove whether the failure is pre-existing.

---

## 5. Read these files before creating anything

Use this order:

1. `AGENTS.md` — always-on routing and non-negotiables;
2. `docs/ARCHITECTURE.md` — one-page code map;
3. `docs/TERMINUS-FRAMEWORK-BUILD-GUIDE.md` — framework architecture and rollout;
4. `sudhir_knowledge/TASK_LIFECYCLE.md` — lifecycle contract;
5. `commands.md` — exact commands;
6. `REPO_CONVENTIONS.md` — intentional local conventions;
7. `sudhir_progress/BOARD.md` and `sudhir_progress/STATUS.md` — current generated state;
8. `sudhir_ideas/IDEA_INDEX.md` — active, rejected, retired, and quarantined ideas;
9. `sudhir_ideas/FOREIGN_WORK_DO_NOT_REUSE.md`, if present, or the generated
  quarantine section in IDEA_INDEX — non-owner work that still blocks
  near-duplicates;
10. `sudhir_knowledge/COMMON_MISTAKES.md` and `WHAT_WORKED.md` — learned prevention patterns;
11. `sudhir_decisions/INDEX.md` — why the framework behaves this way.

Generated status files are read-only views. Never edit BOARD, STATUS, or IDEA_INDEX by hand.

---

## 6. Mode A: contributor clone

Use this mode only when contributing to the same Sudhir portfolio.

### Rules

1. Do not reset or rename the registry.
2. Do not remove existing tasks, records, dossiers, or ZIPs.
3. Pull and regenerate the board before selecting work.
4. Obtain an assigned slug or explicit approval before starting a candidate.
5. Use a branch named for the task or framework change.
6. Do not run two mutating lifecycle commands from separate machines at the same time.
7. Commit registry, generated views, and evidence changes together when they belong to one transition.
8. Never rewrite another revision dossier.

### Distributed concurrency warning

The registry uses a local file lock. It prevents two processes in one checkout from overwriting each other. It does **not** prevent two contributors on different machines from creating conflicting registry commits.

For a shared portfolio, use one of these controls:

- one coordinator performs lifecycle mutations;
- serialize idea/task assignments through pull requests;
- reserve slugs before research;
- require a fresh pull and board regeneration before every registry mutation;
- migrate the registry to a transactional shared service if concurrent authors become common.

A merge conflict in `registry.json` must be resolved semantically. Never choose "ours" or "theirs" for the whole file.

---

## 7. Mode B: independent fork with collision memory

This is the recommended low-effort mode for someone building their own framework from this repository.

### Keep the framework functioning first

Do not immediately rename every `sudhir_*` path. The code, documentation, tests, and generated views use those names consistently. A broad rename before the baseline passes creates unnecessary risk.

Use two stages:

1. **Functional fork:** keep internal path names, create your own remote, policies, and new idea/task slugs.
2. **Namespace migration:** after tests pass, use `sudhir_config.toml` and the root adapter to move canonical roots; then rename user-facing terms through a tested migration.

### Preserve Sudhir's records as collision evidence

The safest initial fork keeps the original records unchanged and treats them as upstream provenance. Your new idea must be structurally different from:

- Sudhir's active ideas and tasks;
- rejected and retired ideas;
- quarantined foreign work;
- active and historical task trees;
- current and historical submission archives;
- external sources.

Do not call an original record yours. Add a fork-level ownership convention, such as a new ADR and a `fork_owner`/`origin` metadata extension, before multiple owners share one registry.

### Avoid slug collisions

A slug is permanently reserved if it exists in any source registry or collision snapshot. Do not append a user name, language, `v2`, `new`, or `redux` to disguise a collision.

Examples of non-novel changes:

```text
resolver-closure-drift -> rust-resolver-closure-drift
mesh-checkpoint-operator-skew -> mesh-checkpoint-operator-skew-v2
domain-halo-digest-rift -> mpi-boundary-hash-drift
```

The name changed; the mechanism/topology/verifier may not have.

---

## 8. Mode C: framework-only distribution

Use this only when making a clean template for other people.

### The critical invariant

An empty active registry must not mean an empty collision corpus.

Before removing operational data, preserve a read-only upstream collision snapshot containing at least:

- source repository and commit;
- idea IDs and slugs;
- titles and summaries;
- categories and languages;
- status, including rejected/retired/quarantined;
- novelty fingerprints;
- closest analogues and differentiators where available;
- task slugs and submission/archive names;
- known do-not-reuse warnings.

Do not include secrets, signed URLs, private feedback, hidden solutions, or restricted task content in a public snapshot.

### Keep, replace, or remove

| Path/type | Framework-only action | Reason |
| --- | --- | --- |
| Root harness Python files | Keep | Framework implementation |
| `.cursor/`, `.agents/skills/` | Keep, then rename owner-specific text carefully | Agent workflow |
| `skeleton/` | Keep | Task scaffolding |
| `repo_tests/` synthetic fixtures | Keep | Regression safety |
| `specs/validation_schema.json` and schema docs | Keep | Step 2a contract |
| `web/` | Keep | Idea-generation inputs |
| Generic framework docs and policies | Keep | Operating contract |
| `sudhir_tasks/active/*` | Remove from the clean active template | Owner task source |
| `sudhir_tasks/archived/*` | Replace with fingerprints/manifests if redistribution is restricted | Owner task source |
| `sudhir_tasks_ready_to_submit/*.zip` | Remove | Current owner submissions |
| `Task_Ready_To_Submit/*.zip` | Remove unless license and distribution are explicit | Historical answer-bearing archives |
| Task-specific idea records/proposals/specs | Move to read-only collision snapshot or remove after safe fingerprint export | Conflict memory without active ownership |
| Task-specific reviews and platform exports | Remove or retain privately | May contain private feedback/evidence |
| Root `submission_*.json` | Remove | Platform data |
| Harbor `jobs/` and agent recordings | Remove | Generated and potentially sensitive |
| Generated BOARD/STATUS/IDEA_INDEX | Regenerate from the new registry | Derived views |
| Common mistakes and what worked | Keep with provenance | High-value framework knowledge |
| Repository-wide ADRs | Keep as origin architecture history, or archive and start a fork ADR index | Decision rationale |
| Task-specific ADRs/research/plans | Archive or summarize | Owner-specific evidence |

### One-time registry initialization

This is a fork migration, not an ordinary lifecycle edit. Perform it only in a fresh independent branch after saving the upstream collision snapshot.

Initialize:

```json
{
  "schema_version": 3,
  "ideas": {},
  "tasks": {}
}
```

Then regenerate views and the empty current submission index:

```bash
.venv/bin/python sudhir_task.py board
.venv/bin/python scripts/build_submission_index.py
.venv/bin/python sudhir_task.py idea validate
```

The formal uniqueness checklist for the clean fork must explicitly search the upstream collision snapshot. If the tooling does not yet read that snapshot, keep the original registry intact until the reader exists. Do not trade a clean board for forgotten collisions.

---

## 9. The pre-proposal conflict screen

This is the most important addition for a cloner.

The platform proposal check is early, but it must not be fed an obviously conflicting idea. Before writing the four proposal fields, run a **lightweight local conflict screen**. This is not the formal six-scope uniqueness dossier and must never be recorded as uniqueness PASS.

Use `sudhir_templates/PREPROPOSAL_CONFLICT_SCREEN_TEMPLATE.md`.

### 9.1 Screen every candidate, not only the favorite

For each candidate, inspect:

- exact and near slug/title matches;
- the same source issue, paper example, patch, benchmark instance, or incident;
- domain/system;
- failure mechanism;
- distributed fix topology;
- verifier/invariant surface;
- agent-facing language/runtime shape;
- causal investigation shape;
- existing active, rejected, retired, legacy, and quarantined records.

### 9.2 Four-part structural fingerprint

Use these four primary axes:

| Axis | Question |
| --- | --- |
| **Domain** | What real system or technical domain is being repaired? |
| **Mechanism** | What actually causes the observable failure? |
| **Topology** | Which independent components/authorities must coordinate? |
| **Verification** | What computed behavior or invariant proves the repair? |

Language and fixture changes are secondary. They do not rescue a collision on mechanism, topology, and verification.

### 9.3 Collision decision rules

| Finding | Decision before proposal |
| --- | --- |
| Same slug or clearly equivalent title | **DROP**; slug remains reserved |
| Same source issue/patch/tests/benchmark instance | **DROP**, unless only an abstract pattern inspired a demonstrably different task and nothing was copied |
| Same mechanism + topology + verification | **DROP**, even if domain or languages differ |
| Same topology + verification with cosmetic mechanism changes | **REWORK or DROP** |
| Three of four fingerprint axes substantially match | Presume conflict; proceed only with a precise structural distinction reviewed by a human |
| Two axes match | Name the nearest analogue and test whether the causal discovery path and graded object are genuinely different |
| Only domain or language matches | Not automatically a conflict; continue screening |
| Candidate differs only by scale, names, fixtures, file format, or language | **DROP** |
| Cannot explain the difference without adjectives such as “more complex,” “advanced,” or “harder” | **DROP or REWORK** |
| Nearest analogue is rejected/retired/quarantined | Still a collision source; status does not free the idea |
| Structural distinction is clear and source reuse boundary is honest | May proceed to the four proposal fields |

### 9.4 Required structural-difference sentence

Before proposal, complete this sentence with concrete mechanics:

```text
Unlike <nearest analogue>, which grades <old verifier object> through
<old topology/mechanism>, this candidate requires <new causal discoveries>
across <new independent authorities> and is verified by <new invariant>.
```

If the sentence remains true after replacing the technical phrases with generic words such as “pipeline,” “state,” or “consistency,” it is probably too vague.

### 9.5 Veto questions

Stop the candidate if any answer is yes:

1. Could the old oracle be adapted mostly by renaming paths and symbols?
2. Could the old tests be reused with fixture substitutions?
3. Is the new domain merely a wrapper around the old graded invariant?
4. Does the same single function or configuration key control success?
5. Is the source issue or patch effectively the answer?
6. Is the candidate only harder because the repository is bigger?
7. Would the new task teach the same agent failure mode with the same repair path?
8. Is ownership or source provenance uncertain?

### 9.6 What the screen may and may not claim

The screen may conclude:

- `PROCEED TO PROPOSAL`;
- `REWORK BEFORE PROPOSAL`;
- `DROP AS COLLISION`;
- `HOLD: OWNERSHIP/SOURCE UNCLEAR`.

It may not conclude:

- uniqueness PASS;
- Step 2a GO;
- hard;
- solvable;
- eligible for submission;
- accepted.

Formal uniqueness happens only after the platform proposal check passes.

---

## 10. Search order for the pre-proposal screen

Use the cheapest and most local evidence first.

### 10.1 Generated portfolio

```bash
.venv/bin/python sudhir_task.py idea list --all
.venv/bin/python sudhir_task.py idea list --all --json > /tmp/all-ideas.json
```

Read BOARD, IDEA_INDEX, and the foreign-work warning.

### 10.2 Idea and research text

Search:

```text
sudhir_ideas/records/
sudhir_ideas/proposals/
sudhir_research/
origin_reference/TERMINUS_PRO_REGISTRY_SNAPSHOT.json
```

Use mechanism and invariant terms, not only candidate names.

### 10.3 Task sources and archives

Search current and historical task manifests/instructions. Do not extract or copy solutions for inspiration.

The advisory similarity tool can compare a drafted task instruction, but it is not sufficient for pre-proposal uniqueness because lexical dissimilarity can hide structural duplication.

### 10.4 External source check

At the screen stage, look only for obvious ownership/copy/collision problems. Do not perform or record the full six-scope uniqueness dossier yet.

After proposal PASS, research external issues, papers, upstream tasks, and other corpora formally with dated evidence.

---

## 11. Proposal sequence after the screen

Only a candidate marked `PROCEED TO PROPOSAL` may enter the formal lifecycle.

### Step 1: produce only the four fields

- Task Idea Summary: 2–5 sentences;
- Idea Category: exact platform label;
- Associated Skills: 5–10;
- Task Tags: 3–6.

Do not include the conflict analysis in the platform fields. The summary should describe the realistic system, observable failure, and desired outcome without revealing the solution.

### Step 2: stop for platform check

The maintainer pastes the fields into Task Idea Proposal and runs Check feedback.

### Step 3: capture the result

After feedback, create/capture the idea and proposal through the lifecycle CLI. Preserve:

- exact fields;
- evidence;
- feedback;
- inspiration source;
- no-copy reuse boundary;
- pre-proposal screen reference.

### Step 4: formal uniqueness

Only proposal `passed` proceeds to the complete six-scope uniqueness dossier:

```text
idea-registry
active-tasks
archived-tasks
submission-archives
upstream-corpus
external-research
```

The upstream collision snapshot from the clone is part of `upstream-corpus` and must be named in evidence.

### Step 5: eligibility and Step 2a

A proposal pass does not override blocked categories, house policy, the long-horizon profile, or Step 2a. Run current eligibility and complete Step 2a before construction.

---

## 12. Conflict examples

### Example A: language-only rewrite

Existing idea:

```text
Rust+C halo exchange after repartition produces a global digest mismatch.
```

Candidate:

```text
Fortran+C++ ghost-cell exchange after remeshing produces a global checksum mismatch.
```

Likely decision: **DROP**. Domain, mechanism, topology, and verifier are substantially the same. Language and nouns changed.

### Example B: same domain, different graded object

Existing idea:

```text
Mesh checkpoint metadata and operator order drift across restart; verifier checks restart-equivalent scientific output.
```

Candidate:

```text
Mesh partition ownership leaks stale security labels after delegated access revocation; verifier checks authorization closure across live and recovered state.
```

Possible decision: **CONTINUE SCREENING**. Domain overlaps, but mechanism, authority topology, and verifier object may differ. The distinction still needs evidence.

### Example C: rejected idea

Existing idea was rejected for weak difficulty. A cloner proposes the same mechanism with more files and deeper nesting.

Decision: **DROP or fundamentally redesign**. Rejection does not release the fingerprint, and file volume is not novelty.

### Example D: same source, different abstract pattern

A public incident describes a stale generation counter. Existing work uses it in envelope-key rotation. A candidate uses only the abstract lesson—competing version authorities—in an unrelated deterministic compiler cache and develops different topology, tests, and fixtures without copying issue text or patches.

Decision: **possible**, but the reuse boundary and structural difference must be explicit. Formal uniqueness still decides.

---

## 13. Ownership rules for an independent fork

Add a fork ADR before accepting new records. It should define:

- owner/team name;
- source Terminus-Pro commit;
- which original records are upstream collision evidence;
- canonical writable roots;
- active registry ownership;
- slug reservation policy;
- whether collaborators may create records directly;
- how external contributions are quarantined;
- licensing and redistribution boundaries.

Recommended metadata extension:

```json
{
  "origin": {
    "repository": "<your fork URL>",
    "owner": "<owner/team>",
    "created_from": "Donsudhir/Terminus-Pro@<sha>",
    "upstream_record": null
  }
}
```

Add this through a versioned registry migration and tests. Do not hand-add different shapes to individual records.

---

## 14. Namespace migration

Do not mass-replace `sudhir` strings on day one.

### Safe order

1. get the clone test baseline green;
2. accept an ADR for the new namespace;
3. change canonical paths in configuration;
4. update the root adapter and tests;
5. migrate one writer at a time;
6. keep historical paths read-only;
7. regenerate views;
8. run path-guidance scans;
9. only then rename lifecycle skills and user-facing documentation;
10. preserve an explicit rollback mapping for one release.

### What not to do

- do not copy directories to new names and keep both mutable;
- do not search-and-replace inside task evidence or historical hashes;
- do not rename accepted ZIPs;
- do not rewrite accepted ADR history;
- do not rename slugs to imply ownership;
- do not change generated files without changing their generator.

---

## 15. First new idea in a clone

Use this complete sequence.

### Before proposal

1. board and ingest;
2. read all active/quarantined idea sources;
3. fill the pre-proposal conflict screen;
4. identify the nearest analogue;
5. write the structural-difference sentence;
6. choose `PROCEED`, `REWORK`, `DROP`, or `HOLD`;
7. verify basic category/structure eligibility.

### Proposal

8. produce the four fields only;
9. stop for platform feedback;
10. capture PASS/FAIL and provenance.

### After proposal PASS

11. create the permanent idea record;
12. complete six-scope uniqueness, including the original clone snapshot;
13. record uniqueness PASS only with evidence;
14. run Step 2a and the long-horizon profile;
15. register the task only after GO;
16. construct under the canonical active task root;
17. run preflight, oracle 1x, and NOP;
18. paper review;
19. rerun preflight after any edit;
20. oracle 10x and transactional package;
21. capture forms and upload;
22. ingest feedback;
23. infer no acceptance.

---

## 16. First revision in a clone

A revision is not a new idea.

1. ingest the current platform export;
2. inspect evaluator-specific status instead of relying on one banner;
3. run `revise` to open a numbered dossier;
4. record feedback verbatim or faithfully;
5. classify the finding against common mistakes;
6. apply the smallest correct fix;
7. rerun every invalidated gate;
8. capture fresh oracle/NOP/10x evidence;
9. recapture DSV/rubric fields when stale;
10. package and update the existing submission.

Do not create a new slug to escape feedback or difficulty history.

---

## 17. Branch and review policy

Recommended branches:

```text
framework/<short-change>
idea/<slug>-research
task/<slug>
revision/<slug>-rev-<n>
policy/<snapshot-or-rule>
```

A pull request that mutates lifecycle state should include:

- registry diff;
- generated view diff;
- evidence paths;
- source task/spec changes if any;
- gate output summary;
- reason for the transition;
- next action;
- explicit statement that no unrelated idea/task status changed.

For conflict-sensitive idea work, require a reviewer to confirm the nearest analogue and structural-difference sentence before proposal fields are used.

---

## 18. What reduces effort safely

Cloning this repository saves work because the following already exist:

- locked Python harness environment;
- root adapter and environment overrides;
- idea/task registry;
- generated board and status views;
- proposal field validator;
- six-scope uniqueness gate;
- policy eligibility and exemptions;
- Step 2a evidence schema and loop;
- long-horizon investigation profile;
- task layout classifier;
- standard task skeleton;
- static, Docker, collapse, integrity, and ZIP checks;
- Harbor oracle/NOP workflow;
- revision dossiers and form capture;
- transactional current ZIP index;
- platform export ingestion;
- common-mistakes and successful-pattern ledgers;
- broad regression tests.

Effort should be spent on:

- choosing a genuinely distinct idea;
- researching its domain;
- designing the causal topology and verifier;
- building a realistic task;
- responding to evidence.

Effort should **not** be spent re-creating status spreadsheets, package scripts, ad hoc checklists, or duplicate root trees.

---

## 19. What must remain manual

Do not automate away these judgments:

- whether two ideas are structurally the same;
- whether source reuse crosses into copying;
- whether the task is fair;
- whether one location can absorb the others;
- whether a verifier accepts multiple valid implementations;
- whether a task is difficult for legitimate reasons;
- whether platform feedback reflects infrastructure or task content;
- whether an external contribution's ownership is clear;
- whether a policy change should become blocking;
- whether an evaluation result is final acceptance.

Automation can collect evidence and block missing fields. It cannot manufacture novelty or ownership.

---

## 20. Clone readiness checklist

### Identity and provenance

- [ ] Source repository and commit recorded.
- [ ] Clone mode selected.
- [ ] License and redistribution boundaries reviewed.
- [ ] Original registry/collision snapshot preserved.
- [ ] New remote and owner/team policy recorded for an independent fork.

### Baseline

- [ ] `uv sync --frozen` completed.
- [ ] Repository regression suite recorded.
- [ ] Ruff result recorded.
- [ ] Docker/Harbor availability recorded.
- [ ] Board, ingest, registry validation, and indexes checked.
- [ ] Pre-existing failures separated from fork changes.

### Conflict safety

- [ ] Active, rejected, retired, legacy, and quarantined ideas remain searchable.
- [ ] Original task/submission fingerprints remain available as a collision corpus.
- [ ] Every selected candidate gets a pre-proposal conflict screen.
- [ ] Nearest analogue and structural difference are reviewed.
- [ ] Formal uniqueness still runs after proposal PASS.
- [ ] No slug is reused.

### Operational safety

- [ ] Generated views are never hand-edited.
- [ ] Historical roots remain read-only.
- [ ] Registry mutations are serialized across collaborators.
- [ ] Task edits invalidate evidence.
- [ ] Current and historical ZIP indexes stay separate.
- [ ] Acceptance requires explicit evidence.

---

## 21. Fifteen-minute contributor start

For a contributor joining Sudhir's existing portfolio:

```bash
git clone git@github.com:Donsudhir/Terminus-Pro.git
cd Terminus-Pro
uv sync --frozen
.venv/bin/python -m repo_tests
.venv/bin/python sudhir_task.py board
.venv/bin/python sudhir_task.py ingest
.venv/bin/python sudhir_task.py idea validate
```

Then:

1. read BOARD and STATUS;
2. read foreign-work and common-mistakes files;
3. obtain an assigned task/framework change;
4. create a branch;
5. do not generate an unreviewed proposal.

---

## 22. Thirty-minute independent-fork start

```bash
git clone git@github.com:Donsudhir/Terminus-Pro.git
cd Terminus-Pro
git remote rename origin upstream
git remote add origin <your-new-repository-url>
git checkout -b fork/bootstrap-<owner>
uv sync --frozen
.venv/bin/python -m repo_tests
.venv/bin/ruff check .
mkdir -p origin_reference
git rev-parse HEAD > origin_reference/TERMINUS_PRO_SOURCE_COMMIT.txt
cp sudhir_progress/registry.json origin_reference/TERMINUS_PRO_REGISTRY_SNAPSHOT.json
.venv/bin/python sudhir_task.py board
.venv/bin/python sudhir_task.py idea validate
```

Then:

1. accept a fork ownership/source-of-truth ADR;
2. decide whether to keep the original registry visible or build a clean registry plus collision-snapshot reader;
3. do not delete original conflict memory;
4. keep internal namespaces until the baseline remains green;
5. screen the first candidate before proposal.

---

## 23. Troubleshooting

### The board shows Sudhir's tasks in my independent fork

Expected if the original registry is still active. Do not delete it merely for appearance. First preserve a collision snapshot and define the fork's registry migration.

### I want an empty registry immediately

An empty active registry is safe only if original ideas/tasks remain a required upstream collision source. Implement or document that reader before resetting.

### My candidate has a different language but resembles an existing task

Treat it as a conflict until mechanism, topology, and verifier are proven different. Language is not a primary novelty axis.

### The same idea was rejected earlier

It remains reserved. Redesign the structural fingerprint or select another candidate.

### Another contributor added a similar idea on another branch

Stop both proposals. Compare timestamps, sources, fingerprints, and ownership. Merge the history into one reserved record or choose one candidate. Do not race to the platform.

### `registry.json` has a Git conflict

Do not take one side wholesale. Reconcile each idea/task transition, preserve both history arrays and evidence, validate links, regenerate views, and run `idea validate`.

### A generated view conflicts but the registry does not

Resolve the registry first, discard generated-view conflict content, and regenerate all views through `board`.

### The clone cannot access Terminus-Pro over HTTPS

Use the repository URL and authentication method granted by the owner. The local reference remote uses SSH. Do not publish credentials or tokens in setup docs.

### The regression suite passes but the candidate still looks duplicated

Correct. Mechanical tests cannot prove creative uniqueness. Stop and perform the structural comparison.

---

## 24. Final rule

The clone is successful when it reduces mechanical setup while preserving provenance and forcing better reasoning.

It is unsuccessful if it makes task generation faster by forgetting old ideas, copying task shapes, resetting collision history, or treating renamed work as novel.

Before any proposal, the maintainer must be able to answer clearly:

1. Who owns this candidate and its source material?
2. What is the nearest existing analogue?
3. Which mechanism, topology, and verifier are genuinely different?
4. Why can the old oracle/tests not be reused by renaming?
5. Where will the formal uniqueness evidence be recorded after proposal PASS?

If any answer is unclear, do not produce the proposal yet.
