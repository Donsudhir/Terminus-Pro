# ADR-0003: Recoverable Regression Baseline

- Status: Accepted
- Date: 2026-07-18
- Scope: Repository test fixtures and submission parity

## Context

The regression suite referenced four full historical task fixtures and one additional task that were never committed. They were absent from the working tree, reachable and unreachable Git objects, remote branches, home-directory backups, and same-named submission archives. The broad `tasks/` ignore rule also prevented nested fixture task directories from being tracked.

Keeping tests pointed at missing names produced dozens of errors and implied historical evidence existed when it did not. Fabricating those exact tasks from test expectations would create false provenance.

## Decision

Modernize the baseline around recoverable evidence:

1. Use an immutable snapshot of the complete `musl-sysroot-splice` task as `repo_tests/fixtures/tasks/harness-clean` for full-harness success, warning, checksum, metrics, and approval behavior.
2. Use focused synthetic fixtures for specific failure detectors such as shadow models, generated shadow executables, hardcoded digests, build-knob discoverability, and path discoverability.
3. Replace one-directory-per-archive parity with `repo_tests/fixtures/submission_index.json`, which pins each archive by zip hash, byte size, layout, task metadata hash, instruction hashes, member count, and validator result.
4. Generate or check the index with `scripts/build_submission_index.py`.
5. Keep `repo_tests/cases.py` as historical evidence, but route active regressions through `repo_tests/current_cases.py`.

## Consequences

- Tests no longer claim lost historical task trees are available.
- Current behavior is pinned by explicit, reviewable fixtures.
- Submission parity is stronger because it checks content hashes rather than directory-name presence.
- Adding or changing a submission zip requires an intentional index update.
- Historical expectations remain readable but are no longer executable evidence.
