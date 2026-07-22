"""Eligibility and evidence-backed exemption regressions for Slice 4."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import eligibility_policy
import sudhir_task


def _valid_exemption(rule_id: str, *, exemption_id: str = "ex-1") -> dict[str, object]:
    if rule_id == eligibility_policy.ui_building_rule_id():
        effective = eligibility_policy.UI_BUILDING_HOUSE_BLOCK_EFFECTIVE_DATE
    else:
        effective = dict(eligibility_policy.CATEGORY_BLOCKS).get(
            rule_id.removeprefix("official.category.").removesuffix(".blocked"),
            eligibility_policy.MILESTONE_BLOCK_EFFECTIVE_DATE,
        )
    return {
        "id": exemption_id,
        "rule_id": rule_id,
        "effective_date": effective,
        "recorded_at": "2026-07-21T00:00:00Z",
        "source": "stb submissions list",
        "platform_state": "NEEDS_REVISION",
        "evidence": ["sudhir_reviews/example/REV-1/ELIGIBILITY.md"],
        "reason": "Submission is already in the revision queue.",
        "status": "active",
    }


class EligibilityPolicyRegressionTest(unittest.TestCase):
    def test_current_unblocked_category_is_eligible(self) -> None:
        record = {"category": "security", **eligibility_policy.new_record_policy_fields()}
        result = eligibility_policy.evaluate(record, action="idea-uniqueness")
        self.assertEqual(result.official_status, "eligible")
        self.assertFalse(result.blocking)

    def test_current_blocked_category_fails_before_uniqueness(self) -> None:
        record = {
            "category": "data-processing",
            **eligibility_policy.new_record_policy_fields(),
        }
        result = eligibility_policy.evaluate(record, action="idea-uniqueness")
        self.assertEqual(result.official_status, "blocked")
        self.assertTrue(result.blocking)
        self.assertIn(
            eligibility_policy.category_rule_id("data-processing"),
            result.rule_ids,
        )

    def test_current_milestone_task_is_blocked(self) -> None:
        record = eligibility_policy.new_record_policy_fields()
        record["category"] = "security"
        record["number_of_milestones"] = 2
        result = eligibility_policy.evaluate(record, action="task-registration")
        self.assertTrue(result.blocking)
        self.assertIn(eligibility_policy.milestone_rule_id(), result.rule_ids)

    def test_net_new_ui_is_officially_eligible_but_house_blocked(self) -> None:
        record = {
            "category": "security",
            **eligibility_policy.new_record_policy_fields(),
        }
        record["subcategories"] = ["ui_building"]
        result = eligibility_policy.evaluate(record, action="idea-uniqueness")
        self.assertEqual(result.official_status, "eligible")
        self.assertEqual(result.house_status, "blocked")
        self.assertTrue(result.blocking)
        self.assertIn(eligibility_policy.ui_building_rule_id(), result.house_rule_ids)
        payload = result.to_dict(action="idea-uniqueness", evaluated_at="now")
        self.assertFalse(payload["official"]["blocking"])
        self.assertTrue(payload["house"]["blocking"])

    def test_evidence_backed_ui_revision_is_house_exempt(self) -> None:
        record = {
            "category": "security",
            **eligibility_policy.new_record_policy_fields(),
        }
        record["subcategories"] = ["ui_building"]
        record["in_flight_exemptions"] = [
            _valid_exemption(eligibility_policy.ui_building_rule_id())
        ]
        result = eligibility_policy.evaluate(record, action="package")
        self.assertEqual(result.official_status, "eligible")
        self.assertEqual(result.house_status, "exempt-in-flight")
        self.assertFalse(result.blocking)

    def test_valid_revision_evidence_exempts_current_block(self) -> None:
        record = {
            "category": "data-processing",
            **eligibility_policy.new_record_policy_fields(),
        }
        exemption = _valid_exemption(
            eligibility_policy.category_rule_id("data-processing")
        )
        record["in_flight_exemptions"] = [exemption]
        result = eligibility_policy.evaluate(record, action="package")
        self.assertEqual(result.official_status, "exempt-in-flight")
        self.assertFalse(result.blocking)
        self.assertEqual(result.exemption_ids, ("ex-1",))

    def test_bare_boolean_or_missing_evidence_cannot_exempt(self) -> None:
        record = {
            "category": "data-processing",
            **eligibility_policy.new_record_policy_fields(),
        }
        record["in_flight_exemptions"] = [
            {
                "id": "invalid",
                "rule_id": eligibility_policy.category_rule_id("data-processing"),
                "status": "active",
                "platform_state": "NEEDS_REVISION",
                "source": "",
                "evidence": [],
                "reason": "",
            }
        ]
        result = eligibility_policy.evaluate(record, action="package")
        self.assertTrue(result.blocking)
        self.assertNotEqual(result.official_status, "exempt-in-flight")

    def test_pre_adr_record_is_readable_but_shipping_requires_evidence(self) -> None:
        record: dict[str, object] = {"category": "data-processing"}
        self.assertTrue(eligibility_policy.ensure_record_policy_fields(record))
        view = eligibility_policy.evaluate(record, action="view")
        package = eligibility_policy.evaluate(record, action="package")
        self.assertEqual(view.official_status, "grandfathered-pending-review")
        self.assertFalse(view.blocking)
        self.assertEqual(package.official_status, "grandfathered-pending-review")
        self.assertTrue(package.blocking)

    def test_load_registry_adds_pre_adr_defaults_without_losing_fields(self) -> None:
        old = {
            "schema_version": 2,
            "ideas": {
                "old": {
                    "id": "IDEA-9999",
                    "slug": "old",
                    "status": "captured",
                    "category": "security",
                }
            },
            "tasks": {"old": {"slug": "old", "category": "security"}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(json.dumps(old), encoding="utf-8")
            with mock.patch.object(sudhir_task, "REGISTRY_PATH", path):
                loaded = sudhir_task.load_registry()
        self.assertEqual(loaded["schema_version"], 3)
        self.assertEqual(
            loaded["ideas"]["old"]["policy_snapshot_id"],
            eligibility_policy.PRE_ADR_POLICY_SNAPSHOT_ID,
        )
        self.assertEqual(loaded["tasks"]["old"]["slug"], "old")

    def test_blocked_new_idea_cannot_record_uniqueness_pass(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-idea",
            category="data-processing",
        )
        registry["ideas"]["blocked-idea"] = idea
        sudhir_task_test_complete_uniqueness(idea)
        args = SimpleNamespace(
            slug="blocked-idea",
            verdict="passed",
            scope=None,
            evidence=None,
            domain=None,
            mechanism=None,
            topology=None,
            verification=None,
            closest=None,
            difference=None,
            reason=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_idea_uniqueness(args)
        self.assertEqual(exit_code, 1)
        self.assertNotEqual(idea["uniqueness"]["status"], "passed")

    def test_ui_idea_cannot_record_uniqueness_pass(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-ui",
            category="security",
            subcategories=["ui_building"],
        )
        registry["ideas"]["blocked-ui"] = idea
        sudhir_task_test_complete_uniqueness(idea)
        args = SimpleNamespace(
            slug="blocked-ui",
            verdict="passed",
            scope=None,
            evidence=None,
            domain=None,
            mechanism=None,
            topology=None,
            verification=None,
            closest=None,
            difference=None,
            reason=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_idea_uniqueness(args)
        self.assertEqual(exit_code, 1)
        self.assertNotEqual(idea["uniqueness"]["status"], "passed")

    def test_blocked_new_idea_cannot_record_step2a_go(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-go",
            category="software-engineering",
        )
        registry["ideas"]["blocked-go"] = idea
        sudhir_task_test_complete_uniqueness(idea)
        idea["uniqueness"]["status"] = "passed"
        args = SimpleNamespace(
            slug="blocked-go",
            verdict="go",
            attempt=1,
            evidence=["sudhir_ideas/specs/blocked-go.md"],
            reason=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_idea_validation(args)
        self.assertEqual(exit_code, 1)
        self.assertNotEqual(idea["validation"]["status"], "go")

    def test_blocked_current_idea_cannot_register_task(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-registration",
            category="debugging",
        )
        registry["ideas"]["blocked-registration"] = idea
        args = SimpleNamespace(
            slug="blocked-registration",
            force=False,
            title=None,
            category=None,
            languages=None,
            number_of_milestones=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_new(args)
        self.assertEqual(exit_code, 1)
        self.assertNotIn("blocked-registration", registry["tasks"])

    def test_ui_idea_cannot_register_task(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-ui-registration",
            category="security",
            subcategories=["ui_building"],
        )
        registry["ideas"]["blocked-ui-registration"] = idea
        args = SimpleNamespace(
            slug="blocked-ui-registration",
            force=False,
            title=None,
            category=None,
            languages=None,
            subcategories=None,
            number_of_milestones=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_new(args)
        self.assertEqual(exit_code, 1)
        self.assertNotIn("blocked-ui-registration", registry["tasks"])

    def test_pre_adr_blocked_task_needs_evidence_before_submitted_phase(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "old-submission",
            category="data-processing",
            status="grandfathered",
        )
        task = sudhir_task.new_entry("old-submission")
        task.update(
            {
                "category": "data-processing",
                "idea_slug": "old-submission",
                "phase": "package",
                "policy_snapshot_id": eligibility_policy.PRE_ADR_POLICY_SNAPSHOT_ID,
            }
        )
        idea["task_slug"] = "old-submission"
        registry["ideas"]["old-submission"] = idea
        registry["tasks"]["old-submission"] = task
        args = SimpleNamespace(slug="old-submission", phase="submitted", next=None)
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_phase(args)
        self.assertEqual(exit_code, 1)
        self.assertEqual(task["phase"], "package")

    def test_blocked_current_task_stops_before_package_build(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "blocked-package",
            category="data-processing",
            status="grandfathered",
        )
        task = sudhir_task.new_entry("blocked-package")
        task.update(
            {
                "category": "data-processing",
                "idea_slug": "blocked-package",
                "phase": "review",
            }
        )
        idea["task_slug"] = "blocked-package"
        registry["ideas"]["blocked-package"] = idea
        registry["tasks"]["blocked-package"] = task
        args = SimpleNamespace(slug="blocked-package", force=True, skip_approve=True)
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "blocked-package"
            task_dir.mkdir()
            with (
                mock.patch.object(sudhir_task, "TASKS_DIR", Path(tmp)),
                mock.patch.object(sudhir_task, "load_registry", return_value=registry),
                mock.patch.object(sudhir_task, "save_registry"),
                mock.patch.object(sudhir_task, "write_board"),
                mock.patch.object(sudhir_task, "enrich_from_source"),
                mock.patch.object(sudhir_task, "_build_submission_zip") as build_zip,
            ):
                exit_code = sudhir_task.cmd_package(args)
        self.assertEqual(exit_code, 1)
        build_zip.assert_not_called()
        self.assertEqual(task["phase"], "review")

    def test_exemption_capture_updates_linked_idea_and_task(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "revision-task",
            category="data-processing",
        )
        task = sudhir_task.new_entry("revision-task")
        task.update({"category": "data-processing", "idea_slug": "revision-task"})
        idea["task_slug"] = "revision-task"
        registry["ideas"]["revision-task"] = idea
        registry["tasks"]["revision-task"] = task
        args = SimpleNamespace(
            slug="revision-task",
            rule_id=eligibility_policy.category_rule_id("data-processing"),
            exemption_id="revision-task-exemption",
            effective_date=None,
            platform_state="NEEDS_REVISION",
            source="stb submissions list",
            evidence=["sudhir_reviews/revision-task/REV-1/ELIGIBILITY.md"],
            reason="Already in the revision queue.",
            first_submitted_at=None,
        )
        with (
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_exemption_capture(args)
        self.assertEqual(exit_code, 0)
        for record in (idea, task):
            self.assertEqual(len(record["in_flight_exemptions"]), 1)
            self.assertEqual(
                record["eligibility_verdict"]["official"]["status"],
                "exempt-in-flight",
            )

    def test_ui_exemption_capture_reads_subcategory_from_task_source(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "revision-ui",
            category="security",
        )
        task = sudhir_task.new_entry("revision-ui")
        task.update({"category": "security", "idea_slug": "revision-ui"})
        idea["task_slug"] = "revision-ui"
        registry["ideas"]["revision-ui"] = idea
        registry["tasks"]["revision-ui"] = task
        args = SimpleNamespace(
            slug="revision-ui",
            rule_id=eligibility_policy.ui_building_rule_id(),
            exemption_id="revision-ui-exemption",
            effective_date=None,
            platform_state="NEEDS_REVISION",
            source="stb submissions list",
            evidence=["sudhir_reviews/revision-ui/REV-1/ELIGIBILITY.md"],
            reason="Already in the revision queue.",
            first_submitted_at=None,
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            tasks_dir = repo / "tasks"
            source = tasks_dir / "revision-ui"
            source.mkdir(parents=True)
            (source / "task.toml").write_text(
                'version = "2.0"\n[metadata]\ncategory = "security"\n'
                'languages = ["typescript"]\nsubcategories = ["ui_building"]\n'
                "number_of_milestones = 0\n",
                encoding="utf-8",
            )
            with (
                mock.patch.object(sudhir_task, "REPO_ROOT", repo),
                mock.patch.object(sudhir_task, "TASKS_DIR", tasks_dir),
                mock.patch.object(sudhir_task, "load_registry", return_value=registry),
                mock.patch.object(sudhir_task, "save_registry"),
                mock.patch.object(sudhir_task, "write_board"),
            ):
                exit_code = sudhir_task.cmd_exemption_capture(args)
        self.assertEqual(exit_code, 0)
        for record in (idea, task):
            self.assertEqual(record["subcategories"], ["ui_building"])
            self.assertEqual(
                record["eligibility_verdict"]["house"]["status"],
                "exempt-in-flight",
            )

    def test_board_exposes_eligibility_without_losing_status_axes(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(registry, "board-idea", category="security")
        sudhir_task._refresh_eligibility(idea, action="package")
        registry["ideas"]["board-idea"] = idea
        board = sudhir_task.render_board(registry)
        self.assertIn("| Execution | Submission | Platform | Eligibility |", board)
        self.assertIn("| ELIGIBLE |", board)
        self.assertEqual(idea["eligibility_verdict"]["action"], "package")

    def test_board_distinguishes_official_and_house_ui_verdicts(self) -> None:
        registry = sudhir_task.empty_registry()
        idea = sudhir_task.new_idea_entry(
            registry,
            "board-ui",
            category="security",
            subcategories=["ui_building"],
        )
        registry["ideas"]["board-ui"] = idea
        board = sudhir_task.render_board(registry)
        self.assertIn("ELIGIBLE / HOUSE BLOCKED", board)

    def test_current_authoring_guidance_names_live_blocks(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        category_files = (
            "sudhir_knowledge/TASK_LIFECYCLE.md",
            "task-type-taxonomy.md",
            ".cursor/rules/idea-validation.mdc",
            ".cursor/rules/task-creation.mdc",
            "web/terminal-bench-task-creation.md",
            "web/bulk-idea-generation.md",
            "web/option-a-seed-refinement.md",
            "web/chatgpt-task-authoring-playbook.md",
        )
        for relative in category_files:
            text = (repo / relative).read_text(encoding="utf-8").lower()
            with self.subTest(path=relative):
                self.assertIn("data-processing", text)
                self.assertIn("blocked", text)
        for relative in (
            "sudhir_knowledge/TASK_LIFECYCLE.md",
            ".cursor/rules/idea-validation.mdc",
            ".cursor/rules/task-creation.mdc",
            "web/terminal-bench-task-creation.md",
            "web/option-a-seed-refinement.md",
            "web/chatgpt-task-authoring-playbook.md",
        ):
            text = (repo / relative).read_text(encoding="utf-8").lower()
            with self.subTest(path=relative):
                self.assertIn("milestone", text)
                self.assertIn("blocked", text)

    def test_retired_ui_scaffold_and_python_compatibility_guidance(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        retired = repo / "skeleton" / "UI_Task_Skeleton"
        self.assertEqual([path for path in retired.rglob("*") if path.is_file()], [])

        skeleton_index = (repo / "skeleton" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("UI_Task_Skeleton", skeleton_index)
        guidance = (repo / ".cursor" / "rules" / "task-creation.mdc").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("skeleton/UI_Task_Skeleton", guidance)
        self.assertIn("Playwright's **Python** bindings", guidance)
        self.assertIn("JavaScript/Vitest", guidance)


def sudhir_task_test_complete_uniqueness(idea: dict[str, object]) -> None:
    uniqueness = idea["uniqueness"]
    assert isinstance(uniqueness, dict)
    uniqueness.update(
        {
            "scope": sorted(sudhir_task.REQUIRED_UNIQUENESS_SCOPES),
            "evidence": ["sudhir_research/example.md"],
            "closest_analogue": "nearest",
            "differentiator": "different mechanism and topology",
        }
    )
    fingerprint = uniqueness["fingerprint"]
    assert isinstance(fingerprint, dict)
    fingerprint.update(
        {
            "domain": "domain",
            "mechanism": "mechanism",
            "topology": "topology",
            "verification": "verification",
        }
    )


if __name__ == "__main__":
    unittest.main()
