# Robust Predicate Scale Parity — Reviewer Appendix

- Task ID: `TASK-RPSP-001`
- Slug: `robust-predicate-scale-parity`
- Category: `scientific-computing`
- Review phase: Step 2a
- Recommendation before mechanical finalize: GO

## Executive finding

The proposed task is a bounded, deterministic mixed-language scientific debugging problem. Its core invariant is affine-equivalent oriented tetrahedral connectivity. Four inconsistent authorities must be reconciled across C, Rust, and Fortran: fast-decision certification, refinement-state propagation, per-input magnitude lifecycle, and parity-preserving connectivity folding.

The design is not a disguised dependency, configuration, timeout, or fixture-repair exercise. It remains hard after an honest public contract because identical geometry symptoms can originate at four different numerical or representation boundaries.

## Mechanical score target

| Family | Result |
| --- | --- |
| Hardness axes | 5 PASS, 0 WARN, 0 FAIL |
| Anti-trivialization checks | 21 PASS, 0 WARN, 0 FAIL |
| Rubric axes | 6 PASS, 0 WARN, 0 FAIL |
| Instruction completeness | PASS |
| Discovery budget | 4 committed discoveries |
| Instruction specificity | Symptoms-only |
| Candidate topologies | 3 |
| Selected fix locations | 4 |
| Planned tests | 12 |
| Maximum per-location concentration | 4/12 = 0.3333 under cap 0.34 |

## Public instruction review

The public instruction is 163 words. Mechanical preflight found:

- no algorithm mentions;
- no schema enumeration signal;
- no API enumeration signal;
- no numeric thresholds;
- no binding phrases;
- no scope-closure phrases;
- no causal-connective disclosure signal;
- final classification `symptoms-only`.

It states the observable failure, working directory, executable, output path, report responsibilities, invariants, and anti-hardcoding boundary. It does not reveal determinant predicates, exact refinement, compiler arithmetic, a three-valued status, per-input normalization, Fortran parity, or selected files and symbols.

## Corpus uniqueness review

All 157 current submission archives and active task metadata were searched.

- Nine lexical `mesh` hits referred to network-service meshes.
- No task covered robust orientation, in-sphere certification, tetrahedral Delaunay validity, affine-equivalent connectivity, or C/Rust/Fortran scientific interoperation.
- The nearest point-cloud task is ML segmentation and accounting, not computational geometry.
- The nearest numerical tasks cover spectral reconstruction, FFT-style numerical stability, and power-system estimation.

Collision verdict: PASS.

## Scientific legitimacy

### Determinant decisions

Orientation and in-sphere tests are determinant-sign decisions. Near zero, ordinary floating-point evaluation can return a sign inconsistent with exact arithmetic. Adaptive refinement is a standard way to retain speed on easy cases while certifying difficult cases.

### Affine metamorphism

Translation and strictly positive uniform scale preserve orientation sign, in-sphere inclusion sign after the expected positive scale factor, and point-identity Delaunay connectivity for nondegenerate input. These are strong metamorphic properties.

### Connectivity invariants

A tetrahedral complex permits independent checks of positive orientation, shared-face reciprocity, one-or-two face incidence, local empty-sphere validity, unique edge and face counts, boundary face count, and Euler value.

### Language roles

- C owns fast certification and exact refinement.
- Rust owns FFI interpretation, input lifecycle, enumeration, and report orchestration.
- Fortran owns parity-preserving row canonicalization and incidence folding.

Fortran is substantive, not decorative.

## Hidden discovery map

| ID | Hidden fact | Planned location | Why it remains hidden |
| --- | --- | --- | --- |
| D1 | The accepted numerical error region is not conservative for the evaluated cancellation-prone expression | `native/series.c::eval_band` | Revealing the bound or arithmetic mismatch points directly to the fix |
| D2 | The custom native uncertainty state is collapsed by host mapping | `host/plate.rs::map_state` | Revealing the tri-state ABI identifies the exact boundary and branch |
| D3 | Magnitude context survives across independent inputs | `host/frame.rs::clear_frame` | Revealing per-input reset turns diagnosis into a direct lifecycle edit |
| D4 | Legacy row folding changes orientation parity and disagrees with upstream convention | `analysis/pack.f90::fold_rows` | Revealing permutation parity turns the Fortran diagnosis into a recipe |

## Alternate topology review

Three plausible distributed topologies were considered:

1. **Selected certification chain** — C certification, Rust status, Rust magnitude lifecycle, Fortran fold.
2. **Numerical certificate chain** — C fast filter, C exact refinement, C certificate packing, Rust status mapping.
3. **Symmetry convention chain** — Fortran canonical fold, Fortran orientation audit, Rust face packing, C orientation stamping.

The selected topology best balances mathematical depth, language diversity, project-specific coupling, and authoring feasibility. Every alternative requires four locations; there is no credible one-file topology.

## Collapse analysis

### One-pass risk

A solver may recognize robust predicates and inspect the C path first. Repairing or replacing only that path still leaves:

- uncertainty collapsed at the Rust boundary;
- magnitude loss before exact refinement on mixed-scale sequences;
- parity and incidence disagreement in Fortran.

### Reference-copy risk

Copying a known robust-predicate implementation cannot satisfy the custom ABI, batch lifecycle, canonical row convention, report topology, or deterministic digest. The task should expose no simple API-compatible slot into which a public file can be dropped unchanged.

### Grep risk

Selected names are deliberately opaque:

- `series.c::eval_band`
- `plate.rs::map_state`
- `frame.rs::clear_frame`
- `pack.f90::fold_rows`

The naming pass removed `bridge.rs`, `order.f90`, `batch.rs`, `reset_frame`, and `canonicalize_cells`. The current selected paths and symbols contain no public instruction noun as a case-insensitive substring.

### Declarative-cluster risk

No threshold table, expected-cell fixture, schema enum, compiler toggle, or report snapshot contains the solution. The output is regenerated and expected mathematics is derived test-side.

### Harness risk

Docker and mixed-language compilation are necessary realism, not the source of difficulty. The mathematical and cross-language reasoning remains after the build is healthy.

## Exact verification strategy

The verifier must use exact rational arithmetic derived from dyadic input mantissas and exponents.

- Orientation: exact 4-by-4 determinant or translated 3-by-3 determinant.
- In-sphere: exact lifted 5-by-5 determinant with orientation convention applied.
- Connectivity: exact candidate checks or invariant verification on emitted cells.
- Orientation: every emitted ordered quadruple is positive.
- Local validity: no other point is strictly inside the corresponding circumsphere.
- Adjacency: reciprocal indices and exact shared opposite faces.
- Incidence: boundary faces occur once and interior faces twice.
- Topology: recompute unique vertices, edges, faces, cells, boundary faces, and Euler value.
- Affine variants: compare canonical point-identity cells.
- Determinism: compare exact output bytes and recomputed FNV-1a digest.

No golden report is needed. Expected signs and properties are computed from each input.

## Planned tests and distribution

| Test | Property | Locations |
| --- | --- | --- |
| `test_r01` | exact orientation decisions | A |
| `test_r02` | exact in-sphere decisions | A |
| `test_r03` | refinement-state preservation | B |
| `test_r04` | generated affine-equivalent connectivity | C |
| `test_r05` | mixed-scale execution-order isolation | C |
| `test_r06` | near-degenerate end-to-end decision parity | A, B |
| `test_r07` | refinement through canonical fold | B, D |
| `test_r08` | positive parity of emitted rows | D |
| `test_r09` | adjacency, incidence, topology agreement | D |
| `test_r10` | alternate clean-build parity | A, B |
| `test_r11` | repeated multi-input byte determinism | C |
| `test_r12` | transformed canonical output and digest parity | C, D |

Distribution:

- A: 4/12
- B: 4/12
- C: 4/12
- D: 4/12
- cap: 0.34

## Baseline failure expectations

The untouched task must fail meaningfully across all four location classes.

Expected NOP symptoms:

- wrong exact signs on at least one cancellation family;
- missing exact escalation on at least one near-sphere family;
- connectivity mismatch when mixed-scale families run in opposite orders;
- at least one parity, adjacency, or topology inconsistency after the Fortran fold;
- transformed canonical output or digest mismatch.

If NOP passes most properties or all failures collapse to one selected location, construction must stop and return to Step 2a.

## Oracle expectations

The oracle should make substantive edits at all four selected locations and nowhere unrelated.

Expected oracle characteristics:

- restores a conservative fast-decision acceptance contract;
- preserves and handles the refinement-required state;
- reconstructs magnitude context for each independent input;
- performs lexicographically minimal even-permutation canonicalization and coherent incidence folding;
- does not replace fixtures, expected outputs, or the pipeline;
- does not add an external geometry library;
- does not bypass any required language.

The verifier must accept equivalent implementations and reject fixture-specific hardcoding.

## Construction stop conditions

Return to Step 2a if any of the following occurs:

- exact refinement cannot be supplied as a healthy bounded scaffold;
- a public reference file can replace the C layer unchanged and pass everything;
- the Fortran layer can be removed without losing a scored scientific property;
- one selected location controls more than 0.34 of scored tests;
- required fixes expand beyond eight substantive locations;
- strict-build parity depends on undefined behavior;
- genuinely degenerate geometry forces an undocumented tie-break;
- task runtime becomes dominated by large combinatorial inputs;
- prompt completeness requires revealing a hidden cause;
- the untouched baseline fails only because the build is broken.

## Source basis

- Jonathan Richard Shewchuk, robust adaptive predicates: https://www.cs.cmu.edu/~quake/robust.html
- CGAL Kernel 23 manual: https://doc.cgal.org/latest/Kernel_23/index.html
- GCC optimize options: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
- Rust Nomicon FFI: https://doc.rust-lang.org/nomicon/ffi.html
- GNU Fortran C interoperability: https://gcc.gnu.org/onlinedocs/gfortran/Interoperability-with-C.html

## Final reviewer checklist

- [x] Unique within the current repository corpus
- [x] Deterministic and offline
- [x] Single-container build
- [x] Genuine C, Rust, and Fortran roles
- [x] Exact test-side mathematics
- [x] Symptoms-only public instruction
- [x] Four committed hidden discoveries
- [x] Three distributed candidate topologies
- [x] Four selected flipping points
- [x] Opaque selected names
- [x] Twelve tests with concentration margin
- [x] Reference-copy resistance
- [x] No task source constructed before GO
- [x] Strict mechanical finalize completed

Reviewer recommendation: GO to construction. Strict finalize exited 0 and the recorded best score is `[0, 0]`.
