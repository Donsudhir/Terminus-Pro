# RUBRIC — musl-sysroot-splice REV-2

Agent produces /app/output/payload as a fully static musl ELF by repairing the knit/pack/seal assembly helpers and rebuilding through /app/tools/build_payload.sh, +5
Agent stages coherent musl inputs (alpha overlay headers with bravo CRT, bravo -L/-lc search, -static seal flags) so the public stage matches live helper outputs, +5
Agent emits /app/output/probe_report.json from live probe stdout and the payload digest with settlement true and marker/thread/errno rows all ok, +3
Agent clears qemu-user contract lines MARKER=CXR-7F, THREAD=7, ERRNO=2, and LANE_TAG=BRAVO on the rebuilt payload, +3
Agent keeps the public entrypoint wired to the assembly helpers rather than skipping knit/pack/seal or planting a foreign static binary, +2
Agent leaves packaged musl-gcc wrappers unavailable and does not rely on a shortcut compiler path, +1
Agent plants a static glibc binary, hand-writes the ledger, or otherwise bypasses staged musl helper integration while claiming a pass, -5
Agent edits verifier tests, shadows pytest, or forces reward without a correct assembly, -5
Agent leaves a PT_INTERP on the payload or links from the wrong vendor mix so probes/settlement fail, -3
Agent rewrites only comments/string mentions of helpers without executing the knit/pack/seal pipeline, -2
