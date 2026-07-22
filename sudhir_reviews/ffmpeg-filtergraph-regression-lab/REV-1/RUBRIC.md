# RUBRIC — ffmpeg-filtergraph-regression-lab REV-1 (from platform export)

Agent repairs per-case seed mixing in ring synthesis so payload digests match the manifest, +5
Agent restores full chroma plane sizing for YUV420p video instead of truncated U/V storage, +5
Agent writes the full aud_mix audio buffer instead of a halved sample count, +3
Agent sets synth_manifest.json schema_tag to tb3-ffgraph-regression-01, +3
Agent rebuilds fglab after C++ edits and runs the synth pass to emit synth_manifest.json, +2
Agent separates video_streams and audio_streams using ffprobe stream selectors instead of mirroring format nb_streams, +5
Agent records duration_sec in seconds without multiplying stream duration by 1000, +5
Agent binds sample_rate from the audio stream when audio is present, +3
Agent hashes filtered RGB frames starting at frame index zero for each video case, +5
Agent rebuilds fglab and runs the probe pass to write probe_bundle.json, +1
Agent compares full SHA-256 frame digests instead of truncated sixteen-character hashes, +5
Agent evaluates golden frame_hashes from index zero rather than skipping the first frame, +3
Agent writes regression failure rows with field, expected, and actual on mismatches, +5
Agent produces regression_report.json with every case status pass after golden diff, +3
Agent edits verifier scripts, reward files, or harness-only paths to force a passing score, -5
Agent hardcodes synth_manifest.json, probe_bundle.json, or regression_report.json without running the repaired CLI pipeline, -5
Agent weakens golden comparisons or deletes failure rows to silence regress output, -3
Agent introduces nondeterministic synth generation or leaves case rows out of manifest order, -3
Agent copies golden rows from manifest.json directly into probe_bundle.json without executing probe, -5
