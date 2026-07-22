# Robust Predicate Scale Parity — Authoring Specification

- Task ID: `TASK-RPSP-001`
- Slug: `robust-predicate-scale-parity`
- Category: `scientific-computing`
- version: 2
- Status: Step 2a approved
- Construction policy: permitted under ADR-0006

## Public instruction draft

The geometry lab under `/app` rebuilds a tetrahedral connectivity report from bundled point-cloud batches. Most ordinary batches look healthy, but equivalent batches shifted or uniformly rescaled in space can produce different canonical cell sets. Near-flat and nearly spherical boundary cases also leave inverted cells, broken neighbor relations, or disagreement between the emitted connectivity and the audit summary.

Correct the scientific pipeline so `/app/output/geometry_report.json` is deterministic and geometrically consistent for every bundled batch and its equivalent transformed variants. Rebuild and run it through `/app/bin/geomlab`. The report must preserve batch identity, canonical cells, adjacency, orientation summary, local validity summary, topology counts, and a reproducibility digest. Input cardinality and point identities must remain unchanged. Equivalent variants must emit the same canonical connectivity, every cell must have consistent handedness and neighbors, and the summary must agree with the emitted structure. Do not replace the bundled inputs or write the report by hand; the checks regenerate it through the compiled pipeline.

Mechanical preflight result: `symptoms-only`, zero specificity families, zero causal-connective signals.

## Authoring Brief

### Triviality (Avoidance) Ledger

- **Single C-file replacement:** blocked by the independent Rust status, Rust lifecycle, and Fortran parity authorities; a public predicate implementation can satisfy only part of the acceptance contract.
- **Compiler-flag-only repair:** blocked by substantive source defects at all four selected locations; strict alternate-build parity is an outcome check, not the intended solution.
- **Golden-output hardcoding:** blocked by runtime-generated dyadic families, regenerated output, reordered execution, and exact property derivation with no solver-visible expected report.
- **Prompt-noun grep:** blocked by opaque selected paths and symbols plus an audited forbidden-token list; obvious public terms occur broadly in scaffold contracts rather than uniquely at fix sites.
- **One test or one location flipping the score:** blocked by twelve coupled tests, four selected locations, and a per-location concentration of 4/12 under the 0.34 cap.
- **Decorative language diversity:** blocked because C certifies numerical decisions, Rust owns FFI and lifecycle control, and Fortran owns parity-preserving canonicalization and incidence folding.
- **Reference-library collapse:** blocked by the custom status ABI, project-specific batch lifecycle, source-visible report contract, and legacy row convention.
- **Fixture or manifest repair:** blocked because the baseline builds and runs, while hidden tests generate new inputs and independently recompute mathematical invariants.

### Per-gate Pitfall Inventory

- **Step 2b construction:** stop if the initial snapshot omits any selected location, exposes a hidden cause in comments or identifiers, or requires the player to invent the entire exact-arithmetic primitive.
- **G1 Docker/build:** pin the base image, keep runtime offline, prove all three language objects are linked, and reject any baseline whose failure is merely a broken compiler or path.
- **G2 test quality:** derive determinant signs and topology with exact rational arithmetic; never compare only to a golden JSON file or the oracle implementation.
- **G3 hardness:** rerun NOP and location-ablation checks; stop if a single edit, public file drop-in, or one selected location passes a majority of scored tests.
- **G4 instruction audit:** preserve the tested 163-word symptoms-only prompt; re-run specificity and causal-density checks after every wording change.
- **G5 paper review:** inspect source for leaked sentinel values, threshold comments, expected cells, filename clues, dead decoys, undefined behavior, and accidental alternate solution paths.
- **G6 oracle review:** require substantive changes at A, B, C, and D; reject fixture replacement, disabled checks, a Rust-only bypass, or broadened tolerance.
- **G7 reproducibility:** run from clean output and build directories, in multiple input orders, under the default and strict builds, with no clock, random, host, or network dependency.
- **G8 packaging:** exclude solution, tests, caches, generated output, debug probes, and reviewer material; validate the final archive with the canonical submission validator.

### Initial Draft Commitments

- Create the complete mixed-language scaffold in the first construction draft, including all four selected paths, all healthy exact-refinement support, all four meaningful decoys, the dyadic corpus, Docker build, twelve tests, and oracle script.
- Keep the public instruction exactly at the mechanically preflighted symptom level unless a changed version is re-audited before any task gate.
- Freeze the selected topology at `native/series.c::eval_band`, `host/plate.rs::map_state`, `host/frame.rs::clear_frame`, and `analysis/pack.f90::fold_rows`; any topology change requires a new Step 2a evidence attempt.
- Make the untouched baseline compile and run to a plausible but mathematically inconsistent report, with meaningful failures attributable across all four selected locations.
- Supply a healthy exact-refinement primitive in the scaffold so solver work is diagnosis and integration rather than writing an unbounded arbitrary-precision library from scratch.
- Keep point sets small, nondegenerate under exact arithmetic, and represented as dyadic values so every scored predicate can be verified exactly and quickly.
- Keep Rust dependency-free, runtime offline, and the normal invocation fixed at `/app/bin/geomlab` writing `/app/output/geometry_report.json`.
- Run oracle once and NOP before paper review, then ten fresh oracle runs only after all paper findings are closed.

### Task identity

- Internal ID: `TASK-RPSP-001`
- Directory slug: `robust-predicate-scale-parity`
- Primary category: `scientific-computing`
- Secondary domain: computational geometry and numerical robustness
- Required implementation languages: C, Rust, and Fortran
- Runtime form: deterministic offline single-container command-line task
- Player work root: `/app`
- Canonical executable: `/app/bin/geomlab`
- Canonical output: `/app/output/geometry_report.json`
- Player-facing files: `instruction.md`, `task.toml`, `environment/`, and solver-owned source files only
- Hidden files: tests and oracle solution must not be copied into the player-visible environment

### Player-facing objective

Repair an existing mixed-language tetrahedral-connectivity pipeline whose ordinary inputs appear plausible but whose near-degenerate and affine-equivalent inputs do not produce one stable oriented complex. The player receives symptoms and a deterministic invocation, not algorithm names, fix locations, threshold values, ABI states, normalization rules, or ordering recipes.

The successful repair must make the compiled pipeline produce the same canonical connectivity for translated and uniformly rescaled representations of the same identified points while preserving exact sign, incidence, and report consistency properties.

### Required behavior

The completed program must:

1. parse every bundled geometry family and all declared variants;
2. preserve the original family, variant, and point identities;
3. evaluate the orientation decisions used to accept tetrahedra;
4. evaluate the local empty-sphere decisions used by the bounded Delaunay scaffold;
5. escalate numerically uncertain fast decisions to the supplied exact refinement path;
6. isolate coordinate-magnitude policy to the current independent input unit;
7. emit only positively oriented tetrahedra under the documented point order;
8. canonicalize each oriented tetrahedron without changing its parity;
9. sort canonical cells deterministically;
10. construct reciprocal four-face adjacency with `-1` for a boundary face;
11. count unique vertices, edges, faces, tetrahedra, and boundary faces from emitted cells;
12. report an Euler value consistent with those counts;
13. report zero orientation and local-validity violations for valid bundled inputs;
14. produce byte-identical output across repeated clean invocations;
15. produce affine-equivalent canonical connectivity for every family variant;
16. compute the report digest from canonical report content rather than from run-specific state;
17. reject malformed input with a nonzero exit status and without a partially valid report;
18. retain a genuine scientific role for C, Rust, and Fortran in the successful pipeline.

The task uses small point sets and a bounded brute-force tetrahedron enumerator. Performance optimization is not the objective. Mathematical and representational consistency is the objective.

### Input contract

The task author must provide a human-readable dyadic coordinate corpus under `environment/data/`.

Required properties:

- Each geometry family has a stable identifier.
- Each variant has a stable identifier and references one family.
- Each point has an integer identity unique within its family.
- Each coordinate is represented losslessly as an integer mantissa and signed power-of-two exponent.
- Variant transforms use translation plus a strictly positive power-of-two uniform scale.
- Variants preserve point cardinality and identities.
- Point sets contain between 6 and 12 points so exhaustive candidate enumeration is bounded.
- Bundled families include ordinary, near-coplanar, near-cospherical, very small, very large, and sequential mixed-scale inputs.
- Nonzero exact determinants must remain nonzero; avoid truly coplanar or truly cospherical ambiguity in scored inputs.
- The player may inspect all bundled data.
- Hidden tests may generate additional dyadic families and transforms using the same documented parser contract.

Suggested text grammar, to be frozen during construction:

- one family header;
- one or more point records containing identity and three mantissa/exponent pairs;
- one or more variant records containing a scale exponent and three translation mantissa/exponent pairs;
- an explicit family terminator.

The parser grammar itself may be evident in the scaffold and fixture. It must not encode expected cells or exact predicate answers.

### Output contract

`/app/output/geometry_report.json` must be valid UTF-8 JSON with stable key ordering and one trailing newline.

Required top-level information:

- schema version;
- ordered per-variant reports;
- a lowercase fixed-width reproducibility digest over the canonical report payload.

Each per-variant report must preserve:

- family identity;
- variant identity;
- ordered point identities;
- canonical oriented tetrahedra as point-identity quadruples;
- one four-entry adjacency row per tetrahedron, aligned with the documented opposite-vertex face order;
- orientation totals;
- local-validity totals;
- topology totals for vertices, edges, faces, tetrahedra, boundary faces, and Euler value.

Construction must freeze exact JSON field names in the solver-visible writer and an example generated by the broken baseline. The public instruction must not enumerate a large machine schema. Hidden tests should parse semantically and separately check byte determinism.

The digest algorithm must be small, deterministic, source-visible, and dependency-free. Use FNV-1a 64-bit over the canonical payload, rendered as 16 lowercase hexadecimal characters. The digest is an integrity and determinism signal, not a security boundary.

### Toolchain contract

- Base image: pinned Ubuntu 24.04 image by immutable digest at construction time.
- Required system tools: GCC, GFortran, Rust compiler, Make, Python 3, and pytest.
- No runtime network access.
- No downloaded runtime data or model artifacts.
- Rust must use the standard library only; do not require Cargo registry access.
- C and Fortran must compile into static objects or archives linked into the Rust-owned executable.
- Build must be reproducible from `/app` using one documented build command.
- Runtime command must be `/app/bin/geomlab` with no required arguments.
- Default compilation must not use `-ffast-math`, unsafe reassociation, or an unspecified excess-precision mode for the predicate translation unit.
- A strict alternate rebuild used by tests must remain compatible with the public build contract.
- The image must contain no solution source, hidden expected report, or test-side exact answers.
- The container must run as a non-root user during normal task execution where compatible with the repository harness.

### Construction manifest

#### Selected topology

The selected topology is the four-authority certification and canonicalization chain:

1. `native/series.c::eval_band`
   - Language: C
   - Role: evaluate a fast bounded numerical decision and return a signed or refinement-required state.
   - Intended baseline defect: the acceptance bound does not conservatively match the operation graph used for a cancellation-prone estimate.
   - Required repair class: restore a valid conservative error region for the actual evaluation and preserve escalation on uncertainty.

2. `host/plate.rs::map_state`
   - Language: Rust
   - Role: map the custom C status into host control flow.
   - Intended baseline defect: a nonnegative shortcut collapses the refinement-required state into an ordinary positive decision.
   - Required repair class: preserve the three-way contract and invoke the supplied exact path when required.

3. `host/frame.rs::clear_frame`
   - Language: Rust
   - Role: initialize the power-of-two coordinate context for the current independent input unit.
   - Intended baseline defect: prior magnitude state survives into later units, causing overflow, underflow, or information loss before exact refinement can help.
   - Required repair class: recompute finite per-unit origin and scale without changing point identities or cross-unit state.

4. `analysis/pack.f90::fold_rows`
   - Language: Fortran with `BIND(C)`
   - Role: parity-preserving canonicalization, deterministic row ordering, and incidence folding for the emitted oriented complex.
   - Intended baseline defect: a legacy row fold applies a parity-changing permutation and an inconsistent row convention.
   - Required repair class: choose the lexicographically least even permutation for each oriented tetrahedron, order rows stably, and fold incidence from the canonical rows.

#### Exact symbol commitments

- `int eval_band(const double *a, const double *b, int32_t n, double *c);`
- `pub(crate) fn map_state(a: i32, b: &mut Frame) -> i8`
- `pub(crate) fn clear_frame(a: &mut Frame, b: &[f64])`
- `integer(c_int) function fold_rows(a, b, c) bind(C)`

The argument names are intentionally opaque. Construction may add surrounding healthy APIs, but these selected paths and symbols must remain the four flipping-point locations unless a new Step 2a attempt explicitly supersedes this record.

#### Healthy scaffold commitments

The author must provide healthy, non-selected scaffold code for:

- exact expansion or exact-integer refinement callable after uncertainty;
- bounded candidate enumeration;
- parser and dyadic transform application;
- report serialization and digesting;
- face matching and adjacency materialization around the Fortran fold;
- malformed-input handling;
- command-line entrypoint and output-directory creation.

The exact refinement path must exist and work in the baseline. The baseline failure must be that it is not always reached, not that the author omitted the hard mathematical primitive and expects the player to invent a full arbitrary-precision package.

#### Decoy commitments

Include believable, healthy semantic neighbors:

- `native/window.c` with an `eval_frame`-style diagnostic helper;
- `host/router.rs` with a `map_code`-style display mapping;
- `host/pool.rs` with a `clear_slot`-style buffer lifecycle helper;
- `analysis/stats.f90` with a `fold_marks`-style scalar aggregate helper.

Decoys must compile and participate in ordinary diagnostics but must not be dead junk, contain comments that exonerate them, or create alternate fixes.

#### File-tree commitment

Initial construction should create no fewer than the following substantive files:

- `instruction.md`
- `task.toml`
- `environment/Dockerfile`
- `environment/Makefile`
- `environment/data/families.geom`
- `environment/native/include/series.h`
- `environment/native/series.c`
- `environment/native/refine.c`
- `environment/native/window.c`
- `environment/host/main.rs`
- `environment/host/plate.rs`
- `environment/host/frame.rs`
- `environment/host/router.rs`
- `environment/host/pool.rs`
- `environment/analysis/pack.f90`
- `environment/analysis/stats.f90`
- `environment/output/.gitkeep`
- `tests/test_task.py`
- `solution/solve.sh`

All selected locations must exist in the initial snapshot. The author may add narrowly necessary headers or modules, but must not grow the task into an open-ended mesh library.

### Acceptance contract

A submission is correct only when all of these outcome properties pass after a clean rebuild:

1. Every exact orientation probe agrees with an independently computed rational determinant sign.
2. Every exact in-sphere probe agrees with an independently computed rational determinant sign under the declared orientation convention.
3. Refinement-required native outcomes remain distinguishable at the Rust boundary and reach exact refinement.
4. Uniform positive power-of-two scale and translation do not change canonical connectivity for a family.
5. Sequentially running tiny and huge families in either order does not change either family's result.
6. Every emitted tetrahedron has positive exact orientation.
7. Every non-boundary adjacency entry is reciprocal and names a tetrahedron sharing exactly the expected face.
8. Every face incidence is one for boundary faces or two for interior faces.
9. No non-vertex point lies strictly inside an emitted tetrahedron's circumsphere under exact arithmetic.
10. Reported topology counts equal counts recomputed from emitted cells.
11. Reported Euler value equals `V - E + F - T` for the emitted tetrahedral complex.
12. Affine-equivalent variants emit equal canonical point-identity cell lists.
13. Repeated clean runs emit byte-identical reports and matching digests.
14. A strict alternate rebuild emits semantically and byte-equivalent output.
15. Malformed input fails closed.
16. The output is regenerated through the compiled pipeline; a handwritten report does not pass.

No acceptance item may require the player's patch to be textually identical to the oracle.

### Work-area boundary

- Player edits are limited to `/app`.
- The canonical working tree is the copied `environment/` content.
- The tests, solution, repository metadata, and host paths are outside the player work area.
- The program may write only beneath `/app/output` and compiler-owned build directories beneath `/app/build`.
- The program must not read hidden test paths, host mounts, network endpoints, clocks, random devices, machine identifiers, or environment secrets.
- Input is read only from the documented geometry data path or a test-provided path through a source-visible internal test hook.
- The normal public invocation requires no flags.

### Anti-hardcoding rule

The player may not:

- replace the input corpus;
- reduce point cardinality;
- change point identities;
- write or copy a precomputed report;
- branch on known family or variant identifiers to emit expected cells;
- embed expected determinant signs or expected connectivity tables;
- disable variants, local-validity checks, adjacency, topology, or digest generation;
- bypass C or Fortran with a separate Rust-only answer path;
- invoke external geometry services or libraries;
- weaken compilation or tests.

Hidden tests generate additional dyadic point families, reorder family execution, change transform exponents and translations, remove the output before each run, and recompute all mathematical properties independently. These checks must detect fixture-specific hardcoding without requiring source-style policing.

### Required secrets / hidden-test families

Keep these facts out of `instruction.md`, ordinary comments, fixture names, and obvious top-level symbols:

1. **Cancellation family** — exact orientation is nonzero while the fast estimate lies inside the correct uncertainty region.
2. **Near-sphere family** — exact in-sphere sign is nonzero and requires refinement.
3. **Status sentinel family** — a native refinement-required result exercises the Rust mapping directly.
4. **Scale-order family** — tiny then huge and huge then tiny executions expose retained magnitude state.
5. **Parity fold family** — an oriented tetrahedron whose fully sorted order is an odd permutation exposes parity loss.
6. **Reciprocity family** — multiple tetrahedra share interior faces and expose row/face convention disagreement.
7. **Generated affine family** — test-created dyadic translations and positive scale powers verify invariance beyond bundled names.
8. **Strict-build family** — a clean alternate optimization build verifies that the repaired certificate is not accidental.
9. **Malformed family** — duplicate identities, non-finite conversions, invalid exponents, and truncated records fail closed.
10. **Anti-tamper family** — output is deleted, inputs are varied, and the binary is rerun before validation.

The exact mantissas, exponents, determinant signs, canonical cell sets, and expected digests are test secrets derived at runtime and must never appear in solver-visible artifacts.

### Test-authoring requirements

Create exactly twelve scored tests in the first complete version. Keep names opaque:

- `test_r01`: exact orientation decisions; selected location A
- `test_r02`: exact in-sphere decisions; selected location A
- `test_r03`: refinement-state preservation; selected location B
- `test_r04`: generated affine-equivalent connectivity; selected location C
- `test_r05`: mixed-scale execution-order isolation; selected location C
- `test_r06`: near-degenerate end-to-end decision parity; selected locations A and B
- `test_r07`: refinement through canonical fold; selected locations B and D
- `test_r08`: positive parity of emitted rows; selected location D
- `test_r09`: adjacency, incidence, and topology agreement; selected location D
- `test_r10`: alternate clean-build parity; selected locations A and B
- `test_r11`: repeated multi-input byte determinism; selected location C
- `test_r12`: transformed canonical output and digest parity; selected locations C and D

Concentration math:

- A controls 4 of 12 tests, ratio `0.3333333333333333`.
- B controls 4 of 12 tests, ratio `0.3333333333333333`.
- C controls 4 of 12 tests, ratio `0.3333333333333333`.
- D controls 4 of 12 tests, ratio `0.3333333333333333`.
- Cap: `0.34`.

Test-side mathematical oracle requirements:

- Parse dyadic values into Python integers and `fractions.Fraction`; do not use floating point for expected signs.
- Compute 4-by-4 orientation determinants exactly.
- Compute 5-by-5 lifted in-sphere determinants exactly, correcting for tetrahedron orientation convention.
- Recompute canonical cells from point identities and exact predicates or verify all defining invariants when multiple equivalent enumerations are possible.
- Recompute faces, edges, adjacency reciprocity, incidence, boundary count, and Euler value independently.
- Generate transforms with positive power-of-two scale and dyadic translations.
- Run in at least two family orders.
- Delete output before every scored generation.
- Check both semantic JSON and exact bytes.
- Check that all required C, Rust, and Fortran objects are linked into the executable.
- Avoid asserting internal function text or exact oracle patch shape.
- Keep the NOP run as a real failing baseline with meaningful failures across all four locations.
- Run the oracle once before paper review and ten fresh times at Step 4.

### Non-goals

- Building a production-scale tetrahedral mesher
- Handling exact coplanar or exact cospherical symbolic degeneracy
- Optimizing asymptotic performance
- Supporting arbitrary coordinate text formats
- Introducing GMP, CGAL, Qhull, or network-fetched dependencies
- Rewriting the project in one language
- Adding a GUI, server, database, concurrency, or distributed execution
- Accepting non-uniform affine transforms
- Using a cryptographic digest
- Hiding the input grammar or output writer from the player
- Requiring a specific source-level patch when outcomes are correct

### Expected difficulty

`hard`

Residual hardness after honest disclosure:

- the same report symptom can arise from an incorrect sign, lost uncertainty status, pre-refinement magnitude loss, or parity-changing canonicalization;
- the relevant authority crosses C numerical logic, Rust FFI and lifecycle logic, and Fortran array/order semantics;
- familiar robust-predicate code does not solve the project-specific status and representation chain;
- the public instruction contains no algorithm, threshold, function, file, status, or ordering recipe.

The task should be difficult for a strong generalist and appropriately bounded for a senior numerical or systems engineer.

### Time estimate

- Expert solver: 3 to 8 focused hours
- Strong generalist: 6 to 14 hours
- Task construction after GO: 8 to 16 hours including fixtures, oracle, Docker, and tests
- Paper review: 1 to 2 hours
- Ten-run oracle validation: 1 to 3 hours depending on image build time

If construction shows the exact refinement scaffold, brute-force enumerator, or Fortran fold cannot be made reliable within these bounds, stop and return to Step 2a rather than expanding scope.

### Authoring metadata

- Author: Sudhir
- Step 2a date: 2026-07-18
- Evidence schema: current repository `specs/validation_schema.json`
- Evidence target: 0 FAIL, 0 WARN
- Uniqueness corpus: 157 current submission archives plus active tasks
- Closest non-colliding tasks reviewed:
  - `lidar-voxel-segment-bind`
  - `hyperspectral-endmember-unmix-bind`
  - `mixed-radix-spectrum-lab`
  - `grid-inertia-rocof-estimate`
- Primary sources:
  - Shewchuk, Adaptive Precision Floating-Point Arithmetic and Robust Predicates
  - CGAL Kernel 23 manual
  - GCC optimization and floating-point option documentation
  - Rust Nomicon FFI chapter
  - GNU Fortran C interoperability documentation
- Selected locations: 4
- Planned scored tests: 12
- Maximum test concentration: 0.34
- Per-location concentration: 0.3333333333333333
- Instruction specificity: symptoms-only
- Construction status: forbidden until strict finalize GO
