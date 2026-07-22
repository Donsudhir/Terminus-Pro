"""Task Idea Proposal form and lifecycle gate regressions."""

from __future__ import annotations

import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import idea_proposal
import sudhir_task

REPO_ROOT = Path(__file__).resolve().parents[1]

VALID_SUMMARY = (
    "An existing offline build workspace produces inconsistent artifacts after a cached dependency graph is restored. "
    "Repair the workspace so clean and restored builds agree while preserving the supported build variants."
)
VALID_CATEGORY = "Build / Compilation / Dependency Management"
VALID_SKILLS = "CMake,dependency resolution,artifact provenance,shell scripting,build debugging"
VALID_TAGS = "cmake,build-cache,dependencies"


def test_category_labels_normalize_to_local_slugs() -> None:
    assert idea_proposal.normalize_category("Scientific Computing") == (
        "Scientific Computing",
        "scientific-computing",
    )
    assert idea_proposal.normalize_category("security") == (
        "Security / Cryptography / Vulnerability Demonstration",
        "security",
    )


def test_form_contract_accepts_required_counts() -> None:
    errors = idea_proposal.field_errors(
        summary=VALID_SUMMARY,
        category=VALID_CATEGORY,
        skills=VALID_SKILLS.split(","),
        tags=VALID_TAGS.split(","),
    )
    assert errors == []


def test_form_contract_rejects_incomplete_fields() -> None:
    errors = idea_proposal.field_errors(
        summary="One sentence only.",
        category="Unknown category",
        skills=["one"],
        tags=["one", "two"],
    )
    assert any("2-5 sentences" in error for error in errors)
    assert any("Idea Category" in error for error in errors)
    assert any("5-10" in error for error in errors)
    assert any("3-6" in error for error in errors)


def test_new_idea_cannot_pass_uniqueness_before_proposal() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "proposal-first")
    assert "platform Task Idea Proposal check is not passed" in sudhir_task._uniqueness_gaps(
        idea
    )
    idea["proposal_check"]["status"] = "passed"
    assert "platform Task Idea Proposal check is not passed" not in sudhir_task._uniqueness_gaps(
        idea
    )


def test_board_exposes_pending_proposal_before_downstream_actions() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "board-proposal")
    idea["next_action"] = "Stale downstream action"
    registry["ideas"]["board-proposal"] = idea
    board = sudhir_task.render_board(registry)
    assert "| Proposal | Idea gate |" in board
    assert "Generate/paste Task Idea Proposal fields and capture Check feedback." in board
    assert "Stale downstream action" not in board


def test_proposal_capture_persists_fields_and_passed_evidence() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "cache-graph-drift")
    registry["ideas"]["cache-graph-drift"] = idea
    args = SimpleNamespace(
        slug="cache-graph-drift",
        verdict="passed",
        summary=VALID_SUMMARY,
        summary_file=None,
        category=VALID_CATEGORY,
        skills=VALID_SKILLS,
        tags=VALID_TAGS,
        evidence=["Snorkel Check feedback screenshot 2026-07-21"],
        feedback="Valid task idea.",
        feedback_file=None,
        source_type="GitHub issue",
        source_reference="https://example.invalid/issues/42",
        reuse_boundary="Uses the cache symptom only; no prose, patch, or tests are copied.",
    )
    with tempfile.TemporaryDirectory() as tmp:
        proposals = Path(tmp) / "proposals"
        with (
            mock.patch.object(sudhir_task, "IDEA_PROPOSALS_DIR", proposals),
            mock.patch.object(sudhir_task, "load_registry", return_value=registry),
            mock.patch.object(sudhir_task, "save_registry"),
            mock.patch.object(sudhir_task, "write_board"),
        ):
            exit_code = sudhir_task.cmd_idea_proposal(args)
        rendered = (proposals / "cache-graph-drift.md").read_text(encoding="utf-8")

    assert exit_code == 0
    proposal = idea["proposal_check"]
    assert proposal["status"] == "passed"
    assert proposal["category_slug"] == "build-and-dependency-management"
    assert idea["category"] == "build-and-dependency-management"
    assert "Task Idea Summary" in rendered
    assert "Valid task idea." in rendered
    assert "GitHub issue" in rendered


def test_failed_proposal_requires_feedback_and_evidence() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "invalid-proposal")
    registry["ideas"]["invalid-proposal"] = idea
    args = SimpleNamespace(
        slug="invalid-proposal",
        verdict="failed",
        summary=VALID_SUMMARY,
        summary_file=None,
        category=VALID_CATEGORY,
        skills=VALID_SKILLS,
        tags=VALID_TAGS,
        evidence=None,
        feedback=None,
        feedback_file=None,
        source_type=None,
        source_reference=None,
        reuse_boundary=None,
    )
    with mock.patch.object(sudhir_task, "load_registry", return_value=registry):
        exit_code = sudhir_task.cmd_idea_proposal(args)
    assert exit_code == 2
    assert idea["proposal_check"]["status"] == "pending"


def test_inspiration_ladder_and_lifecycle_skills_require_proposal_first() -> None:
    sources = (REPO_ROOT / "web" / "idea-inspiration-sources.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "GitHub issues",
        "SWE-bench",
        "Terminal-Bench papers",
        "Advent of Code",
        "Stack Overflow",
        "Reddit",
        "Task Idea Summary",
        "Associated Skills",
        "Task Tags",
    ):
        assert phrase in sources

    agent_skill = (
        REPO_ROOT / ".agents" / "skills" / "sudhir-task-lifecycle" / "SKILL.md"
    ).read_text(encoding="utf-8")
    cursor_skill = (
        REPO_ROOT / ".cursor" / "skills" / "sudhir-task-lifecycle" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert agent_skill == cursor_skill
    assert "output only these" in agent_skill
    assert "Check feedback" in agent_skill
    assert "Only proposal=`passed`" in agent_skill
