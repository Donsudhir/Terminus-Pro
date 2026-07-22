# Idea Inspiration Source Ladder

Use this source ladder every time a new Terminus task proposal is generated.
Sources provide **inspiration and evidence**, never a license to copy an issue,
benchmark instance, test suite, patch, or proprietary text. Every candidate
still needs current eligibility, six-scope uniqueness, and Step 2a validation.

## Tier 1 — outstanding, closest to real tasks

### 1. GitHub issues

Prefer real issue reports labeled or described as:

- bug, regression, performance
- CLI, Docker, configuration
- help wanted, good first issue
- refactor only when the underlying behavior is non-trivial

Useful ecosystems include Kubernetes, Docker, uv, Ruff, Homebrew, Neovim,
Redis, PostgreSQL, Click, and other mature systems. FastAPI, Pandas, and
Python-centric issues are inspiration-only under the current no-Python-primary
house policy and category blocks.

A source issue should contribute a realistic symptom, environment shape, and
failure mechanism. Do not copy its patch or tests. Convert it into a distinct,
offline, deterministic, single-container scenario with a different distributed
fix topology and verifier surface.

### 2. SWE-bench

Use SWE-bench to learn realistic issue/repository/test shapes: parsing edges,
API behavior, serialization, filesystem semantics, CLI behavior, and config
precedence. Do not reuse benchmark instances, issue prose, patches, or tests.
Most instances naturally look like `software-engineering` or `debugging`, which
are blocked for net-new work; route only genuinely different ideas whose real
core belongs to an allowed category.

### 3. Terminal-Bench papers and task analyses

Use papers to understand why agents fail: wrong source of truth, destructive
step repetition, long-horizon coherence loss, wrong artifact location/format,
and shallow verification. Learn benchmark-design principles rather than copying
tasks.

## Tier 2 — excellent sources

### 4. Advent of Code

Use parsing, state-machine, simulation, and file-handling motifs only as raw
inspiration. Reject direct puzzle solving and blank-canvas implementations.
A viable proposal embeds the motif in an existing realistic system and requires
coupled diagnosis rather than implementing a fully stated algorithm.

### 5. Unix programming challenges

High-value surfaces include grep, sort, uniq, diff, find, xargs, sed, and awk.
Prefer compatibility, encoding, process, filesystem, or pipeline interactions
that span multiple authorities. Reject one-regex or one-flag repairs.

### 6. Real DevOps incidents

Use Docker, Git, Linux, Nginx, systemd, Make, and deployment/build failures.
Prefer restore/replay, dependency graph, namespace, permission, and artifact
provenance problems. Net-new multi-container work remains blocked locally.

## Tier 3 — hidden gold mines

### 7. Bug trackers

Mozilla, Rust, Node.js, OpenSSL, SQLite, and similar trackers contain realistic
failure reports. Capture URL, retrieval date, symptom, and the structural change
that makes the proposal unique.

### 8. Release notes

Bug-fix bullets such as symlink handling, encoding, recursive deletion, and
parser corrections are useful seeds. A release-note sentence alone is never a
complete task: recover the real failure context from authoritative sources.

### 9. Stack Overflow

Use questions as weak signals for recurring failure modes in Bash, Docker,
sed/awk, permissions, encoding, and CLI tooling. Verify the behavior against
official documentation or deterministic local reproduction before using it.
Do not copy question/answer text.

### 10. Reddit and community discussions

Relevant communities include programming, DevOps, Docker, Linux, Neovim, and
language-specific forums. Treat posts as leads only. Verify every important
technical claim through official docs, upstream issues, or reproducible tests.

## Tier 4 — books for systems thinking

- *The Unix Programming Environment* — pipelines, files, shell, parsing,
  automation.
- *The Linux Programming Interface* — signals, permissions, symlinks, file
  descriptors, pipes, processes.
- *Advanced Programming in the UNIX Environment* — IPC, sockets, locking,
  process semantics.
- *Software Engineering at Google* — maintenance, testing, configuration,
  tooling.
- *Designing Data-Intensive Applications* — consistency, replication, logs,
  serialization. Net-new `data-processing` is currently blocked, so use these
  mechanisms only when the actual core maps honestly to an allowed category.

Do not reproduce book exercises or substantial copyrighted text. Use concepts
and cite the source.

## Tier 5 — recurring model weakness surfaces

Prefer these when they produce a coherent hard task rather than a checklist:

- Bash, find, sed, awk, xargs
- Git history and recovery operations
- Dockerfiles and multi-stage builds
- Make, CMake, Bazel, Gradle
- YAML/TOML and configuration precedence
- permissions, symbolic links, file descriptors, CRLF/LF, UTF-8/BOM
- environment variables and layered configuration
- deterministic database migration/recovery mechanics
- regular-expression edge cases inside a larger system
- CI/CD artifact provenance and build graph drift
- large-repository navigation with multiple plausible authorities

## Source-to-proposal conversion rules

1. **Current policy first.** Reject blocked category, milestone, UI, and
   multi-container starts before investing in proposal text.
2. **Existing system, not blank canvas.** The task starts from a realistic
   repository/environment with meaningful existing behavior.
3. **Symptoms, not solution.** The proposal summary describes the incident and
   expected observable outcome without naming fix files, algorithms, or patch
   steps.
4. **At least three discoveries and three coordinated locations.** One issue
   does not justify a task if it collapses to one obvious edit.
5. **Distinct from the source.** Change more than names/languages/fixtures:
   require a different causal topology, evidence path, and invariant surface.
6. **Hidden tests are independently authored.** Never copy upstream or
   benchmark tests; verify observable behavior and allow alternative valid
   implementations.
7. **Record provenance.** Save URL, source type, retrieval date, claim,
   confidence, and proposal implication.
8. **Social sources are leads.** GitHub discussions, Stack Overflow, and Reddit
   never outrank official docs or reproducible behavior.
9. **No quota copying.** The suggested 35/20/15/etc. distribution is inspiration
   mix, not an acceptance target. Current category blocks and portfolio balance
   take precedence.

## Proposal-first output contract

For the single candidate selected to enter the lifecycle, output only these
paste-ready fields first:

1. **Task Idea Summary** — 2–5 clear sentences.
2. **Idea Category** — one exact platform display label.
3. **Associated Skills** — 5–10 concise skills.
4. **Task Tags** — 3–6 descriptive tags.

Then stop. The user runs **Check feedback** in the platform form. Uniqueness,
Step 2a, task files, oracle design, and packaging begin only after the proposal
check is captured as passed.
