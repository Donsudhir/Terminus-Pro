# SOLUTION — musl-sysroot-splice REV-1

The approach is to repair the assembly stages so they splice a coherent static musl toolchain instead of a hybrid that only looks right. Preferred headers and CRT from one consistent pairing, then point the link search at the archives that actually match that ABI. Drop the dynamic linker path and keep the build fully static. After the binary runs clean under qemu-user, rebuild the ledger from those live probe lines and the payload digest. Dont hand-write the artifact. The public entrypoint has to emit both outputs.
