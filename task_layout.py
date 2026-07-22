"""Canonical task-layout classification shared by source and ZIP consumers."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

STANDARD = "standard"
MILESTONE = "milestone"
LEGACY_MILESTONE = "legacy-milestone"
INVALID = "invalid"


@dataclass(frozen=True)
class LayoutReport:
    kind: str
    milestone_names: tuple[str, ...]
    declared_count: int | None
    declared_step_names: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return self.kind in {STANDARD, MILESTONE} and not self.errors

    @property
    def milestone_count(self) -> int:
        return len(self.milestone_names)


def _normalize_name(name: str) -> str:
    normalized = name.replace("\\", "/").lstrip("/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.rstrip("/")


def _inventory_from_names(names: Iterable[str]) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    dirs: set[str] = set()
    for raw_name in names:
        name = _normalize_name(raw_name)
        if not name:
            continue
        parts = name.split("/")
        files.add(name)
        for end in range(1, len(parts)):
            dirs.add("/".join(parts[:end]))
    return files, dirs


def _declared_metadata(task_data: dict[str, Any]) -> tuple[int | None, tuple[str, ...]]:
    metadata = task_data.get("metadata")
    raw_count = metadata.get("number_of_milestones") if isinstance(metadata, dict) else None
    declared_count = raw_count if isinstance(raw_count, int) and not isinstance(raw_count, bool) else None
    steps = task_data.get("steps")
    names = (
        tuple(str(step.get("name")) for step in steps if isinstance(step, dict))
        if isinstance(steps, list)
        else ()
    )
    return declared_count, names


def number_of_milestones(task_data: dict[str, Any] | None) -> int:
    declared_count, _names = _declared_metadata(task_data or {})
    return declared_count if declared_count is not None and declared_count > 0 else 0


def _step_names(files: set[str], dirs: set[str]) -> tuple[str, ...]:
    names: set[str] = set()
    for name in files | dirs:
        parts = name.split("/")
        if len(parts) >= 2 and parts[0] == "steps":
            names.add(parts[1])
    def sort_key(name: str) -> tuple[int, int | str]:
        match = re.fullmatch(r"milestone_([1-9][0-9]*)", name)
        return (0, int(match.group(1))) if match else (1, name)

    return tuple(sorted(names, key=sort_key))


def _legacy_signals(files: set[str]) -> tuple[str, ...]:
    signals = sorted(
        name
        for name in files
        if re.fullmatch(r"milestone_[1-9][0-9]*\.md", name)
        or re.fullmatch(r"tests/test_m[1-9][0-9]*\.py", name)
        or re.fullmatch(r"solution/solve[1-9][0-9]*\.sh", name)
    )
    return tuple(signals)


def _validate_standard(
    files: set[str],
    dirs: set[str],
    task_data: dict[str, Any],
    declared_count: int | None,
    declared_steps: tuple[str, ...],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_files = {
        "instruction.md",
        "task.toml",
        "environment/Dockerfile",
        "solution/solve.sh",
        "tests/test.sh",
        "tests/test_outputs.py",
    }
    missing = sorted(required_files - files)
    if missing:
        errors.append("standard task missing required file(s): " + ", ".join(missing))
    if "steps" in dirs or declared_steps:
        errors.append("standard task must not contain steps/ or [[steps]] blocks")
    if declared_count not in {0}:
        errors.append(
            "standard task metadata.number_of_milestones must be 0, "
            f"found {declared_count!r}"
        )
    legacy = _legacy_signals(files)
    if legacy:
        errors.append("standard task contains legacy milestone artifact(s): " + ", ".join(legacy))
    return errors, warnings


def _validate_milestone(
    files: set[str],
    dirs: set[str],
    task_data: dict[str, Any],
    declared_count: int | None,
    declared_steps: tuple[str, ...],
    step_names: tuple[str, ...],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    numbered: list[tuple[int, str]] = []
    for name in step_names:
        match = re.fullmatch(r"milestone_([1-9][0-9]*)", name)
        if match is None:
            errors.append(f"invalid step directory name: steps/{name}/")
            continue
        numbered.append((int(match.group(1)), name))
    numbered.sort()
    milestone_names = tuple(name for _, name in numbered)
    actual_numbers = [number for number, _ in numbered]
    if actual_numbers != list(range(1, len(numbered) + 1)):
        errors.append("milestone directories must be sequential from milestone_1")
    if len(numbered) < 2:
        errors.append("milestone tasks must contain at least 2 milestones")

    required_common = {"task.toml", "environment/Dockerfile"}
    missing_common = sorted(required_common - files)
    if missing_common:
        errors.append("milestone task missing required file(s): " + ", ".join(missing_common))

    for number, name in numbered:
        prefix = f"steps/{name}"
        required = {
            f"{prefix}/instruction.md",
            f"{prefix}/tests/test.sh",
            f"{prefix}/tests/test_m{number}.py",
            f"{prefix}/solution/solve.sh",
            f"{prefix}/solution/solve{number}.sh",
        }
        missing = sorted(required - files)
        if missing:
            errors.append(f"{prefix}/ missing required file(s): " + ", ".join(missing))

    forbidden_root = sorted(
        ({"instruction.md"} & files)
        | ({"tests", "solution"} & dirs)
        | set(_legacy_signals(files))
    )
    if forbidden_root:
        errors.append(
            "milestone task contains deprecated root-level content: "
            + ", ".join(forbidden_root)
        )
    if declared_count != len(numbered):
        errors.append(
            "metadata.number_of_milestones does not match steps/: "
            f"declared={declared_count!r}, actual={len(numbered)}"
        )
    if declared_steps != milestone_names:
        errors.append(
            "[[steps]] names do not match milestone directories: "
            f"declared={list(declared_steps)}, directories={list(milestone_names)}"
        )
    if "agent" in task_data or "verifier" in task_data:
        errors.append("milestone task must not define top-level [agent] or [verifier]")

    steps = task_data.get("steps")
    if isinstance(steps, list):
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                errors.append(f"[[steps]] entry {index} must be a table")
                continue
            for table_name in ("agent", "verifier"):
                table = step.get(table_name)
                timeout = table.get("timeout_sec") if isinstance(table, dict) else None
                if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
                    errors.append(
                        f"steps/{step.get('name', index)} [{table_name}].timeout_sec "
                        "must be positive"
                    )
    return errors, warnings


def classify_inventory(names: Iterable[str], task_data: dict[str, Any]) -> LayoutReport:
    files, dirs = _inventory_from_names(names)
    declared_count, declared_steps = _declared_metadata(task_data)
    step_names = _step_names(files, dirs)
    legacy = _legacy_signals(files)
    has_steps = "steps" in dirs or bool(step_names)

    if has_steps:
        kind = MILESTONE
        errors, warnings = _validate_milestone(
            files,
            dirs,
            task_data,
            declared_count,
            declared_steps,
            step_names,
        )
    elif (declared_count or 0) > 0 or legacy:
        kind = LEGACY_MILESTONE
        errors = [
            "legacy milestone layout detected; migrate to steps/milestone_N/ before validation"
        ]
        warnings = list(legacy)
    else:
        kind = STANDARD
        errors, warnings = _validate_standard(
            files,
            dirs,
            task_data,
            declared_count,
            declared_steps,
        )

    return LayoutReport(
        kind=kind,
        milestone_names=step_names if kind == MILESTONE else (),
        declared_count=declared_count,
        declared_step_names=declared_steps,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def classify_task_dir(
    task_dir: Path,
    task_data: dict[str, Any] | None = None,
) -> LayoutReport:
    task_dir = task_dir.resolve()
    if task_data is None:
        task_toml = task_dir / "task.toml"
        try:
            task_data = tomllib.loads(task_toml.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            task_data = {}
    names = [
        path.relative_to(task_dir).as_posix()
        for path in task_dir.rglob("*")
        if path.is_file()
    ]
    return classify_inventory(names, task_data)


def instruction_paths(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [task_dir / "steps" / name / "instruction.md" for name in report.milestone_names]
    return [task_dir / "instruction.md"]


def test_sh_paths(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [task_dir / "steps" / name / "tests" / "test.sh" for name in report.milestone_names]
    return [task_dir / "tests" / "test.sh"]


def test_dirs(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [task_dir / "steps" / name / "tests" for name in report.milestone_names]
    return [task_dir / "tests"]


def verifier_paths(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [
            task_dir / "steps" / name / "tests" / f"test_m{index}.py"
            for index, name in enumerate(report.milestone_names, start=1)
        ]
    return [task_dir / "tests" / "test_outputs.py"]


def solution_entrypoints(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [task_dir / "steps" / name / "solution" / "solve.sh" for name in report.milestone_names]
    return [task_dir / "solution" / "solve.sh"]


def solution_dirs(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [task_dir / "steps" / name / "solution" for name in report.milestone_names]
    return [task_dir / "solution"]


def solution_implementations(task_dir: Path, report: LayoutReport) -> list[Path]:
    if report.kind == MILESTONE:
        return [
            task_dir / "steps" / name / "solution" / f"solve{index}.sh"
            for index, name in enumerate(report.milestone_names, start=1)
        ]
    return solution_entrypoints(task_dir, report)
