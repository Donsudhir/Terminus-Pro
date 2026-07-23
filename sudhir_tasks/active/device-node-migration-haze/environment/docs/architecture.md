# Architecture

The cutover lab stages a service root from a source tree into a destination
staging tree, then probes whether post-cutover opens and identities still match
the pre-cutover contract.

Major subsystems:

- `loom/` — C rematerialization helpers (selected + decoy)
- `veil/` — Rust roster fidelity helpers (selected + decoy)
- `tether/` — Rust open-path rebinding helpers (selected + decoy)
- `crate/` — orchestration, report emission, and thin pass wrappers
- `probe/` — deterministic open/identity helpers used by the pipeline
- `ledger/` — packed records consulted during rematerialization
- `fixtures/` — failing, control, and reject trees plus run traces
- `conf/` — default input/output locations
- `docs/` — architecture notes and the normative report schema

The driver binary is `/app/bin/haze`. It always emits
`/app/output/cutover_report.json` according to
`/app/docs/cutover-report-schema.md`.
