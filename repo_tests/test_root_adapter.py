"""Canonical-root adapter, read-only, parity, and rollback regressions."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from unittest import mock

import pytest

import root_adapter
import sudhir_task
from scripts import build_submission_index


def test_default_roots_match_sudhir_config() -> None:
    roots = root_adapter.load_roots()
    assert roots.tasks == root_adapter.REPO_ROOT / "sudhir_tasks" / "active"
    assert roots.specs == root_adapter.REPO_ROOT / "sudhir_ideas" / "specs"
    assert roots.submissions == root_adapter.REPO_ROOT / "sudhir_tasks_ready_to_submit"
    assert roots.historical_submissions == root_adapter.REPO_ROOT / "Task_Ready_To_Submit"
    assert roots.current_submission_index != roots.historical_submission_index


def test_environment_overrides_configured_canonical_roots() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "sudhir_config.toml").write_text(
            'version = 1\ntasks_dir = "configured/tasks"\n'
            'specs_dir = "configured/specs"\nsubmissions_dir = "configured/zips"\n'
            'reviews_dir = "configured/reviews"\njobs_dir = "configured/jobs"\n',
            encoding="utf-8",
        )
        roots = root_adapter.load_roots(
            repo_root=repo,
            environ={
                "TB3_TASKS_DIR": str(repo / "env/tasks"),
                "TB3_SUBMISSIONS_DIR": str(repo / "env/zips"),
            },
        )
    assert roots.tasks == repo / "env/tasks"
    assert roots.submissions == repo / "env/zips"
    assert roots.specs == repo / "configured/specs"


def test_historical_accessors_are_read_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        roots = root_adapter.load_roots(repo_root=Path(tmp), environ={})
        with pytest.raises(root_adapter.HistoricalRootWriteError):
            roots.assert_writable(roots.historical_submission_zip("example"))
        with pytest.raises(root_adapter.HistoricalRootWriteError):
            roots.assert_writable(roots.historical_tasks / "example" / "task.toml")
        assert roots.assert_writable(roots.submission_zip("example")) == roots.submission_zip(
            "example"
        ).resolve(strict=False)


def test_canonical_directory_creation_never_touches_historical_roots() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        roots = root_adapter.load_roots(repo_root=Path(tmp), environ={})
        roots.ensure_canonical_dirs()
        assert all(
            path.is_dir()
            for path in (roots.tasks, roots.specs, roots.submissions, roots.reviews, roots.jobs)
        )
        assert not roots.historical_tasks.exists()
        assert not roots.historical_specs.exists()
        assert not roots.historical_submissions.exists()


def test_explicit_rollback_mapping_restores_old_defaults_without_deletion() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        roots = root_adapter.legacy_rollback_roots(repo_root=repo)
        assert roots.tasks == repo / "tasks"
        assert roots.specs == repo / "specs"
        assert roots.submissions == repo / "Task_Ready_To_Submit"
        assert roots.historical_writes_allowed is True
        sentinel = roots.submissions / "preserved.zip"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_bytes(b"preserved")
        assert roots.assert_writable(sentinel) == sentinel.resolve(strict=False)
        assert sentinel.read_bytes() == b"preserved"


def test_status_views_share_one_registry_generation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        board = root / "BOARD.md"
        status = root / "STATUS.md"
        ideas = root / "IDEA_INDEX.md"
        registry = sudhir_task.empty_registry()
        with (
            mock.patch.object(sudhir_task, "BOARD_PATH", board),
            mock.patch.object(sudhir_task, "STATUS_PATH", status),
            mock.patch.object(sudhir_task, "IDEA_INDEX_PATH", ideas),
        ):
            sudhir_task.write_board(registry)
        generations = {
            next(
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("Generation:")
            )
            for path in (board, status, ideas)
        }
        assert len(generations) == 1
        assert "Do not edit it by hand" in status.read_text(encoding="utf-8")


def test_status_view_transaction_rolls_back_on_replace_failure() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        paths = [root / "BOARD.md", root / "IDEA_INDEX.md", root / "STATUS.md"]
        for index, path in enumerate(paths):
            path.write_text(f"old-{index}\n", encoding="utf-8")
        real_replace = sudhir_task.os.replace
        replacement_count = 0

        def fail_second_generated_replace(source: Path, destination: Path) -> None:
            nonlocal replacement_count
            if str(source).endswith(".tmp"):
                replacement_count += 1
                if replacement_count == 2:
                    raise OSError("injected grouped-view failure")
            real_replace(source, destination)

        with (
            mock.patch.object(sudhir_task, "BOARD_PATH", paths[0]),
            mock.patch.object(sudhir_task, "IDEA_INDEX_PATH", paths[1]),
            mock.patch.object(sudhir_task, "STATUS_PATH", paths[2]),
            mock.patch.object(
                sudhir_task.os,
                "replace",
                side_effect=fail_second_generated_replace,
            ),
            pytest.raises(OSError, match="injected grouped-view failure"),
        ):
            sudhir_task.write_board(sudhir_task.empty_registry())
        assert [path.read_text(encoding="utf-8") for path in paths] == [
            "old-0\n",
            "old-1\n",
            "old-2\n",
        ]


def _seed_package_task(root: Path, slug: str) -> tuple[Path, dict[str, object]]:
    tasks = root / "canonical-tasks"
    task_dir = tasks / slug
    (task_dir / "environment").mkdir(parents=True)
    (task_dir / "task.toml").write_text(
        'version = "2.0"\n[metadata]\ncategory = "security"\n'
        'subcategories = []\nlanguages = ["rust"]\nnumber_of_milestones = 0\n',
        encoding="utf-8",
    )
    (task_dir / "instruction.md").write_text("Repair the fixture.\n", encoding="utf-8")
    (task_dir / "environment" / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
    entry = sudhir_task.new_entry(slug)
    entry.update({"category": "security", "phase": "review", "revision": 1})
    registry: dict[str, object] = {
        "schema_version": 3,
        "ideas": {},
        "tasks": {slug: entry},
    }
    return tasks, registry


def test_package_writes_canonical_zip_and_refreshes_current_index() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        slug = "canonical-package"
        tasks, registry = _seed_package_task(root, slug)
        submissions = root / "current-submissions"
        current_index = root / "progress" / "CURRENT.json"
        args = type("Args", (), {"slug": slug, "force": True, "skip_approve": True})()
        with (
            mock.patch.object(sudhir_task, "TASKS_DIR", tasks),
            mock.patch.object(sudhir_task, "SUBMISSIONS_DIR", submissions),
            mock.patch.object(sudhir_task, "CURRENT_SUBMISSION_INDEX_PATH", current_index),
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
            mock.patch.object(sudhir_task, "_task_execution_gaps", return_value=[]),
            mock.patch.object(
                sudhir_task,
                "run_gate",
                return_value={"result": "PASS", "exit_code": 0},
            ),
            mock.patch.object(
                build_submission_index,
                "write_index_atomic",
                return_value={"archive_count": 1},
            ) as write_index,
        ):
            exit_code = sudhir_task.cmd_package(args)
        canonical_zip = submissions / f"{slug}.zip"
        assert exit_code == 0
        assert canonical_zip.is_file()
        write_index.assert_called_once_with(submissions, current_index)
        assert not (root / "Task_Ready_To_Submit" / f"{slug}.zip").exists()


def test_package_restores_previous_zip_when_index_refresh_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        slug = "rollback-package"
        tasks, registry = _seed_package_task(root, slug)
        submissions = root / "current-submissions"
        submissions.mkdir()
        canonical_zip = submissions / f"{slug}.zip"
        canonical_zip.write_bytes(b"previous-package")
        current_index = root / "progress" / "CURRENT.json"
        args = type("Args", (), {"slug": slug, "force": True, "skip_approve": True})()
        with (
            mock.patch.object(sudhir_task, "TASKS_DIR", tasks),
            mock.patch.object(sudhir_task, "SUBMISSIONS_DIR", submissions),
            mock.patch.object(sudhir_task, "CURRENT_SUBMISSION_INDEX_PATH", current_index),
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
            mock.patch.object(sudhir_task, "_task_execution_gaps", return_value=[]),
            mock.patch.object(
                sudhir_task,
                "run_gate",
                return_value={"result": "PASS", "exit_code": 0},
            ),
            mock.patch.object(
                build_submission_index,
                "write_index_atomic",
                side_effect=OSError("index unavailable"),
            ),
        ):
            exit_code = sudhir_task.cmd_package(args)
        assert exit_code == 1
        assert canonical_zip.read_bytes() == b"previous-package"


def test_active_guidance_contains_no_historical_archive_writer() -> None:
    for relative in (
        "commands.md",
        "workflow.md",
        ".cursor/rules/task-creation.mdc",
        ".cursor/rules/review-and-submit.mdc",
    ):
        text = (root_adapter.REPO_ROOT / relative).read_text(encoding="utf-8")
        assert not re.search(
            r"(?im)^\s*(?:zip|rm\s+-f|cp|mv)\b[^\n]*Task_Ready_To_Submit",
            text,
        ), relative


def test_production_consumers_do_not_fallback_to_legacy_writable_roots() -> None:
    sudhir_driver = (root_adapter.REPO_ROOT / "sudhir_task.py").read_text(
        encoding="utf-8"
    )
    validate_loop = (root_adapter.REPO_ROOT / "validate_loop.py").read_text(
        encoding="utf-8"
    )
    approve = (root_adapter.REPO_ROOT / "approve_task.py").read_text(encoding="utf-8")
    self_index = (
        root_adapter.REPO_ROOT / "scripts" / "build_submission_index.py"
    ).read_text(encoding="utf-8")
    assert "Task_Ready_To_Submit" not in sudhir_driver
    assert 'SPECS_DIR = Path(os.environ.get("TB3_SPECS_DIR", "specs"))' not in validate_loop
    assert 'return Path(configured).expanduser() if configured else REPO_ROOT / "specs"' not in approve
    assert "DEFAULT_SUBMISSION_DIR = root_adapter.ROOTS.submissions" in self_index
