# VERIFICATION — musl-sysroot-splice REV-3

The tests checks the public rebuild path rather than string proxies. They replace knit_main and pack_main with failing stubs so the entrypoint must call those helpers for real. They require the public stage to match live helper outputs bit for bit, including headers and CRT digests plus pack response files. They also prove the final ELF is fully static musl with no interpreter, and qemu-user plus ledger checks still enforce the release contract.
