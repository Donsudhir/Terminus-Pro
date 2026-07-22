# Snorkel inbox

Drop Snorkel platform submission exports here, then run:

```bash
python3 sudhir_task.py ingest
```

Each `*.json` export is parsed for difficulty, solvability, static-check
outcome, upload time, and per-agent pass rates, written into
`sudhir_progress/registry.json`, and then moved to `../archive/` so it is
ingested exactly once. The status board (`sudhir_progress/BOARD.md`) is
re-rendered automatically.

## How to get an export

The platform ("Terminus-2nd-Edition") serves feedback behind app auth and S3,
so there is no unattended API pull configured. In the platform UI open a
submission and download its JSON blob (named like
`submission_<id>.json`). This repo also ingests any `submission_*.json`
left at the repository root.

See `python3 sudhir_task.py sync-snorkel` for the network-pull extension point.
