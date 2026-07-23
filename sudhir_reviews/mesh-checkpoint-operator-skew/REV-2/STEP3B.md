# STEP3B — mesh-checkpoint-operator-skew — REV-2

Date: 2026-07-23
Checksum rewritten by post-edit preflight; oracle/NOP/10x reconfirmed.

## Edit ledger

- **Preservation-safe:** `tests/test_outputs.py` — removed unused local `buf` in `_f64_le_bytes` (platform Fast Static `ruff` F841 hard FAIL). Behavior unchanged: still returns `array("d", [float(value)]).tobytes()`.
- **Preservation-safe:** `environment/requirements.txt` — byte-identical alias of `verifier-requirements.txt` so the platform lockfile probe finds `requirements.txt` with `--require-hashes` / `--hash=sha256:` (Dockerfile still installs from `verifier-requirements.txt`).
- No instruction, oracle, decoy, schema, or Dockerfile toolchain edits. Single-stage Dockerfile retained (agent must rebuild at runtime; platform carve-out WARN).

## §1–7 review-and-submit

Unchanged from REV-1 except verifier hygiene (unused local removed). Residual hardness and contracts unchanged.

## Collapse WARN justifications

Same as REV-1: RC2, CR1, GX3, GX7 — still 0 FAIL / WARN-only; no padding.

## Post-edit Step 2b / Step 4 evidence

- Preflight A/B/C: PASS
- Oracle 1x: **1.0** — `jobs/2026-07-23__03-30-47`
- NOP: **0.0** — `jobs/2026-07-23__03-31-28`
- Oracle 10x: **10/10 @ 1.0** — `jobs/2026-07-23__03-32-02`
- Post-10x NOP: **0.0** — `jobs/2026-07-23__03-33-12`

## Decision

Fast Static blocker fixed. Ready for re-package and re-upload.
