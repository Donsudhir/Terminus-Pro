"""Shared standard/current-milestone/legacy layout classifier regressions."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import task_layout


def standard_files() -> set[str]:
    return {
        "task.toml",
        "instruction.md",
        "environment/Dockerfile",
        "tests/test.sh",
        "tests/test_outputs.py",
        "solution/solve.sh",
    }


def milestone_files(count: int = 2) -> set[str]:
    files = {"task.toml", "environment/Dockerfile"}
    for index in range(1, count + 1):
        prefix = f"steps/milestone_{index}"
        files.update(
            {
                f"{prefix}/instruction.md",
                f"{prefix}/tests/test.sh",
                f"{prefix}/tests/test_m{index}.py",
                f"{prefix}/solution/solve.sh",
                f"{prefix}/solution/solve{index}.sh",
            }
        )
    return files


def standard_toml() -> dict[str, object]:
    return {
        "version": "2.0",
        "metadata": {"number_of_milestones": 0},
        "agent": {"timeout_sec": 900},
        "verifier": {"timeout_sec": 450},
        "environment": {"build_timeout_sec": 600},
    }


def milestone_toml(count: int = 2) -> dict[str, object]:
    return {
        "version": "2.0",
        "metadata": {"number_of_milestones": count},
        "environment": {"build_timeout_sec": 600},
        "steps": [
            {
                "name": f"milestone_{index}",
                "agent": {"timeout_sec": 900.0},
                "verifier": {"timeout_sec": 450.0},
            }
            for index in range(1, count + 1)
        ],
    }


class TaskLayoutRegressionTest(unittest.TestCase):
    def test_standard_inventory_is_valid(self) -> None:
        report = task_layout.classify_inventory(standard_files(), standard_toml())
        self.assertEqual(report.kind, task_layout.STANDARD)
        self.assertTrue(report.valid)
        self.assertEqual(report.milestone_count, 0)

    def test_current_milestone_inventory_is_valid(self) -> None:
        report = task_layout.classify_inventory(milestone_files(), milestone_toml())
        self.assertEqual(report.kind, task_layout.MILESTONE)
        self.assertTrue(report.valid)
        self.assertEqual(report.milestone_names, ("milestone_1", "milestone_2"))

    def test_legacy_root_layout_is_identified_not_misreported_as_standard(self) -> None:
        files = standard_files() | {
            "milestone_1.md",
            "milestone_2.md",
            "tests/test_m1.py",
            "tests/test_m2.py",
            "solution/solve1.sh",
            "solution/solve2.sh",
        }
        report = task_layout.classify_inventory(files, milestone_toml())
        self.assertEqual(report.kind, task_layout.LEGACY_MILESTONE)
        self.assertFalse(report.valid)
        self.assertIn("migrate to steps/milestone_N", report.errors[0])

    def test_one_milestone_is_invalid(self) -> None:
        report = task_layout.classify_inventory(milestone_files(1), milestone_toml(1))
        self.assertEqual(report.kind, task_layout.MILESTONE)
        self.assertFalse(report.valid)
        self.assertTrue(any("at least 2" in error for error in report.errors))

    def test_milestone_root_content_is_invalid(self) -> None:
        files = milestone_files() | {"instruction.md", "tests/test_outputs.py"}
        report = task_layout.classify_inventory(files, milestone_toml())
        self.assertFalse(report.valid)
        self.assertTrue(any("deprecated root-level" in error for error in report.errors))

    def test_step_names_and_count_must_match_directories(self) -> None:
        data = milestone_toml()
        data["metadata"] = {"number_of_milestones": 3}
        data["steps"][1]["name"] = "milestone_3"
        report = task_layout.classify_inventory(milestone_files(), data)
        self.assertFalse(report.valid)
        self.assertTrue(any("number_of_milestones" in error for error in report.errors))
        self.assertTrue(any("names do not match" in error for error in report.errors))

    def test_milestone_requires_per_step_timeouts_and_no_top_level_tables(self) -> None:
        data = milestone_toml()
        del data["steps"][0]["verifier"]
        data["agent"] = {"timeout_sec": 900}
        report = task_layout.classify_inventory(milestone_files(), data)
        self.assertFalse(report.valid)
        self.assertTrue(any("top-level" in error for error in report.errors))
        self.assertTrue(any("verifier" in error for error in report.errors))

    def test_source_helpers_point_inside_each_current_milestone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in milestone_files():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("x\n", encoding="utf-8")
            report = task_layout.classify_task_dir(root, milestone_toml())
            self.assertTrue(report.valid)
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in task_layout.instruction_paths(root, report)],
                [
                    "steps/milestone_1/instruction.md",
                    "steps/milestone_2/instruction.md",
                ],
            )
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in task_layout.verifier_paths(root, report)],
                [
                    "steps/milestone_1/tests/test_m1.py",
                    "steps/milestone_2/tests/test_m2.py",
                ],
            )
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in task_layout.solution_entrypoints(root, report)],
                [
                    "steps/milestone_1/solution/solve.sh",
                    "steps/milestone_2/solution/solve.sh",
                ],
            )


if __name__ == "__main__":
    unittest.main()
