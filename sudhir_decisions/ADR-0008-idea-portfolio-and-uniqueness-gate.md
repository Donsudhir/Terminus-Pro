# ADR-0008: Idea Portfolio and Super-Uniqueness Gate

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Related: ADR-0001 (single source), ADR-0007 (pipeline registry and board)

## Context

The task registry tracked execution phases but the idea bank was a manual list. It did not clearly answer whether an idea had passed uniqueness research, been approved for execution, actually been built, uploaded, or explicitly accepted. Reserved alternatives were unstructured strings, historical tasks had no honest provenance marker, and repeated import of unchanged root-level platform exports added duplicate notes. This made idea status easy to misread and allowed an evaluation success signal to look like final acceptance.

The user requires every idea to stay documented from capture through execution and platform decision, with unusually strong novelty rather than renamed versions of saturated task families.

## Decision

1. Upgrade `sudhir_progress/registry.json` to schema version 2. It remains the only mutable source of truth and now contains separate `ideas` and `tasks` maps.
2. Every idea receives a permanent `IDEA-NNNN` ID, an append-only history, a record path, an idea-gate status, a Step 2a verdict, and a structured uniqueness dossier. Rejected slugs are never reused.
3. Render both `sudhir_progress/BOARD.md` and `sudhir_ideas/IDEA_INDEX.md` from the registry. Never edit status in either Markdown view.
4. Keep five questions separate on every portfolio row:
   - Is the idea approved?
   - Is uniqueness proven?
   - Was it executed?
   - Was it submitted?
   - What did the platform explicitly decide?
5. `EVALUATION PASSED` is not `ACCEPTED`. Only direct reviewer/platform evidence may set `accepted` or `rejected` through the outcome command.
6. A non-legacy idea cannot enter construction until it has:
   - a fingerprint covering domain, failure mechanism, distributed fix topology, and verifier/invariant surface;
   - searches across the idea registry, active tasks, archived tasks, submission archives, upstream corpus, and current external research;
   - a nearest-analogue comparison and structural differentiator;
   - collision-audit evidence paths;
   - a recorded Step 2a GO and evidence path.
7. Historical tasks are backfilled as `legacy` when no trustworthy original uniqueness dossier exists. Do not invent retrospective proof to make the board look complete.
8. Platform export ingestion is idempotent by submission identity and source hash, so unchanged exports do not append duplicate history.
9. CLI transactions hold a repository-specific process lock and replace the registry atomically, preventing concurrent agent sessions from silently losing one another's updates.

## Consequences

- Idea approval, execution, upload, and acceptance can no longer be conflated.
- Reserved and rejected ideas remain visible, preventing accidental reuse and repeated exploration of known collisions.
- The construction gate is mechanically blocked when novelty or Step 2a evidence is incomplete.
- A `legacy` warning is intentionally visible until genuine historical evidence is found; warnings are preferable to fabricated certainty.
- Agents must update the registry at each real transition and regenerate both views before ending a session.
