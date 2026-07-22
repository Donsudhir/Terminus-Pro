# Resolver architecture

`forge solve PROJECT` reads a project file with `profile`, `catalog`, `roots`,
`apis`, and `seed` fields. Root constraints use
`name:low-code:high-code:channel:exact-code`; channel is `stable` or
`preview`, and a dash means no exact code.

Catalog rows are validated against the request and admitted under the active
profile before the dependency walk commits a closure. The lock writer
serializes only that committed closure; it does not receive raw catalog rows
or policy frames.

After writing the lock, the build stage creates a fresh Cargo consumer with
path dependencies to every selected payload and runs Cargo offline with a
generated lock. Diagnostic sampling uses a parallel path and writes a compact
resolve log.
