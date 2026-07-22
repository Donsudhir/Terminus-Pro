# TASK-RPSP-001 Step 3b Paper Review

- Date: 2026-07-18
- Revision: 4
- Status: CLEAN
- Difficulty estimate: Hard
- Recommended action: Proceed to Step 4
- Diagnostics: quality check not run; verifier-health not required after clean paper analysis, exact location ablations, and explicit alternate-solution proof

## Lifecycle reconciliation

The authoritative board showed a package created before Step 3b review and before Step 4 oracle stress. That package and its approval evidence were invalidated through registry revision 3, the final-only zip was removed, cheap gates were rerun, and the task returned to review. Confirmed review edits then opened revision 4 and invalidated evidence again before revalidation.

## Rules reviewed

- `sudhir_knowledge/TASK_LIFECYCLE.md`
- `.cursor/rules/00-authoring-critical.mdc`
- `.cursor/rules/task-creation.mdc`
- `.cursor/rules/review-and-submit.mdc`
- `.cursor/rules/difficulty-calibration.mdc`
- `writing_tests.mdc`
- `reviewer_checklist.mdc`
- `instructions_prompt.mdc`
- `ci_checks.mdc`
- `task-type-taxonomy.md`
- Docker environment and image guidance
- ADR-0006 and ADR-0007

A sub-review claimed these repository policy files were missing because it searched inside the task directory. That finding is unsupported: policies are repository review inputs and would be forbidden task payload if copied into the task.

## Structural review

### Instruction

Verdict: PASS.

- 163 words in two plain paragraphs.
- Human-style problem report with no roleplay, headings, checklist, emoji, or decorative markers.
- Absolute `/app` paths.
- No task name, canary, algorithm, threshold, function, file location, or cause disclosure.
- Goal, invocation, output, identity preservation, affine-equivalent connectivity, handedness, adjacency, summary consistency, determinism, and anti-hardcoding boundary are stated.
- No operational requirement is delegated to an environment hint file.

### Environment

Verdict: PASS.

- Standard single-container environment with 36 files excluding Dockerfile/compose.
- C, Rust, and Fortran perform substantive scientific work.
- Sanctioned Rust runtime is digest-pinned.
- Apt and Python dependencies are pinned and installed at build time.
- `WORKDIR /app`, tmux, asciinema, offline verifier, narrow COPY operations, and `.dockerignore` are present.
- No solution, tests, hidden answer, AI-scaffolding filename, license, build artifact, privileged option, compose service, or network dependency appears in the environment.
- Documentation describes subsystem responsibilities and data/report contracts without a repair walkthrough.
- Review edit removed the cause-adjacent statement that sequential processing exercises reusable host state.

### Oracle

Verdict: PASS.

- Deterministic, offline, noninteractive four-target repair.
- Exactly the approved C, two Rust, and Fortran locations are rewritten.
- 283 non-boilerplate lines and 186 lines of real edit distance.
- Adds conservative magnitude-based certification, preserves exact escalation, reconstructs per-input scale state, and supplies parity-preserving row and incidence folding.
- No fixture replacement, output hardcoding, test modification, no-op rewrite, cosmetic padding, or language bypass.

### Verifier

Verdict: PASS after revision 4 corrections.

- Canonical offline `test.sh` and binary reward.
- Twelve opaque pytest functions with informative behavioral docstrings.
- Exact integer determinant, orientation, in-sphere, cell, adjacency, incidence, topology, and digest derivation.
- Generated transformed families plus all nine bundled batches.
- No source parsing or binary-symbol implementation policing remains.
- No mutable golden file, network, random value, wall-clock assertion, shared test order, or hidden output contract.
- Current tests accept an alternate sentinel and an alternate positive-parity canonical representation.

### Metadata and structure

Verdict: PASS.

- Edition 2 metadata, anonymous author, hard scientific-computing category, small codebase, applicable tags, three real languages, no milestones, internet disabled.
- Agent, verifier, build, CPU, memory, and storage budgets are coherent and within platform caps.
- Required standard-task files are present.
- Authoring-only output contract, construction manifest, metrics, and checksum are excluded by packaging rules.
- No final zip exists during review.

## Honest-instruction audit

| Mode | Result | Reason |
| --- | --- | --- |
| Answer recital | PASS | No scenario, field, and value triples are enumerated. |
| Polarity contradiction | PASS | No binary output is described with both polarities in one scope. |
| Value over-specification | PASS | No candidate output values or threshold list appears. |
| Undefined metaphor jargon | PASS | Geometry, connectivity, handedness, adjacency, topology, and digest are standard terms anchored in source/docs. |
| Instruction ambiguity | PASS | Invocation, output, invariants, and restrictions are explicit without implementation causes. |
| Instruction by reference | PASS | Environment docs supplement architecture; they do not carry the user request. |
| Test traceability | PASS | Every asserted report field lives in instruction prose or solver-visible report code/docs. |

## Post-oracle collapse audit

Stage: post-oracle.

Smallest plausible successful patch:

A conservative magnitude-based decision region in C, a distinct exact-escalation state in Rust, per-input coordinate-state reconstruction in Rust, and parity-preserving row plus incidence folding in Fortran. The Fortran portion remains a substantial algorithmic rewrite. No strict subset satisfies the report invariants.

Likely editable frontier:

- `native/series.c::eval_band`
- `host/plate.rs::map_state`
- `host/frame.rs::clear_frame`
- `analysis/pack.f90::fold_rows`

Requirement-to-file map:

- Certified signs and exact escalation: native series plus host state mapping.
- Scale-equivalent processing and execution-order isolation: host frame lifecycle.
- Positive row orientation, deterministic representation, incidence, and topology: Fortran fold plus healthy Rust aggregation.
- Deterministic serialization and digest: healthy writer and digest modules.

Oracle line count: 283 non-boilerplate lines; real edit distance 186.

Discoverability:

- Prompt nouns do not grep to selected paths or symbols.
- Test names are opaque.
- No correction markers, commented answers, cause statements, or reference files exist.
- No file references more than two selected symbols.
- Runtime failures remain outcome-level.
- Architecture docs state responsibilities without naming retained state or the repair.

Red flags: none remaining.

Residual hardness:

The solver must derive a safe cancellation bound from the supplied magnitude series, preserve a third foreign status through host control flow, recover per-input dyadic scaling semantics, and implement an orientation-preserving tetrahedral representation plus face-incidence fold in Fortran. A public robust-predicate implementation repairs only part of the chain.

Collapse verdict: PASS. Mechanical result is 0 FAIL, 0 WARN, 23 PASS.

## Scientific correctness review

- Orientation uses the same signed 3-by-3 determinant convention in Rust, C, and tests.
- In-sphere decisions use the same lifted 4-by-4 determinant and positive-orientation convention.
- Uniform positive power-of-two scaling preserves determinant signs; common translations cancel from relative coordinates.
- Parser alignment limits exact coordinates to one million after exponent alignment, keeping orientation and lifted in-sphere products inside signed 128-bit range.
- Candidate enumeration is bounded to at most 495 tetrahedra for twelve points.
- Exact zero determinants are excluded from scored fixtures.
- Every emitted row is checked for positive exact orientation.
- Cell identity is verified independently of the chosen positive-parity row representation.
- Adjacency is recomputed in emitted row order, so alternate valid canonical forms are accepted.
- Face incidence, boundary count, edge count, cell count, Euler value, and local empty-sphere validity are derived independently.
- Digest scope and compact JSON bytes are recomputed independently.
- Malformed input fails before atomic report rename.
- All bundled family identities, point identities, and nine variant identities are exercised.

No scientific contradiction or overflow path remains for accepted input bounds.

## Per-test feasibility

| Test | Checks | Valid approaches | Chain dependence | Exact assertions | Risk | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `test_r01` | Positive cancellation certificate | Always-refine or conservative fast bound | None | Exact sign uniquely determined | Low | Keep |
| `test_r02` | Negative alternating certificate | Always-refine or conservative fast bound | None | Exact sign uniquely determined | Low | Keep |
| `test_r03` | Distinct foreign refinement state | Any non-sign sentinel with refinement flag | None | Sentinel no longer pinned | Low | Keep revised |
| `test_r04` | Generated affine-equivalent cell identity | Any correct predicate/canonical representation | None | Unordered cell set is unique | Low | Keep |
| `test_r05` | Source-family order independence | Any deterministic sorted report | None | Byte equality is required determinism | Low | Keep |
| `test_r06` | End-to-end positive and negative exact resolution | Fast filter, always-refine, or other certified path | Coupled A+B by one scientific decision chain | Final signs are unique | Low | Keep |
| `test_r07` | Exact escalation reaches positive folded output | Multiple status and parity representations | Coupled B+D by one pipeline invariant | Geometric outcomes are unique | Low | Keep revised |
| `test_r08` | Positive exact handedness | Any even positive row permutation | None | Sign is unique | Low | Keep |
| `test_r09` | Reciprocal adjacency and topology accounting | Any deterministic positive row order | None | Derived from emitted cells | Low | Keep revised |
| `test_r10` | Strict/default build parity | Any deterministic certified implementation | Coupled A+B under alternate build | Equivalent documents required | Low | Keep |
| `test_r11` | Repeat determinism, all bundled inputs, malformed fail-closed | Any valid implementation | C controls transformed results; other checks independent | Identities come from immutable corpus | Low | Keep revised |
| `test_r12` | Transformed positive output and digest coherence | Any stable positive row representation | Coupled C+D by one transformed-output invariant | Digest and geometry uniquely derived | Low | Keep revised |

Joint tests combine locations only where the public outcome is itself end-to-end. Each location also has isolated coverage, and one-location ablations remain behavioral rather than compile-only.

## Multiple valid approaches

Approach A is the oracle: magnitude-sum fast bound, zero-valued refinement sentinel, fresh min/max frame, lex-least-even row representation, and sorted face run-length folding.

Approach B was executed in a disposable container: always return the exact-refinement state from C, use a different non-sign Rust sentinel with host control flow keyed on the refinement flag, and use lex-greatest-even row representation in Fortran. It passed all twelve revised tests with reward 1.

This proves the verifier checks the public scientific contract rather than the oracle's exact implementation.

## Location distribution

Final single-location ablations:

- A fails only r01, r02, r06, r10.
- B fails only r03, r06, r07, r10.
- C fails only r04, r05, r11, r12.
- D fails only r07, r08, r09, r12.

Each location controls 4/12 tests, ratio 0.3333 under cap 0.34. Every ablation is a behavioral verifier failure; none is compile-only.

## Findings and dispositions

| Finding | Severity | Class | Disposition |
| --- | --- | --- | --- |
| Package created before review/Step 4 | High process | lifecycle defect | Invalidated and removed through revision 3 |
| Exact mapped sentinel required | Medium | task defect | Relaxed to any distinct non-sign refinement state |
| Lex-least-even row form required | Medium | task defect | Cell identity and adjacency made representation-agnostic |
| Binary symbols parsed by verifier | Medium | task defect | Removed implementation proxy |
| Bundled corpus replacement not directly caught | Medium | task defect | All nine bundled batches now exercised |
| Architecture exposed reusable host state | Medium | discoverability warning | Reworded to neutral process/serialization description |
| Review policy files reported missing in task | Unsupported | false finding | Rejected; policies correctly remain at repository root |
| First revised bundled test assumed common variant names | Medium drafting | task defect | Corrected before final preflight |
| Harbor compose teardown permission denial | Infrastructure | external issue | Rewards had zero errors; all stale containers removed |

No HIGH or MEDIUM task defect remains.

## Revalidation evidence

- Final preflight: static PASS, Dockerfile PASS, collapse 23/23 PASS, packaging preview PASS, checksum current.
- Local oracle: 12 passed, reward 1.
- Local NOP: 12 failed, reward 0.
- Alternate valid implementation: 12 passed, reward 1.
- Four location ablations: each exact 4-fail / 8-pass declared subset.
- Harbor oracle: `jobs/2026-07-18__23-21-05/result.json`, mean 1.0, zero errors.
- Harbor NOP: `jobs/2026-07-18__23-22-00/result.json`, mean 0.0, zero errors.
- Stale Harbor task containers: none.
- Ruff: PASS.
- Repository pytest: 240 passed, 26 skipped.
- Task checksum: current.
- Submission index: current for 157 archives.
- Registry: revision 4, phase `review`, all cheap gates PASS.
- Final RPSP zip before Step 4: absent.
- Whitespace check: PASS.

## Final decision

Step 3b CLEAN. No verifier-health or quality-check escalation is justified by the final paper review. The task may proceed to Step 4, where oracle 10x, a fresh NOP, final packaging, archive validation, parity inspection, and `approve_task.py` are still required before any APPROVED or SUBMITTABLE claim.
