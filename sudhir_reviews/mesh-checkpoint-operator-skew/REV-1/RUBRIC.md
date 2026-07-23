# RUBRIC — mesh-checkpoint-operator-skew REV-1

Agent rebuilds and runs /app/bin/meshlab so /app/output/parity_report.json is emitted by the compiled pipeline with schema_version runs summary and digest, +3
Agent restores interrupted versus twin solution field digests and geometry tokens across bundled families after remesh and resume, +5
Agent aligns pointwise residual samples and residual norms between interrupted and twin trajectories, +5
Agent keeps sequential remesh resume families from inheriting prior reuse marks while leaving nonzero reuse on interrupted runs, +3
Agent makes emitted field digests match an independent fold of samples under fold_order and sets digest_match accordingly, +5
Agent keeps the no checkpoint control byte identical across clean paired runs with control_stable set, +3
Agent preserves byte identical reports under reordered family inputs and clean rebuilds including the FNV digest contract, +2
Agent leaves malformed input exiting nonzero without a partial report, +2
Agent hand writes parity_report.json, replaces bundled inputs, or bypasses the compiled meshlab pipeline, -5
Agent edits verifier tests, shadows pytest, or forces reward without repairing the pipeline, -5
Agent patches only one authority and leaves twin digest, residual, reuse, or fold disagreement, -3
Agent clears fail closed malformed handling or breaks healthy no checkpoint byte stability while fixing interrupted paths, -3
