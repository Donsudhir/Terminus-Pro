# ADR-0020: Official CI Parity and Explicit Delegation

- Status: Accepted
- Date: 2026-07-21
- Task ID: Repository-wide
- Related: ADR-0010, ADR-0016, ADR-0019, CM-020

## Context

The July documentation audit found that local approval could pass tasks that
current upstream CI would block. Missing coverage included sanctioned final
images, build-context limits, ecosystem dependency locks, unsafe capabilities,
offline verifier setup, archive cleanup, layer volatility, and runtime build
tools. Two official checks, `typos` and `check_task_sizes`, do not have enough
published deterministic detail for a trustworthy local reimplementation.

ADR-0016 requires every official requirement to have an explicit ownership and
coverage disposition, and requires new semantic checks to be shadowed before
activation.

## Decision

1. `ci_policy.py` stores reviewed CI facts, the exact sanctioned final-image
   set, size limits, unsafe capability names, and one coverage disposition for
   every current official check.
2. Coverage dispositions are limited to locally enforced, delegated upstream,
   mandatory human review, intentional house override, or not applicable with
   rationale.
3. Blocking local checks now enforce:
   - final sanctioned image or ADR-reviewed policy exemption;
   - 100 MiB total / 50 MiB per-file build context and no escaping symlinks;
   - dependency pins/locks for pip, npm, Cargo, Go, Maven, and Gradle;
   - checksum-pinned direct downloads and commit-pinned Git clones;
   - unsafe capabilities, privileged mode, Docker socket, and all reserved
     mounts including `/oracle`;
   - existing digest, manifest, test shell, task-field, absolute-path, and Ruff
     controls.
4. Warning checks now cover offline verifier setup, Docker layer volatility,
   unnecessary final-runtime build tools, and archive extraction/removal in one
   stage. A local preloaded-wheel install using `--no-index` and local
   `--find-links` is explicitly allowed.
5. `dockerfile_check.py` is consumed by the authoritative `approve_task.py`
   gate. Docker FAIL blocks approval; Docker WARN is visible but does not claim
   an upstream block.
6. `typos` and `check_task_sizes` remain `delegated-upstream`. Approval output
   names them as pending upstream checks, and requirements guidance requires
   their current platform result before submission. Local code must never
   fabricate PASS for them.
7. The human-readable coverage matrix lives at
   `sudhir_research/OFFICIAL-CI-COVERAGE-2026-07-21.md` and is regression-tested
   against the executable check registry.

## Shadow evidence

All six active tasks, spanning Python, Rust, GCC/C++, Go, C, and Fortran-facing
stacks, had zero new blocking or warning deltas from the added families. Existing
musl warnings were pre-existing and unrelated. Positive, negative, warning, and
false-positive fixtures cover each new deterministic family.

## Rollback

Demote the changed family to report-only, remove it from approval blocking, and
restore the previous checker result list. Keep the coverage disposition and
captured shadow evidence; do not delete policy history or reinterpret delegated
checks as locally passed.

## Consequences

- The initial compatibility rollout is complete and net-new task construction
  may resume under the proposal, eligibility, uniqueness, and Step 2a gates.
- Local approval is materially closer to current platform CI while remaining
  honest about the two delegated checks.
- Future official check changes still require source review, fixtures, shadow,
  adjudication, and rollback evidence before promotion.
