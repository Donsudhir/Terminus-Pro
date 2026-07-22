from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

import sudhir_task


def test_run_gate_propagates_canonical_roots() -> None:
    """Pipeline subprocesses receive every canonical Sudhir workspace root."""
    completed = SimpleNamespace(returncode=0, stdout="", stderr="")
    with mock.patch.object(sudhir_task.subprocess, "run", return_value=completed) as run:
        result = sudhir_task.run_gate(["python3", "noop.py"], "probe")

    assert result["result"] == "PASS"
    environment = run.call_args.kwargs["env"]
    assert environment["TB3_TASKS_DIR"] == str(sudhir_task.TASKS_DIR)
    assert environment["TB3_SPECS_DIR"] == str(sudhir_task.SPECS_DIR)
    assert environment["TB3_SUBMISSIONS_DIR"] == str(sudhir_task.SUBMISSIONS_DIR)
    assert environment["TB3_REVIEWS_DIR"] == str(sudhir_task.REVIEWS_DIR)
    assert environment["TB3_JOBS_DIR"] == str(sudhir_task.JOBS_DIR)


def _complete_uniqueness(idea: dict[str, object]) -> None:
    proposal = idea["proposal_check"]
    assert isinstance(proposal, dict)
    proposal["status"] = "passed"
    uniqueness = idea["uniqueness"]
    assert isinstance(uniqueness, dict)
    uniqueness.update(
        {
            "status": "passed",
            "scope": sorted(sudhir_task.REQUIRED_UNIQUENESS_SCOPES),
            "evidence": ["sudhir_research/example.md"],
            "closest_analogue": "A superficially similar upstream task",
            "differentiator": "Different mechanism, distributed topology, and invariants",
        }
    )
    fingerprint = uniqueness["fingerprint"]
    assert isinstance(fingerprint, dict)
    fingerprint.update(
        {
            "domain": "domain boundary",
            "mechanism": "cross-runtime semantic drift",
            "topology": "three coordinated module roots",
            "verification": "independent invariant families",
        }
    )


def test_new_idea_is_blocked_until_uniqueness_and_step2a_go() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "novel-probe")

    assert idea["status"] == "captured"
    assert sudhir_task._approval_gaps(idea)

    _complete_uniqueness(idea)
    validation = idea["validation"]
    assert isinstance(validation, dict)
    validation.update(
        {
            "status": "go",
            "attempt": 1,
            "evidence": ["sudhir_ideas/specs/novel-probe.md"],
        }
    )
    assert sudhir_task._approval_gaps(idea) == []


def test_new_idea_template_includes_long_horizon_profile() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "causal-incident")

    template = sudhir_task._idea_template(idea)

    assert "Long-horizon investigation profile" in template
    assert "Weakness areas (2-4" in template
    assert "Causal chain (4-8" in template
    assert "Meaningful-action estimate (20-100" in template
    assert "Task Idea Proposal" in idea["next_action"]


def test_approved_idea_without_evidence_is_registry_error() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "premature-idea", status="approved")
    registry["ideas"][idea["slug"]] = idea

    errors, _warnings = sudhir_task.validate_idea_registry(registry)

    assert any("uniqueness verdict is not passed" in error for error in errors)
    assert any("Step 2a validation verdict is not GO" in error for error in errors)


def test_incomplete_uniqueness_pass_is_registry_error_before_approval() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "false-positive")
    uniqueness = idea["uniqueness"]
    assert isinstance(uniqueness, dict)
    uniqueness["status"] = "passed"
    registry["ideas"][idea["slug"]] = idea

    errors, _warnings = sudhir_task.validate_idea_registry(registry)

    assert any("incomplete novelty fingerprint" in error for error in errors)


def test_task_execution_gate_blocks_new_idea_but_allows_known_old_work() -> None:
    registry = sudhir_task.empty_registry()
    task = sudhir_task.new_entry("candidate")
    registry["tasks"]["candidate"] = task
    candidate = sudhir_task.new_idea_entry(registry, "candidate")
    candidate["task_slug"] = "candidate"
    registry["ideas"]["candidate"] = candidate

    assert sudhir_task._task_execution_gaps(registry, task)

    candidate["status"] = "legacy"
    assert sudhir_task._task_execution_gaps(registry, task) == []
    candidate["status"] = "grandfathered"
    assert sudhir_task._task_execution_gaps(registry, task) == []


def test_platform_evaluation_pass_is_not_acceptance() -> None:
    snorkel = {"difficulty": "HARD", "solvable": True, "static_outcome": "PASS"}

    assert sudhir_task._infer_platform_status(snorkel) == "evaluation-passed"
    assert sudhir_task._infer_platform_status({**snorkel, "state": "ACCEPTED"}) == "accepted"
    assert sudhir_task._infer_platform_status({"state": "EVALUATION_PENDING"}) == (
        "in-evaluation"
    )
    assert sudhir_task._infer_platform_status({"state": "REVIEW_PENDING"}) == "in-review"


def test_gate_phase_is_labeled_as_development() -> None:
    task = sudhir_task.new_entry("in-dev")
    task["phase"] = "gates"

    assert sudhir_task._execution_status(task) == "IN DEVELOPMENT / GATES"
    task["phase"] = "package"
    assert sudhir_task._execution_status(task) == "IN DEVELOPMENT / PACKAGE"


def test_quarantined_import_is_not_in_active_idea_rows() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "stale-import", status="retired")
    idea.update(
        {
            "portfolio_scope": "quarantined",
            "task_slug": "stale-import",
            "quarantine": {"reason": "Not recognized as active."},
        }
    )
    task = sudhir_task.new_entry("stale-import")
    task.update(
        {
            "portfolio_scope": "quarantined",
            "snorkel": {"source_file": "submission_old.json", "uploaded_at": "2026-05-01"},
        }
    )
    registry["ideas"]["stale-import"] = idea
    registry["tasks"]["stale-import"] = task

    assert "Stale Import" not in "\n".join(sudhir_task._idea_rows(registry))
    assert "Stale Import" in "\n".join(sudhir_task._quarantine_rows(registry))
    errors, _warnings = sudhir_task.validate_idea_registry(registry)
    assert errors == []


def test_idea_board_separates_execution_submission_and_platform() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "tracked-idea", status="legacy")
    idea["task_slug"] = "tracked-idea"
    registry["ideas"]["tracked-idea"] = idea
    task = sudhir_task.new_entry("tracked-idea")
    task.update(
        {
            "phase": "feedback",
            "snorkel": {
                "submission_id": "submission-1",
                "difficulty": "HARD",
                "solvable": True,
                "static_outcome": "PASS",
            },
        }
    )
    registry["tasks"]["tracked-idea"] = task

    board = sudhir_task.render_board(registry)

    assert "| Execution | Submission | Platform |" in board
    assert "| EXECUTED | SUBMITTED | EVALUATION PASSED |" in board


def test_live_platform_stage_suppresses_stale_feedback_table() -> None:
    registry = sudhir_task.empty_registry()
    idea = sudhir_task.new_idea_entry(registry, "under-review", status="grandfathered")
    idea["task_slug"] = "under-review"
    registry["ideas"]["under-review"] = idea
    task = sudhir_task.new_entry("under-review")
    task.update(
        {
            "phase": "submitted",
            "snorkel": {"submission_id": "old", "solvable": False},
            "platform_status": {"status": "in-review", "source": "explicit"},
        }
    )
    registry["tasks"]["under-review"] = task

    board = sudhir_task.render_board(registry)

    assert "IN REVIEW" in board
    assert "## Snorkel feedback" not in board
