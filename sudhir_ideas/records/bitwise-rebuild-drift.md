# Idea: Bitwise Rebuild Drift

- Idea ID: `IDEA-0018`
- Slug: `bitwise-rebuild-drift`
- Category: build-and-dependency-management
- Languages: TBD (candidate: c, python, shell)
- Created: 2026-07-19T10:58:40Z
- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)

## Problem in one line

An independent rebuild of a shipped artifact does not match it byte-for-byte; the solver must eliminate every nondeterminism source across the toolchain and prove convergence with a provenance manifest.

## Structural archetype

Reproducibility audit: the verifier grades a *property of the build process* (independent paths converge bit-identically, repeatedly) rather than program behavior, plus a provenance artifact enumerating what previously diverged. No other portfolio idea grades process-determinism as the outcome.

## Novelty fingerprint

- Domain/system: an offline build pipeline — a code generator, compiler wrapper scripts, an archiver/linker stage, and a packaging step — with a shipped "golden" artifact and two build entry paths (developer script and release script).
- Failure mechanism: codegen iterates a pointer-keyed hash map so emitted symbol order varies per process (masked by a build cache that froze the first result); the archiver embeds mtime/uid unless an env flag is set that the docs claim defaults on but does not; a wrapper script's locale-sensitive sort orders linker inputs differently under the two entry paths.
- Distributed fix topology: generator ordering, archiver invocation/flag plumbing, and wrapper-script collation must all be fixed; any one alone leaves a diff class (symbol order, metadata bytes, or section order).
- Verifier/invariant surface: repeated rebuilds identical to each other; both entry paths identical to each other; behavior preserved against golden functional tests; provenance manifest correctly attributes the historical diff classes.

## Collision audit

Search every required scope: idea registry, active tasks, archived tasks, submission
archives, upstream corpus, and current external research.

- Closest analogue (preliminary): musl-sysroot-splice (IDEA-0006) shares the toolchain domain but is a staging-correctness task (build the right thing); this is process-determinism (build the same thing twice). Different mechanism, topology, and verifier surface. resolver-closure-drift (IDEA-0025) is dependency-resolution history archaeology, also distinct.
- Structural differentiator: the graded object is a fixed-point property of the pipeline itself, verified differentially; there is no "wrong output" to patch directly.
- Evidence paths and retrieval dates: local registry + active-task scan 2026-07-19 (no collision beyond the noted domain neighbors). Full six-scope audit TODO before uniqueness PASS.

## Why it is hard (five hardness axes)

- Discover: the solver must attribute each diff region to its source — symbol-order entropy in codegen, metadata embedding in the archiver, and locale collation in a wrapper — none of which is named anywhere and one of which is masked by a cache.
- Synthesize: byte diffs at the end of the pipeline must be traced backwards through packaging, linking, archiving, and generation; the causal map spans every stage.
- Diagnose: the symptom is a binary diff blob; the solver must invent the experiments (controlled rebuilds, cache disabling, stage-output bisection) that localize each divergence.
- Navigate coupling: fixing codegen ordering invalidates the build cache, which suddenly *exposes* the archiver metadata diff the cache had been hiding; the locale fix changes link order, which is only safe because behavior is re-verified — order matters and partial fixes look like regressions.
- Reason beyond training: generic reproducible-build lore (SOURCE_DATE_EPOCH exists) does not locate this repo's specific entropy sources; the misdocumented default and the cache masking defeat recipe application.

## Hidden discoveries (>= 3) and fix locations (>= 3)

1. The build cache replays the first codegen result, so nondeterminism only appears with the cache cold — rebuild diffs vanish "randomly," and the solver must discover the cache to get a faithful experiment.
2. The archiver's determinism env flag is documented as default-on in the build README but the wrapper never sets it — provable by inspecting archive member headers.
3. Linker input order differs between entry paths because one script sorts under a different locale — provable by diffing stage-wise file lists.
4. Fix locations: code generator emission order, archiver wrapper/flag plumbing, entry-script collation — three distinct pipeline stages.

## Long-horizon investigation profile (new ideas)

- Weakness areas (2-4, primary first): hidden environment/process state (primary); misleading documentation; tool selection.
- Causal chain (4-8 dependent stages): (1) reproduce the mismatch against the golden artifact; (2) discover rebuilds are self-identical only because of the cache, disable it for honest experiments; (3) bisect stage outputs to attribute the symbol-order diff to codegen; (4) fix emission ordering, re-diff, attribute residual metadata bytes to the archiver and falsify the README's default claim; (5) plumb the flag, re-diff, attribute section order to entry-path collation; (6) unify collation; (7) prove convergence: repeat builds, cross-path builds, behavior tests, and write the provenance manifest.
- Heterogeneous evidence surfaces (>= 3): binary artifact diffs, build logs, wrapper scripts and configuration, archive member metadata, documentation (as a falsifiable claim source).
- Competing hypotheses and deterministic falsifiers (>= 2): H1 "compiler itself is nondeterministic" — falsified by hashing per-TU compiler outputs across runs; H2 "golden artifact was built from different sources" — falsified once all three entropy sources are controlled and the rebuild converges to the golden bytes.
- Failing scenario and healthy control: full-pipeline rebuilds diverge; single-TU compile outputs are already stable and must remain byte-stable (guards against sledgehammer post-processing that rewrites artifacts instead of fixing the pipeline — behavior tests also pin the output's functional identity).
- Meaningful-action estimate (20-100, no busywork): ~40-70 (controlled rebuilds, cache discovery, stage bisection, three fixes, convergence proof).
- Determinism strategy: the *goal* is determinism; the harness provides fixed toolchain versions and virtual timestamps so the only entropy is the bugs themselves; offline, single container.
- Domain and why this is not trivia: tests supply-chain build engineering — designing controlled experiments over a multi-stage pipeline — not recall of one reproducibility flag.

## Symptoms-only instruction sketch

"Security cannot reproduce our shipped artifact: their rebuild differs from the release, and two of their own rebuilds differed from each other once. Make the build converge — any two builds from this tree, through either build path, must produce byte-identical output that still passes the functional suite — and produce a signed-off provenance manifest accounting for what used to differ."

## Decision notes

Captured 2026-07-19; fingerprinted same day. Step 2a watchpoints: the provenance manifest must require genuine attribution (schema checked against the actual historical diff classes) so it cannot be bluffed, and the cache-masking discovery must not collapse into "delete the cache directory" — the cache must be legitimate infrastructure the fixed pipeline keeps using.
