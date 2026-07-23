"""Regression coverage for ADR-0021 strict DSV Humanizer policy."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import dsv_humanizer
import sudhir_dossier
import sudhir_task

PASSING_TEXTS = {
    "difficulty": (
        "This task is hard because the visible failure can begin in several separate "
        "authorities that only disagree on carefully chosen inputs. A narrow patch often "
        "repairs the first symptom while leaving stored state or a neighboring execution "
        "path inconsistent. The solver must trace how identity, ordering, and validation "
        "travel through the complete operation instead of trusting one healthy run. Broad "
        "fallbacks are also unsafe since the valid fast path must keep its normal behavior."
    ),
    "solution": (
        "The repair establishes one authority for each decision and carries that value "
        "through every producer and consumer. It rebuilds derived state when the original "
        "source changes, rather than reusing a stale result. Strict validation rejects "
        "mismatched records before they can affect later work. The remaining paths preserve "
        "valid data and produce the same result when the operation is repeated."
    ),
    "verification": (
        "The tests checks generated failing cases beside healthy controls so a broad "
        "rejection cannot earn full reward. They compare observable results across equivalent "
        "modes and independently inspect the persisted evidence used by later operations. "
        "Tampered or mismatched inputs must fail closed. Repeat runs must keep the same "
        "accepted values while preserving the expected efficient path for valid inputs."
    ),
}


def validate_passing() -> dsv_humanizer.ValidationReport:
    return dsv_humanizer.validate_texts(
        difficulty=PASSING_TEXTS["difficulty"],
        solution=PASSING_TEXTS["solution"],
        verification=PASSING_TEXTS["verification"],
    )


class DsvHumanizerPolicyTest(unittest.TestCase):
    def test_passing_set_satisfies_strict_contract(self) -> None:
        report = validate_passing()
        self.assertTrue(report.ok, dsv_humanizer.format_findings(report))
        self.assertEqual(report.normalized, PASSING_TEXTS)
        self.assertEqual(report.metrics["difficulty"]["sentences"], 4)
        self.assertEqual(report.metrics["solution"]["sentences"], 4)
        self.assertEqual(report.metrics["verification"]["sentences"], 4)

    def test_rejects_humanizer_patterns_and_forbidden_punctuation(self) -> None:
        report = dsv_humanizer.validate_texts(
            difficulty=PASSING_TEXTS["difficulty"].replace(
                "the visible failure", "a vibrant tapestry that underscores the importance"
            ),
            solution=PASSING_TEXTS["solution"].replace(
                "one authority", "one crucial authority—without compromise"
            ),
            verification=PASSING_TEXTS["verification"],
        )
        codes = {finding.code for finding in report.findings}
        self.assertIn("H01", codes)
        self.assertIn("H04", codes)
        self.assertIn("H07", codes)
        self.assertIn("DSV009", codes)

    def test_rejects_wrong_openers_markdown_and_partial_shape(self) -> None:
        report = dsv_humanizer.validate_texts(
            difficulty="## Hard\n\n" + PASSING_TEXTS["difficulty"],
            solution=PASSING_TEXTS["solution"],
            verification=PASSING_TEXTS["verification"].replace(
                "The tests checks", "The verifier checks"
            ),
        )
        codes = {finding.code for finding in report.findings}
        self.assertIn("DSV002", codes)
        self.assertIn("DSV003", codes)
        self.assertIn("DSV006", codes)

    def test_audit_hash_detects_later_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rev = Path(tmp)
            files = sudhir_dossier.dsv_form_paths(rev)
            for field, path in files.items():
                sudhir_dossier.write_capture_file(
                    path,
                    f"{field} test",
                    PASSING_TEXTS[field],
                )
            report = dsv_humanizer.validate_files(files)
            self.assertTrue(report.ok, dsv_humanizer.format_findings(report))
            audit = rev / dsv_humanizer.AUDIT_FILENAME
            dsv_humanizer.write_audit(audit, report, files)
            payload = json.loads(audit.read_text(encoding="utf-8"))
            self.assertEqual(payload["scope"], list(dsv_humanizer.FIELD_ORDER))
            self.assertEqual(
                payload["acceptance_precedence"],
                list(dsv_humanizer.ACCEPTANCE_PRECEDENCE),
            )
            self.assertEqual(payload["transformation_boundary"], "wording-and-rhythm-only")
            self.assertEqual(
                dsv_humanizer.verify_audit(audit, files),
                (True, "acceptance-safe DSV Humanizer audit matches current form files"),
            )
            files["solution"].write_text(
                files["solution"].read_text(encoding="utf-8") + "Changed.\n",
                encoding="utf-8",
            )
            ok, detail = dsv_humanizer.verify_audit(audit, files)
            self.assertFalse(ok)
            self.assertIn("changed after strict Humanizer audit", detail)

    def test_audit_rejects_broader_transformation_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rev = Path(tmp)
            files = sudhir_dossier.dsv_form_paths(rev)
            for field, path in files.items():
                sudhir_dossier.write_capture_file(path, field, PASSING_TEXTS[field])
            report = dsv_humanizer.validate_files(files)
            self.assertTrue(report.ok, dsv_humanizer.format_findings(report))
            audit = rev / dsv_humanizer.AUDIT_FILENAME
            dsv_humanizer.write_audit(audit, report, files)
            payload = json.loads(audit.read_text(encoding="utf-8"))
            payload["transformation_boundary"] = "semantic-rewrite"
            audit.write_text(json.dumps(payload), encoding="utf-8")
            ok, detail = dsv_humanizer.verify_audit(audit, files)
            self.assertFalse(ok)
            self.assertIn("invalid Humanizer transformation boundary", detail)

    def test_new_preupload_template_requires_dsv_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rev = Path(tmp)
            preupload = rev / "PREUPLOAD.md"
            preupload.write_text(
                sudhir_dossier.preupload_template(1, "test"),
                encoding="utf-8",
            )
            ok, detail = sudhir_dossier.preupload_complete(preupload)
            self.assertFalse(ok)
            self.assertIn(dsv_humanizer.AUDIT_FILENAME, detail)

    def test_agent_and_cursor_skills_are_byte_identical(self) -> None:
        root = Path(__file__).resolve().parent.parent
        relative_files = (
            "SKILL.md",
            "references/HUMANIZER-POLICY.md",
            "references/LICENSE",
        )
        for relative in relative_files:
            agent = root / ".agents/skills/terminus-dsv-humanizer" / relative
            cursor = root / ".cursor/skills/terminus-dsv-humanizer" / relative
            self.assertEqual(agent.read_bytes(), cursor.read_bytes(), relative)
        skill = (
            root / ".agents/skills/terminus-dsv-humanizer/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: terminus-dsv-humanizer\n"))
        self.assertIn(dsv_humanizer.UPSTREAM_COMMIT, skill)


class DsvFormCaptureIntegrationTest(unittest.TestCase):
    def _patched_workspace(self, root: Path):
        reviews = root / "reviews"
        registry = root / "registry.json"
        submissions = root / "subs"
        tasks = root / "tasks"
        ideas = root / "ideas"
        submissions.mkdir()
        tasks.mkdir()
        ideas.mkdir()
        entry = sudhir_task.new_entry("strict-form-task")
        entry["revision"] = 1
        sudhir_dossier.open_revision_workspace(reviews, entry, reason="strict form test")
        registry.write_text(
            json.dumps(
                {
                    "schema_version": sudhir_task.REGISTRY_SCHEMA_VERSION,
                    "ideas": {},
                    "tasks": {"strict-form-task": entry},
                }
            ),
            encoding="utf-8",
        )
        patches = (
            mock.patch.object(sudhir_task, "REPO_ROOT", root),
            mock.patch.object(sudhir_task, "REVIEWS_DIR", reviews),
            mock.patch.object(sudhir_task, "SUBMISSIONS_DIR", submissions),
            mock.patch.object(sudhir_task, "TASKS_DIR", tasks),
            mock.patch.object(sudhir_task, "REGISTRY_PATH", registry),
            mock.patch.object(sudhir_task, "BOARD_PATH", root / "BOARD.md"),
            mock.patch.object(sudhir_task, "STATUS_PATH", root / "STATUS.md"),
            mock.patch.object(sudhir_task, "IDEA_INDEX_PATH", root / "IDEA_INDEX.md"),
            mock.patch.object(sudhir_task, "IDEAS_DIR", ideas),
        )
        return reviews, registry, tasks, patches

    def test_partial_dsv_capture_fails_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews, registry, _tasks, patches = self._patched_workspace(root)
            difficulty = root / "difficulty.txt"
            difficulty.write_text(PASSING_TEXTS["difficulty"], encoding="utf-8")
            before = registry.read_bytes()
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8]:
                rc = sudhir_task.cmd_form_capture(
                    type(
                        "A",
                        (),
                        {
                            "slug": "strict-form-task",
                            "difficulty_file": str(difficulty),
                            "solution_file": None,
                            "verification_file": None,
                            "rubric_file": None,
                        },
                    )()
                )
            self.assertEqual(rc, 1)
            self.assertEqual(registry.read_bytes(), before)
            audit = reviews / "strict-form-task/REV-1" / dsv_humanizer.AUDIT_FILENAME
            self.assertFalse(audit.exists())

    def test_passing_atomic_capture_writes_hash_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews, registry, tasks, patches = self._patched_workspace(root)
            task = tasks / "strict-form-task"
            task.mkdir()
            instruction = task / "instruction.md"
            instruction.write_text("Task source must remain byte-identical.\n", encoding="utf-8")
            instruction_before = instruction.read_bytes()
            source_files: dict[str, Path] = {}
            for field, body in PASSING_TEXTS.items():
                source_files[field] = root / f"{field}.txt"
                source_files[field].write_text(body, encoding="utf-8")
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8]:
                rc = sudhir_task.cmd_form_capture(
                    type(
                        "A",
                        (),
                        {
                            "slug": "strict-form-task",
                            "difficulty_file": str(source_files["difficulty"]),
                            "solution_file": str(source_files["solution"]),
                            "verification_file": str(source_files["verification"]),
                            "rubric_file": None,
                        },
                    )()
                )
            self.assertEqual(rc, 0)
            rev = reviews / "strict-form-task/REV-1"
            ok, detail = sudhir_dossier.strict_dsv_complete(rev)
            self.assertTrue(ok, detail)
            self.assertEqual(instruction.read_bytes(), instruction_before)
            data = json.loads(registry.read_text(encoding="utf-8"))
            ref = data["tasks"]["strict-form-task"]["learning"]["form_refs"]["dsv_audit"]
            self.assertTrue(ref.endswith(dsv_humanizer.AUDIT_FILENAME))

    def test_rubric_only_capture_never_invokes_humanizer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviews, _registry, _tasks, patches = self._patched_workspace(root)
            rubric = root / "rubric.txt"
            rubric_body = (
                "Agent produces a vibrant report—this wording is intentionally outside "
                "the DSV policy, +5\n"
            )
            rubric.write_text(rubric_body, encoding="utf-8")
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8], mock.patch.object(
                dsv_humanizer,
                "validate_texts",
                side_effect=AssertionError("Humanizer must not inspect rubric prose"),
            ):
                rc = sudhir_task.cmd_form_capture(
                    type(
                        "A",
                        (),
                        {
                            "slug": "strict-form-task",
                            "difficulty_file": None,
                            "solution_file": None,
                            "verification_file": None,
                            "rubric_file": str(rubric),
                        },
                    )()
                )
            self.assertEqual(rc, 0)
            rev = reviews / "strict-form-task/REV-1"
            self.assertIn(rubric_body.strip(), (rev / "RUBRIC.md").read_text(encoding="utf-8"))
            self.assertFalse((rev / dsv_humanizer.AUDIT_FILENAME).exists())

    def test_package_force_cannot_bypass_missing_dsv_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _reviews, _registry, tasks, patches = self._patched_workspace(root)
            (tasks / "strict-form-task").mkdir()
            args = type(
                "A",
                (),
                {"slug": "strict-form-task", "force": True, "skip_approve": True},
            )()
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7], patches[8], mock.patch.object(
                sudhir_task, "_task_execution_gaps", return_value=[]
            ), mock.patch.object(
                sudhir_task, "_eligibility_gaps", return_value=[]
            ), mock.patch.object(sudhir_task, "enrich_from_source"):
                rc = sudhir_task.cmd_package(args)
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
