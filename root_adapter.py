"""Canonical and historical repository-root resolution.

Canonical roots are writable and come from ``sudhir_config.toml`` with explicit
``TB3_*`` environment overrides. Compatibility roots are read-only unless a
tested, explicit rollback mapping is requested by code.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parent

_DEFAULTS = {
    "tasks_dir": "sudhir_tasks/active",
    "specs_dir": "sudhir_ideas/specs",
    "submissions_dir": "sudhir_tasks_ready_to_submit",
    "reviews_dir": "sudhir_reviews",
    "jobs_dir": "sudhir_logs/jobs",
}
_ENV_KEYS = {
    "tasks_dir": "TB3_TASKS_DIR",
    "specs_dir": "TB3_SPECS_DIR",
    "submissions_dir": "TB3_SUBMISSIONS_DIR",
    "reviews_dir": "TB3_REVIEWS_DIR",
    "jobs_dir": "TB3_JOBS_DIR",
}


class HistoricalRootWriteError(PermissionError):
    """Raised when production code attempts to write through a historical root."""


@dataclass(frozen=True)
class RootSet:
    repo_root: Path
    tasks: Path
    specs: Path
    submissions: Path
    reviews: Path
    jobs: Path
    historical_tasks: Path
    historical_specs: Path
    historical_submissions: Path
    current_submission_index: Path
    historical_submission_index: Path
    validation_schema: Path
    board: Path
    status: Path
    idea_index: Path
    historical_writes_allowed: bool = False

    def task_dir(self, slug: str) -> Path:
        return self.tasks / slug

    def submission_zip(self, slug: str) -> Path:
        return self.submissions / f"{slug}.zip"

    def historical_submission_zip(self, slug: str) -> Path:
        return self.historical_submissions / f"{slug}.zip"

    def assert_writable(self, path: Path) -> Path:
        candidate = path.expanduser().resolve(strict=False)
        if self.historical_writes_allowed:
            return candidate
        for root in (
            self.historical_tasks,
            self.historical_specs,
            self.historical_submissions,
        ):
            resolved_root = root.resolve(strict=False)
            if candidate == resolved_root or candidate.is_relative_to(resolved_root):
                raise HistoricalRootWriteError(
                    f"historical compatibility root is read-only: {candidate}"
                )
        return candidate

    def ensure_canonical_dirs(self) -> None:
        for path in (self.tasks, self.specs, self.submissions, self.reviews, self.jobs):
            self.assert_writable(path)
            path.mkdir(parents=True, exist_ok=True)

    def environment(self) -> dict[str, str]:
        return {
            "TB3_TASKS_DIR": str(self.tasks),
            "TB3_SPECS_DIR": str(self.specs),
            "TB3_SUBMISSIONS_DIR": str(self.submissions),
            "TB3_REVIEWS_DIR": str(self.reviews),
            "TB3_JOBS_DIR": str(self.jobs),
            "TB3_VALIDATION_SCHEMA": str(self.validation_schema),
        }


def _resolve(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve(strict=False) if path.is_absolute() else (root / path).resolve(strict=False)


def load_roots(
    *,
    repo_root: Path = REPO_ROOT,
    environ: Mapping[str, str] | None = None,
    config_path: Path | None = None,
) -> RootSet:
    root = repo_root.expanduser().resolve(strict=False)
    values = dict(_DEFAULTS)
    path = config_path or root / "sudhir_config.toml"
    if path.is_file():
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in values:
            if isinstance(data.get(key), str) and data[key].strip():
                values[key] = data[key]
    environment = os.environ if environ is None else environ
    for key, env_key in _ENV_KEYS.items():
        if environment.get(env_key):
            values[key] = environment[env_key]

    return RootSet(
        repo_root=root,
        tasks=_resolve(root, values["tasks_dir"]),
        specs=_resolve(root, values["specs_dir"]),
        submissions=_resolve(root, values["submissions_dir"]),
        reviews=_resolve(root, values["reviews_dir"]),
        jobs=_resolve(root, values["jobs_dir"]),
        historical_tasks=root / "tasks",
        historical_specs=root / "specs",
        historical_submissions=root / "Task_Ready_To_Submit",
        current_submission_index=root / "sudhir_progress" / "CANONICAL_SUBMISSION_INDEX.json",
        historical_submission_index=root / "repo_tests" / "fixtures" / "submission_index.json",
        validation_schema=root / "specs" / "validation_schema.json",
        board=root / "sudhir_progress" / "BOARD.md",
        status=root / "sudhir_progress" / "STATUS.md",
        idea_index=root / "sudhir_ideas" / "IDEA_INDEX.md",
    )


def legacy_rollback_roots(*, repo_root: Path = REPO_ROOT) -> RootSet:
    """Return the pre-migration mapping for an explicit code rollback only."""
    root = repo_root.expanduser().resolve(strict=False)
    return RootSet(
        repo_root=root,
        tasks=root / "tasks",
        specs=root / "specs",
        submissions=root / "Task_Ready_To_Submit",
        reviews=root / "sudhir_reviews",
        jobs=root / "jobs",
        historical_tasks=root / "tasks",
        historical_specs=root / "specs",
        historical_submissions=root / "Task_Ready_To_Submit",
        current_submission_index=root / "repo_tests" / "fixtures" / "submission_index.json",
        historical_submission_index=root / "repo_tests" / "fixtures" / "submission_index.json",
        validation_schema=root / "specs" / "validation_schema.json",
        board=root / "sudhir_progress" / "BOARD.md",
        status=root / "sudhir_progress" / "STATUS.md",
        idea_index=root / "sudhir_ideas" / "IDEA_INDEX.md",
        historical_writes_allowed=True,
    )


ROOTS = load_roots()
