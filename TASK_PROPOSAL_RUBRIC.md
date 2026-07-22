### Rubric Authoring Guidelines (for editing in the UI)

**Canonical line shape (paste exactly this shape into Snorkel):**

```text
Agent <trace-visible behavior>, +5
Agent <another behavior>, +2
Agent <undesirable behavior>, -5
```

Wrong (rejected on ERS 2026-07-19 / CM-015):

```text
- +2 Recovery via vaultctl …
- -2 Tampering with tests …
```

Rules:
- Every line starts with "Agent" and ends with ", [Score]"
- Only use +1, +2, +3, +5, -1, -2, -3, -5 (NEVER use +4, -4)
- Every check must be **binary** (yes/no evaluation from the trace)
- Include at least **5 checks** per task
- Rubrics must **map to the optimal sequence of steps** to solve the task
- **No double-counting**: one behavior → one check (unless clearly distinct aspects)
- **No perfect scores**: Rubrics should rarely yield a perfect score unless the trace is exceptionally clean
- Include significant negative penalties for unsafe/redundant behavior
- Focus on **trace-evidenced actions** only — if you can't see it in the trace, you can't grade it
- No standard pytest checks (unless the task IS a testing task)
- No meta-checks (reading task.yaml/instructions.md — these are passed automatically)
- Importance: Critical (±5), Major (±3), Minor (±1 to ±2) — do not flatten everything to ±1/±2 on a multi-bug task
- Positive phrasing always — use negative points for undesirable behaviors, not negative wording
- Don't refer oracle/NOP runs, approval flow, zip validation, or flakiness checks; only refer agent task-solving behavior
- Have at least 3 negative rubrics
- Keep total rubrics maximum cumulative score (calculated by summing all positive criteria) between 10-40
- Rubric points per milestone (milestone tasks only): each milestone gets 10–40 max cumulative points (sum of positive criteria); total for N milestones falls between N×10 and N×40 (e.g., 1→10–40, 2→20–80, 3→30–120)
- Store the paste in `sudhir_reviews/<slug>/REV-<n>/RUBRIC.md` before upload; never ship `rubric*.txt` inside the task zip
