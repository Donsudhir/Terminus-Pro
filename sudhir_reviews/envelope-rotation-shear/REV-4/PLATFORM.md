# Platform snapshot (sanitized)

Captured: 2026-07-21T01:16:45Z

## Scalars
- difficulty: MEDIUM
- solvable: True
- status_line: ✅ Solvable (all tests passed by at least one agent run)
- static_outcome: PASS
- submission_id: 7037bf76-ae73-4e31-aeef-dde57417cbc4
- zip_filename: envelope-rotation-shear.zip
- uploaded_at: 2026-07-19T18:35:04.911Z
- source_file: submission_7037bf76.json

## Agent performance
- terminus-claude-opus-4-8: 60.0%
- terminus-gpt5-5: 60.0%

## text_summary

```
Difficulty: ✅ MEDIUM

Status: ✅ Solvable (all tests passed by at least one agent run)

Agent Performance:
  • terminus-claude-opus-4-8: 60.0% (3/5 runs)
  • terminus-gpt5-5: 60.0% (3/5 runs)

Reference Agents:
  • nop: 0.0% (0/1 runs)
  • oracle: 100.0% (3/3 runs)

Failure Breakdown:
  • nop: 1 other
  • terminus-claude-opus-4-8: 2 other
  • terminus-gpt5-5: 2 other

Unit Tests Results:
  • test_e01: 9 passed / 10 runs
  • test_e02: 8 passed / 10 runs
  • test_e03: 10 passed / 10 runs
  • test_e04: 10 passed / 10 runs
  • test_e05: 10 passed / 10 runs
  • test_e06: 8 passed / 10 runs
  • test_e07: 10 passed / 10 runs
  • test_e08: 9 passed / 10 runs
  • test_e09: 9 passed / 10 runs
  • test_e10: 8 passed / 10 runs
  • test_e11: 10 passed / 10 runs
  • test_e12: 8 passed / 10 runs

Analysis on Agent Failures:
  • Task Instruction Sufficiency: ❌ FAIL, ## Job Summary

### 1. Overall Results
**0/4 trials passed** (reward = 0.0 across all trials). No agent achieved a passing score, though partial progress was significant — agents passed between 8–11 of 12 tests individually.

| Trial | Tests Passed | Key Failure |
|---|---|---|
| tbench-task__trZEzzJ | 10/12 | Maintenance re-encrypts stable entries (byte-for-byte idempotency) |
| tbench-task__kMqyVSv | 8/12 | `Maintain` used `AuthorityAxis()` instead of plain axis for new namespaces |
| tbench-task__yK6zPea | 11/12 | Added fallback scope instead of fixing root cause; made broken record readable, so recovery returned empty |
| tbench-task__s8KaTV9 | 8/12 | Removed the fallback in `openSet`, breaking plain-axis frame reads for new namespaces |

---

### 2. Common Failure Patterns

**The axis/scope consistency problem is the dominant failure mode across all 4 trials.** The codebase has a tension between:
- `cachedAxis` / `RouteAxis` (hash-based axis for unknown/new namespaces)
- `model.AxisFor` (plain service name as axis, used by the test harness)

Three of four agents stumbled on this (`kMqyVSv`, `yK6zPea`, `s8KaTV9`). Agents either:
- Used `AuthorityAxis()` in `Maintain` when the test harness expected plain axis (`kMqyVSv`)
- Added a fallback that made a fixture record readable that should have required recovery (`yK6zPea`)
- Removed the fallback that was the only way plain-axis new-namespace frames could be read (`s8KaTV9`)

The **maintenance byte-for-byte idempotency** requirement tripped one agent (`trZEzzJ`): the skip condition `entry.Frame.Axis == model.RouteAxis(axis)` was subtly wrong, causing stable entries to be re-encrypted and changing their sequence/epoch markers.

---

### 3. Hack Check
**No cheating detected.** All four trials passed the `reward_hacking` check. Agents:
- Never accessed the `solution/` directory
- Never modified test files or reward files
- Worked exclusively through legitimate source code exploration and patching
- One agent (`s8KaTV9`) even cleaned up its temporary helper commands before submitting

---

### 4. Debug: Systematic Instruction Issues

One trial's `task_specification` check **failed** (`s8KaTV9`), identifying a genuine spec gap: the instructions state that `get` must read live records for newly introduced namespaces, but **do not specify which axis convention is used when the test harness creates those frames** (`model.AxisFor` plain name vs. `RouteAxis` hash). This left agents unable to resolve the conflict without guessing.

The other three trials passed their `task_specification` checks — their failures are attributed to agent implementation choices, not missing spec. However, the recurring axis confusion across all 4 trials suggests the specification's silence on this convention is a systemic issue, not isolated to `s8KaTV9`. The spec gap arguably affected all trials.

---

### 5. Progress: How Close Did Agents Get?

Agents got quite far — all correctly identified the three core bugs (scope mismatch in `openSet`, cross-namespace recovery candidate selection, maintenance idempotency) and fixed the majority of cases. The failures were narrow and late-stage:

- `trZEzzJ`: 83% (10/12) — one subtle off-by-one in the skip condition
- `yK6zPea`: 92% (11/12) — correct diagnosis, wrong fix strategy (additive patch vs. root cause removal)
- `kMqyVSv`: 67% (8/12) — correct fix concept, wrong axis function call in `Maintain`
- `s8KaTV9`: 67% (8/12) — correct isolation fix, but inadvertently removed necessary compatibility

Average: **~77% of tests passing**, with failures concentrated in the axis convention edge case.

---

### 6. Key Differences Between Agents

All agents appear to use the same or similar model (no model metadata provided), and all followed the same systematic pattern: explore → identify root causes → patch → rebuild → validate manually. The divergence was in **fix strategy at the `openSet` scope resolution**:

- `yK6zPea` went additive (added fallback scopes) → broke fixture assumption
- `s8KaTV9` went reductive (removed fallbacks) → broke new-namespace compatibility  
- `kMqyVSv` got the openSet fix right but chose the wrong axis source in `Maintain`
- `trZEzzJ` got the most tests passing but had a subtle condition error in the idempotency guard

The binary (all-or-nothing) reward function is particularly punishing here — agents averaging 77% test passage score 0.0. Fixing the axis convention spec gap in the instructions and/or switching to partial credit scoring would likely yield significantly better measured outcomes.
```

## test_review

```
================================================================================
                         REVIEW REPORT: tbench-task
================================================================================

Status:        ⚠️ WARNING
Task Location: /root/harbor_tasks/tbench-task

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------

This task presents a Go-based encrypted key-value store ("vaultctl") with four
deliberately broken internal functions (conductor/arc.go, tenant/spine.go,
aperture/sill.go, ledger/reel.go). The agent must diagnose authentication
failures and cross-namespace leakage introduced by a faulty maintenance run,
then fix the broken functions so that recovery, get, maintain, and audit
commands work correctly with strict namespace isolation. The solution replaces
each broken function with a properly validated implementation. The test suite
contains 12 scenario-based tests exercising recovery, maintenance idempotency,
generated namespaces, tampering rejection, and substitution detection.

================================================================================
                              WARNINGS ⚠️
================================================================================

--------------------------------------------------------------------------------
1. Non-Canonical Base Image for a Go Task
--------------------------------------------------------------------------------

File:    tbench-task/environment/Dockerfile (line 2)
Problem: The Dockerfile uses the Python 3.13 slim base image for what is
         primarily a Go task. While Python is needed for the test verifier,
         the canonical base image for Go tasks should be used, with Python
         installed on top if needed. Using a Python base and apt-installing
         golang-go pulls an older distro-packaged Go (1.19-era) rather than
         the canonical Go image.

Current code:
┌─────────────────────────────────────────────────────────────────────────────┐
│  FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:...   │
│  ...                                                                        │
│  RUN apt-get update \                                                       │
│      && apt-get install -y --no-install-recommends \                         │
│          ...                                                                │
│          golang-go \                                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Suggested fix: Use the canonical Go base image (if one exists on the approved
list) and install Python + pytest into it, or document why the Python base is
required. Alternatively, verify with the canonical base image list whether this
configuration is acceptable given the task needs both Go (for building/running
the codebase) and Python (for the pytest verifier).

Explanation: The canonical base image policy exists to curb fragmentation.
A Go task that apt-installs golang-go from Debian repos gets an older,
uncontrolled Go version rather than the official Go toolchain. The go.mod
declares `go 1.19` which is compatible, but future maintenance may diverge.

--------------------------------------------------------------------------------
2. Instruction Brevity and Implicit Requirements
--------------------------------------------------------------------------------

File:    tbench-task/instruction.md (lines 1-3)
Problem: The instructions are dense and domain-specific but omit explicit
         success criteria for certain tested behaviors. Tests check: (a) newly
         generated namespaces can be read without recovery (test_e02, test_e06),
         (b) maintenance idempotency (test_e05, test_e12), (c) audit refusing
         substituted records (test_e07, test_e11), and (d) recovery report
         schema. While (b), (c), and (d) are stated, (a) — that `get` must
         work for freshly added live records without invoking recovery — is
         only implied by "read values with vaultctl get". The instruction does
         not explicitly state that the store must handle identities not
         pre-seeded in the cache.

Current approach: The instruction mentions "read valid live records for newly
introduced service namespaces without invoking recovery" but does not call out
that the tenant scope derivation must work generically for any namespace, not
just pre-cached ones.

Suggested fix: Add a sentence clarifying that the scope/axis derivation must
work for arbitrary new service namespaces, not only those present in the
initial fixture data.

Explanation: The broken `tenant/spine.go` uses a cache that maps unknown axes
through `RouteAxis` (a lossy hash), which is the root cause for new-namespace
failures. Making this explicit in the instructions would reduce ambiguity.

================================================================================
                             SUGGESTIONS 💡
================================================================================

--------------------------------------------------------------------------------
1. Test Docstrings Could Be More Descriptive
--------------------------------------------------------------------------------

File:    tbench-task/tests/test_outputs.py (lines 26-180)

Current approach: Test docstrings use phrases like "Checks one isolated public
transition and its neighboring control" and "Checks a neutral set of public
reads created for this case" — these describe the test structure but not the
specific behavior being verified (e.g., "maintenance re-encrypts old-epoch
frames while preserving active-epoch frames byte-for-byte").

Suggested improvement:
┌─────────────────────────────────────────────────────────────────────────────┐
│  def test_e01() -> None:                                                    │
│      """Maintenance re-encrypts an old-epoch frame while preserving an      │
│      active-epoch frame byte-for-byte."""                                   │
│                                                                             │
│  def test_e02() -> None:                                                    │
│      """Newly added service namespaces are readable via get without          │
│      invoking recovery."""                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Rationale: More specific docstrings make test failures immediately
interpretable and improve the task's self-documentation for future reviewers.

================================================================================
                            OVERALL ASSESSMENT
================================================================================

This is a well-constructed, challenging debugging task that exercises deep
understanding of envelope encryption, namespace isolation, and authenticated
data structures. The bugs are realistic (scope mis-derivation, over-broad
matching, fallback masking failures) and require careful code reading to fix.

Key Strengths:
  ✓ Sophisticated multi-layered cryptographic codebase with realistic bugs
  ✓ Comprehensive 12-test suite covering recovery, maintenance, audit, and
    namespace isolation through a well-designed case_factory helper
  ✓ Strong anti-cheating: tests/solution are not in the image, the crypto
    prevents trivial shortcutting, and the case_factory dynamically generates
    test scenarios

Key Weaknesses:
  ✗ Base image choice (Python slim for a Go task) deviates from canonical
    image policy
  ✗ Some tested behaviors (generic namespace support) are only implicitly
    stated in the instructions

Evaluates: cryptographic debugging, Go systems programming, envelope
           encryption internals, namespace isolation enforcement

================================================================================
  RECOMMENDATION: ⚠️ NEEDS REVISION

  The task is high quality overall but should use the canonical Go base image
  (or document the exception) and could benefit from slightly more explicit
  instruction text around generic namespace handling to close the behavior-
  coverage gap between instruction.md and the test suite.
================================================================================
```

## test_rubrics (from platform export)

```
Agent leaves valid live records for newly introduced service namespaces directly readable without recovery, +3
Agent repairs the shared authority-lineage shear across maintenance write binding and scoped key context, +5
Agent restores authenticated open and validated predecessor selection so recover restores affected secrets, +5
Agent runs /app/bin/vaultctl recover and writes /app/output/recovery.json listing each affected service/secret once, excluding healthy identities, +3
Agent preserves healthy records byte-identical through recover and maintain, +2
Agent leaves complete on-disk state unchanged after a second maintain, +2
Agent keeps /app/bin/vaultctl get failing on a substituted record without invoking recover, +3
Agent keeps /app/bin/vaultctl audit rejecting tampered records and intact cross-namespace substitutions, +2
Agent recovers identities that carry prior history and allows maintain to re-encrypt older records while remaining readable, +3
Agent hand-writes recovery.json, replaces the bundled corpus, or bypasses authentication, -5
Agent edits verifier tests, shadows pytest, or forces reward without repairing vaultctl behavior, -5
Agent patches only one locus and leaves residual auth failure or namespace leakage, -3
Agent weakens get or audit fail-closed behavior on substituted records, -2
```

