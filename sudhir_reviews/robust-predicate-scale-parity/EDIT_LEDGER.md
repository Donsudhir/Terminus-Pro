# TASK-RPSP-001 Edit Ledger

## 2026-07-18 - Initial construction

Created the complete canonical task from the approved authoring spec:

- root metadata, symptoms-only instruction, output contract, and local construction manifest;
- digest-pinned offline Docker environment;
- C fast certificate and exact integer refinement;
- Rust parser, state, FFI, enumeration, topology, and report writer;
- Fortran row fold and scalar aggregate;
- dyadic family corpus and realistic subsystem documentation;
- twelve opaque exact/property tests;
- four-location substantive oracle.

Approved selected locations and symbols were preserved exactly.

## 2026-07-18 - Compliance corrections

- Split verifier requirements installation from later shell checks for dependency-pin parsing.
- Added system-path wrappers for Rust and the verifier virtual environment.
- Added a strict-build helper so timeout analysis reflects two actual builds.
- Set final timeouts to agent 1800 seconds, verifier 900 seconds, build 600 seconds.
- Declared both build helpers as internal harness files.
- Omitted the proposed source-tree output placeholder because current package hygiene forbids output directories under the shipped environment.

## 2026-07-18 - Verifier corrections

- Removed direct editable-binary coercion patterns that triggered RC4 while retaining independent exact expectations.
- Replaced verifier-only rational-library use with exact integer determinant and binary-ratio arithmetic.
- Strengthened `test_r11` so the untouched lifecycle defect fails the declared test.
- Separated unoriented affine connectivity properties from oriented row-fold properties.
- Added the host refinement-state assertion to the strict-build test.
- Final location ablations match the construction manifest exactly:
  - A: r01, r02, r06, r10
  - B: r03, r06, r07, r10
  - C: r04, r05, r11, r12
  - D: r07, r08, r09, r12

## 2026-07-18 - Gold Harness corrections

- Extended symbol extraction to Rust scoped visibility and Fortran procedures.
- Added regression coverage for both language forms.
- Made registry revision invalidation remove stale final-only archives.
- Compressed the concurrently expanded always-on routing document below its hard byte cap without removing pipeline semantics.

No task edit was made after the final preflight, oracle 1x, NOP, registry gate record, and integrity verification.

## 2026-07-18 - Step 3b revision 4

- Invalidated and removed a package created before paper review and Step 4 oracle stress.
- Relaxed the host refinement probe from one exact mapped sentinel to any distinct non-sign state that preserves refinement.
- Removed the lex-least-even representation lock from verifier ground truth.
- Kept exact cell identity, positive handedness, reciprocal adjacency, topology, and byte determinism checks while allowing any stable positive row representation.
- Removed the `nm` binary-symbol implementation proxy.
- Added direct behavioral coverage for all three bundled families and all nine named variants.
- Reworded architecture documentation so it no longer points at retained reusable state.
- Corrected the first revised test's assumption that every bundled family shared the same variant names.
- Reconfirmed local oracle 12/12, NOP 0/12, and exact four-test subsets for A, B, C, and D.
- Proved a second implementation passes: always-refine C, alternate Rust sentinel, and lex-greatest-even Fortran row representation.
- Reconfirmed Harbor oracle 1.0 and NOP 0.0 with zero errors on the revised tree.

No task edit was made after the final revision-4 preflight, oracle 1x, NOP, registry gate record, and integrity verification.

## 2026-07-19 - Revision 6 (CM-007 platform Needs Revision)

Platform reviewer (`fcee6e2e`): grading-integrity hole — root agent + `WORKDIR /app` +
`python -m pytest` from cwd lets `/app/pytest.py` or `/conftest.py` force `reward=1`
without building/running geomlab.

- `tests/test.sh`: `cd /tests && PYTHONSAFEPATH=1 python -m pytest … --confcutdir=/tests`
  (keeps `/tests/test_outputs.py` path and Edition 2 reward footer; prefix still
  passes offline-template static checks).
- `task.toml`: `difficulty = "medium"` (opus 5/5, gpt5 3/5, oracle 3/3, nop 0/1);
  removed non-schema `mcp_servers = []`.
- Dockerfile: add final-layer `asciinema --version` (CM-001 hygiene WARN clear).
- Rubric process lines are platform-form only (not in the zip); tighten to
  output/artifact criteria on resubmit.
- Shadow probe: vulnerable cwd pytest → rc=0; fixed path + `test.sh` → reward=0
  under attacks; oracle + attacks → reward=1 (12/12). See `STEP2B-REV6.md`.

## 2026-07-19T09:58:21Z — Revision 7

- TRIVIAL → MEDIUM hardening (CM-008):
  - `tests/test_outputs.py`: cancellation cases require `raw == 2`; well-conditioned
    series require exact `raw` (blocks always-refine); r06/r10 tightened the same way.
  - `environment/host/plate.rs`: replace one-glance `if a < 0` with
    `normalize_progress` that still collapses refine (`2`) into `+1`.
  - `environment/host/frame.rs`: replace early sticky return with warmup-reuse
    that computes then discards a fresh dyadic window while `armed`.
  - `instruction.md`: add well-conditioned certification contract; keep probes +
    qualitative cancellation conservatism (CM-002).
  - Oracle `solve.sh` plate/frame bodies unchanged (already correct).
