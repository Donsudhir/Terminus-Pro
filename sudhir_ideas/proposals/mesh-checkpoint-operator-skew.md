# Task Idea Proposal — mesh-checkpoint-operator-skew

Generated: 2026-07-22T21:16:43Z
Platform check: PASSED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

A mixed-language scientific solver checkpoints mid-run, remeshes, then resumes. After resume, residual norms and iteration counts can look plausible, but solution-field digests and pointwise residuals disagree with a never-interrupted twin run on the same case. Fresh runs without checkpoint remain correct and must stay byte-stable. Bring interrupted and uninterrupted trajectories into agreement on field digests, residual contracts, and the healthy no-checkpoint control.

### Idea Category

Scientific Computing

Normalized local category: `scientific-computing`

### Associated Skills

finite-element or mesh-based solvers, checkpoint/restart semantics, operator reuse under geometry change, numerical residual diagnosis, mixed-language numerics, floating-point reduction discipline, deterministic scientific verification

### Task Tags

checkpoint-restart, mesh, operator-cache, scientific-computing, residuals

## Check feedback

Similarity PASS. Idea quality PASS (Decision: Accept; Verifiable: Accept; Well-specified: Uncertain; Solvable: Accept; Difficult: Accept; Interesting: Strong Accept; Outcome-verified: Accept). Category alignment FAIL (selected scientific; suggested debugging) — treated as non-blocking per author policy. Metadata similarity PASS.

## Inspiration provenance

- Source type: real DevOps/scientific incident pattern
- Source reference: checkpoint/restart after remesh operator-reuse failures (inspiration only; Terminal-Bench / HPC incident patterns 2026-07-23)
- Reuse boundary: Inspired by remesh+resume residual green / solution wrong failure shape; no upstream patch, issue prose, or benchmark tests copied.
