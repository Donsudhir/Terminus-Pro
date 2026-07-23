# Submission Output Template

Use only after final task approval. Generated rubric and explanation text is emitted in chat and must not enter the task source or submission archive.

## UI rubric

- Follow `TASK_PROPOSAL_RUBRIC.md`.
- Emit one copy-paste code block in chat.
- Base every criterion and score on the finished task and verified behavior.
- Do not include hidden implementation hints or unsupported claims.

## Explanations

Load `terminus-dsv-humanizer` and use its pinned, source-locked 33-pattern
workflow. Validate and capture all three fields together; partial DSV updates
are forbidden.

Acceptance lock: platform requirements and reviewer feedback first, finished
task truth second, TERMINUS project rules third, Humanizer style last. Change
wording and rhythm only. Never change obligation strength, technical meaning,
failure modes, solution facts, verifier properties, counts, or evidence claims.

### Difficulty Explanation

Start exactly with `This task is hard because` and write four or five sentences.

### Solution Explanation

Write four or five sentences explaining the real overall approach and central idea.

### Verification Explanation

Start exactly with `The tests checks` and write four or five sentences.

## Voice checklist

- Plain technical voice and simple English.
- Vary sentence length.
- Use one paragraph and 45–140 words per field.
- Preserve the required openers; do not manufacture other grammar mistakes.
- No em dash, en dash, semicolon, academic voice, buzzword, or polished transition phrase.
- Do not repeat the task description or repeat wording across sections.
- Avoid file names, function names, paths, and repository structure unless necessary.
- Never invent information beyond the completed solution and test evidence.
