# TASK-MCOS-001 — mesh-checkpoint-operator-skew — Super-Uniqueness Dossier

- Idea: `mesh-checkpoint-operator-skew` (IDEA-0032)
- Category: scientific-computing
- Archetype: long-horizon investigation — checkpoint/resume after remesh where residuals look healthy but solution fields disagree with an uninterrupted twin
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** a mixed-language scientific mesh solver with mid-run checkpoint, remesh, resume, operator/assembly reuse, and twin uninterrupted controls.
2. **Failure mechanism:** after remesh+resume, residual norms / iteration counts remain plausible while solution-field digests and pointwise residuals disagree with a never-interrupted twin; operator or geometry-bound cached state is reused across a changed mesh authority.
3. **Distributed fix topology:** checkpoint serialization boundary, remesh/geometry authority, operator or assembly cache invalidation, and mixed-language field packing/reduction must coordinate. No single-module “clear cache” or “bump mesh id” clears the matrix.
4. **Verifier/invariant surface:** interrupted vs uninterrupted field-digest parity, residual contracts, byte-stable no-checkpoint healthy control, and deterministic reports.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` on 2026-07-23.

Scientific neighbours:

- `sparse-jacobian-color-contract` — sparse residual sensitivity / coloring / unpack; no remesh checkpoint.
- `robust-predicate-scale-parity` — geometric predicates under affine scale; no solver resume.
- `krylov-orthogonality-loss` — reserved Krylov restart/storage/reduction family; not remesh+operator reuse.
- `reproducible-reduction-parity` / `certified-enclosure-drift` — reduction/enclosure families; different mechanism.
- `amg-coarsen-parity-rift` (IDEA-0036, same batch) — AMG coarsening under reordering; not checkpoint/remesh.

No idea combines remesh+resume, operator reuse under geometry change, and twin uninterrupted field-digest parity. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: envelope-rotation-shear, musl-sysroot-splice, resolver-closure-drift, robust-predicate-scale-parity, rowgroup-prune-mirage, sparse-jacobian-color-contract. None is a mesh checkpoint/remesh operator-reuse task. **No collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Content-scanned `Task_Ready_To_Submit/` and `sudhir_tasks_ready_to_submit/` zip `instruction.md` for `remesh|checkpoint.?restart|operator.?cach|mesh.?adapt|restart.?parity|solution.?digest|field.?digest` (2026-07-23). Name/content hits were unrelated (`quota-mesh-rebalance`, `swarm-mesh-coord-heal`, magnetometer residual debug, SJCC residual lab, RCD resolver). **No remesh-checkpoint operator-skew collision.**

### 4. Upstream corpus

Portfolio + prior TB research notes (RPSP/SJCC/ERS dossiers) contain no Terminal-Bench public task whose intellectual core is FEM/mesh remesh+checkpoint with twin-run field parity under stale operator reuse. Closest scientific actives remain RPSP/SJCC (different mechanisms). **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `checkpoint restart remesh operator reuse finite element solver wrong solution residual looks fine`
- PETSc SNES / MOOSE stateful residual discussions (inspiration only)

External literature describes stateful residual / MF operator / remesh hygiene as real engineering failure modes. No public Terminal-Bench task instance, patch, or test suite was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is a production FEM checkpoint/restart after adaptive remesh that leaves a stale operator or assembly cache. Ordinary “implement checkpoint I/O” or “clear the preconditioner” recipes do not match this distributed twin-run parity contract across mixed-language packing and geometry authorities.

## Closest analogue and structural difference

- **Closest analogue:** reserved `krylov-orthogonality-loss` (restart-coupled iterative invariants) and active `sparse-jacobian-color-contract` (residual pipeline metamorphic parity).
- **Structural difference:** this idea’s core is **geometry-changing remesh + resume** with **operator/assembly reuse** judged by **interrupted vs uninterrupted field digests**, not Krylov subspace storage or sparse Jacobian coloring/unpack.

## Result

Uniqueness PASS for `mesh-checkpoint-operator-skew`. Proceed to Step 2a.
