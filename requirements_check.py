#!/usr/bin/env python3
"""
Terminal-Bench task requirements checker.

Maps the upstream Task Requirements checklist to repo-local automated gates
and explicit manual reminders. Run when reviewing a task before submit:

    python3 requirements_check.py tasks/<task-name>
    python3 requirements_check.py tasks/<task-name> --quick
    python3 requirements_check.py tasks/<task-name> --json

Exit codes: 0 = all automated checks PASS, 1 = at least one FAIL, 2 = WARN-only
(Manual checklist items do not affect the exit code.)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

import model_policy
import root_adapter
import task_layout

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parent

# Files that must not appear in a submission zip (repo may keep output_contract.toml).
PACKAGING_FORBIDDEN_ROOT = frozenset(
    {
        "rubric.txt",
        "rubrics.txt",
        "quality_check_adjudication.json",
        "construction_manifest.json",
        ".step2b-checksum",
        ".step2b-metrics.jsonl",
    }
)
BANNED_AI_FILENAMES = frozenset(
    {
        "claude.md",
        "claude.txt",
        "agents.md",
        "agent.md",
        "skills.md",
        "skill.md",
        "ai_instructions.md",
        "ai_notes.md",
        "agent_notes.md",
        "copilot.md",
        "copilot-instructions.md",
        ".cursorrules",
    }
)
BANNED_AI_DIRS = frozenset({".cursor", ".aider", ".continue", ".claude"})

CODEBASE_SIZE_BANDS = {
    "minimal": (0, 20),
    "small": (21, 199),
    "large": (200, None),
}


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    MANUAL = "manual"
    SKIP = "skip"


@dataclass
class Check:
    section: str
    requirement: str
    status: Status
    detail: str = ""
    command: str = ""


@dataclass
class Report:
    task_dir: Path
    task_name: str
    checks: list[Check] = field(default_factory=list)

    def add(
        self,
        section: str,
        requirement: str,
        status: Status,
        *,
        detail: str = "",
        command: str = "",
    ) -> None:
        self.checks.append(
            Check(
                section=section,
                requirement=requirement,
                status=status,
                detail=detail,
                command=command,
            )
        )

    @property
    def has_fail(self) -> bool:
        return any(c.status == Status.FAIL for c in self.checks)

    @property
    def has_warn(self) -> bool:
        return any(c.status == Status.WARN for c in self.checks)

    def exit_code(self) -> int:
        if self.has_fail:
            return 1
        if self.has_warn:
            return 2
        return 0


def resolve_task_dir(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def load_task_toml(task_dir: Path) -> dict:
    path = task_dir / "task.toml"
    if tomllib is None:
        raise RuntimeError("tomllib is required (Python 3.11+)")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def count_environment_files(task_dir: Path) -> int:
    env = task_dir / "environment"
    if not env.is_dir():
        return 0
    return sum(1 for p in env.rglob("*") if p.is_file())


def is_milestone_task(task_data: dict) -> bool:
    meta = task_data.get("metadata") or {}
    count = meta.get("number_of_milestones", 0)
    return isinstance(count, int) and count > 0


def list_verifier_py_files(task_dir: Path, task_data: dict) -> list[Path]:
    layout = task_layout.classify_task_dir(task_dir, task_data)
    return [path for path in task_layout.verifier_paths(task_dir, layout) if path.exists()]


def check_structural_layout(report: Report, task_dir: Path, task_data: dict) -> None:
    section = "Structural Requirements"
    layout = task_layout.classify_task_dir(task_dir, task_data)
    if layout.errors:
        for error in layout.errors:
            report.add(section, "canonical task layout", Status.FAIL, detail=error)
    else:
        report.add(
            section,
            "canonical task layout",
            Status.PASS,
            detail=f"{layout.kind}; milestones={layout.milestone_count}",
        )

    readme = task_dir / "README.md"
    if readme.exists():
        report.add(section, "README.md (optional)", Status.PASS, detail="present")
    else:
        report.add(section, "README.md (optional)", Status.PASS, detail="not present (ok)")


def check_task_toml_fields(report: Report, task_dir: Path, task_data: dict) -> None:
    section = "task.toml Requirements"
    version = task_data.get("version")
    if version == "2.0":
        report.add(section, 'version = "2.0"', Status.PASS)
    else:
        report.add(section, 'version = "2.0"', Status.FAIL, detail=f"got {version!r}")

    meta = task_data.get("metadata")
    if not isinstance(meta, dict):
        report.add(section, "[metadata] table", Status.FAIL, detail="missing or invalid [metadata]")
        return

    required_meta = (
        "category",
        "subcategories",
        "number_of_milestones",
        "difficulty",
        "codebase_size",
        "languages",
        "tags",
        "expert_time_estimate_min",
        "junior_time_estimate_min",
    )
    for key in required_meta:
        if key in meta:
            report.add(section, f"metadata.{key}", Status.PASS)
        else:
            report.add(section, f"metadata.{key}", Status.FAIL, detail="missing")

    tags = meta.get("tags")
    if isinstance(tags, list) and 3 <= len(tags) <= 6:
        report.add(section, "tags (3–6 keywords)", Status.PASS, detail=str(len(tags)) + " tags")
    elif isinstance(tags, list):
        report.add(
            section,
            "tags (3–6 keywords)",
            Status.WARN if tags else Status.FAIL,
            detail=f"found {len(tags)} tag(s); submission requires ~3–6",
        )
    else:
        report.add(section, "tags (3–6 keywords)", Status.FAIL, detail="tags must be a list")

    env = task_data.get("environment") or {}
    if env.get("allow_internet") is False:
        report.add(section, "[environment].allow_internet = false", Status.PASS)
    else:
        report.add(
            section,
            "[environment].allow_internet = false",
            Status.FAIL,
            detail=f"got {env.get('allow_internet')!r}",
        )

    layout = task_layout.classify_task_dir(task_dir, task_data)
    timeout_blocks = [("environment", "build_timeout_sec")]
    if layout.kind == task_layout.STANDARD:
        timeout_blocks = [
            ("agent", "timeout_sec"),
            ("verifier", "timeout_sec"),
            *timeout_blocks,
        ]
    for block, key in timeout_blocks:
        table = task_data.get(block) or {}
        if isinstance(table.get(key), (int, float)) and table[key] > 0:
            report.add(section, f"[{block}].{key}", Status.PASS)
        else:
            report.add(section, f"[{block}].{key}", Status.FAIL, detail="missing or non-positive")

    if layout.kind == task_layout.MILESTONE:
        for step in task_data.get("steps") or []:
            if not isinstance(step, dict):
                continue
            name = step.get("name", "?")
            for block in ("agent", "verifier"):
                table = step.get(block) or {}
                timeout = table.get("timeout_sec") if isinstance(table, dict) else None
                if isinstance(timeout, (int, float)) and not isinstance(timeout, bool) and timeout > 0:
                    report.add(section, f"[[steps]] {name} [{block}].timeout_sec", Status.PASS)
                else:
                    report.add(
                        section,
                        f"[[steps]] {name} [{block}].timeout_sec",
                        Status.FAIL,
                        detail="missing or non-positive",
                    )

    codebase_size = meta.get("codebase_size")
    file_count = count_environment_files(task_dir)
    if codebase_size in CODEBASE_SIZE_BANDS:
        lo, hi = CODEBASE_SIZE_BANDS[codebase_size]
        in_band = file_count >= lo and (hi is None or file_count <= hi)
        if in_band:
            report.add(
                section,
                f"codebase_size={codebase_size!r} vs environment file count",
                Status.PASS,
                detail=f"{file_count} files under environment/",
            )
        else:
            report.add(
                section,
                f"codebase_size={codebase_size!r} vs environment file count",
                Status.WARN,
                detail=(
                    f"environment/ has {file_count} files; band for {codebase_size!r} is "
                    f"{'0–20' if codebase_size == 'minimal' else '20+' if codebase_size == 'small' else '200+'}"
                ),
            )
    else:
        report.add(section, "codebase_size (minimal|small|large)", Status.FAIL, detail=str(codebase_size))


def check_solution_standards(report: Report, task_dir: Path, task_data: dict) -> None:
    section = "Solution Requirements"
    layout = task_layout.classify_task_dir(task_dir, task_data)

    def audit_solve(path: Path, label: str) -> None:
        if not path.exists():
            report.add(section, label, Status.FAIL, detail="file missing")
            return
        text = path.read_text(encoding="utf-8")
        if text.startswith("#!/"):
            report.add(section, f"{label} shebang", Status.PASS)
        else:
            report.add(section, f"{label} shebang", Status.WARN, detail="missing #!/bin/bash")
        if re.search(r"set\s+-euo\s+pipefail", text):
            report.add(section, f"{label} set -euo pipefail", Status.PASS)
        else:
            report.add(
                section,
                f"{label} set -euo pipefail",
                Status.WARN,
                detail="solve.sh should use set -euo pipefail per submission standards",
            )

    if layout.kind == task_layout.MILESTONE:
        for entrypoint, implementation in zip(
            task_layout.solution_entrypoints(task_dir, layout),
            task_layout.solution_implementations(task_dir, layout),
            strict=True,
        ):
            audit_solve(entrypoint, entrypoint.relative_to(task_dir).as_posix())
            audit_solve(implementation, implementation.relative_to(task_dir).as_posix())
    else:
        path = task_dir / "solution" / "solve.sh"
        audit_solve(path, path.relative_to(task_dir).as_posix())


def check_test_docstrings(report: Report, task_dir: Path, task_data: dict) -> None:
    section = "Test Requirements"
    files = list_verifier_py_files(task_dir, task_data)
    if not files:
        report.add(section, "pytest file with test docstrings", Status.FAIL, detail="no verifier .py found")
        return

    missing_all: list[str] = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                if not ast.get_docstring(node):
                    missing_all.append(f"{path.relative_to(task_dir)}::{node.name}")

    if missing_all:
        report.add(
            section,
            "informative docstrings on every test",
            Status.FAIL,
            detail="missing: " + ", ".join(missing_all[:6])
            + (" …" if len(missing_all) > 6 else ""),
        )
    else:
        report.add(section, "informative docstrings on every test", Status.PASS)


def check_legacy_canary_policy(report: Report, task_dir: Path) -> None:
    """Edition 2: canary strings are not required; legacy E1 patterns must be absent."""
    section = "Canary policy (Edition 2)"
    import run_static_checks as rsc

    reporter = rsc.Reporter()
    rsc.check_canary(task_dir, reporter)
    if reporter.has_failures():
        detail = reporter.failures[0] if reporter.failures else "legacy canary string found"
        report.add(section, "no legacy canary strings in task tree", Status.FAIL, detail=detail)
    else:
        report.add(
            section,
            "canary strings not required (Edition 2)",
            Status.PASS,
            detail="do not add harbor-canary / terminal-bench-canary markers",
        )
        report.add(section, "no legacy canary strings in task tree", Status.PASS)


def check_packaging_hygiene(report: Report, task_dir: Path) -> None:
    section = "Submission packaging"
    hits: list[str] = []
    for name in PACKAGING_FORBIDDEN_ROOT:
        if (task_dir / name).exists():
            hits.append(name)
    for path in task_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name.lower() in BANNED_AI_FILENAMES:
            hits.append(path.relative_to(task_dir).as_posix())
        for part in path.parts:
            if part in BANNED_AI_DIRS:
                hits.append(path.relative_to(task_dir).as_posix())
                break
    if hits:
        report.add(
            section,
            "no forbidden submission artifacts in task tree",
            Status.WARN,
            detail="remove before zipping: " + ", ".join(sorted(set(hits))[:10]),
        )
    else:
        report.add(section, "no forbidden submission artifacts in task tree", Status.PASS)


def run_subprocess_gate(
    report: Report,
    section: str,
    requirement: str,
    argv: list[str],
    *,
    skip: bool = False,
) -> None:
    if skip:
        report.add(section, requirement, Status.SKIP, detail="skipped (--quick)")
        return
    try:
        proc = subprocess.run(
            argv,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        report.add(section, requirement, Status.FAIL, detail=str(exc))
        return

    combined = (proc.stdout or "") + (proc.stderr or "")
    tail = "\n".join(combined.strip().splitlines()[-12:]) if combined.strip() else "(no output)"
    cmd = " ".join(argv)

    if proc.returncode == 0:
        report.add(section, requirement, Status.PASS, command=cmd)
    elif proc.returncode == 2:
        report.add(section, requirement, Status.WARN, detail=tail, command=cmd)
    else:
        report.add(section, requirement, Status.FAIL, detail=tail, command=cmd)


def add_manual_checklist(report: Report, task_name: str) -> None:
    section = "Manual (required before submit)"
    openai_model = model_policy.CURRENT_OPENAI_MODEL
    anthropic_model = model_policy.CURRENT_ANTHROPIC_MODEL
    task_path = root_adapter.ROOTS.task_dir(task_name)
    zip_path = root_adapter.ROOTS.submission_zip(task_name)
    items = [
        (
            "instruction.md quality (concise, no hints/answers, absolute paths)",
            "Review prose; optional: harbor tasks check … "
            f"-m {model_policy.QUALITY_CHECK_MODEL}",
        ),
        (
            "Tests cover every explicit and critical implicit requirement",
            "Map each instruction requirement to a test_* function",
        ),
        (
            "Difficulty: frontier pass rate < 80% (worst model)",
            f"stb harbor run -m {openai_model.harbor_flag} -p {task_path}\n"
            f"stb harbor run -m {anthropic_model.harbor_flag} -p {task_path}\n"
            "Run 5 trials per current model; calibrate difficulty in task.toml",
        ),
        (
            "Step 2b: oracle 1x PASS + NOP score 0.0",
            f"harbor run -p {task_path} -a oracle\n"
            f"harbor run -p {task_path} -a nop",
        ),
        (
            "Rubric: ≥3 distinct negative-reward criteria (e.g. -1)",
            "Author in Snorkel submission UI (not in task zip)",
        ),
        (
            "LLMaJ checks (behavior_in_task_description, anti_cheating, …)",
            f"harbor tasks check {task_path} -m {model_policy.QUALITY_CHECK_MODEL}",
        ),
        (
            "Delegated official CI: typos + check_task_sizes",
            "Confirm both checks PASS in the current upstream pre-submission result; "
            "local approval reports them as delegated, never inferred PASS",
        ),
        (
            "Preflight + packaging approval",
            f"./scripts/check-task.sh {task_path}\n"
            f"python3 approve_task.py --task-dir {task_path} --zip {zip_path} --skip-verifier-health",
        ),
    ]
    for req, cmd in items:
        report.add(section, req, Status.MANUAL, command=cmd)


def run_all_checks(task_dir: Path, *, quick: bool, run_ruff: bool) -> Report:
    task_name = task_dir.name
    report = Report(task_dir=task_dir, task_name=task_name)

    if not task_dir.is_dir():
        report.add("Setup", "task directory exists", Status.FAIL, detail=str(task_dir))
        return report

    try:
        task_data = load_task_toml(task_dir)
    except Exception as exc:
        report.add("Setup", "parse task.toml", Status.FAIL, detail=str(exc))
        add_manual_checklist(report, task_name)
        return report

    check_structural_layout(report, task_dir, task_data)
    check_task_toml_fields(report, task_dir, task_data)
    check_solution_standards(report, task_dir, task_data)
    check_test_docstrings(report, task_dir, task_data)
    check_legacy_canary_policy(report, task_dir)
    check_packaging_hygiene(report, task_dir)

    auto = "Automated CI / repo gates"
    run_subprocess_gate(
        report,
        auto,
        "run_static_checks.py (edition_2)",
        ["python3", str(REPO_ROOT / "run_static_checks.py"), "--task-dir", str(task_dir), "--version", "edition_2"],
    )
    run_subprocess_gate(
        report,
        auto,
        "dockerfile_check.py",
        ["python3", str(REPO_ROOT / "dockerfile_check.py"), str(task_dir)],
    )
    run_subprocess_gate(
        report,
        auto,
        "collapse_check.py (anti-trivialization RC1–RC7)",
        ["python3", str(REPO_ROOT / "collapse_check.py"), str(task_dir)],
        skip=quick,
    )

    if run_ruff:
        tests_dir = task_dir / "tests"
        if tests_dir.is_dir():
            run_subprocess_gate(
                report,
                auto,
                "ruff check tests/",
                ["ruff", "check", str(tests_dir)],
            )
        else:
            report.add(auto, "ruff check tests/", Status.SKIP, detail="no tests/ directory")
    else:
        report.add(
            auto,
            "ruff check tests/",
            Status.SKIP,
            detail="pass --ruff to enable",
        )

    add_manual_checklist(report, task_name)
    return report


STATUS_ICON = {
    Status.PASS: "✅",
    Status.FAIL: "❌",
    Status.WARN: "⚠️",
    Status.MANUAL: "📋",
    Status.SKIP: "⏭️",
}


def print_report(report: Report) -> None:
    print(f"=== Task Requirements Check: {report.task_name} ===")
    print(f"Path: {report.task_dir}\n")

    sections: list[str] = []
    for check in report.checks:
        if check.section not in sections:
            sections.append(check.section)

    for section in sections:
        print(f"## {section}")
        for check in report.checks:
            if check.section != section:
                continue
            icon = STATUS_ICON[check.status]
            line = f"  {icon} {check.requirement}"
            if check.detail:
                line += f"\n      → {check.detail}"
            if check.command and check.status == Status.MANUAL:
                for cmd_line in check.command.splitlines():
                    line += f"\n      $ {cmd_line}"
            print(line)
        print()

    n_pass = sum(1 for c in report.checks if c.status == Status.PASS)
    n_fail = sum(1 for c in report.checks if c.status == Status.FAIL)
    n_warn = sum(1 for c in report.checks if c.status == Status.WARN)
    n_manual = sum(1 for c in report.checks if c.status == Status.MANUAL)
    print(
        f"Summary: {n_pass} pass, {n_fail} fail, {n_warn} warn, {n_manual} manual "
        f"(manual items do not affect exit code)"
    )
    if report.has_fail:
        print("Result: FAIL — fix automated failures, then rerun.")
    elif report.has_warn:
        print("Result: WARN — automated checks passed with warnings.")
    else:
        print("Result: PASS — automated checks OK; complete manual items before submit.")


def print_json(report: Report) -> None:
    payload = {
        "task": report.task_name,
        "task_dir": str(report.task_dir),
        "exit_code": report.exit_code(),
        "checks": [
            {**asdict(c), "status": c.status.value} for c in report.checks
        ],
    }
    print(json.dumps(payload, indent=2))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a Terminal-Bench task against submission requirements.",
    )
    parser.add_argument(
        "task_dir",
        help="Path to task directory (e.g. tasks/my-task)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip collapse_check.py (faster structural pass)",
    )
    parser.add_argument(
        "--ruff",
        action="store_true",
        help="Also run ruff check on tests/",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON on stdout",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    task_dir = resolve_task_dir(args.task_dir)
    report = run_all_checks(task_dir, quick=args.quick, run_ruff=args.ruff)
    if args.json:
        print_json(report)
    else:
        print_report(report)
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
