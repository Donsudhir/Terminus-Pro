# TASK-RPSP-001 Step 2b Evidence

- Date: 2026-07-18
- Status: PASS
- Historical note: superseded for current-tree evidence by Step 3b revision 4; retained as the construction record
- Canonical source: `sudhir_tasks/active/robust-predicate-scale-parity`
- Registry phase: `review`
- Registry revision: 2
- Next phase: Step 3b paper review

## Construction inventory

- Standard, single-container, offline task
- Languages: Rust, C, Fortran
- Total task files on disk: 47, including local checksum and metrics
- Integrity-tracked files: 44
- Environment files excluding Dockerfile and compose: 36
- Selected oracle targets: 4 across 3 roots
- Scored tests: 12
- Local construction manifest: present and excluded from packaging
- Final submission archive: not created; final-only submission directory contains no RPSP zip

## Discovery-budget confirmation

### D1 - numerical certificate

Confirmed at `environment/native/series.c::eval_band`. The baseline acceptance region uses the rounded result rather than the supplied magnitude series, allowing cancellation to be certified with the opposite sign. The public instruction, file name, comments, and opaque test names do not reveal this cause. Oracle ablation A fails only `test_r01`, `test_r02`, `test_r06`, and `test_r10`.

### D2 - foreign status

Confirmed at `environment/host/plate.rs::map_state`. The baseline mapping collapses the refinement-required native state into an ordinary positive result. The public instruction does not name a status encoding or FFI cause. Oracle ablation B fails only `test_r03`, `test_r06`, `test_r07`, and `test_r10`.

### D3 - per-input magnitude context

Confirmed at `environment/host/frame.rs::clear_frame`. The baseline retains a coordinate context across independent transformed inputs. No instruction, path, comment, or runtime message names a reset policy. Oracle ablation C fails only `test_r04`, `test_r05`, `test_r11`, and `test_r12`.

### D4 - parity-preserving row fold

Confirmed at `environment/analysis/pack.f90::fold_rows`. The baseline sorts row values without preserving orientation parity and reports raw face totals rather than unique incidence. The public instruction reports only handedness, neighbor, and summary symptoms. Oracle ablation D fails only `test_r07`, `test_r08`, `test_r09`, and `test_r12`.

All four discoveries survive construction in their approved locations. Each location controls exactly 4 of 12 tests, ratio 0.3333 under cap 0.34.

## Discoverability gate

1. Instruction points to implementation locations: no.
2. Environment contains correction markers, hidden walkthroughs, commented answers, or answer-shaped fixtures: no.
3. Selected paths or symbols contain public instruction nouns: no; CR1 and CR7 pass.
4. Test names reveal repair steps: no; tests are `test_r01` through `test_r12`.
5. Broken runtime output identifies an exact repair: no; process errors remain subsystem-level and the normal baseline emits plausible structured output.
6. One visible orchestrator names all fix symbols: no; CR8 reports at most two selected symbols referenced by one file.

No discoverability signal required removal after the final draft.

## Mechanical gates

### Canonical preflight

Command: `./scripts/check-task.sh <canonical-task-root>`

- Static: PASS with no warning
- Dockerfile: PASS
- Collapse: PASS, 0 FAIL / 0 WARN / 23 PASS
- Packaging preview: PASS
- Integrity checksum: PASS, 44 tracked files

Collapse details:

- Oracle targets: 4 across 3 roots
- Oracle non-boilerplate LOC: 283
- Real edit distance: 186 lines
- Dominant root share: 50%
- RC1-RC8: PASS
- CR1, CR2, CR7-CR9: PASS
- GX1-GX10: PASS
- Instruction: symptoms-only, zero triggered specificity families

### Container build

- Sanctioned Rust base is digest-pinned.
- C, GFortran, Rust, Python verifier, tmux, and asciinema are available offline.
- Final local development image built without compiler warnings.
- Local image ID after the final environment edit: `sha256:d44fc87db240d71a517c6f36758b064d7a27947103b39d71eeb2171d59cf860e`.

### Local behavior

- Oracle: 12 passed, reward 1
- Untouched baseline: 12 failed, reward 0
- Four single-location ablations: exact declared 4-fail / 8-pass subsets for A, B, C, and D

### Harbor Step 2b sanity

Final current-tree evidence:

- Oracle job: `jobs/2026-07-18__22-42-37/result.json`
  - trials: 1
  - errors: 0
  - mean reward: 1.0
- NOP job: `jobs/2026-07-18__22-43-34/result.json`
  - trials: 1
  - errors: 0
  - mean reward: 0.0

Harbor's compose teardown hit the machine's existing Snap-daemon permission problem after each completed trial. This did not create a Harbor exception or alter reward. Stale task containers were terminated through their internal process trees and a final Docker check found none remaining.

### Repository certification

- Ruff: PASS
- Pytest: 240 passed, 26 skipped
- Task integrity: PASS
- Submission index: current for 157 archives
- Premature final archive: absent
- Stale task containers: none
- `git diff --check`: PASS

## First-pass misses and minimal corrections

1. Docker dependency parser treated commands chained after the requirements install as unpinned packages. Split the pinned install into its own Docker layer.
2. Verifier timeout analysis double-counted two direct `make` calls as four sites. Moved the two real builds into source-visible build scripts and set verifier/agent budgets to 900/1800, removing the warning without weakening coverage.
3. RC4 interpreted direct `str(BINARY)` call arguments as editable expected-value derivation. Switched to neutral path conversion while keeping all independent exact assertions.
4. GX8 rejected verifier-only `fractions` derivation. Replaced it with exact integer determinant arithmetic and exact binary-float ratios using the standard library primitives already represented by the environment's integer refinement.
5. CR1 could not recognize Rust `pub(crate)` or Fortran procedures. Extended the Gold Harness extractor and added a regression test; the task now records all four selected symbols.
6. Login shells omitted Rust and verifier virtual-environment paths. Added explicit system-path wrappers and verified the image under login-shell execution.
7. Initial location ablation showed two test-subset mismatches. Isolated affine cell-set checks from row-fold semantics and added the declared status assertion to the strict-build test. Final ablations match the manifest exactly.
8. A premature pipeline archive existed before Step 4. Registry revision invalidation now deletes stale final-only archives; the stale zip was removed and current gates were re-recorded.

## Decision

Step 2b PASS. Proceed to Step 3b paper review. Do not package, approve, or run oracle 10x until review is complete and any review edit has re-entered the Step 2b gate chain.
