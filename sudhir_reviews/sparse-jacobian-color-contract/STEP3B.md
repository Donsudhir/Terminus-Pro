# TASK-SJCC-001 Step 3b Paper Review

- Date: 2026-07-19
- Revision: 1
- Status: CLEAN after revision-1 instruction / CLI / tell fixes
- Difficulty estimate: Hard
- Recommended action: Proceed to Harbor oracle 1x + NOP, then Step 4
- Diagnostics: quality check not run; verifier-health not required after clean paper analysis and exact location ablations already recorded in Step 2b

## Lifecycle reconciliation

Cheap gates had passed at revision 0. Step 3b found a CM-002 honest-instruction gap (`--resume-check` and SENSLAB_* used by tests but under-documented) plus a `leaked` symbol tell in `vault.rs` and a CR1 collision risk from naming `span_info` next to `reset_span`. Revision 1 opened, fixes applied, cheap gates re-verified PASS, Docker oracle 12/12 and NOP 10/12 fail reconfirmed.

## Rules reviewed

- `sudhir_knowledge/TASK_LIFECYCLE.md`
- `sudhir_knowledge/COMMON_MISTAKES.md` (CM-001…CM-005)
- `.cursor/rules/00-authoring-critical.mdc`
- `.cursor/rules/review-and-submit.mdc`
- `.cursor/rules/difficulty-calibration.mdc`
- `task-type-taxonomy.md`
- ADR-0009

## Structural review

### Instruction

Verdict: PASS after revision 1.

- ~250 words in three plain paragraphs; human-style problem report.
- Absolute `/app` paths; no task name, canary, algorithm, threshold, or fix-path disclosure.
- Documents observable contracts for SENSLAB_INPUT / SENSLAB_OUTPUT and `--mode-echo` without backtick schema dumps (RC6 symptoms-only).
- Uses “scale summary” rather than `span_info` to avoid CR1 stem collision with `reset_span`.
- Mechanical audit: symptoms-only, 0 triggered families.

### Environment

Verdict: PASS.

- 36 files excluding Dockerfile/compose (`small`).
- C, Rust, and Fortran perform substantive scientific work; decoys are real non-fix helpers.
- Digest-pinned Rust image; apt/Python pinned at build; `WORKDIR /app`; tmux + asciinema; final-layer `asciinema --version` (CM-001).
- `.dockerignore` present; no solution/tests COPY; offline verifier; `allow_internet = false`.
- Docs describe report layout without repair walkthroughs.
- Revision 1 renamed the `leaked` local in `vault.rs` to `carry`.

### Oracle

Verdict: PASS.

- Deterministic offline four-target repair at A–D only.
- Additive C/Rust rewrites plus surgical Fortran unpack edit.
- Collapse RC1/GX2/GX3 green; no fixture replacement or test mutation.

### Verifier

Verdict: PASS.

- Canonical offline `test.sh` and binary reward footer.
- Twelve opaque pytest functions with behavioral docstrings.
- Metamorphic permutation, resume (`--mode-echo`), scale, support, directional-product, determinism, and digest checks.
- No golden packed matrices on solver-visible surfaces; independent dense probes.
- Env overrides and `--mode-echo` now match instruction contracts (CM-002).

### Metadata and structure

Verdict: PASS.

- Edition 2, anonymous author, hard scientific-computing, small codebase, three languages, no milestones.
- Timeouts coherent (build 600 / verifier 900 / agent 1800).
- Required standard-task files present; authoring-only artifacts excluded by packaging rules.

## Honest-instruction audit

| Mode | Result | Reason |
| --- | --- | --- |
| Answer recital | PASS | No scenario/field/value triples enumerated. |
| Polarity contradiction | PASS | `same: true` is a single required polarity for `--mode-echo`. |
| Value over-specification | PASS | No candidate numeric answer lists. |
| Undefined metaphor jargon | PASS | Domain terms anchored in docs/code (`ledger`, packed layout, digest). |
| Instruction ambiguity | PASS | Invocation, env overrides, `--mode-echo`, output, and restrictions are explicit. |
| Instruction by reference | PASS | Docs supplement schema; user request stands alone. |
| Test traceability | PASS | Asserted fields live in instruction prose or solver-visible report docs/code. |

## Collapse / difficulty

| Gate | Result |
| --- | --- |
| Hardness axes (Discover/Synthesize/Diagnose/Coupling/Beyond-training) | PASS — four distributed authorities; symptoms-only; CPR drop-in insufficient |
| Instruction completeness | PASS — instruction alone cannot locate A–D |
| `collapse_check.py` | PASS — 0 FAIL / 0 WARN / 23 PASS (revision 1) |
| Flipping-point | PASS — 4×4/12 under 0.34 cap (Step 2b) |
| NOP majority fail | PASS — Docker 10 failed / 2 passed |
| Oracle green | PASS — Docker 12/12 |

## Per-test feasibility

| Test | Checks | Approaches | Chain-dep | Risk |
| --- | --- | --- | --- | --- |
| test_k01 | permutation packed parity | 2+ | no | LOW |
| test_k02 | products + packed entries | 2+ | no | LOW |
| test_k03 | `--mode-echo` same=true | 2+ | yes (plan path) | MEDIUM |
| test_k04 | scale-equivalent products | 2+ | no | MEDIUM |
| test_k05 | mixed-scale span isolation | 2+ | yes (order) | MEDIUM |
| test_k06 | combo perm + mode-echo | 2+ | yes | MEDIUM |
| test_k07 | ledger vs packed counts | 2+ | no | LOW |
| test_k08 | dense probe unpack | 2+ | no | LOW |
| test_k09 | summary/ledger agreement | 2+ | yes | LOW |
| test_k10 | reorder determinism | 2+ | yes | MEDIUM |
| test_k11 | active-batch scale summary | 2+ | yes | LOW |
| test_k12 | byte digest identity | 2+ | yes | MEDIUM |

No HIGH feasibility blockers. MEDIUM items are metamorphic couplings, not single-technique traps.

## Revision 1 edit ledger

| Change | Why |
| --- | --- |
| Rename `--resume-check` → `--mode-echo` in router + tests | Opaque public CLI; documentable without resume/check CR1 noise |
| Document SENSLAB_INPUT/OUTPUT and `--mode-echo` in instruction (no backtick dumps) | CM-002: test-invoked contracts must be stated |
| Avoid naming `span_info` in instruction | CR1 stem collision with `reset_span` |
| Rename `leaked` → `carry` in `vault.rs` | Remove solver-visible bug tell |
| Regenerate `.step2b-checksum` | Integrity after edits |

## Fresh mechanical evidence (revision 1)

```text
Gate summary for 'sparse-jacobian-color-contract':
  static=PASS, dockerfile=PASS, collapse=PASS, integrity=PASS

collapse_check: 0 FAIL, 0 WARN, 23 PASS

Docker NOP:  10 failed, 2 passed
Docker oracle: 12 passed

Harbor oracle 1x: mean 1.000, 0 exceptions  → jobs/2026-07-19__02-58-38
Harbor NOP:      mean 0.000, 0 exceptions  → jobs/2026-07-19__02-59-20
```

Compose teardown logged `permission denied` stopping containers (CM-003 / snap-docker); trial rewards still completed cleanly. Prefer sudo cleanup before Step 4 oracle 10x.

## Findings summary

| Severity | Count | Disposition |
| --- | --- | --- |
| HIGH | 0 remaining | CM-002 gap fixed in revision 1 |
| MEDIUM | 0 remaining | — |
| LOW | 1 | Harbor compose down permission denied — infra, not task defect |

## Verdict

CLEAN. Harbor oracle 1x = 1.0 and NOP = 0.0 recorded. Proceed to Step 4 (oracle 10x, package, approve). Do not package before 10x.
