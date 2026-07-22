# DIFFICULTY — envelope-rotation-shear REV-3

This task is hard because one authority identity has to stay consistent across maintenance writes, namespace context, authenticated reads, and historical recovery. Valid records in newly introduced namespaces must open directly, but an intact record copied from another namespace must fail without recovery. A permissive compatibility change breaks isolation, while an overly strict change breaks healthy generated reads. The solver also has to recover prior-history records and keep repeat maintenance byte-stable without weakening authentication.
