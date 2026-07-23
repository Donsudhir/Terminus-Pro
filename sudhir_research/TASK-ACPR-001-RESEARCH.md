# TASK-ACPR-001 — amg-coarsen-parity-rift — Super-Uniqueness Dossier

- Idea: `amg-coarsen-parity-rift` (IDEA-0036)
- Category: scientific-computing
- Archetype: long-horizon investigation — algebraic multigrid hierarchy construction that breaks solution/residual parity under equivalent matrix reorderings while smoothness and coarse-size summaries look fine
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** an algebraic multigrid (AMG) preconditioner / hierarchy builder with smoother–coarse coupling, sparse matrix reorderings, and residual/solution-digest reporting.
2. **Failure mechanism:** the same matrix under two equivalent reorderings yields different convergence curves and fine-grid solution digests; smoothness indicators and coarse-size summaries can look fine versus a fixed healthy ordering control.
3. **Distributed fix topology:** strength/coarsening selection, prolongation/restriction (or aggregate) construction, and apply/V-cycle coupling must remain algebraically consistent under reordering. Hard-coding one permutation is rejected.
4. **Verifier/invariant surface:** both reorderings meet the same residual and solution-digest contracts; healthy ordering control stays green; smoothness/coarse-size bait is not success.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` on 2026-07-23.

Scientific neighbours:

- `sparse-jacobian-color-contract` (IDEA-0012 / TASK-SJCC-001) — sparse residual sensitivity coloring/compress/unpack metamorphic parity; not AMG coarsening hierarchy under reordering.
- `krylov-orthogonality-loss` (IDEA-0010, reserved) — Krylov restart/storage/reduction subspace invariants; not AMG coarsen/prolong.
- `mesh-checkpoint-operator-skew` (IDEA-0032) — remesh+checkpoint with stale operator/assembly reuse vs uninterrupted twin; **different mechanism** (geometry/resume authority, not AMG coarsening parity). Do not conflate.
- `robust-predicate-scale-parity`, `reproducible-reduction-parity`, `certified-enclosure-drift` — predicate/reduction/enclosure families; unrelated.

No idea combines AMG coarsening under equivalent reorderings, smoothness/coarse-size bait, and dual-ordering residual + solution-digest parity. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/` includes `sparse-jacobian-color-contract` and (separately) mesh-checkpoint construction elsewhere; none is an AMG coarsening-parity task. **No collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Strict content scan of submission zips for `\bamg\b|algebraic.?multigrid|coarsen|prolongation|restriction.?operator` (2026-07-23): **0 hits** beyond the unrelated SJCC archive (sparse Jacobian, not AMG). **No collision.**

### 4. Upstream corpus

Local `tasks/` and prior TB research notes contain no Terminal-Bench public task whose core is AMG coarsening parity under equivalent reorderings. Nearest public science neighbour found in external search is Harbor `amr-poisson-optimize` (geometric AMR / coarse–fine reflux performance) — **not** algebraic multigrid coarsening metamorphic parity. **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `Terminal-Bench algebraic multigrid AMG coarsening reordering parity solution digest`
- Classical AMG coarsening / CLJP / strength-of-connection literature (inspiration only)

External AMG literature describes real coarsening-order sensitivity. No public Terminal-Bench task instance, patch, or test suite matching this dual-ordering residual/digest contract was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is an AMG setup that indexes strength or coarse sets by raw row order rather than matrix-graph identity, so equivalent permutations change the hierarchy while smoothness heuristics still look plausible. Textbook “implement classical AMG” or SJCC coloring recipes do not match this distributed coarsen/prolong/apply parity verifier.

## Closest analogue and structural difference

- **Closest analogue:** active `sparse-jacobian-color-contract` (metamorphic sparse scientific parity) and reserved `krylov-orthogonality-loss` (iterative subspace invariants). `mesh-checkpoint-operator-skew` is a same-batch scientific neighbour with a **different** remesh/resume mechanism — not a collision.
- **Structural difference:** this idea’s core is **AMG hierarchy coarsening/apply consistency under equivalent reorderings**, graded by **residual + fine-grid solution digests** with **smoothness/coarse-size bait** — not Jacobian coloring/unpack, not Krylov restart storage, and not remesh-checkpoint operator reuse.

## Result

Uniqueness PASS for `amg-coarsen-parity-rift`. Do not start Step 2a in this session.
