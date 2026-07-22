# ADR-0010: Common Mistakes Ledger and Prevention Checks

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Related: ADR-0001, ADR-0007

## Context

Two platform rejections in the same weekend shared a pattern: local oracle and
static gates looked green while Snorkel AutoEval or agent difficulty failed for
reasons the authoring chat did not re-check. The asciinema/`python3` symlink
trap (CM-001) and the RPSP instruction discoverability gap (CM-002) were each
fixable once diagnosed, but nothing forced the next chat to load those
lessons before packaging again.

The knowledge graph already has `FAILURE-*` nodes, yet agents do not reliably
read the whole graph at chat start. A short, checklist-shaped ledger is needed
as a mandatory start-of-chat and pre-upload surface, with mechanical enforcement
where the failure is detectable from task files alone.

## Decision

1. Maintain `sudhir_knowledge/COMMON_MISTAKES.md` as the human ledger of
   recurring authoring and platform failures. Entries are append-only; status
   moves from `active` to `prevented` when a check or ADR closes the hole.
2. Every task chat loads that ledger after `board` + `ingest` (lifecycle skill
   and `AGENTS.md`).
3. Before claiming package/approve or upload-ready, walk the ledger’s pre-upload
   checklist and record justified WARNs in the task’s Step 3b/4 review notes.
4. Encode CM-001 in `dockerfile_check.py` as `python_interpreter_hygiene` so
   repointing `/usr/bin/python3` onto the image Python while `asciinema` is
   installed is a FAIL, not a tribal memory.
5. New platform rejections that are not already in the ledger must add a CM row
   and a knowledge-graph FAILURE node in the same session that diagnoses them.

## Consequences

- Lessons survive chat boundaries without re-deriving them from screenshots.
- Some mistakes stay review-only (CM-002 style instruction honesty) because
  mechanical detection would either over-block symptoms-only prose or miss
  CR1 collisions; those stay `active` with an explicit checklist.
- The ledger never replaces evidence rules: PASS/READY still requires fresh
  command output.
