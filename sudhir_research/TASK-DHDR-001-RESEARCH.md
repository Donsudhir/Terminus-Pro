# TASK-DHDR-001 — domain-halo-digest-rift — Super-Uniqueness Dossier

- Idea: `domain-halo-digest-rift` (IDEA-0041)
- Category: scientific-computing
- Archetype: long-horizon investigation — post-repartition partitioned PDE where local residuals look healthy but global field digests / cross-rank checksums disagree with a never-repartitioned twin
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** a partitioned PDE-like solver with C numerical kernels, a Rust partition/halo orchestrator, ghost-layer exchange, shared-face ownership, and a never-repartitioned twin control.
2. **Failure mechanism:** after domain repartition, local residuals / per-rank norms and orchestrator “synced” marks stay green while global field digests and cross-rank checksums diverge from the twin; ghost packing, shared-face ownership, and reduction ordering interact (including irregular-partition halo-width and Rust metadata ahead of lagging C buffers).
3. **Distributed fix topology:** halo pack/unpack, face-ownership authority, reduction-tree / fold order, and Rust↔C sync-stage metadata must coordinate. No single-module “widen halo” or “force allreduce” clears the matrix.
4. **Verifier/invariant surface:** repartitioned vs never-repartitioned field-digest parity, cross-rank checksum / reduce contracts, byte-stable non-repartition healthy control, deterministic reports.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `sudhir_ideas/IDEA_INDEX.md` on 2026-07-23.

Scientific neighbours:

- `mesh-checkpoint-operator-skew` — remesh+checkpoint/resume with operator reuse; twin digests, but mechanism is geometry-change resume, not repartition halo/reduce coupling.
- `amg-coarsen-parity-rift` — AMG coarsening under equivalent reorderings; not halo exchange.
- `sparse-jacobian-color-contract` — sparse residual sensitivity / coloring / unpack; no domain repartition.
- `reproducible-reduction-parity` — reduction parity family; no ghost-layer / partition ownership topology.
- `krylov-orthogonality-loss` — reserved Krylov restart/storage; not repartition halo.
- `certified-enclosure-drift` — enclosure certification; different deliverable.

No idea combines post-repartition halo/ghost packing, shared-face ownership, reduction ordering, and twin never-repartitioned global digest parity under healthy local residuals. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/` scanned 2026-07-23 (including mesh-checkpoint-operator-skew, sparse-jacobian-color-contract, robust-predicate-scale-parity, resolver-closure-drift, musl-sysroot-splice, envelope-rotation-shear, rowgroup-prune-mirage). Content hits for `field_digest` are MCOS twin-run remesh/resume only. **No repartition-halo collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Content-scanned `sudhir_tasks_ready_to_submit/*.zip` `instruction.md` for `halo|repartition|ghost.?layer|domain.?decomp|partition.?map|field.?digest` (2026-07-23). Only `mesh-checkpoint-operator-skew.zip` matched `field digest` (remesh twin parity). **No domain-halo-digest-rift collision.**

### 4. Upstream corpus

Portfolio + prior TB research notes (MCOS/SJCC/RPSP/AMG dossiers) contain no Terminal-Bench public task whose intellectual core is repartition-coupled halo exchange + global reduce digest drift with a never-repartitioned twin. Closest scientific neighbour remains MCOS (different mechanism: remesh/operator reuse). **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `PETSc DMPlex repartition halo exchange ghost layer digest mismatch local residual correct`
- PETSc-users threads on DMPlex halo / partitioner issues (e.g. 2023-Feb halo/partitioner wrong field with healthy 1-proc; PetscSF halo exchange discussions) — inspiration only for symptom shape (local/green vs parallel-boundary wrong).

External literature describes halo/ghost and partition-boundary ownership as real engineering failure modes. No public Terminal-Bench task instance, patch, or test suite was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is a production partitioned PDE that repartitions mid-campaign and leaves stale ghost packing, shared-face ownership, or non-associative reduce order while local norms stay plausible. Ordinary “implement MPI halo” or “use MPI_Allreduce” recipes do not match this distributed twin-run parity contract across Rust orchestrator metadata and C kernels.

## Closest analogue and structural difference

- **Closest analogue:** `mesh-checkpoint-operator-skew` (twin field-digest parity under a healthy control) and reserved `reproducible-reduction-parity` (reduction-order sensitivity).
- **Structural difference:** this idea’s core is **domain repartition → halo/ghost packing + shared-face ownership + reduce-order coupling** judged by **repartitioned vs never-repartitioned global digests**, not remesh/operator reuse or cross-implementation reduction parity alone.

## Result

Uniqueness PASS for `domain-halo-digest-rift`. Proceed to Step 2a.
