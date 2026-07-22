# Mixed-language sensitivity lab

The compiled driver coordinates four cooperating layers under `native/`,
`host/`, `analysis/`, and `kernels/`. Incidence patterns feed a partition
stage; the host binds finite-difference rosters, chooses magnitudes, and
assembles the JSON artifact; analysis reindexes compressed results; kernels
evaluate the residual families.

Data under `data/` declares families, unknown ids, affine tags, and optional
permutations. Configuration under `conf/` sets default IO paths and magnitude
floors. Report field layout is described in `docs/report-format.md`.

Build with `tools/build_all.sh`. Run with `tools/run_senslab.sh` or `/app/bin/senslab`.
