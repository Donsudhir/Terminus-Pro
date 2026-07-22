# ADR-0005: Normalize Repository Text to LF

- Status: Accepted
- Date: 2026-07-18
- Scope: Text files in the Gold repository

## Context

Several tracked files use CRLF endings. Git interpreted the carriage return as trailing whitespace on modified lines, making whitespace checks noisy even though Ruff and Python handled the files correctly.

## Decision

Track a `.gitattributes` policy that treats Python, shell, Markdown, MDC, TOML, JSON, text, and `.gitignore` files as text with LF checkout and staging normalization. The whitespace policy keeps real end-of-line, end-of-file, and space-before-tab checks while recognizing a carriage return as part of an existing CRLF ending during migration.

## Consequences

- `git diff --check` passes without hiding real trailing spaces.
- Existing CRLF files will be normalized to LF the next time Git stages or otherwise rewrites them.
- Binary archives are unaffected.
