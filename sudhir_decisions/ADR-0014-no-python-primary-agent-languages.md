# ADR-0014: No Python-Primary Agent Languages

- Status: Accepted
- Date: 2026-07-19
- Task ID: Repository-wide
- Related: ADR-0001, ADR-0010, CM-011

## Context

Frontier models are already strong on Python. Sudhir’s TERMINUS work is meant
to stress niche, difficult, less-common languages and multi-language scientific
pipelines. After repeated EASY difficulty rejections on SJCC (`d9082cd8`),
Sudhir directed that new projects must not be built as Python-primary agent
work.

Verifier harnesses commonly use pytest; that is not the same as asking the
agent to solve a Python application.

## Decision

1. **New tasks:** do not use Python as an agent-facing / fix-path language.
   Prefer genuinely necessary niche stacks (e.g. C, C++, Rust, Fortran, Zig,
   Ada, Haskell, OCaml, or other low-prevalence systems languages) with at
   least two cooperating authorities when the topology needs them.
2. **Allowed Python:** Dockerfile/tooling glue and verifier-only pytest under
   `tests/` remain allowed. Do not put the solvable core under
   `environment/**/*.py` or teach the oracle as a Python rewrite.
3. **Ideas:** Step 2a REJECT (or redesign) any concept whose natural
   implementation is a Python script/service unless Sudhir explicitly waives
   this ADR for that idea.
4. **In-flight tasks** already mid-revision (e.g. SJCC Rust/C/Fortran) keep
   their language topology; do not rewrite them to Python, and do not add new
   Python fix surfaces.

## Consequences

- Idea validation and task creation must check language choice before GO.
- Snorkel “Language” form dropdown should reflect the agent-facing languages,
  not “Python” merely because the verifier uses pytest.
- CM-011 tracks violations and start-of-chat recall.
