# REV-8 reviewer feedback — sparse-jacobian-color-contract

Thank you for the well-designed scientific-computing task and its strong numerical coverage. Before acceptance, please document the exact FNV-1a digest algorithm or relax the verifier to accept the documented digest contract, replace the verifier requirements with a complete pinned and hash-locked dependency set, and add tests for schema_version plus changed runtime.conf step settings so the configuration requirement is verified rather than only the defaults.

Source: stb submissions feedback d9082cd8-c0ad-4174-a34f-4731f0b63907 (2026-07-22).
Agent-run analysis (instruction sufficiency): digest payload "all bytes before the digest field" is ambiguous about whether the outer closing "}" is hashed; near-miss agent broke working closed-object hashing. Patch: make closing-brace inclusion explicit; keep working FNV-1a contract.
