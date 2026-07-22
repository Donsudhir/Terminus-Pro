"""Regression coverage for shared-layout consumer activation."""

from __future__ import annotations

import unittest
from pathlib import Path

import collapse_check
import requirements_check
import run_static_checks
import task_layout

REPO_ROOT = Path(__file__).resolve().parents[1]
MILESTONE_SKELETON = REPO_ROOT / "skeleton" / "milestone_template"


class TaskLayoutConsumerRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.task_data = run_static_checks.load_toml_file(MILESTONE_SKELETON / "task.toml")

    def test_static_consumers_accept_current_milestone_paths(self) -> None:
        reporter = run_static_checks.run_checks(
            MILESTONE_SKELETON,
            {"required_files", "task_structure", "test_sh", "instruction"},
        )
        self.assertEqual(reporter.failures, [])
        self.assertEqual(reporter.warnings, [])

    def test_requirements_consumer_uses_shared_layout(self) -> None:
        report = requirements_check.Report(
            task_dir=MILESTONE_SKELETON,
            task_name=MILESTONE_SKELETON.name,
        )
        requirements_check.check_structural_layout(report, MILESTONE_SKELETON, self.task_data)
        canonical = [
            check
            for check in report.checks
            if check.requirement == "canonical task layout"
        ]
        self.assertEqual(len(canonical), 1)
        self.assertEqual(canonical[0].status, requirements_check.Status.PASS)
        self.assertIn("milestone; milestones=2", canonical[0].detail)

    def test_collapse_consumer_aggregates_step_local_surfaces(self) -> None:
        layout = task_layout.classify_task_dir(MILESTONE_SKELETON, self.task_data)
        self.assertTrue(layout.valid)
        self.assertIn("/app/hello.txt", collapse_check.load_instruction(MILESTONE_SKELETON))
        self.assertIn("TestMilestone2", collapse_check.load_tests(MILESTONE_SKELETON))
        sources = {
            source["path"]
            for source in collapse_check.analyze_oracle(MILESTONE_SKELETON)["sources"]
        }
        self.assertEqual(
            sources,
            {
                "steps/milestone_1/solution/solve.sh",
                "steps/milestone_2/solution/solve.sh",
            },
        )


if __name__ == "__main__":
    unittest.main()
