# STEP3B — mesh-checkpoint-operator-skew — REV-1

Date: 2026-07-23
Checksum verified before review; post-edit preflight + oracle/NOP reconfirmed.

## Edit ledger

- **Preservation-safe:** `instruction.md` — named `MESHLAB_INPUT` / `MESHLAB_OUTPUT` in the public contract instead of deferring path overrides to `runtime.conf` only (Hard FAIL under instruction-honesty rule 4 / tb3-reviewer §4). Avoided `agree`/`disagree` substring collisions with True-valued summary flags. Kept graded field inventory + schema citation (WW-010).
- No oracle, decoy, test, or Dockerfile edits in this pass.

## §1–7 review-and-submit

| Section | Verdict | Notes |
| --- | --- | --- |
| 1 Instruction | PASS | Symptoms-only; absolute paths; entrypoint `/app/bin/meshlab`; schema keys present; env overrides named; no solve walkthrough. Length ~4 short paragraphs (preferred 1–3) — LOW note only. |
| 2 Environment | PASS | Digest-pinned Dockerfile, `.dockerignore`, offline deps, no AI scaffolding, 28 env files (`small`), no shipped build artifacts after hygiene. |
| 3 Oracle | PASS | Three-root substantive repair; oracle 1.0 after edit (`2026-07-23__03-11-43`). No decoy touches. |
| 4 Verifiers | PASS | CM-007 test.sh; binary reward; twin/control + fold metamorphic checks; schema-aligned. |
| 5 Metadata | PASS | `version=2.0`, hard, scientific-computing, c++/rust/fortran, anonymous author, `allow_internet=false`. |
| 6 Structure | PASS | Standard single-step layout; construction_manifest present and aligned. |
| 7 Difficulty | PASS | See Part A/B; residual hardness is cross-language remesh+resume diagnosis. |

## Part A — collapse / residual hardness

**Hardness axes:** Discover / Synthesize / Diagnose / Navigate coupling / Reason beyond training — all PASS for remesh+resume twin parity across C++/Rust/Fortran.

**Smallest plausible patch:** Fix geometry-token restore in `braid_q`, replace OR-accumulate reuse bind in `latch_r`, fold under active order in `sift_s`. Not one-file; not recipe.

**Frontier:** `native/span.cpp`, `host/shelf.rs`, `pack/fold.f90` (+ decoys unused by oracle).

**Discovery budget vs draft:** Still matches reviewer appendix (token bind, reuse keying, fold order).

### Collapse WARN justifications (do not pad)

| Check | Severity | Justification |
| --- | --- | --- |
| RC2 Oracle Predictability | WARN | Only `host/shelf.rs` hits a weak dir-keyword (`host`); 1/3 targets. Native/pack remain opaque. Not grep-collapse of the fix. |
| CR1 Symbol-Table Compliance | WARN | Extra symbols are same-file helpers (`mix64`, `hash_span`, shelf struct methods) rewritten because solve uses whole-file heredocs for the three manifest loci — not additional fix locations or decoys. |
| GX3 Oracle Edit Distance | WARN | 47-line real edit distance is A16 WARN-band; residual hardness is three-authority coupling, not LOC. Do not pad comments/LOC (A16 anti-gaming). |
| GX7 Test-Literal Homing | WARN | Orphans `order_a.case` / `order_b.case` are verifier-local tmp names in `test_m10`, not agent I/O contracts. |

Mechanical stack: **0 FAIL**.

## Part B — per-test feasibility

| Test | Risk | Notes |
| --- | --- | --- |
| test_m01–m03, m05–m07, m11 | LOW | Twin/control metamorphic; multi-family. |
| test_m04, m08–m09, m12 | LOW | Independent fold / digest contracts from schema. |
| test_m10 | LOW | Reorder families; tmp case names verifier-only. |

No HIGH-risk single-technique or order-flaky tests identified.

## Post-edit Step 2b reconfirm

- Preflight A/B/C: PASS (`/tmp/mcos-3b-preflight.txt`)
- Oracle 1x: **1.0** — `jobs/2026-07-23__03-11-43`
- NOP: **0.0** — `jobs/2026-07-23__03-12-14`
- Checksum rewritten by post-edit preflight

## Decision

Step 3b complete after preservation-safe edits. Step 2b PASS re-confirmed. Ready for Step 4 packaging.
