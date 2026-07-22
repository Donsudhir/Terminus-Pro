# Root adapter inventory and migration — 2026-07-21

Decision: ADR-0019. Implementation: Slice 7.

## Root roles

| Root | Role | Write policy | Primary owner |
| --- | --- | --- | --- |
| `sudhir_tasks/active/` | current task source | canonical writable | `sudhir_task.py`, explicit task-path tools |
| `sudhir_ideas/specs/` | current Step 2a specs/state/evidence | canonical writable | `validate_loop.py` |
| `sudhir_tasks_ready_to_submit/` | current submission ZIPs | canonical writable | `sudhir_task.py package` |
| `sudhir_reviews/` | revision dossiers | canonical writable | `sudhir_dossier.py` / driver |
| `sudhir_logs/jobs/` | current job evidence | canonical writable | Harbor / evidence capture |
| `tasks/` | upstream compatibility task surface | read-only in production | explicit fixture/reference readers |
| `specs/` | tracked schema + compatibility state | read-only in production | validation-schema reader, historical state |
| `Task_Ready_To_Submit/` | 159-archive historical/reference corpus | immutable/read-only | uniqueness, reference, regression index |

## Writer inventory

### Canonical writers

- `sudhir_task.py cmd_package` — writes one canonical ZIP, validates/approves it,
  atomically refreshes the current index, and restores the previous ZIP if
  index refresh fails.
- `sudhir_task.py cmd_revise` — removes only the canonical current ZIP,
  atomically refreshes the current index, and restores the ZIP on failure.
- `validate_loop.py` — writes Step 2a state, logs, evidence, specs, and candidates
  under the canonical spec root; every write/delete checks the adapter.
- `sudhir_dossier.py` — writes revision dossiers under the configured review root.
- `sudhir_task.py save_registry` — atomic registry replacement.
- `sudhir_task.py write_board` — grouped BOARD/IDEA_INDEX/STATUS replacement from
  one registry snapshot and one generation digest, with rollback on replacement
  failure.
- `scripts/build_submission_index.py` — atomic current-index writer by default;
  historical mode is explicit and intended only for deliberate corpus-baseline
  maintenance.

### Removed or blocked writers

- Manual `zip` commands targeting `Task_Ready_To_Submit/` were removed from
  active commands, workflow, task-creation, and review guidance.
- `root_adapter.RootSet.assert_writable()` raises
  `HistoricalRootWriteError` for writes under `tasks/`, `specs/`, or
  `Task_Ready_To_Submit/`.

## Reader inventory

### Canonical readers

- `sudhir_task.py` loads all configured roots through `root_adapter.py`.
- `validate_loop.py` writes canonical specs and reads the explicitly tracked
  compatibility validation schema.
- `approve_task.py configured_specs_dir()` resolves canonical specs through the
  adapter.
- `collapse_check.py load_construction_manifest()` uses canonical specs for a
  canonical active task and preserves fixture-relative spec lookup for isolated
  tests.
- `requirements_check.py` renders manual commands with canonical task/ZIP paths.
- `scripts/sudhir-env.sh` exports root-adapter values rather than duplicating
  path literals.

### Historical/reference readers

- `repo_tests/test_validate_submission_zip.py` intentionally validates both
  archive populations independently.
- `repo_tests/fixtures/submission_index.json` is the historical 159-archive
  regression index.
- Historical ZIPs remain valid inputs to uniqueness/reference research and ZIP
  validation. Canonical archives take precedence for current package state.

### Fixture-only readers

- `repo_tests/fixtures/tasks/` remains an isolated static-check fixture root.
- Temporary `tasks/` and `specs/` paths inside tests are allowed only outside
  the repository historical roots.

## Index ownership

- Current: `sudhir_progress/CANONICAL_SUBMISSION_INDEX.json` — generated current
  state, 6 archives at migration.
- Historical: `repo_tests/fixtures/submission_index.json` — immutable/reference
  baseline, 159 archives at migration.
- The two indexes are never merged and never infer the role of one population
  from the other.

## Rollback mapping

`root_adapter.legacy_rollback_roots()` restores the pre-migration defaults for
an explicit code rollback without deleting either population. Rollback must not
copy, rewrite, or merge archives. Generated status views can be regenerated from
registry after restoring the prior code.

## Shadow/parity evidence

- Canonical current index: 6/6 valid.
- Historical index: 159/159 valid.
- Active tasks: 6/6 canonical sources, zero static failures before enforcement.
- No production writer required a dual-write window; direct canonical packaging
  plus ZIP/index rollback proves parity without creating a second mutable copy.
- Three names overlap both populations at migration and are byte-identical by
  SHA-256: `musl-sysroot-splice.zip`, `robust-predicate-scale-parity.zip`, and
  `sparse-jacobian-color-contract.zip`. Other current archives have no same-name
  historical counterpart and are not copied merely to force symmetry.
