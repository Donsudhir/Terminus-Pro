# ADR-0017: UI House Block and Python Playwright Compatibility

- Status: Accepted
- Date: 2026-07-21
- Task ID: Repository-wide
- Related: ADR-0010, ADR-0016, CM-020, CM-022

## Context

Current Terminus EC subtype guidance still recognizes `ui_building`, but it
requires UI verification to remain Python pytest. Browser automation must use
Playwright's Python bindings rather than a JavaScript or TypeScript Playwright
suite.

This repository independently blocks net-new UI tasks as a house policy. The
local checker and `skeleton/UI_Task_Skeleton/` nevertheless encoded a retired
Vitest plus TypeScript Playwright generation. No active canonical task, current
submission ZIP, or historical submission ZIP uses `ui_building`, so preserving
that scaffold creates future risk without protecting current work.

ADR-0016 requires official and house policy to remain distinct and requires
source-backed exemptions for work already in platform review or revision. It
also forbids silently rewriting task source or historical evidence during a
policy migration.

## Decision

1. `ui_building` remains a recognized official subtype. Its presence is not
   represented as an official platform block.
2. Net-new `ui_building` work is blocked by the repository's **house**
   eligibility profile before uniqueness PASS, Step 2a GO, task registration,
   packaging, or submission.
3. A UI task already in platform review or revision may continue only with the
   same source-backed exemption evidence required by ADR-0016. A bare boolean
   or local claim is insufficient.
4. An exempt in-flight UI revision must use standard Python pytest verification
   plus Playwright's Python bindings. It uses `tests/test_outputs.py`, the
   standard offline `tests/test.sh`, CM-007 safe-path hardening, the semantic
   binary reward footer, pinned Python Playwright dependencies, and browser
   installation at image-build time.
5. Verifier-side `package.json`, Vitest configuration, JavaScript/TypeScript
   Playwright configuration, JS/TS verifier specs, npm test runners, and the
   separate UI reward footer are obsolete and fail local compatibility checks.
   Application code under `environment/` may still use JavaScript or
   TypeScript.
6. The retired UI scaffold is deleted rather than moved or maintained. Git
   history preserves it. No replacement UI scaffold is provided because new
   starts are house-blocked.
7. No active task source, submission archive, exemption, checksum, or platform
   outcome is automatically modified by this decision.

## Consequences

- Official and house verdicts can differ: a net-new UI record is officially
  eligible but house-blocked.
- An evidence-backed UI revision can be structurally compatible without
  reopening net-new UI authoring.
- Standard and milestone task verdicts remain unchanged.
- Any future decision to permit net-new UI work requires a new ADR, a supported
  scaffold, shadow evidence, and explicit eligibility-profile promotion.

## Rollback

Demote the UI compatibility checks to report-only and restore the prior house
profile through a superseding ADR. Do not restore the JavaScript/Vitest
scaffold as a validity requirement. Preserve all evidence, historical archives,
and recorded exemptions.
