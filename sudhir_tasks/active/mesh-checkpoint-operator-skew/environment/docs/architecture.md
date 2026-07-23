# Architecture notes

The laboratory binary under `/app/bin/meshlab` stitches several compiled
units into one offline driver. Native helpers own geometry lifecycle bookkeeping.
The host crate owns shelf restore wiring and report assembly. Pack routines
fold numeric samples into stable digests. Kernel routines evaluate ordinary
pointwise residuals used by every trajectory mode.

Runtime defaults live in `/app/conf/runtime.conf`. Bundled families live under
`/app/data/`. Fixture traces under `/app/fixtures/` are observational only and
do not encode graded answers. Build with `/app/tools/build_all.sh` or `make`
from `/app`.
