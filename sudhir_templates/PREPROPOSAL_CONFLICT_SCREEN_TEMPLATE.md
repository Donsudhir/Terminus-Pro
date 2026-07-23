# Pre-Proposal Conflict Screen — <candidate-slug>

> **SCREEN ONLY — NOT A UNIQUENESS PASS.**
>
> Complete this before producing the four Task Idea Proposal fields. Formal
> six-scope uniqueness research happens only after the platform proposal check
> passes.

- Screened by: <owner/reviewer>
- Date: <YYYY-MM-DD>
- Clone source: <repository>@<commit>
- Candidate owner: <person/team>
- Decision: <PROCEED TO PROPOSAL | REWORK BEFORE PROPOSAL | DROP AS COLLISION | HOLD: OWNERSHIP/SOURCE UNCLEAR>

## 1. Candidate in one paragraph

<Describe the realistic existing system, observable failure, and intended
outcome without giving the fix.>

## 2. Inspiration and ownership

- Source type: <original | issue | paper | release note | incident | discussion | other>
- Source reference: <URL/title/path>
- Source owner/license: <known facts or unresolved>
- What inspired the candidate: <abstract pattern only>
- What will not be copied: <issue text, patch, tests, fixtures, answer, benchmark instance, etc.>
- Ownership concern: <none | explain>

## 3. Exact collision checks

| Source | Search performed | Match found | Evidence/reference |
| --- | --- | --- | --- |
| Active idea registry | <terms/slugs> | <yes/no> | <record/path> |
| Rejected/retired ideas | <terms/slugs> | <yes/no> | <record/path> |
| Quarantined/foreign ideas | <terms/slugs> | <yes/no> | <record/path> |
| Active tasks | <terms/slugs> | <yes/no> | <task/path> |
| Archived tasks | <terms/slugs> | <yes/no> | <task/path> |
| Submission archives/index | <terms/slugs> | <yes/no> | <archive/index> |
| Clone-origin collision snapshot | <terms/slugs> | <yes/no> | <snapshot/path> |
| Obvious external/source collision | <terms/source> | <yes/no> | <URL/note> |

## 4. Structural fingerprint

| Axis | Candidate | Nearest analogue | Same, related, or different? | Concrete evidence |
| --- | --- | --- | --- | --- |
| Domain/system | <...> | <...> | <same/related/different> | <...> |
| Failure mechanism | <...> | <...> | <same/related/different> | <...> |
| Distributed fix topology | <...> | <...> | <same/related/different> | <...> |
| Verifier/invariant surface | <...> | <...> | <same/related/different> | <...> |
| Language/runtime shape | <...> | <...> | <same/related/different> | <...> |
| Causal investigation shape | <...> | <...> | <same/related/different> | <...> |

## 5. Nearest analogue

- Analogue slug/title: <...>
- Status: <active | submitted | rejected | retired | legacy | quarantined | external>
- Why it is the nearest: <technical explanation>

Complete this sentence:

> Unlike <nearest analogue>, which grades <old verifier object> through <old
> topology/mechanism>, this candidate requires <new causal discoveries> across
> <new independent authorities> and is verified by <new invariant>.

## 6. Oracle/test reuse challenge

Answer each with evidence.

- Could the old oracle be adapted mainly by renaming paths/symbols? <yes/no + why>
- Could the old tests be reused with fixture substitutions? <yes/no + why>
- Is the new domain only a wrapper around the old graded invariant? <yes/no + why>
- Does one old function/configuration still control success? <yes/no + why>
- Is difficulty coming from file volume or obscurity? <yes/no + why>
- Would the task train the same agent failure with the same repair path? <yes/no + why>

Any unexplained `yes` blocks proposal.

## 7. Basic policy screen

This is not the final eligibility verdict.

- Proposed platform category: <exact display label>
- Local normalized category: <slug>
- Proposed agent-facing languages: <non-Python-primary stack>
- Milestone task: <yes/no>
- UI-building task: <yes/no>
- Multi-container task: <yes/no>
- Known current policy block: <none | explain>
- In-flight exemption required: <no | evidence needed>

## 8. Decision rationale

### If PROCEED TO PROPOSAL

<Explain why no obvious local/source collision exists and why the structural
difference is strong enough to justify asking the platform proposal check. Do
not call the idea unique yet.>

### If REWORK

<Name the exact axes that must change. “Make it harder” is not sufficient.>

### If DROP

<Name the collision and reserve the candidate slug/source so it is not recycled.>

### If HOLD

<Name the ownership, source, policy, or evidence question that must be resolved.>

## 9. Reviewer sign-off

- Reviewer: <name>
- Decision confirmed: <yes/no>
- Nearest analogue confirmed: <yes/no>
- Structural-difference sentence is concrete: <yes/no>
- Proposal fields may now be produced: <yes/no>

## 10. Formal next step

If and only if the decision is `PROCEED TO PROPOSAL`:

1. produce only Task Idea Summary, Idea Category, Associated Skills, and Task Tags;
2. stop for platform Check feedback;
3. capture PASS/FAIL and provenance;
4. after PASS, complete the full six-scope uniqueness dossier;
5. never use this screen as uniqueness evidence by itself.
