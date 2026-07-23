# ADR-0023: Pre-proposal conflict screen for clones

- Status: Accepted
- Date: 2026-07-23
- Task ID: Repository-wide
- Supersedes: None
- Related: ADR-0008, ADR-0011, ADR-0018, ADR-0019

## Context

ADR-0018 correctly makes the four-field platform proposal check the first formal
lifecycle gate and blocks full uniqueness research until proposal PASS. A clone
of Terminus-Pro, however, already contains active, rejected, retired, legacy,
and quarantined ideas plus task and archive history. Immediately drafting a
platform proposal without first reading that local collision corpus can waste a
proposal check, duplicate another owner's work, or disguise the same mechanism,
topology, and verifier through new language and domain names.

The lifecycle already supports quarantining foreign work while retaining its
fingerprint and reserved slug. A clone can create an additional risk if it
resets the active registry and thereby forgets the source repository's
fingerprints.

## Decision

1. Every selected candidate receives a lightweight **pre-proposal conflict
   screen** before the four platform fields are produced.
2. The screen checks ownership and obvious collisions across active, rejected,
   retired, legacy, and quarantined ideas/tasks, local archives, and any
   clone-origin collision snapshot.
3. The primary comparison axes are domain/system, failure mechanism,
   distributed fix topology, and verifier/invariant surface. Language, fixture,
   size, and noun changes are secondary and cannot establish novelty by
   themselves.
4. Same mechanism + topology + verification is a blocking collision even when
   domain or languages differ. Rejected, retired, and quarantined status does
   not release a fingerprint or slug for reuse.
5. The screen records the nearest analogue, an exact structural-difference
   sentence, source ownership, and a no-copy reuse boundary. It returns only:
   `PROCEED TO PROPOSAL`, `REWORK BEFORE PROPOSAL`, `DROP AS COLLISION`, or
   `HOLD: OWNERSHIP/SOURCE UNCLEAR`.
6. The screen is not formal uniqueness research, does not search or adjudicate
   all six uniqueness scopes, and can never record uniqueness PASS, Step 2a GO,
   difficulty, solvability, eligibility, or acceptance.
7. After `PROCEED TO PROPOSAL`, ADR-0018 remains unchanged: output only Task Idea
   Summary, Idea Category, Associated Skills, and Task Tags, then stop for
   platform Check feedback.
8. Only proposal PASS may begin the complete six-scope uniqueness dossier. For
   an independent fork, the Terminus-Pro source registry/collision snapshot is
   mandatory evidence under `upstream-corpus`.
9. A framework-only distribution may start with an empty active registry only
   after preserving a sanitized, read-only clone-origin collision corpus and
   making it a required uniqueness input.
10. The canonical screen template is
    `sudhir_templates/PREPROPOSAL_CONFLICT_SCREEN_TEMPLATE.md`; clone onboarding
    is `docs/CLONER-START-HERE.md`.

## Consequences

- Obvious local or ownership conflicts are rejected before consuming a platform
  proposal check.
- The proposal-first lifecycle remains intact because the screen is a local
  veto, not a uniqueness verdict.
- Cloners gain a low-effort operating path without treating Sudhir's portfolio
  as their own or erasing its collision value.
- Formal uniqueness still requires the exact six scopes and evidence after
  proposal PASS.
- Creative structural judgment remains human-reviewed; lexical similarity and
  schema completeness cannot prove novelty.
