# STEP3B — device-node-migration-haze — REV-2

Date: 2026-07-23
Paper review after Step 2b preflight PASS (collapse 0 FAIL / 5 WARN) and Harbor
oracle 1x / NOP. No task-file edits in this pass (no dirty-flag).

## Edit ledger

- None. Construction already absorbed collapse FAIL remediations (three roots
  `loom/`/`veil/`/`tether/`, CR8 wrappers, `reject_delta`/`reject_stable`,
  inflated oracle bodies, instruction GX9 slim). Spec amended accordingly.

## §1–7 review-and-submit

| Section | Verdict | Notes |
| --- | --- | --- |
| 1 Instruction | PASS | Symptoms-only cutover symptoms; absolute paths; `/app/bin/haze`; schema citation; `HAZE_*` overrides named; no solve walkthrough. Slightly long (LOW). |
| 2 Environment | PASS | Digest-pinned rust:1.85-slim Dockerfile, `.dockerignore`, offline hash-locked verifier deps, C+Rust only, ≥20 env files, no shipped build artifacts. Specials are project `HZSP` files (no CAP_MKNOD). |
| 3 Oracle | PASS | Three-root substantive repair (`knit_p`/`hinge_q`/`moor_r`); Harbor oracle 1.0 (`2026-07-23__04-11-07`). Decoys untouched. |
| 4 Verifiers | PASS | CM-007 test.sh; binary reward; failing/control/reject metamorphic probes; schema-aligned. |
| 5 Metadata | PASS | `version=2.0`, hard, system-administration, c/rust, anonymous author, `allow_internet=false`. |
| 6 Structure | PASS | Standard single-step layout; construction_manifest aligned with amended spec. |
| 7 Difficulty | PASS | Residual hardness is packed-ledger materialization + special-entry fidelity + staging-relative rebinding across three roots. |

## Part A — collapse / residual hardness

**Hardness axes:** Discover / Synthesize / Diagnose / Navigate coupling / Reason beyond training — PASS for count-green / open-red cutover with control+reject matrix.

**Smallest plausible patch:** Correct packed rematerialize in `knit_p`, special-entry roster fidelity in `hinge_q`, and relative-anchor rebinding in `moor_r`. Not one-file; not `cp -a` recipe.

**Frontier:** `loom/loom.c`, `veil/veil.rs`, `tether/tether.rs` (+ decoys unused by oracle).

**Discovery budget vs draft:** Matches amended reviewer appendix (packed decode, special fidelity, relative anchor).

### Collapse WARN justifications (do not pad)

| Check | Severity | Justification |
| --- | --- | --- |
| RC3 Verifier Shallowness | WARN | Structure-heavy JSON navigation still asserts domain probe outcomes (`open_ok`/`identity_ok`/`path_ok`/`mode_ok`, control stability, reject polarity, digest). Not format-only existence checks. |
| RC6 Instruction Specificity | WARN | Cause-revealing family is weak (ALL_CAPS `HAZE_*` env override names required by CM-002). No algorithm/cause nouns. |
| CR1 Symbol-Table Compliance | WARN | Extra symbols are same-file helpers/structs rewritten because solve uses whole-file heredocs for the three manifest loci — not additional fix locations or decoys. |
| GX3 Oracle Edit Distance | WARN | 63-line real edit distance is A16 WARN-band; residual hardness is three-authority coupling, not LOC. Do not pad comments/LOC (A16 anti-gaming). |
| GX6 Causal Connective Density | WARN | Borderline connective rate from symptoms prose (“while”, “so”); no cause disclosure. |

Mechanical stack: **0 FAIL**.

## Part B — per-test feasibility

| Test | Risk | Notes |
| --- | --- | --- |
| test_h01–h02, h06, h10 | LOW | Identity/openability / interaction; materialization-sensitive. |
| test_h03, h05, h07, h11 | LOW | Mode/owner fidelity + control byte stability. |
| test_h04, h08–h09, h12 | LOW | Path rebinding + reject polarity; report consistency. |

No HIGH-risk single-technique or order-flaky tests identified.

## Step 2b evidence (pre–dirty-flag; no 3b edits)

- Preflight A/B/C: PASS (collapse 0 FAIL / 5 WARN)
- Oracle 1x: **1.0** — `jobs/2026-07-23__04-11-07`
- NOP: **0.0** — `jobs/2026-07-23__04-11-57`

## Decision

Step 3b complete with no task edits. Ready for Step 4 (oracle 10x + package). Re-run `check-task.sh` before packaging if revise invalidated gate stamps; Harbor 1x/NOP remain valid while the working tree is unchanged.
