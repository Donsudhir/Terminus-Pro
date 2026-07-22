"""Regression coverage for ADR-0012 dossier + CM-007 static gate."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run_static_checks
import sudhir_dossier
import sudhir_task


class SudhirDossierHelpersTest(unittest.TestCase):
    def test_suggest_cm_ids_from_pytest_shadow_feedback(self) -> None:
        text = "plant /app/pytest.py and sys.path shadow with confcutdir"
        self.assertIn("CM-007", sudhir_dossier.suggest_cm_ids(text))

    def test_preupload_requires_checked_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PREUPLOAD.md"
            path.write_text("- [ ] still open\n", encoding="utf-8")
            ok, _detail = sudhir_dossier.preupload_complete(path)
            self.assertFalse(ok)
            path.write_text("- [x] done\nREADY_FOR_PACKAGE: yes\n", encoding="utf-8")
            ok, _detail = sudhir_dossier.preupload_complete(path)
            self.assertTrue(ok)


class SudhirTaskDossierCommandsTest(unittest.TestCase):
    def test_revise_creates_rev_workspace_with_form_stubs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews = root / "reviews"
            registry = root / "registry.json"
            submissions = root / "subs"
            submissions.mkdir()
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "ideas": {},
                        "tasks": {
                            "demo-task": sudhir_task.new_entry("demo-task"),
                        },
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(sudhir_task, "REPO_ROOT", root), mock.patch.object(
                sudhir_task, "REVIEWS_DIR", reviews
            ), mock.patch.object(sudhir_task, "SUBMISSIONS_DIR", submissions), mock.patch.object(
                sudhir_task, "REGISTRY_PATH", registry
            ), mock.patch.object(sudhir_task, "BOARD_PATH", root / "BOARD.md"), mock.patch.object(
                sudhir_task, "IDEA_INDEX_PATH", root / "IDEA_INDEX.md"
            ), mock.patch.object(sudhir_task, "STATUS_PATH", root / "STATUS.md"
            ), mock.patch.object(sudhir_task, "IDEAS_DIR", root / "ideas"):
                (root / "ideas").mkdir()
                rc = sudhir_task.cmd_revise(
                    type("A", (), {"slug": "demo-task", "reason": "unit-test revise"})()
                )
                self.assertEqual(rc, 0)
                rev_dir = reviews / "demo-task" / "REV-1"
                self.assertTrue((rev_dir / "NOTES.md").is_file())
                self.assertTrue((rev_dir / "FEEDBACK.md").is_file())
                self.assertTrue((rev_dir / "DIFFICULTY.md").is_file())
                self.assertTrue((rev_dir / "SOLUTION.md").is_file())
                self.assertTrue((rev_dir / "VERIFICATION.md").is_file())
                self.assertTrue((rev_dir / "RUBRIC.md").is_file())
                self.assertTrue((rev_dir / "PREUPLOAD.md").is_file())
                data = json.loads(registry.read_text(encoding="utf-8"))
                self.assertEqual(data["tasks"]["demo-task"]["revision"], 1)
                self.assertEqual(len(data["tasks"]["demo-task"]["revisions"]), 1)

    def test_form_capture_stores_all_paste_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews = root / "reviews"
            registry = root / "registry.json"
            submissions = root / "subs"
            submissions.mkdir()
            entry = sudhir_task.new_entry("form-task")
            entry["revision"] = 1
            registry.write_text(
                json.dumps({"schema_version": 2, "ideas": {}, "tasks": {"form-task": entry}}),
                encoding="utf-8",
            )
            texts = root / "paste"
            texts.mkdir()
            for name, body in {
                "d.txt": "This task is hard because unit test.",
                "s.txt": "The solution rebuilds the path.",
                "v.txt": "The tests checks exact cases.",
                "r.txt": "Agent emits report digest, +5\n",
            }.items():
                (texts / name).write_text(body, encoding="utf-8")
            with mock.patch.object(sudhir_task, "REPO_ROOT", root), mock.patch.object(
                sudhir_task, "REVIEWS_DIR", reviews
            ), mock.patch.object(sudhir_task, "SUBMISSIONS_DIR", submissions), mock.patch.object(
                sudhir_task, "REGISTRY_PATH", registry
            ), mock.patch.object(sudhir_task, "BOARD_PATH", root / "BOARD.md"), mock.patch.object(
                sudhir_task, "IDEA_INDEX_PATH", root / "IDEA_INDEX.md"
            ), mock.patch.object(sudhir_task, "IDEAS_DIR", root / "ideas"):
                (root / "ideas").mkdir()
                sudhir_dossier.open_revision_workspace(
                    reviews, entry, reason="form test"
                )
                # persist entry into registry after workspace open mutated it
                data = json.loads(registry.read_text(encoding="utf-8"))
                data["tasks"]["form-task"] = entry
                registry.write_text(json.dumps(data), encoding="utf-8")
                rc = sudhir_task.cmd_form_capture(
                    type(
                        "A",
                        (),
                        {
                            "slug": "form-task",
                            "difficulty_file": str(texts / "d.txt"),
                            "solution_file": str(texts / "s.txt"),
                            "verification_file": str(texts / "v.txt"),
                            "rubric_file": str(texts / "r.txt"),
                        },
                    )()
                )
                self.assertEqual(rc, 0)
                rev = reviews / "form-task" / "REV-1"
                self.assertIn("This task is hard because", (rev / "DIFFICULTY.md").read_text())
                self.assertIn("The solution rebuilds", (rev / "SOLUTION.md").read_text())
                self.assertIn("The tests checks", (rev / "VERIFICATION.md").read_text())
                self.assertIn("Agent emits report digest", (rev / "RUBRIC.md").read_text())


class Cm007StaticCheckTest(unittest.TestCase):
    def test_vulnerable_test_sh_fails_cm007(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task = Path(tmp) / "shadow-task"
            (task / "tests").mkdir(parents=True)
            (task / "tests" / "test_outputs.py").write_text(
                "def test_ok():\n    assert True\n", encoding="utf-8"
            )
            (task / "tests" / "test.sh").write_text(
                "#!/bin/bash\n"
                "mkdir -p /logs/verifier\n"
                'if [ "$PWD" = "/" ]; then\n'
                '    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."\n'
                "    echo 0 > /logs/verifier/reward.txt\n"
                "    exit 1\n"
                "fi\n"
                "python -m pytest -o cache_dir=/tmp/pytest_cache "
                "--ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA\n"
                "if [ $? -eq 0 ]; then\n"
                "    echo 1 > /logs/verifier/reward.txt\n"
                "else\n"
                "    echo 0 > /logs/verifier/reward.txt\n"
                "fi\n",
                encoding="utf-8",
            )
            task_data = {
                "metadata": {
                    "difficulty": "hard",
                    "category": "scientific-computing",
                    "languages": ["python"],
                    "number_of_milestones": 0,
                }
            }
            reporter = run_static_checks.Reporter()
            run_static_checks.check_test_sh(task, task_data, reporter)
            joined = "\n".join(reporter.failures)
            self.assertIn("CM-007", joined)

    def test_hardened_test_sh_passes_cm007(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            task = Path(tmp) / "safe-task"
            (task / "tests").mkdir(parents=True)
            (task / "tests" / "test_outputs.py").write_text(
                "def test_ok():\n    assert True\n", encoding="utf-8"
            )
            (task / "tests" / "test.sh").write_text(
                Path(
                    "/home/sudhir/Projects/TERMINUS/skeleton/Default_Task_Skeleton/tests/test.sh"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            task_data = {
                "metadata": {
                    "difficulty": "hard",
                    "category": "scientific-computing",
                    "languages": ["python"],
                    "number_of_milestones": 0,
                }
            }
            reporter = run_static_checks.Reporter()
            run_static_checks.check_test_sh(task, task_data, reporter)
            self.assertTrue(
                any("CM-007 pytest cwd-shadow hardening present" in msg for msg in reporter.passes)
            )
            self.assertFalse(any("CM-007" in msg for msg in reporter.failures))


if __name__ == "__main__":
    unittest.main()
