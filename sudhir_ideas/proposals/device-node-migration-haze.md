# Task Idea Proposal — device-node-migration-haze

Generated: 2026-07-22T21:16:44Z
Platform check: PASSED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

A host migration tool copies a service root between staging trees and reports success from file counts and exit codes. After cutover, device-backed services fail to open required nodes, lose expected major/minor identity, or bind the wrong path, while ordinary file bytes look intact. A non-device healthy control tree still migrates cleanly. Make device nodes, permissions, and service open paths match the pre-migration contract, keep the file-only control green, and leave deliberately broken device fixtures rejected.

### Idea Category

System / Environment Setup & Configuration

Normalized local category: `system-administration`

### Associated Skills

Unix device nodes, mknod and permissions, rootfs migration, bind-mount diagnosis, service startup debugging, filesystem metadata fidelity, systems programming in C or Rust, offline deterministic fixtures

### Task Tags

device-nodes, rootfs-migration, permissions, linux, service-restore

## Check feedback

Similarity PASS. Idea quality PASS (Decision: Accept; Verifiable: Accept; Well-specified: Uncertain; Solvable: Accept; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (selected sys_env_setup; suggested debugging) — non-blocking. Metadata similarity PASS.

## Inspiration provenance

- Source type: Unix programming / DevOps incident
- Source reference: device-node and rootfs migration fidelity incidents (inspiration only; 2026-07-23)
- Reuse boundary: Inspired by count-green migration that loses device identity; no upstream scripts or tests copied.
