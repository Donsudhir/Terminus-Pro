# ADR-0004: Locked Toolchain and Configurable Roots

- Status: Accepted
- Date: 2026-07-18
- Scope: Harness environment and Sudhir workspace compatibility

## Context

The repository previously had no local virtual environment contract, lock file, or project metadata. The setup manifest referenced a missing requirements file and versions that did not match the host. Core paths were also hardcoded to upstream `specs`, `jobs`, and submission locations.

## Decision

- Standardize the harness on Python 3.12 through `.python-version` and `pyproject.toml`.
- Use `uv.lock` and `uv sync --frozen` as the dependency source of truth.
- Pin pytest 8.4.1, pytest-json-ctrf 0.3.5, PyYAML 6.0.3, Ruff 0.15.12, and jsonschema 4.26.0.
- Keep external Harbor and Docker versions recorded as observed host tools rather than Python lock dependencies.
- Support `TB3_TASKS_DIR`, `TB3_SPECS_DIR`, `TB3_VALIDATION_SCHEMA`, `TB3_SUBMISSIONS_DIR`, `TB3_REVIEWS_DIR`, and `TB3_JOBS_DIR`.
- Source `scripts/sudhir-env.sh` for the canonical Sudhir workspace while preserving upstream defaults when those variables are absent.

## Consequences

- Harness tests and lint no longer depend on Conda base packages.
- Existing upstream commands continue to work by default.
- Sudhir task sources and final archives use canonical personal paths without duplicate mutable copies.
- Environment changes are reproducible and reviewable through the lock file.
