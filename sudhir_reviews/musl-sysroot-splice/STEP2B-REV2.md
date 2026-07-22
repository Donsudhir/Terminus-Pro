# Step 2b — musl-sysroot-splice REV-2

Preflight: `./scripts/check-task.sh tasks/musl-sysroot-splice` — PASS (collapse/dockerfile WARN only; CM-007 present).

- Oracle 1x: `jobs/2026-07-19__14-50-19` mean **1.0**
- NOP: `jobs/2026-07-19__14-50-58` mean **0.0**

Verifier revision addresses CM-006 (behavioral musl + live knit/pack/seal).
