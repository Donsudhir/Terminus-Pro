# SOLUTION — rowgroup-prune-mirage REV-2

The repair treats validity as a single decision that has to survive every stage. The Rust producer computes persisted markers only from live values, while keeping an explicit absence signal. The C++ planner stays conservative when an older slab cannot prove exclusion, and the batch path applies the same effective validity before matching or summing lanes. I kept archived artifacts untouched and rebuilt the binaries so fresh and historical data meet one contract. This also leaves the healthy selective and batch paths doing their original jobs.
