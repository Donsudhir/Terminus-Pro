# STEP3B — REV-2 paper review — rowgroup-prune-mirage

- Date: 2026-07-19
- Decision: **ACCEPT WITH NOTES for Step 4**
- Scope: current REV-2 task tree after generated-input verifier hardening

## Evidence reviewed

- Strict Step 2a v2 spec: PASS; attempt 1 was 0 FAIL / 0 WARN.
- Six-scope uniqueness: PASS in `sudhir_research/TASK-RPM-001-RESEARCH.md`.
- Docker image build: PASS, image `sha256:c90efb35…`.
- Preflight: PASS; 47-file checksum written.
- Harbor oracle 1x: `jobs/2026-07-19__22-43-53`, mean 1.0, zero errors.
- Harbor NOP: `jobs/2026-07-19__22-44-37`, mean 0.0, zero errors.
- Local oracle: 12/12; untouched baseline: 0/12.
- Exact single-location ablations:
  - A: `p01,p03,p05,p07,p10` fail; 7 pass.
  - B: `p02,p03,p06,p08,p11` fail; 7 pass.
  - C: `p04,p05,p06,p09,p12` fail; 7 pass.

## Review change and invalidation discipline

The first verifier draft reconstructed the internal origin/presence authority in
a helper and reused only bundled fresh CSVs. That was mechanically valid but too
close to narrating the diagnosis and too weak against fixture-specific answers.
REV-2 now generates fresh CSV rows per test, checks producer markers against
verifier-owned logical outcomes, removes the explanatory helper, and directly
compares repeated audit bytes. The edit invalidated earlier gate/Harbor evidence;
preflight, oracle 1x, NOP, and all three ablations were rerun on the current tree.

## Instruction and honesty review

The instruction is 164 words in three direct paragraphs. It sounds like a real
finance/support incident, states the rebuild/audit/ingest surfaces and concise
report schema, and uses only absolute paths. It gives observable outcomes, not
null representation, persisted summaries, dictionaries, generation boundaries,
or repair sites. It has no task name, canary, roleplay, synthetic headings,
answer recital, value over-specification, or undefined metaphor jargon.

Every operational requirement has coverage:

- archived and fresh correctness: archive matrix plus generated fresh artifacts;
- equivalent execution modes: selective/full and row/batch cases;
- selective path preserved: healthy page-read controls;
- batch path preserved: healthy path selection and answer control;
- archive immutability: reset/hashed source behavior and no writer use on archives;
- repeated bytes: fresh artifact and full audit report comparisons;
- report schema: JSON parsing and every named case field;
- offline/rebuild: image and Harbor execution with baked dependencies.

## Environment and oracle review

The environment contains 41 meaningful non-Docker files, no padding, no build
artifacts, no golden output, no AI scaffolding, and no hidden walkthrough. The
historical format note is plausible stale operational documentation and is
experimentally falsifiable; it does not contain the public command contract or a
repair recipe. The C++/Rust split is failure-bearing: Rust alone produces new
artifacts, while C++ independently decides archive reads and evaluates batch
lanes.

The oracle performs 83 lines of real comment-stripped edit distance and 142
non-boilerplate transitive LOC across three declared functions. It adds semantic
logic, has no runtime downloads, random state, clocks, retries, or hardware
thresholds, and solves every public requirement. Scenario values enter through
typed artifact state rather than fix-path literals.

## Collapse audit

Stage: post-oracle

Smallest plausible successful patch:
A coordinated producer correction, conservative generation-aware selective
admission, and validity-first batch evaluation across one Rust and two C++
modules. Any equivalent shared-normalization design still has to cross those
three typed boundaries because archives are immutable and fresh producer output
is independently graded.

Likely editable frontier:

- `rust/src/ember/fold.rs`
- `cpp/src/harbor/veil.cpp`
- `cpp/src/lattice/rill.cpp`

Requirement-to-file map is many-to-many: generated correctness exercises Rust
plus either C++ read path; archived selective correctness exercises decoder,
planner, and row/batch execution; fast-path preservation exercises planner,
execution, and work counters; repeated bytes depend on healthy report code plus
all semantic inputs.

Oracle line count: 142 non-boilerplate LOC; GX3 real edit distance 83.

Discoverability:
The instruction, opaque test names, and fix-path symbols do not identify the
validity migration. Runtime disagreement first separates by plan, then artifact
inspection distinguishes producer metadata from consumer interpretation. A
reader sees several plausible modules and three realistic competing hypotheses.
The row implementation provides a healthy behavioral reference, not a list of
other repair sites.

Red flags: none unresolved.

Residual hardness:
The solver must prove payload integrity, separate producer metadata from reader
interpretation, preserve immutable archives, coordinate Rust and C++, and retain
two optimized paths. Generic null/index/vector recipes and broad fallbacks do
not clear the generated and healthy-control matrix.

Collapse verdict: **WARN, accepted with one justification**.

### RC2 WARN disposition

RC2 reports `rust/src/ember/fold.rs` as predictable only because the visible
language directory token `rust` overlaps the implementation language. The
semantic diagnostic is empty, two of three oracle targets are unpredictable,
and neither `ember`, `fold`, nor `tilt_a` overlaps an instruction or test noun.
Knowing that one component is written in Rust does not identify this file among
nine Rust source files or disclose its role. This is a language-directory false
positive, not a discoverability shortcut.

All other 22 collapse checks PASS, including CR1/2/7/8/9 and GX1–GX10.

## Per-test feasibility

| Test | Checks | Valid approaches | Chain dependency | Exact values | Risk |
| --- | --- | --- | --- | --- | --- |
| p01 | generated producer markers | 2+ artifact implementations | none | uniquely derived from generated rows | LOW |
| p02 | archived selective row answer and work avoidance | conservative admission or correct local decoding | none | unique aggregate | LOW |
| p03 | producer markers plus archive admission | 2+ coordinated designs | A+B by design in one test | unique outcomes | MEDIUM |
| p04 | archived batch absence count | mask-first or normalized-lane batch | none | unique count | LOW |
| p05 | generated producer plus batch behavior | 2+ coordinated designs | A+C by design in one test | unique outcomes | MEDIUM |
| p06 | selective-batch interaction | 2+ coordinated designs | B+C by design in one test | unique aggregate | MEDIUM |
| p07 | generated sparse selective case | 2+ producer representations | none | unique zero result/work count | LOW |
| p08 | archive + healthy selective controls | correct admission or safe normalized descriptors | none | unique aggregates/counter relation | LOW |
| p09 | batch negative range | 2+ lane-filter implementations | none | unique aggregate | LOW |
| p10 | generated markers and repeated bytes | any deterministic valid writer | none | unique artifact semantics; bytes compared to itself | LOW |
| p11 | neighboring-generation selective behavior | conservative or generation-aware planner | none | unique aggregates | LOW |
| p12 | full archived batch plus healthy path | 2+ batch implementations | none | unique aggregates/path property | LOW |

The three paired tests intentionally prove location coupling but create their own
fresh preconditions and do not depend on other test order or state. Every test
runs its own subprocess inputs under `tmp_path`; the session fixture only rebuilds
the current source. No test uses time, network, random values, polling, or shared
mutable expected state. `verifier_health.py` is therefore not escalated; the exact
manual behavioral ablations provide stronger task-specific evidence.

## Multiple valid approaches

Two valid families remain acceptable:

1. Keep artifact generations distinct, produce faithful fresh markers, admit
   incomplete historical markers conservatively, and apply effective validity in
   the batch kernel.
2. Normalize every decoded slab into a generation-neutral descriptor, have the
   producer emit the same descriptor semantics, and make planner/batch consumers
   use that shared descriptor.

Tests grade aggregates, artifact marker properties, work counters, and repeated
bytes, not the oracle's helper names or source shape. Both approaches can pass.

## CM/WW review

- CM-006: core outcomes are behavioral; no string/source proxy controls reward.
- CM-007: `cd /tests`, `PYTHONSAFEPATH=1`, and `--confcutdir=/tests` present.
- CM-008: no Python-primary core, no always-fallback escape, and loci are opaque.
- CM-010: typed-boundary absorption and stage-skipping attacks recorded and
  dynamically backed by exact ablations.
- CM-011 / WW-008: Rust and C++ are necessary agent-facing languages; pytest is
  verifier-only.
- WW-001/002/004/005/006 apply to ablations, outcome tests, verifier hardening,
  and final form capture.

## Decision

**ACCEPT WITH NOTES for Step 4.** The only warning is the justified RC2 language-
directory overlap. No HIGH or MEDIUM task defect remains. Step 4 still requires
oracle 10x, a fresh post-stress NOP, complete form capture, package validation,
source parity, and `approve_task.py` exit 0.
