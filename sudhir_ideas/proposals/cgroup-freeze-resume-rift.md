# Task Idea Proposal — cgroup-freeze-resume-rift

Generated: 2026-07-22T21:16:45Z
Platform check: FAILED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

A single-host process supervisor freezes worker trees before maintenance and thaws them afterward. After thaw, status tools report running counts and healthy cgroup membership, but long-lived workers lose held locks, reopen sockets on the wrong path, and fail the next checkpoint. Nearby healthy control jobs that never freeze still complete. Restore the freeze/thaw path so frozen workers resume with the same observable runtime contract as the never-frozen controls, including lock ownership, socket endpoints, and checkpoint success.

### Idea Category

System / Environment Setup & Configuration

Normalized local category: `system-administration`

### Associated Skills

Linux cgroups, process lifecycle management, file-descriptor inheritance, lock and socket state diagnosis, checkpoint/resume debugging, namespace and mount inspection, systems programming in C or Rust, deterministic offline reproduction

### Task Tags

cgroups, freeze-thaw, process-resume, linux, checkpointing

## Check feedback

Similarity PASS. Idea quality PASS but Decision: Uncertain (Verifiable: Uncertain; Well-specified: Reject; Solvable: Uncertain; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (suggested debugging). Metadata similarity PASS. Parked as failed/uncertain — not advancing without rewrite.

## Inspiration provenance

- Source type: Linux systems incident pattern
- Source reference: cgroup freeze/thaw resume lock/socket loss (inspiration only; 2026-07-23)
- Reuse boundary: Proposal Decision Uncertain + Well-specified Reject; retained as failed so slug/family is not recycled.
