# Resolver architecture

`forge solve PROJECT` reads a project file with profile, catalog, roots,
apis, and seed fields.

## Constraint syntax

Root and dependency constraints use the five-field form
`name:low:high:channel:exact-code`:

- `name` is the package key.
- `low` and `high` are integer package codes; a matching row has
  `low <= code < high`.
- `channel` is `stable` or `preview`.
- `exact-code` is an integer package code, or `-` when no exact pin applies.

A catalog row satisfies a constraint when the name matches, the code lies in
that half-open interval, any exact pin matches that code, and a
`stable`-channel request never selects a preview row. Multiple constraints on
the same key tighten to the intersection of their bounds and channels.

## Catalog attributes

Each catalog row carries boolean `preview` and `withdrawn` flags in addition
to name, version, code, source id, needs, payload, and api.

## Profile admission

The project `profile` is one of `plain`, `alpha`, `beta`, or `mixed`:

- `plain` admits only ordinary non-preview, non-withdrawn rows. An exact pin
  that targets a withdrawn row fails under this profile.
- `alpha` may admit a preview row when the request channel is `preview`.
- `beta` may admit a withdrawn row when the request carries a matching exact
  code.
- `mixed` preserves both the alpha preview selection and the beta withdrawn
  selection in one graph.

The two established edge-case behaviors are alpha preview selection under a
preview-channel request, and beta retained selection of a withdrawn package
under an exact pin. Those behaviors apply equally to bundled catalog rows and
to newly generated package names and ranges.

## Solve pipeline

Catalog rows are validated against the request and admitted under the active
profile before the dependency walk commits a closure. The lock writer
serializes only that committed closure; it does not receive raw catalog rows
or policy frames. On success the solver writes `/app/output/workspace.lock`
and `/app/output/build-report.json`.

After writing the lock, the build stage creates a fresh Cargo consumer with
path dependencies to every selected payload and runs Cargo offline with a
generated lock. Diagnostic sampling uses a parallel path and writes a compact
resolve log.
