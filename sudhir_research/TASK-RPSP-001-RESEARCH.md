# TASK-RPSP-001 Research and Uniqueness Record

- Date: 2026-07-18
- Status: Step 2a approved
- Confidence: High for uniqueness; medium-high for final authoring feasibility until construction

## Corpus uniqueness

The audit inspected all 157 current submission archives plus active task instructions and metadata.

- Nine archives matched the word `mesh`, but each used it for distributed-system network meshes rather than geometry.
- `lidar-voxel-segment-bind` uses point clouds and voxel segmentation, but it is a machine-learning accounting and replay task. It does not use exact predicates, Delaunay topology, determinant certification, or C/Fortran geometry kernels.
- `hyperspectral-endmember-unmix-bind` is spectral reconstruction and abundance accounting.
- `mixed-radix-spectrum-lab` covers FFT-style numerical stability and thread parity, not geometry.
- `grid-inertia-rocof-estimate` covers power-system estimation, not exact geometric decisions.
- No active task instruction matched robust geometry terms.

Conclusion: robust 3D predicate correctness and affine-equivalent tetrahedral topology are unoccupied in this repository.

## Authoritative sources

### Shewchuk robust predicates

Source: https://www.cs.cmu.edu/~quake/robust.html

- Orientation and in-circle/in-sphere decisions reduce to determinant signs.
- Ordinary floating point can return a wrong sign when the determinant is near zero.
- Adaptive arithmetic can compute only as much precision as needed to certify a sign.
- The reference implementation explicitly warns that excess internal precision can invalidate assumptions unless the processor is configured consistently.

Implication: determinant sign and downstream topology are strong, deterministic verification surfaces. A reference implementation alone must not solve the complete task.

### CGAL kernel robustness

Source: https://doc.cgal.org/latest/Kernel_23/index.html

- Inexact predicates can make inconsistent control-flow decisions in geometric algorithms.
- Exact predicates with inexact constructions are a useful performance/correctness boundary.
- Predicates are fundamental control-flow units for triangulation, convex hull, orientation, and in-sphere decisions.
- Affine transformations and exact-predicate kernel choices provide meaningful metamorphic tests.

Implication: affine-equivalent connectivity and local topology checks are scientifically grounded properties rather than arbitrary expected outputs.

### GCC floating-point optimization

Source: https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html

- `-ffp-contract=fast` permits contraction into fused operations.
- `-Ofast` enables optimizations that are not valid for every standards-compliant numerical program.
- `-ffast-math` changes assumptions about rounding, finite values, association, and excess precision.
- Link-time optimization merges some floating-point options conservatively across translation units.

Implication: translation-unit and link-level numerical policy can legitimately disagree with a filter's derived error assumptions.

### Rust FFI

Source: https://doc.rust-lang.org/nomicon/ffi.html

- Rust cannot verify that foreign declarations match the C implementation.
- Correct ABI types and representations are the programmer's responsibility.
- `#[repr(C)]`, correct status types, and safe wrappers are required for reliable interoperability.

Implication: a tri-valued scientific status can be lost at the language boundary without memory corruption or obvious build failure.

### Fortran/C interoperability

Source: https://gcc.gnu.org/onlinedocs/gfortran/Interoperability-with-C.html

- `BIND(C)` provides standardized procedure and type interoperability.
- C and Fortran array dimensions and default indexing order differ.

Implication: a legacy Fortran connectivity fold can disagree with C/Rust conventions while remaining deterministic and superficially plausible.

## Selected scientific story

Affine-invariant tetrahedral connectivity requires four coordinated properties:

1. a filtered determinant path whose uncertainty bound remains valid under the compiled arithmetic;
2. a cross-language status mapping that preserves the exact-fallback escalation state;
3. coordinate normalization scoped to each affine-equivalent batch rather than shared globally;
4. canonical connectivity folding consistent with the sign and vertex conventions used upstream.

This is one scientific invariant spanning three languages, not four unrelated debugging defects.

## Reference-copy risk

Shewchuk-style C code is highly available. The task therefore keeps a custom tri-valued ABI, per-batch normalization contract, and Fortran canonicalization layer. Copying a known predicate implementation can repair only part of the system and cannot satisfy affine-equivalent connectivity or canonical report checks by itself.

## Selected fix locations

- `native/series.c::eval_band`
- `host/plate.rs::map_state`
- `host/frame.rs::reset_frame`
- `analysis/pack.f90::fold_rows`

Each name is intentionally opaque relative to the public instruction.

## Planned test distribution

Twelve opaque tests are planned. Each selected location controls four tests, giving 4/12 = 0.3333 under concentration cap 0.34. Cross-location tests couple the C filter to the Rust status map, the two Rust lifecycle locations, and the Rust state to the Fortran fold.

## Main risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Copy a public robust predicate | Custom ABI and downstream invariants keep the rest unsolved |
| One compiler flag fixes everything | Substantive filter, status, lifecycle, and folding logic all remain required |
| Fortran becomes decorative | Fortran owns canonical connectivity and topology incidence folding |
| Tests leak expected geometry | Test-side exact arithmetic derives signs and properties from raw inputs |
| A golden topology is rewritten | No solver-visible golden output; affine variants and invariants are generated |
| Prompt reveals causes | Mechanical instruction audit and causal-density check both passed on the draft |

## Symptoms-only instruction draft

The geometry lab under `/app` rebuilds a tetrahedral connectivity report from bundled point-cloud batches. Most ordinary batches look healthy, but equivalent batches shifted or uniformly rescaled in space can produce different canonical cell sets. Near-flat and nearly spherical boundary cases also leave inverted cells, broken neighbor relations, or disagreement between the emitted connectivity and the audit summary.

Correct the scientific pipeline so `/app/output/geometry_report.json` is deterministic and geometrically consistent for every bundled batch and its equivalent transformed variants. Rebuild and run it through `/app/bin/geomlab`. The report must preserve batch identity, canonical cells, adjacency, orientation summary, local validity summary, topology counts, and a reproducibility digest. Input cardinality and point identities must remain unchanged. Equivalent variants must emit the same canonical connectivity, every cell must have consistent handedness and neighbors, and the summary must agree with the emitted structure. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

Mechanical preflight:

- Instruction specificity: PASS, symptoms-only, zero triggered families.
- Causal-connective density: PASS, zero detected connectives in 163 words.

## Validation outcome

- Attempt: 1
- Mechanical score: 0 FAIL, 0 WARN
- Strict authoring-spec lint: PASS
- Finalize: exit 0
- Decision: GO under ADR-0006
- Evidence: `sudhir_ideas/specs/robust-predicate-scale-parity-attempt-1-evidence.json`
- Authoring spec: `sudhir_ideas/specs/robust-predicate-scale-parity.md`
- Reviewer appendix: `sudhir_ideas/specs/robust-predicate-scale-parity-reviewer.md`
