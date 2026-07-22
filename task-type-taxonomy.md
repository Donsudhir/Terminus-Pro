# Task Type Taxonomy (Category)

Each task must be labeled with a category from this taxonomy. The category describes the primary theme, topic, or activity in the task.

In addition, there exists another axis of categorization called **subtypes**, or **subcategories** (in `task.toml`). Refer to [task-creation.mdc](../.cursor/rules/task-creation.mdc) (subcategories section) for more information.

## Before creating a task (mandatory)

**Do not start Step 2a validation or Step 2b file creation until you have read this file for the chosen category.**

1. **Pick the category** using the table in [Choosing a Category](#choosing-a-category) below. If two categories fit, choose the one that describes the **primary activity** the agent must perform.
2. **Read that category's section** — definition, examples, and **Authoring guidance** (where present). Blocked categories (`data-processing`, `software-engineering`, `debugging`) must not be used for net-new tasks.
3. **Apply category guardrails during ideation** — reject or redesign ideas that match the category's "Reject / avoid" patterns before drafting `specs/<task-name>.md` or any file under `tasks/`.
4. **Set `task.toml` `[metadata].category`** to the exact kebab-case slug from this file (e.g. `security`, not `Security`).

## Investigation profile is not a category

New ideas follow `sudhir_knowledge/LONG_HORIZON_TASK_PHILOSOPHY.md`, but its
weakness areas are a separate authoring axis. A task may require long-horizon
debugging, log triage, SQL investigation, Git reasoning, or recovery from a
wrong hypothesis while its primary category remains `system-administration`,
`security`, `scientific-computing`,
`build-and-dependency-management`, or another allowed value. Choose the label
from the actual intellectual core. The profile does not unblock `debugging` or
`software-engineering` or `data-processing`, and it must not be used to disguise a generic repair
task.

## Categories

### system-administration

Tasks involving OS-level configuration, user management, package management, processes, or installing, configuring, and bringing up services, networks, and environments.

**Examples:**

- Configure a systemd service
- Set up user permissions
- Install and configure Nginx

**Authoring guidance:** Prefer live state reconciliation, namespace/mount/cgroup/device-node drift, restore/replay under concurrent load, destructive admin phases, and misleading status tools that only check surface health. Avoid policy-knob transcription and single-config fixes.

### build-and-dependency-management

Compile code, manage dependencies, build components.

**Examples:**

- Fix a broken build configuration
- Resolve dependency conflicts
- Set up a multi-stage Docker build

**Authoring guidance:** Prefer coupled build-graph failures across toolchains, feature flags, and transitive deps. Avoid "flip one CMake variable" or single-manifest repair without broader system coupling.

### data-processing

> **Currently blocked** — not accepting net-new submissions since 2026-07-10. Evidence-backed tasks already in review or the revision queue may continue; do not reuse that exemption for a new idea.

Tasks that transform, parse, filter, aggregate datasets or files and directories and generate derived output.

**Examples:**

- Parse and transform CSV data
- Aggregate log files
- Filter and sort JSON datasets

**Authoring guidance:** Prefer multi-stage pipelines with interacting invariants and ambiguous intermediate state. Avoid pure spec-implementation ETL where every field computation is stated in the instruction.

### games

Tasks centered on game-like or simulated environments, interactive puzzles, or simulation games that run in the terminal.

**Examples:**

- Complete a VimGolf challenge
- Solve a terminal-based puzzle
- Navigate a text adventure

**Authoring guidance:** Prefer puzzles requiring exploration and state reasoning, not scripted walkthroughs. Avoid hidden-instance "find the one broken file" difficulty.

### software-engineering

> **Currently blocked** — not accepting new submissions. The `software-engineering` category is paused. Do not submit new tasks under this category until this note is removed.

Tasks focused on developing or testing features and algorithms, fixing bugs and improving/optimizing an existing feature, implementing tests, or maintaining software projects.

**Examples:**

- Implement a caching algorithm
- Fix a race condition
- Optimize database queries

### machine-learning

Tasks requiring training, fine-tuning, running inference, or evaluating machine learning models, including dependency setup, running training loops, and managing data pipelines for ML tasks.

**Examples:**

- Fine-tune a model on custom data
- Debug a training pipeline
- Optimize inference performance

**Authoring guidance:** Prefer checkpoint/resume, data-pipeline coupling, and evaluation invariants that break under subtle config drift. Avoid blank-canvas "implement this training loop from the spec" tasks.

### debugging

> **Currently blocked** — not accepting new submissions. The `debugging` category is paused. Do not submit new tasks under this category until this note is removed.

Tasks that require identifying, diagnosing, and fixing errors in scripts, codebases, or system configurations.

**Examples:**

- Find and fix a memory leak
- Debug a failing test suite
- Diagnose a production crash

### security

Tasks related to cryptography, authentication, permissions, penetration-style tests, exploit, validate vulnerabilities, reverse engineering or security configuration.

**Examples:**

- Find a SQL injection vulnerability
- Configure secure TLS settings
- Reverse engineer a binary

**Authoring guidance (read before creating a security task):**

**Prefer ideas built around:**

- Authority splits and capability confusion (multiple policy/decoding/trust sources that disagree)
- Revocation, freshness, or lineage drift across restore, reload, or replay
- Split decode / split policy authorities (no single knob fixes every scenario)
- Binary or protocol predicates recovered from behavior, not from named standards in the instruction
- Verifier-bypass bait where a local checker validates the wrong invariant

**Reject / avoid (these collapse to easy despite security flavor):**

- Toy jail or hardening checklist — editable surface is one config plus a few shell scripts and the prompt is an orthogonal security bullet list
- Pre-factored safe-extractor recipe — helper names mirror prompt nouns (`validate`, `extract`, `canon`, `install`)
- Security aura without residual reasoning — real daemons, exploit framing, or crypto nouns do not substitute for coupled diagnosis
- Orthogonal checklist completion — each requirement independent with no tradeoffs; count insight clusters, not bullet count
- Policy-knob transcription — instruction names exact files and knobs to set
- In-distribution crypto recipes — HMAC verification, standard TLS hardening steps, textbook safe-parsing patterns

**Construction notes:**

- Instruction must stay symptoms-only (RC6). When the protocol surface is rich, extra RC6 discipline is required — do not name algorithms, schemas, or fix locations.
- Run idea-validation checks 12–14 (grep-collapse, pre-factored-helper, security-aura discount) explicitly for security ideas.
- Tests must verify domain-correct security outcomes across multiple scenarios, not checklist completion on one path.

### scientific-computing

Tasks using scientific libraries or workflows, such as numerical computation, simulations, or domain-specific research code.

**Examples:**

- Implement a numerical solver
- Debug a simulation
- Optimize a scientific computation

**Authoring guidance:** Prefer checkpoint/resume semantics, conflicting numerical-policy authorities, reduction ordering / FP non-associativity, and plausible-but-wrong outputs where stability alone misleads. Avoid formula-recitation spec tasks.

## Distribution Guidelines

To ensure benchmark diversity:

- No single type should exceed ~30% of total tasks
- At least four types should each represent ≥10%

## Choosing a Category

Pick the category that best describes the primary activity:

| Primary activity          | Category                                   |
| ------------------------- | ------------------------------------------ |
| OS/server configuration   | `system-administration`                    |
| Build systems, packages   | `build-and-dependency-management`          |
| ETL, file processing      | `data-processing` (currently blocked)      |
| Interactive challenges    | `games`                                    |
| Code development, testing | `software-engineering` (currently blocked) |
| ML model work             | `machine-learning`                         |
| Finding/fixing bugs       | `debugging` (currently blocked)            |
| Security issues           | `security`                                 |
| Scientific code           | `scientific-computing`                     |
