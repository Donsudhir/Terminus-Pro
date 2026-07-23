# SOLUTION — musl-sysroot-splice REV-3

Repair the assembly helpers so they splice one coherent static musl toolchain instead of a hybrid that only looks right. Prefer matching headers with the matching CRT objects, then point link search at the archives that match that ABI. Keep the link fully static and drop the dynamic interpreter path. After qemu-user clears the contract probes, rebuild the ledger from those live lines and the payload digest through the public entrypoint.
