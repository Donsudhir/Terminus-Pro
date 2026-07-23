# Task Idea Proposal — aead-epoch-bound-drift

Generated: 2026-07-22T21:16:45Z
Platform check: FAILED
Evidence: chat-2026-07-23 Snorkel Task Idea Proposal Check feedback pasted by Sudhir

## Paste-ready fields

### Task Idea Summary

A local sealed-object store rewraps records across key epochs and verifies tags before open. After a routine epoch advance, some historical records open with the wrong binding, some valid records fail verification, and a shallow tag-valid counter stays mostly green. Freshly written current-epoch records must keep working, and deliberately corrupted controls must stay rejected. Restore open/rewrap behavior so epoch lineage, associated data binding, and reject/accept controls all agree.

### Idea Category

Security / Cryptography / Vulnerability Demonstration

Normalized local category: `security`

### Associated Skills

AEAD cryptography, key epoch rotation, associated-data binding, sealed storage design, cryptographic protocol debugging, systems programming in C/Rust/Go, fail-closed verification

### Task Tags

aead, key-rotation, associated-data, sealed-storage, cryptography

## Check feedback

Similarity PASS. Idea quality FAIL (Decision: Reject; Verifiable: Accept; Well-specified: Reject; Solvable: Uncertain; Difficult: Accept; Interesting: Accept; Outcome-verified: Accept). Category alignment FAIL (suggested debugging). Metadata similarity PASS.

## Inspiration provenance

- Source type: cryptography / sealed-storage incident pattern
- Source reference: AEAD epoch AAD binding drift (inspiration only; 2026-07-23)
- Reuse boundary: Platform Idea quality Reject; retained as failed so family is not silently recycled.
