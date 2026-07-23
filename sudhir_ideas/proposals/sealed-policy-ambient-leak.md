# Task Idea Proposal — sealed-policy-ambient-leak

Generated: 2026-07-22T21:16:45Z
Platform check: FAILED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

An offline privilege helper applies a sealed local policy, drops privileges, then performs sealed-path file operations for callers. After a policy reload and session restore, some callers still succeed on paths the sealed policy should deny, while others are denied incorrectly even though the policy text looks current. Surface health checks only count allow/deny totals and stay green. Make sealed-path enforcement and restored sessions agree so denied and allowed controls match the intended policy outcomes without weakening healthy allow cases.

### Idea Category

Security / Cryptography / Vulnerability Demonstration

Normalized local category: `security`

### Associated Skills

Linux capabilities, privilege dropping, policy reload semantics, ambient authority analysis, setuid helper hardening, path confinement, systems programming in C or Rust, adversarial scenario testing

### Task Tags

capabilities, policy-reload, path-confinement, privilege-drop, security

## Check feedback

Similarity PASS. Idea quality FAIL (Decision: Reject; Verifiable: Uncertain; Well-specified: Reject; Solvable: Uncertain; Difficult: Accept; Interesting: Reject; Outcome-verified: Uncertain). Category alignment FAIL (suggested debugging). Metadata similarity PASS.

## Inspiration provenance

- Source type: security / capability incident pattern
- Source reference: sealed policy ambient authority after reload (inspiration only; 2026-07-23)
- Reuse boundary: Platform Idea quality Reject; retained as failed so family is not silently recycled.
