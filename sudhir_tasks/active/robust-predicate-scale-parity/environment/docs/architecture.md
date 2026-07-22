# Geometry Lab Architecture

The executable is assembled from three language layers. The native layer evaluates compact numerical series and exposes bounded integer refinements. The host layer reads dyadic families, applies declared transforms, enumerates bounded tetrahedron candidates, constructs face links, and serializes the report. The analysis layer receives oriented integer rows through a C-compatible interface and returns their stable row order plus face-incidence totals.

Family reports are produced in one process and sorted before serialization. Data values remain dyadic until the host prepares floating and integer views for the lower layers. Point identities, rather than array positions, are carried into the report.

The normal executable reads the paths in `config/runtime.conf`. `GEOMLAB_INPUT` and `GEOMLAB_OUTPUT` provide equivalent process-local overrides for automated laboratory runs. The output writer emits compact UTF-8 JSON with stable key order and one trailing newline.
