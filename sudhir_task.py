#!/usr/bin/env python3
"""Sudhir task pipeline driver.

One entry point for the whole Terminal-Bench / TERMINUS task lifecycle so a
chat never has to re-derive the process. It keeps a single JSON registry as the
source of truth, renders a human-readable status board, drives the cheap gate
chain through the existing harness scripts, and ingests Snorkel platform
submission exports so feedback shows up on the board automatically.

This module is stdlib-only (matches the rest of the repo-root harness) and
computes every path from the repository root plus ``sudhir_config.toml`` so it
works regardless of the current working directory.

Subcommands:
    idea ...         Capture, research, validate, reserve, reject, and list ideas.
    idea proposal    Capture proposal form fields and Check feedback verdict.
    new <slug>       Register a task and scaffold its idea record.
    status [slug]    Print the registry (all tasks, or one) as JSON.
    board            Re-render sudhir_progress/BOARD.md from the registry.
    phase <slug> <p> Advance/record a lifecycle phase for a task.
    revise <slug>    Open a revision dossier; bump counter; invalidate downstream.
    gates <slug>     Run static + dockerfile + collapse + integrity gates.
    package <slug>   Build the submission zip, validate, and approve it.
    evidence <slug>  Record Harbor oracle/NOP/10x job evidence into the registry.
    feedback-capture Capture reviewer feedback into the current REV dossier.
    form-capture     Store difficulty/solution/verification/rubric paste fields.
    rubric-capture   Capture UI rubric paste into the current REV dossier.
    learn-check      Print applicable CM preventions; check PREUPLOAD checklist.
    ingest [paths]   Parse Snorkel submission_*.json exports into the registry.
    outcome <slug>   Record an explicit platform/reviewer outcome.
    eligibility      Evaluate current official/house task eligibility.
    exemption-capture Store source-backed in-flight exemption evidence.
    sync-snorkel     Explain/attempt the optional network pull (needs creds).
    backfill         Seed the registry from existing active tasks + archives.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import eligibility_policy
import idea_proposal
import root_adapter
import sudhir_dossier

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - repo pins 3.12
    tomllib = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parent

# Ordered lifecycle phases mirrored from sudhir_knowledge/TASK_LIFECYCLE.md.
PHASES: tuple[str, ...] = (
    "idea",       # Phase 0/1: idea recorded, research in flight
    "step2a",     # Phase 1: Step 2a validation loop
    "construct",  # Phase 2/3: task source + Docker under construction
    "gates",      # Phase 4: cheap gates + oracle 1x/NOP
    "review",     # Phase 5: paper review / hardening
    "package",    # Phase 6: oracle 10x, packaging, approval
    "submitted",  # uploaded to the Snorkel platform
    "feedback",   # platform verdict ingested
)

PHASE_LABELS = {
    "idea": "Idea",
    "step2a": "Step 2a",
    "construct": "Construction",
    "gates": "Cheap gates",
    "review": "Review",
    "package": "Package/approve",
    "submitted": "Submitted",
    "feedback": "Feedback",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _display_repo_path(path: Path) -> Path:
    return path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path


# --------------------------------------------------------------------------- #
# Canonical + historical roots (ADR-0016 / Slice 7)
# --------------------------------------------------------------------------- #
ROOTS = root_adapter.ROOTS
TASKS_DIR = ROOTS.tasks
ARCHIVED_DIR = REPO_ROOT / "sudhir_tasks" / "archived"
SPECS_DIR = ROOTS.specs
SUBMISSIONS_DIR = ROOTS.submissions
REVIEWS_DIR = ROOTS.reviews
JOBS_DIR = ROOTS.jobs
REGISTRY_PATH = REPO_ROOT / "sudhir_progress" / "registry.json"
REGISTRY_LOCK_PATH = Path("/tmp") / (
    "terminus-registry-" + hashlib.sha256(str(REPO_ROOT).encode()).hexdigest()[:12] + ".lock"
)
BOARD_PATH = ROOTS.board
STATUS_PATH = ROOTS.status
IDEAS_DIR = REPO_ROOT / "sudhir_ideas"
IDEA_INDEX_PATH = ROOTS.idea_index
IDEA_PROPOSALS_DIR = IDEAS_DIR / "proposals"
SNORKEL_DIR = REPO_ROOT / "sudhir_snorkel"
SNORKEL_INBOX = SNORKEL_DIR / "inbox"
SNORKEL_ARCHIVE = SNORKEL_DIR / "archive"
LEGACY_SUBMISSIONS_DIR = ROOTS.historical_submissions
CURRENT_SUBMISSION_INDEX_PATH = ROOTS.current_submission_index


# --------------------------------------------------------------------------- #
# Registry model
# --------------------------------------------------------------------------- #
REGISTRY_SCHEMA_VERSION = 3

IDEA_STATUSES: tuple[str, ...] = (
    "captured",
    "researching",
    "reserved",
    "validating",
    "approved",
    "grandfathered",
    "rejected",
    "retired",
    "legacy",
)
MANUAL_IDEA_STATUSES: tuple[str, ...] = tuple(
    status for status in IDEA_STATUSES if status != "legacy"
)
UNIQUENESS_STATUSES: tuple[str, ...] = ("pending", "passed", "failed", "not-recorded")
VALIDATION_STATUSES: tuple[str, ...] = ("not-started", "in-progress", "go", "stop", "not-recorded")
PLATFORM_STATUSES: tuple[str, ...] = (
    "not-submitted",
    "pending",
    "in-evaluation",
    "in-review",
    "evaluation-passed",
    "needs-revision",
    "accepted",
    "rejected",
)
REQUIRED_UNIQUENESS_SCOPES: frozenset[str] = frozenset(
    {
        "idea-registry",
        "active-tasks",
        "archived-tasks",
        "submission-archives",
        "upstream-corpus",
        "external-research",
    }
)


def empty_registry() -> dict[str, Any]:
    return {"schema_version": REGISTRY_SCHEMA_VERSION, "ideas": {}, "tasks": {}}


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.is_file():
        return empty_registry()
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    data["schema_version"] = REGISTRY_SCHEMA_VERSION
    data.setdefault("ideas", {})
    data.setdefault("tasks", {})
    for record in (data["ideas"] or {}).values():
        eligibility_policy.ensure_record_policy_fields(record)
        _ensure_idea_proposal(record)
    for record in (data["tasks"] or {}).values():
        eligibility_policy.ensure_record_policy_fields(record)
    return data


def _ensure_idea_proposal(idea: dict[str, Any]) -> bool:
    if isinstance(idea.get("proposal_check"), dict):
        return False
    uniqueness = idea.get("uniqueness") or {}
    established = (
        uniqueness.get("status") == "passed"
        or idea.get("status") in {"approved", "grandfathered", "legacy", "rejected", "retired"}
    )
    idea["proposal_check"] = idea_proposal.new_proposal_check(
        summary=str(idea.get("summary") or ""),
        category=idea.get("category"),
        status="not-recorded" if established else "pending",
    )
    return True


def save_registry(reg: dict[str, Any]) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(reg, indent=2, sort_keys=True) + "\n"
    temporary = REGISTRY_PATH.with_name(f".{REGISTRY_PATH.name}.{os.getpid()}.tmp")
    try:
        temporary.write_text(rendered, encoding="utf-8")
        os.replace(temporary, REGISTRY_PATH)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def registry_lock() -> Iterator[None]:
    """Serialize whole CLI transactions so concurrent sessions cannot lose updates."""
    REGISTRY_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY_LOCK_PATH.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def new_entry(slug: str) -> dict[str, Any]:
    entry = {
        "slug": slug,
        "idea_slug": slug,
        "portfolio_scope": "active",
        "title": slug.replace("-", " ").title(),
        "category": None,
        "languages": [],
        "phase": "idea",
        "next_action": "Record the idea and start Step 2a validation.",
        "created": utc_now(),
        "updated": utc_now(),
        "revision": 0,
        "source_dir": None,
        "gates": {},
        "package": {},
        "snorkel": {},
        "evidence": {},
        "revisions": [],
        "learning": {"cm_hits": [], "patterns_applied": [], "form_refs": {}},
        "notes": [],
        **eligibility_policy.new_record_policy_fields(),
    }
    _refresh_eligibility(entry, action="capture")
    return entry


def _next_idea_id(reg: dict[str, Any]) -> str:
    used = []
    for idea in reg.get("ideas", {}).values():
        match = re.fullmatch(r"IDEA-(\d+)", str(idea.get("id", "")))
        if match:
            used.append(int(match.group(1)))
    return f"IDEA-{max(used, default=0) + 1:04d}"


def new_idea_entry(
    reg: dict[str, Any],
    slug: str,
    *,
    title: str | None = None,
    category: str | None = None,
    languages: list[str] | None = None,
    subcategories: list[str] | None = None,
    skills: list[str] | None = None,
    tags: list[str] | None = None,
    summary: str = "",
    status: str = "captured",
) -> dict[str, Any]:
    now = utc_now()
    validation_status = "not-recorded" if status == "legacy" else "not-started"
    uniqueness_status = "not-recorded" if status == "legacy" else "pending"
    idea = {
        "id": _next_idea_id(reg),
        "slug": slug,
        "title": title or slug.replace("-", " ").title(),
        "summary": summary,
        "category": category,
        "languages": list(languages or []),
        "status": status,
        "portfolio_scope": "active",
        "task_slug": None,
        "proposal_check": idea_proposal.new_proposal_check(
            summary=summary,
            category=category,
            skills=skills,
            tags=tags,
            status="not-recorded" if status in {"approved", "grandfathered", "legacy", "rejected", "retired"} else "pending",
        ),
        "record": f"sudhir_ideas/records/{slug}.md",
        "uniqueness": {
            "status": uniqueness_status,
            "checked_at": None,
            "scope": [],
            "evidence": [],
            "fingerprint": {
                "domain": "",
                "mechanism": "",
                "topology": "",
                "verification": "",
            },
            "closest_analogue": "",
            "differentiator": "",
            "reason": "Historical idea dossier was not recorded."
            if status == "legacy"
            else "",
        },
        "validation": {
            "status": validation_status,
            "attempt": 0,
            "evidence": [],
            "reason": "Historical Step 2a evidence was not recorded."
            if status == "legacy"
            else "",
        },
        "next_action": "Do not reuse without a fresh uniqueness dossier."
        if status in {"approved", "grandfathered", "legacy", "rejected", "retired"}
        else "Paste the Task Idea Proposal fields into Snorkel and capture Check feedback before uniqueness.",
        "created": now,
        "updated": now,
        "history": [
            {
                "at": now,
                "event": f"idea {status}",
                "reason": "Imported historical task without a complete idea dossier."
                if status == "legacy"
                else "Idea captured.",
            }
        ],
        **eligibility_policy.new_record_policy_fields(),
    }
    idea["subcategories"] = list(subcategories or [])
    eligibility = _refresh_eligibility(idea, action="capture")
    if eligibility.blocking:
        idea["next_action"] = "Eligibility blocked by current net-new submission policy."
    return idea


def get_entry(reg: dict[str, Any], slug: str) -> dict[str, Any] | None:
    return reg["tasks"].get(slug)


def _refresh_eligibility(
    record: dict[str, Any],
    *,
    action: str,
) -> eligibility_policy.EligibilityResult:
    result = eligibility_policy.evaluate(record, action=action)
    record["eligibility_verdict"] = result.to_dict(
        action=action,
        evaluated_at=utc_now(),
    )
    return result


def _eligibility_gaps(record: dict[str, Any], *, action: str) -> list[str]:
    result = _refresh_eligibility(record, action=action)
    return list(result.reasons) if result.blocking else []


def _print_eligibility_block(gaps: list[str]) -> None:
    print("Eligibility is blocked:")
    for gap in gaps:
        print(f"- {gap}")


def touch(entry: dict[str, Any]) -> None:
    entry["updated"] = utc_now()


def add_note(entry: dict[str, Any], text: str) -> None:
    entry.setdefault("notes", []).append({"at": utc_now(), "text": text})


def add_idea_history(idea: dict[str, Any], event: str, reason: str) -> None:
    idea.setdefault("history", []).append(
        {"at": utc_now(), "event": event, "reason": reason}
    )
    idea["updated"] = utc_now()


def _uniqueness_gaps(idea: dict[str, Any]) -> list[str]:
    uniqueness = idea.get("uniqueness") or {}
    gaps: list[str] = []
    proposal_status = (idea.get("proposal_check") or {}).get("status")
    if proposal_status not in {"passed", "not-recorded"}:
        gaps.append("platform Task Idea Proposal check is not passed")
    if uniqueness.get("status") != "passed":
        gaps.append("uniqueness verdict is not passed")
    missing_scopes = REQUIRED_UNIQUENESS_SCOPES - set(uniqueness.get("scope") or [])
    if missing_scopes:
        gaps.append("missing search scopes: " + ", ".join(sorted(missing_scopes)))
    if not uniqueness.get("evidence"):
        gaps.append("no collision-audit evidence is recorded")
    fingerprint = uniqueness.get("fingerprint") or {}
    missing_fingerprint = [
        field
        for field in ("domain", "mechanism", "topology", "verification")
        if not str(fingerprint.get(field, "")).strip()
    ]
    if missing_fingerprint:
        gaps.append("incomplete novelty fingerprint: " + ", ".join(missing_fingerprint))
    if not str(uniqueness.get("closest_analogue", "")).strip():
        gaps.append("closest analogue is not named")
    if not str(uniqueness.get("differentiator", "")).strip():
        gaps.append("structural differentiator is not recorded")
    return gaps


def _proposal_gaps(idea: dict[str, Any]) -> list[str]:
    proposal = idea.get("proposal_check") or {}
    status = proposal.get("status")
    if status in {"passed", "not-recorded"}:
        return []
    return ["platform Task Idea Proposal check is not passed"]


def _approval_gaps(idea: dict[str, Any]) -> list[str]:
    gaps = _uniqueness_gaps(idea)
    validation = idea.get("validation") or {}
    if validation.get("status") != "go":
        gaps.append("Step 2a validation verdict is not GO")
    if not validation.get("evidence"):
        gaps.append("Step 2a evidence path is not recorded")
    gaps.extend(_eligibility_gaps(idea, action="approval"))
    return gaps


def validate_idea_registry(reg: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ideas = reg.get("ideas") or {}
    tasks = reg.get("tasks") or {}
    seen_ids: dict[str, str] = {}

    for slug, idea in ideas.items():
        _ensure_idea_proposal(idea)
        errors.extend(
            f"{slug}: {error}"
            for error in eligibility_policy.policy_field_errors(idea)
        )
        if idea.get("slug") != slug:
            errors.append(f"{slug}: map key and idea slug disagree")
        idea_id = str(idea.get("id", ""))
        if not re.fullmatch(r"IDEA-\d{4}", idea_id):
            errors.append(f"{slug}: invalid or missing idea id")
        elif idea_id in seen_ids:
            errors.append(f"{slug}: duplicate idea id also used by {seen_ids[idea_id]}")
        else:
            seen_ids[idea_id] = slug
        if idea.get("status") not in IDEA_STATUSES:
            errors.append(f"{slug}: invalid idea status {idea.get('status')!r}")

        uniqueness_status = (idea.get("uniqueness") or {}).get("status")
        if uniqueness_status not in UNIQUENESS_STATUSES:
            errors.append(f"{slug}: invalid uniqueness status {uniqueness_status!r}")
        elif uniqueness_status == "passed":
            proposal_status = (idea.get("proposal_check") or {}).get("status")
            if proposal_status not in {"passed", "not-recorded"}:
                errors.append(f"{slug}: proposal check is not passed")
            errors.extend(f"{slug}: {gap}" for gap in _uniqueness_gaps(idea))
        validation_status = (idea.get("validation") or {}).get("status")
        if validation_status not in VALIDATION_STATUSES:
            errors.append(f"{slug}: invalid Step 2a status {validation_status!r}")

        task_slug = idea.get("task_slug")
        if task_slug:
            task = tasks.get(task_slug)
            if task is None:
                errors.append(f"{slug}: linked task {task_slug!r} does not exist")
            elif task.get("idea_slug") != slug:
                errors.append(f"{slug}: linked task points to {task.get('idea_slug')!r}")

        portfolio_scope = idea.get("portfolio_scope", "active")
        if portfolio_scope not in {"active", "quarantined"}:
            errors.append(f"{slug}: invalid portfolio scope {portfolio_scope!r}")
        if portfolio_scope == "quarantined" and idea.get("status") != "retired":
            errors.append(f"{slug}: quarantined idea must have status 'retired'")

        if idea.get("status") == "approved":
            errors.extend(f"{slug}: {gap}" for gap in _approval_gaps(idea))
            eligibility = _refresh_eligibility(idea, action="registry-validate")
            if eligibility.blocking:
                errors.extend(f"{slug}: {reason}" for reason in eligibility.reasons)
        elif idea.get("status") == "legacy":
            warnings.append(f"{slug}: legacy idea has no retrospective uniqueness proof")
        elif idea.get("status") == "grandfathered":
            warnings.append(f"{slug}: known active task predates the structured uniqueness dossier")
        elif idea.get("status") != "retired" and (
            idea.get("uniqueness") or {}
        ).get("status") != "passed":
            warnings.append(f"{slug}: uniqueness is not yet proven")

    for slug, task in tasks.items():
        errors.extend(
            f"{slug}: {error}"
            for error in eligibility_policy.policy_field_errors(task)
        )
        idea_slug = task.get("idea_slug")
        if not idea_slug:
            errors.append(f"{slug}: task has no idea_slug link")
        elif idea_slug not in ideas:
            errors.append(f"{slug}: linked idea {idea_slug!r} does not exist")
        elif task.get("portfolio_scope", "active") != ideas[idea_slug].get(
            "portfolio_scope", "active"
        ):
            errors.append(f"{slug}: task and idea portfolio scopes disagree")
        platform_status = (task.get("platform_status") or {}).get("status")
        if platform_status is not None and platform_status not in PLATFORM_STATUSES:
            errors.append(f"{slug}: invalid platform status {platform_status!r}")
        if task.get("portfolio_scope", "active") == "active" and task.get("phase") in {
            "package",
            "submitted",
        }:
            eligibility = _refresh_eligibility(task, action="package")
            if eligibility.blocking:
                errors.extend(f"{slug}: {reason}" for reason in eligibility.reasons)

    return errors, warnings


def _task_execution_gaps(reg: dict[str, Any], task: dict[str, Any]) -> list[str]:
    idea_slug = task.get("idea_slug") or task.get("slug")
    idea = (reg.get("ideas") or {}).get(idea_slug)
    if idea is None:
        return [f"task has no linked idea record for {idea_slug!r}"]
    if idea.get("status") in {"legacy", "grandfathered"}:
        return []
    gaps = _approval_gaps(idea)
    if idea.get("status") != "approved":
        gaps.insert(0, f"idea gate is {idea.get('status')!r}, not 'approved'")
    return list(dict.fromkeys(gaps))


def _print_execution_block(gaps: list[str]) -> None:
    print("Execution is blocked:")
    for gap in gaps:
        print(f"- {gap}")


# --------------------------------------------------------------------------- #
# Board rendering
# --------------------------------------------------------------------------- #
def _phase_index(phase: str) -> int:
    try:
        return PHASES.index(phase)
    except ValueError:
        return -1


def _gate_glyph(entry: dict[str, Any]) -> str:
    gates = entry.get("gates") or {}
    if not gates:
        return "-"
    results = [g.get("result") for g in gates.values() if isinstance(g, dict)]
    if not results:
        return "-"
    if all(r == "PASS" for r in results):
        return "PASS"
    if any(r == "FAIL" for r in results):
        return "FAIL"
    return "WARN"


def _snorkel_cell(entry: dict[str, Any]) -> str:
    explicit = entry.get("platform_status") or {}
    if explicit.get("source") == "explicit":
        return str(explicit.get("status", "pending")).replace("-", " ").upper()
    sn = entry.get("snorkel") or {}
    if not sn:
        return "-"
    parts = []
    if sn.get("difficulty"):
        parts.append(str(sn["difficulty"]))
    if sn.get("solvable") is True:
        parts.append("solvable")
    elif sn.get("solvable") is False:
        parts.append("unsolved")
    if sn.get("static_outcome"):
        parts.append(f"static:{sn['static_outcome']}")
    return ", ".join(parts) if parts else "-"


def _linked_task(reg: dict[str, Any], idea: dict[str, Any]) -> dict[str, Any] | None:
    task_slug = idea.get("task_slug")
    if not task_slug:
        return None
    return (reg.get("tasks") or {}).get(task_slug)


def _execution_status(task: dict[str, Any] | None) -> str:
    if task is None or task.get("phase") in {None, "idea", "step2a"}:
        return "NOT STARTED"
    if task.get("phase") in {"construct", "gates", "review"}:
        if (task.get("snorkel") or {}).get("submission_id"):
            return "EXECUTED / REVISING"
        if task.get("phase") == "gates":
            return "IN DEVELOPMENT / GATES"
        if task.get("phase") == "review":
            return "IN DEVELOPMENT / REVIEW"
        return "IN DEVELOPMENT"
    if task.get("phase") == "package" and not (task.get("snorkel") or {}).get(
        "submission_id"
    ):
        return "IN DEVELOPMENT / PACKAGE"
    return "EXECUTED"


def _submission_status(task: dict[str, Any] | None) -> str:
    if task is None:
        return "NOT SUBMITTED"
    snorkel = task.get("snorkel") or {}
    if snorkel.get("submission_id") or task.get("phase") in {"submitted", "feedback"}:
        return "SUBMITTED"
    package = task.get("package") or {}
    if package.get("approved") is True and package.get("validated") is True:
        return "READY"
    return "NOT SUBMITTED"


def _infer_platform_status(snorkel: dict[str, Any]) -> str:
    if not snorkel:
        return "not-submitted"
    state = str(snorkel.get("state") or "").upper()
    if state in {"ACCEPTED", "APPROVED"}:
        return "accepted"
    if state in {"REJECTED", "DECLINED"}:
        return "rejected"
    if state in {"EVALUATION_PENDING", "IN_EVALUATION", "EVALUATING"}:
        return "in-evaluation"
    if state in {"REVIEW_PENDING", "IN_REVIEW", "UNDER_REVIEW"}:
        return "in-review"
    if state in {"NEEDS_REVISION", "REVISION_REQUESTED"}:
        return "needs-revision"
    if snorkel.get("static_outcome") not in {None, "PASS"}:
        return "needs-revision"
    if snorkel.get("solvable") is False:
        return "needs-revision"
    difficulty = str(snorkel.get("difficulty") or "").upper()
    if difficulty and difficulty != "HARD":
        return "needs-revision"
    if snorkel.get("solvable") is True and difficulty == "HARD":
        # This is an evaluation signal, not a final reviewer acceptance.
        return "evaluation-passed"
    return "pending"


def _platform_status(task: dict[str, Any] | None) -> str:
    if task is None:
        return "NOT SUBMITTED"
    explicit = task.get("platform_status") or {}
    status = explicit.get("status") or _infer_platform_status(task.get("snorkel") or {})
    return str(status).replace("-", " ").upper()


def _eligibility_status(record: dict[str, Any]) -> str:
    result = eligibility_policy.evaluate(record, action="view")
    official = result.official_status.replace("-", " ").upper()
    house = result.house_status.replace("-", " ").upper()
    return official if official == house else f"{official} / HOUSE {house}"


def _idea_rows(
    reg: dict[str, Any],
    status_filter: str | None = None,
    portfolio_scope: str | None = "active",
) -> list[str]:
    ideas = list((reg.get("ideas") or {}).values())
    if portfolio_scope is not None:
        ideas = [
            idea
            for idea in ideas
            if idea.get("portfolio_scope", "active") == portfolio_scope
        ]
    if status_filter:
        ideas = [idea for idea in ideas if idea.get("status") == status_filter]
    order = {status: index for index, status in enumerate(IDEA_STATUSES)}
    ideas.sort(key=lambda idea: (order.get(idea.get("status"), 99), idea.get("id", "")))

    rows = [
        "| ID | Idea | Proposal | Idea gate | Unique | Execution | Submission | Platform | Eligibility | Task | Next action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idea in ideas:
        task = _linked_task(reg, idea)
        uniqueness = (idea.get("uniqueness") or {}).get("status", "pending")
        proposal = (idea.get("proposal_check") or {}).get("status", "not-recorded")
        if proposal == "pending":
            next_action = "Generate/paste Task Idea Proposal fields and capture Check feedback."
        elif proposal == "failed":
            next_action = "Revise/recheck the Task Idea Proposal or reject the idea."
        else:
            next_action = (task or {}).get("next_action") or idea.get("next_action") or "-"
        rows.append(
            "| {id} | {title} | {proposal} | {gate} | {unique} | {execution} | {submission} | "
            "{platform} | {eligibility} | {task} | {next_action} |".format(
                id=idea.get("id", "?"),
                title=str(idea.get("title") or idea.get("slug") or "?").replace("|", "\\|"),
                proposal=str(proposal).replace("-", " ").upper(),
                gate=str(idea.get("status", "?")).replace("-", " ").upper(),
                unique=str(uniqueness).replace("-", " ").upper(),
                execution=_execution_status(task),
                submission=_submission_status(task),
                platform=_platform_status(task),
                eligibility=_eligibility_status(task or idea),
                task=idea.get("task_slug") or "-",
                next_action=str(next_action).replace("|", "\\|"),
            )
        )
    return rows


def _idea_totals(reg: dict[str, Any], portfolio_scope: str = "active") -> list[str]:
    ideas = [
        idea
        for idea in (reg.get("ideas") or {}).values()
        if idea.get("portfolio_scope", "active") == portfolio_scope
    ]
    counts = {status: 0 for status in IDEA_STATUSES}
    for idea in ideas:
        status = idea.get("status")
        if status in counts:
            counts[status] += 1
    populated = [
        f"{status.replace('-', ' ').title()}: {count}"
        for status, count in counts.items()
        if count
    ]
    return [f"- Active ideas tracked: {len(ideas)}", "- " + " | ".join(populated)]


def _quarantine_rows(reg: dict[str, Any]) -> list[str]:
    ideas = [
        idea
        for idea in (reg.get("ideas") or {}).values()
        if idea.get("portfolio_scope") == "quarantined"
    ]
    ideas.sort(key=lambda idea: idea.get("id", ""))
    rows = [
        "| ID | Imported name | Source export | Uploaded | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for idea in ideas:
        task = _linked_task(reg, idea) or {}
        snorkel = task.get("snorkel") or {}
        quarantine = idea.get("quarantine") or {}
        rows.append(
            "| {id} | {title} | {source} | {uploaded} | {reason} |".format(
                id=idea.get("id", "?"),
                title=str(idea.get("title") or idea.get("slug") or "?").replace(
                    "|", "\\|"
                ),
                source=snorkel.get("source_file") or "-",
                uploaded=str(snorkel.get("uploaded_at") or "-")[:10],
                reason=str(quarantine.get("reason") or "-").replace("|", "\\|"),
            )
        )
    return rows


def _registry_view_digest(reg: dict[str, Any]) -> str:
    payload = json.dumps(reg, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def render_board(
    reg: dict[str, Any],
    *,
    generated_at: str | None = None,
    registry_digest: str | None = None,
) -> str:
    tasks = [
        task
        for task in reg["tasks"].values()
        if task.get("portfolio_scope", "active") == "active"
    ]
    tasks.sort(key=lambda e: (-_phase_index(e.get("phase", "")), e.get("slug", "")))

    lines: list[str] = []
    lines.append("# Task Status Board")
    lines.append("")
    generated_at = generated_at or utc_now()
    registry_digest = registry_digest or _registry_view_digest(reg)
    lines.append(f"Generated: {generated_at} by `sudhir_task.py board`.")
    lines.append(f"Generation: `{registry_digest}`")
    lines.append("")
    lines.append(
        "This file is rendered from `sudhir_progress/registry.json`. "
        "Do not edit by hand; run `python3 sudhir_task.py board`."
    )
    lines.append("")

    lines.append("## Idea portfolio")
    lines.append("")
    lines.extend(_idea_rows(reg))
    lines.append("")
    lines.extend(_idea_totals(reg))
    lines.append("")

    quarantined_count = sum(
        idea.get("portfolio_scope") == "quarantined"
        for idea in (reg.get("ideas") or {}).values()
    )
    if quarantined_count:
        lines.append("## Quarantined historical imports")
        lines.append("")
        lines.append(
            "Preserved for provenance, but excluded from the active idea and task counts."
        )
        lines.append("")
        lines.extend(_quarantine_rows(reg))
        lines.append("")

    lines.append("## Pipeline")
    lines.append("")
    lines.append("| Task | Phase | Category | Rev | Gates | Snorkel | Next action |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for t in tasks:
        lines.append(
            "| {slug} | {phase} | {cat} | {rev} | {gates} | {sn} | {next} |".format(
                slug=t.get("slug", "?"),
                phase=PHASE_LABELS.get(t.get("phase", ""), t.get("phase", "?")),
                cat=t.get("category") or "-",
                rev=t.get("revision", 0),
                gates=_gate_glyph(t),
                sn=_snorkel_cell(t),
                next=(t.get("next_action") or "-").replace("|", "\\|"),
            )
        )
    lines.append("")

    feedback = [
        t
        for t in tasks
        if t.get("snorkel")
        and (t.get("platform_status") or {}).get("status")
        not in {"in-evaluation", "in-review"}
    ]
    if feedback:
        lines.append("## Snorkel feedback")
        lines.append("")
        lines.append(
            "| Task | Difficulty | Solvable | Static | Uploaded | Agent pass rates |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for t in feedback:
            sn = t["snorkel"]
            perf = sn.get("agent_performance") or {}
            perf_str = ", ".join(
                f"{name}: {pct}" for name, pct in perf.items()
            ) or "-"
            solvable = sn.get("solvable")
            solvable_str = (
                "yes" if solvable is True else "no" if solvable is False else "-"
            )
            lines.append(
                "| {slug} | {diff} | {solv} | {static} | {up} | {perf} |".format(
                    slug=t.get("slug", "?"),
                    diff=sn.get("difficulty") or "-",
                    solv=solvable_str,
                    static=sn.get("static_outcome") or "-",
                    up=(sn.get("uploaded_at") or "-")[:10],
                    perf=perf_str.replace("|", "\\|"),
                )
            )
        lines.append("")

    counts: dict[str, int] = {}
    for t in tasks:
        counts[t.get("phase", "?")] = counts.get(t.get("phase", "?"), 0) + 1
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Tasks tracked: {len(tasks)}")
    if quarantined_count:
        lines.append(f"- Quarantined imports: {quarantined_count}")
    for phase in PHASES:
        if counts.get(phase):
            lines.append(f"- {PHASE_LABELS[phase]}: {counts[phase]}")
    lines.append("")
    return "\n".join(lines)


def render_idea_index(
    reg: dict[str, Any],
    *,
    generated_at: str | None = None,
    registry_digest: str | None = None,
) -> str:
    generated_at = generated_at or utc_now()
    registry_digest = registry_digest or _registry_view_digest(reg)
    lines = [
        "# Sudhir Idea Portfolio",
        "",
        f"Generated: {generated_at} by `sudhir_task.py board`.",
        f"Generation: `{registry_digest}`",
        "",
        "This index is rendered from `sudhir_progress/registry.json`; do not edit it by hand.",
        "The registry deliberately separates idea approval, uniqueness, execution, submission,",
        "and final platform outcome so an evaluation pass is never mistaken for acceptance.",
        "",
        "## Portfolio",
        "",
    ]
    lines.extend(_idea_rows(reg))
    lines.append("")
    lines.extend(_idea_totals(reg))
    quarantined_count = sum(
        idea.get("portfolio_scope") == "quarantined"
        for idea in (reg.get("ideas") or {}).values()
    )
    if quarantined_count:
        lines.extend(
            [
                "",
                "## Quarantined historical imports",
                "",
                "These stale exports are retained only to explain provenance and are not active ideas.",
                "",
            ]
        )
        lines.extend(_quarantine_rows(reg))
    lines.extend(
        [
            "",
            "## Status contract",
            "",
            "- **Proposal:** PENDING until the four Snorkel Task Idea Proposal fields",
            "  receive captured Check feedback. PASSED is required before uniqueness PASS.",
            "- **Idea gate:** CAPTURED -> RESEARCHING/RESERVED -> VALIDATING -> APPROVED or REJECTED.",
            "  GRANDFATHERED means known active work that predates the structured dossier.",
            "- **Unique:** PASSED means a recorded fingerprint, nearest-analogue comparison,",
            "  required corpus searches, and evidence exist. PENDING is not approval.",
            "- **Execution:** NOT STARTED, IN DEVELOPMENT, EXECUTED, or EXECUTED/REVISING;",
            "  derived from the linked task and prior submission evidence.",
            "- **Submission:** NOT SUBMITTED, READY, or SUBMITTED; derived from package/upload evidence.",
            "- **Platform:** IN EVALUATION and IN REVIEW are live platform stages.",
            "  EVALUATION PASSED is only a test signal. Only explicit reviewer/platform",
            "  evidence may set ACCEPTED or REJECTED.",
            "- **Quarantined:** stale or unrecognized imports preserved outside the active portfolio.",
            "",
            "## Super-uniqueness gate",
            "",
            "No non-legacy idea may enter construction until all of the following are recorded:",
            "",
            "1. a four-part novelty fingerprint: domain, failure mechanism, distributed topology,",
            "   and verifier/invariant surface;",
            "2. searches across the idea registry, active tasks, archived tasks, submission archives,",
            "   upstream corpus, and current external research;",
            "3. the closest analogue and the structural difference, not merely a new name/language;",
            "4. evidence paths for the collision audit;",
            "5. a Step 2a GO with evidence.",
            "",
            "If any item is missing, the idea remains PENDING and execution is blocked.",
            "",
        ]
    )
    return "\n".join(lines)


def render_status(
    reg: dict[str, Any],
    *,
    generated_at: str | None = None,
    registry_digest: str | None = None,
) -> str:
    generated_at = generated_at or utc_now()
    registry_digest = registry_digest or _registry_view_digest(reg)
    tasks = [
        task
        for task in (reg.get("tasks") or {}).values()
        if task.get("portfolio_scope", "active") == "active"
    ]
    tasks.sort(key=lambda task: (-_phase_index(task.get("phase", "")), task.get("slug", "")))
    actionable = [
        task
        for task in tasks
        if _platform_status(task) not in {"ACCEPTED"}
        and str(task.get("next_action") or "").strip()
    ]
    phase_counts: dict[str, int] = {}
    for task in tasks:
        phase = str(task.get("phase") or "?")
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    lines = [
        "# Current Status",
        "",
        f"Generated: {generated_at} by `sudhir_task.py board`.",
        f"Generation: `{registry_digest}`",
        "",
        "This file is generated from `sudhir_progress/registry.json` in the same",
        "view transaction as BOARD and IDEA_INDEX. Do not edit it by hand.",
        "",
        "## Immediate next actions",
        "",
        "| Task | Phase | Platform | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for task in actionable[:10]:
        lines.append(
            "| {slug} | {phase} | {platform} | {next_action} |".format(
                slug=task.get("slug", "?"),
                phase=PHASE_LABELS.get(task.get("phase", ""), task.get("phase", "?")),
                platform=_platform_status(task),
                next_action=str(task.get("next_action") or "-").replace("|", "\\|"),
            )
        )
    if not actionable:
        lines.append("| - | - | - | No active next action |")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Active tasks: {len(tasks)}",
            f"- Active ideas: {sum(idea.get('portfolio_scope', 'active') == 'active' for idea in (reg.get('ideas') or {}).values())}",
        ]
    )
    for phase in PHASES:
        if phase_counts.get(phase):
            lines.append(f"- {PHASE_LABELS[phase]}: {phase_counts[phase]}")
    lines.append("")
    return "\n".join(lines)


def _write_generated_views_atomically(payloads: dict[Path, str]) -> None:
    temporary_paths: dict[Path, Path] = {}
    previous: dict[Path, bytes | None] = {}
    replaced: list[Path] = []
    try:
        for path, content in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            previous[path] = path.read_bytes() if path.exists() else None
            temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
            temporary.write_text(content, encoding="utf-8")
            temporary_paths[path] = temporary
        for path, temporary in temporary_paths.items():
            os.replace(temporary, path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            original = previous[path]
            if original is None:
                path.unlink(missing_ok=True)
                continue
            restore = path.with_name(f".{path.name}.{os.getpid()}.restore")
            restore.write_bytes(original)
            os.replace(restore, path)
        raise
    finally:
        for temporary in temporary_paths.values():
            temporary.unlink(missing_ok=True)


def write_board(reg: dict[str, Any]) -> None:
    generated_at = utc_now()
    registry_digest = _registry_view_digest(reg)
    _write_generated_views_atomically(
        {
            BOARD_PATH: render_board(
                reg, generated_at=generated_at, registry_digest=registry_digest
            ),
            IDEA_INDEX_PATH: render_idea_index(
                reg, generated_at=generated_at, registry_digest=registry_digest
            ),
            STATUS_PATH: render_status(
                reg, generated_at=generated_at, registry_digest=registry_digest
            ),
        }
    )


# --------------------------------------------------------------------------- #
# task.toml sniffing (best-effort, stdlib)
# --------------------------------------------------------------------------- #
def read_task_toml(source_dir: Path) -> dict[str, Any]:
    toml_path = source_dir / "task.toml"
    if not toml_path.is_file() or tomllib is None:
        return {}
    try:
        return tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except Exception:  # pragma: no cover - defensive
        return {}


def enrich_from_source(entry: dict[str, Any], source_dir: Path) -> None:
    meta = (read_task_toml(source_dir).get("metadata") or {})
    if meta.get("category"):
        entry["category"] = meta["category"]
    if meta.get("languages"):
        entry["languages"] = list(meta["languages"])
    if isinstance(meta.get("subcategories"), list):
        entry["subcategories"] = list(meta["subcategories"])
    milestone_count = meta.get("number_of_milestones")
    if isinstance(milestone_count, int) and milestone_count >= 0:
        entry["number_of_milestones"] = milestone_count
    _refresh_eligibility(entry, action="source-refresh")
    entry["source_dir"] = str(_display_repo_path(source_dir))


# --------------------------------------------------------------------------- #
# Subprocess gate helpers
# --------------------------------------------------------------------------- #
def run_gate(cmd: list[str], label: str) -> dict[str, Any]:
    """Run a gate subprocess and classify its exit code.

    Repo convention: 0 = PASS, 1 = FAIL, 2 = WARN for the check scripts.
    """
    print(f"== {label}: {' '.join(cmd)} ==")
    environment = os.environ.copy()
    environment.update(
        {
            "TB3_TASKS_DIR": str(TASKS_DIR),
            "TB3_SPECS_DIR": str(SPECS_DIR),
            "TB3_SUBMISSIONS_DIR": str(SUBMISSIONS_DIR),
            "TB3_REVIEWS_DIR": str(REVIEWS_DIR),
            "TB3_JOBS_DIR": str(JOBS_DIR),
            "TB3_VALIDATION_SCHEMA": str(ROOTS.validation_schema),
        }
    )
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=environment,
    )
    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    if proc.returncode == 0:
        result = "PASS"
    elif proc.returncode == 2:
        result = "WARN"
    else:
        result = "FAIL"
    return {
        "result": result,
        "exit_code": proc.returncode,
        "at": utc_now(),
        "cmd": " ".join(cmd),
    }


# --------------------------------------------------------------------------- #
# Snorkel export parsing
# --------------------------------------------------------------------------- #
_DIFF_RE = re.compile(r"Difficulty:\s*[^\w]*\s*([A-Za-z]+)")
_STATUS_RE = re.compile(r"Status:\s*(.+)")
_PERF_RE = re.compile(r"•\s*([\w.\-]+):\s*([\d.]+%)\s*\(([^)]*)\)")


def parse_text_summary(text: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if not text:
        return out
    m = _DIFF_RE.search(text)
    if m:
        out["difficulty"] = m.group(1).upper()
    m = _STATUS_RE.search(text)
    if m:
        status_line = m.group(1).strip()
        out["solvable"] = "Solvable" in status_line
        out["status_line"] = status_line
    perf: dict[str, str] = {}
    # Only capture the Agent Performance block (before "Reference Agents").
    perf_region = text.split("Reference Agents")[0]
    for name, pct, _runs in _PERF_RE.findall(perf_region):
        perf[name] = pct
    if perf:
        out["agent_performance"] = perf
    return out


def parse_submission_export(path: Path) -> dict[str, Any] | None:
    """Extract the load-bearing fields from a Snorkel submission export."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None

    docs = data.get("task_documents") or []
    sd: dict[str, Any] = {}
    if docs and isinstance(docs[0], dict):
        sd = docs[0].get("submission_document") or {}

    upload = sd.get("upload_a_zip_file") or {}
    filename = upload.get("filename") or ""
    slug = Path(filename).stem if filename else None

    static = sd.get("feedbackbutton-fast_static_checks") or {}
    parsed = parse_text_summary(sd.get("text_summary") or "")

    def _task_id() -> str | None:
        tid = data.get("task_id")
        if isinstance(tid, dict):
            return tid.get("id")
        return tid if isinstance(tid, str) else None

    def _submission_id() -> str | None:
        sid = data.get("submission_id")
        if isinstance(sid, dict):
            return sid.get("id")
        return sid if isinstance(sid, str) else None

    snorkel = {
        "project": data.get("project"),
        "project_id": (data.get("project_id") or {}).get("id")
        if isinstance(data.get("project_id"), dict)
        else data.get("project_id"),
        "assignment_id": (data.get("assignment_id") or {}).get("id")
        if isinstance(data.get("assignment_id"), dict)
        else data.get("assignment_id"),
        "task_id": _task_id(),
        "submission_id": _submission_id(),
        "zip_filename": filename or None,
        "uploaded_at": upload.get("uploadedAt"),
        "static_outcome": static.get("feedback_outcome"),
        "quality_summary_present": bool(sd.get("quality_check_summary")),
        "source_file": path.name,
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "ingested_at": utc_now(),
    }
    snorkel.update(parsed)
    return {"slug": slug, "snorkel": snorkel}


def _iter_export_paths(explicit: list[str]) -> list[Path]:
    if explicit:
        return [Path(p) if Path(p).is_absolute() else REPO_ROOT / p for p in explicit]
    paths: list[Path] = []
    paths.extend(sorted(REPO_ROOT.glob("submission_*.json")))
    if SNORKEL_INBOX.is_dir():
        paths.extend(sorted(SNORKEL_INBOX.glob("*.json")))
    return paths


# --------------------------------------------------------------------------- #
# Subcommands
# --------------------------------------------------------------------------- #
def cmd_new(args: argparse.Namespace) -> int:
    slug = args.slug
    reg = load_registry()
    if slug in reg["tasks"] and not args.force:
        print(f"Task '{slug}' already registered. Use --force to reset its entry.")
        return 1

    idea = reg["ideas"].get(slug)
    if idea is None:
        idea = new_idea_entry(
            reg,
            slug,
            title=args.title,
            category=args.category,
            languages=_split_csv(args.languages),
            subcategories=_split_csv(getattr(args, "subcategories", None)),
            skills=_split_csv(getattr(args, "skills", None)),
            tags=_split_csv(getattr(args, "tags", None)),
        )
        reg["ideas"][slug] = idea
    elif idea.get("task_slug") not in {None, slug}:
        print(f"Idea '{slug}' is already linked to task '{idea['task_slug']}'.")
        return 1

    if args.category:
        idea["category"] = args.category
    if args.languages:
        idea["languages"] = _split_csv(args.languages)
    if getattr(args, "subcategories", None):
        idea["subcategories"] = _split_csv(args.subcategories)
    if args.number_of_milestones is not None:
        idea["number_of_milestones"] = args.number_of_milestones
    proposal_gaps = _proposal_gaps(idea)
    if proposal_gaps:
        print("Cannot register task before the proposal check:")
        for gap in proposal_gaps:
            print(f"- {gap}")
        return 1
    eligibility_gaps = _eligibility_gaps(idea, action="task-registration")
    if eligibility_gaps:
        _print_eligibility_block(eligibility_gaps)
        return 1

    entry = new_entry(slug)
    if args.category:
        entry["category"] = args.category
    if args.languages:
        entry["languages"] = [x.strip() for x in args.languages.split(",") if x.strip()]
    if getattr(args, "subcategories", None):
        entry["subcategories"] = _split_csv(args.subcategories)
    if args.title:
        entry["title"] = args.title
    if args.number_of_milestones is not None:
        entry["number_of_milestones"] = args.number_of_milestones
    source_dir = TASKS_DIR / slug
    if source_dir.is_dir():
        enrich_from_source(entry, source_dir)
    entry_eligibility_gaps = _eligibility_gaps(entry, action="task-registration")
    if entry_eligibility_gaps:
        _print_eligibility_block(entry_eligibility_gaps)
        return 1
    entry["idea_slug"] = slug
    _refresh_eligibility(entry, action="task-registration")
    reg["tasks"][slug] = entry
    idea["task_slug"] = slug
    idea["next_action"] = "Complete uniqueness research, then run Step 2a validation."
    add_idea_history(idea, "task linked", f"Linked task registry entry {slug}.")
    save_registry(reg)
    write_board(reg)

    _scaffold_idea_record(idea)

    print(f"Registered '{slug}' at phase 'idea'.")
    print("Next: complete the uniqueness dossier before Step 2a validation.")
    return 0


def _split_csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def _idea_record_path(idea: dict[str, Any]) -> Path:
    record = str(idea.get("record") or f"sudhir_ideas/records/{idea['slug']}.md")
    path = Path(record)
    return path if path.is_absolute() else REPO_ROOT / path


def _idea_proposal_path(slug: str) -> Path:
    return IDEA_PROPOSALS_DIR / f"{slug}.md"


def _scaffold_idea_record(idea: dict[str, Any]) -> None:
    idea_path = _idea_record_path(idea)
    if idea_path.exists():
        return
    idea_path.parent.mkdir(parents=True, exist_ok=True)
    idea_path.write_text(_idea_template(idea), encoding="utf-8")
    print(f"Scaffolded idea record: {idea_path.relative_to(REPO_ROOT)}")


def _idea_template(idea: dict[str, Any]) -> str:
    legacy = idea.get("status") == "legacy"
    placeholder = (
        "Not recorded — imported historical work; do not invent retrospective evidence."
        if legacy
        else "TODO — required before this idea can be approved."
    )
    return "\n".join(
        [
            f"# Idea: {idea['title']}",
            "",
            f"- Idea ID: `{idea['id']}`",
            f"- Slug: `{idea['slug']}`",
            f"- Category: {idea['category'] or 'TBD (see task-type-taxonomy.md)'}",
            f"- Languages: {', '.join(idea['languages']) or 'TBD'}",
            f"- Created: {idea['created']}",
            f"- Proposal check: {(idea.get('proposal_check') or {}).get('status', 'not-recorded')}",
            f"- Proposal form: `sudhir_ideas/proposals/{idea['slug']}.md`",
            "- Status source: `sudhir_progress/registry.json` (never maintain status here by hand)",
            "",
            "## Problem in one line",
            "",
            idea.get("summary") or placeholder,
            "",
            "## Novelty fingerprint",
            "",
            f"- Domain/system: {placeholder}",
            f"- Failure mechanism: {placeholder}",
            f"- Distributed fix topology: {placeholder}",
            f"- Verifier/invariant surface: {placeholder}",
            "",
            "## Collision audit",
            "",
            "Search every required scope: idea registry, active tasks, archived tasks, submission",
            "archives, upstream corpus, and current external research.",
            "",
            f"- Closest analogue: {placeholder}",
            f"- Structural differentiator: {placeholder}",
            f"- Evidence paths and retrieval dates: {placeholder}",
            "",
            "## Why it is hard (five hardness axes)",
            "",
            f"- Discover: {placeholder}",
            f"- Synthesize: {placeholder}",
            f"- Diagnose: {placeholder}",
            f"- Navigate coupling: {placeholder}",
            f"- Reason beyond training: {placeholder}",
            "",
            "## Hidden discoveries (>= 3) and fix locations (>= 3)",
            "",
            placeholder,
            "",
            "## Long-horizon investigation profile (new ideas)",
            "",
            f"- Weakness areas (2-4, primary first): {placeholder}",
            f"- Causal chain (4-8 dependent stages): {placeholder}",
            f"- Heterogeneous evidence surfaces (>= 3): {placeholder}",
            f"- Competing hypotheses and deterministic falsifiers (>= 2): {placeholder}",
            f"- Failing scenario and healthy control: {placeholder}",
            f"- Meaningful-action estimate (20-100, no busywork): {placeholder}",
            f"- Determinism strategy: {placeholder}",
            f"- Domain and why this is not trivia: {placeholder}",
            "",
            "## Symptoms-only instruction sketch",
            "",
            placeholder,
            "",
            "## Decision notes",
            "",
            "Status changes are append-only in the registry history. Put durable technical rationale",
            "here, but never claim uniqueness, GO, submission, or acceptance without evidence.",
            "",
        ]
    )


def cmd_idea_new(args: argparse.Namespace) -> int:
    reg = load_registry()
    if args.slug in reg["ideas"]:
        print(f"Idea '{args.slug}' already exists; slugs are never reused.")
        return 1
    if args.slug in reg["tasks"]:
        print(f"Task '{args.slug}' already exists; run `idea backfill` instead.")
        return 1
    idea = new_idea_entry(
        reg,
        args.slug,
        title=args.title,
        category=args.category,
        languages=_split_csv(args.languages),
        subcategories=_split_csv(getattr(args, "subcategories", None)),
        skills=_split_csv(getattr(args, "skills", None)),
        tags=_split_csv(getattr(args, "tags", None)),
        summary=args.summary or "",
    )
    if args.number_of_milestones is not None:
        idea["number_of_milestones"] = args.number_of_milestones
        eligibility = _refresh_eligibility(idea, action="capture")
        if eligibility.blocking:
            idea["next_action"] = "Eligibility blocked by current net-new submission policy."
    reg["ideas"][args.slug] = idea
    save_registry(reg)
    write_board(reg)
    _scaffold_idea_record(idea)
    print(
        f"Captured {idea['id']} '{args.slug}'. Proposal check and uniqueness are "
        "PENDING; execution is blocked."
    )
    return 0


def _read_optional_text(inline: str | None, file_value: str | None) -> str | None:
    if inline is not None and file_value is not None:
        raise ValueError("provide inline text or a file, not both")
    if file_value is None:
        return inline
    path = Path(file_value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.read_text(encoding="utf-8").strip()


def cmd_idea_proposal(args: argparse.Namespace) -> int:
    reg = load_registry()
    idea = _get_idea_or_error(reg, args.slug)
    if idea is None:
        return 1
    proposal = dict(idea.get("proposal_check") or {})
    try:
        summary_arg = _read_optional_text(args.summary, args.summary_file)
        feedback_arg = _read_optional_text(args.feedback, args.feedback_file)
    except (OSError, ValueError) as exc:
        print(f"Cannot capture proposal: {exc}")
        return 2

    summary = summary_arg if summary_arg is not None else str(proposal.get("summary") or "")
    category = args.category or str(proposal.get("category_label") or idea.get("category") or "")
    skills = (
        _split_csv(args.skills)
        if args.skills is not None
        else list(proposal.get("associated_skills") or [])
    )
    tags = (
        _split_csv(args.tags)
        if args.tags is not None
        else list(proposal.get("task_tags") or [])
    )
    inspiration = dict(proposal.get("inspiration") or {})
    source_type = args.source_type or str(inspiration.get("source_type") or "")
    source_reference = args.source_reference or str(
        inspiration.get("source_reference") or ""
    )
    reuse_boundary = args.reuse_boundary or str(
        inspiration.get("reuse_boundary") or ""
    )
    errors = idea_proposal.field_errors(
        summary=summary,
        category=category,
        skills=skills,
        tags=tags,
    )
    if args.verdict in {"passed", "failed"} and not args.evidence:
        errors.append(f"proposal {args.verdict} requires at least one --evidence reference")
    if args.verdict == "failed" and not (feedback_arg or proposal.get("feedback")):
        errors.append("proposal failed requires --feedback or --feedback-file")
    if args.verdict in {"passed", "failed"}:
        for label, value in (
            ("--source-type", source_type),
            ("--source-reference", source_reference),
            ("--reuse-boundary", reuse_boundary),
        ):
            if not value.strip():
                errors.append(f"proposal {args.verdict} requires {label}")
    if errors:
        print("Cannot capture Task Idea Proposal:")
        for error in errors:
            print(f"- {error}")
        return 2

    normalized = idea_proposal.normalize_category(category)
    assert normalized is not None
    proposal.update(
        {
            "status": args.verdict,
            "summary": summary,
            "category_label": normalized[0],
            "category_slug": normalized[1],
            "associated_skills": skills,
            "task_tags": tags,
            "checked_at": utc_now() if args.verdict in {"passed", "failed"} else None,
            "evidence": list(dict.fromkeys(args.evidence or proposal.get("evidence") or [])),
            "feedback": feedback_arg if feedback_arg is not None else str(proposal.get("feedback") or ""),
            "inspiration": {
                "source_type": source_type,
                "source_reference": source_reference,
                "reuse_boundary": reuse_boundary,
            },
        }
    )
    idea["proposal_check"] = proposal
    idea["summary"] = summary
    idea["category"] = normalized[1]
    if args.verdict == "passed":
        idea["next_action"] = "Complete the novelty fingerprint and six-scope collision audit."
    elif args.verdict == "failed":
        idea["next_action"] = "Revise the proposal fields and rerun Check feedback, or reject the idea."
    else:
        idea["next_action"] = "Paste the proposal fields into Snorkel and run Check feedback."
    add_idea_history(
        idea,
        f"proposal {args.verdict}",
        proposal["feedback"] or "Task Idea Proposal fields captured.",
    )
    proposal_path = _idea_proposal_path(args.slug)
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.write_text(
        idea_proposal.render_proposal(args.slug, proposal, generated_at=utc_now()),
        encoding="utf-8",
    )
    save_registry(reg)
    write_board(reg)
    print(f"Idea '{args.slug}' proposal set to '{args.verdict}'.")
    display_path = (
        proposal_path.relative_to(REPO_ROOT)
        if proposal_path.is_relative_to(REPO_ROOT)
        else proposal_path
    )
    print(f"Saved proposal: {display_path}")
    return 0


def _get_idea_or_error(reg: dict[str, Any], slug: str) -> dict[str, Any] | None:
    idea = (reg.get("ideas") or {}).get(slug)
    if idea is None:
        print(f"No idea '{slug}' in registry. Run `idea new` or `idea backfill` first.")
    return idea


def cmd_idea_status(args: argparse.Namespace) -> int:
    reg = load_registry()
    idea = _get_idea_or_error(reg, args.slug)
    if idea is None:
        return 1
    if args.status in {"approved"}:
        gaps = _approval_gaps(idea)
        if gaps:
            print("Cannot approve idea:")
            for gap in gaps:
                print(f"- {gap}")
            return 1
    if args.status in {"grandfathered", "rejected", "retired", "reserved"} and not args.reason:
        print(f"Status '{args.status}' requires --reason.")
        return 2
    old_status = idea.get("status")
    idea["status"] = args.status
    if args.next:
        idea["next_action"] = args.next
    elif args.status == "reserved":
        idea["next_action"] = "Keep reserved; rerun uniqueness research before activation."
    elif args.status == "rejected":
        idea["next_action"] = "None; slug remains reserved and may not be reused."
    add_idea_history(
        idea,
        f"status {old_status} -> {args.status}",
        args.reason or "Status synchronized with recorded evidence.",
    )
    save_registry(reg)
    write_board(reg)
    print(f"Idea '{args.slug}' status set to '{args.status}'.")
    return 0


def cmd_idea_quarantine(args: argparse.Namespace) -> int:
    reg = load_registry()
    idea = _get_idea_or_error(reg, args.slug)
    if idea is None:
        return 1
    task_slug = idea.get("task_slug")
    task = (reg.get("tasks") or {}).get(task_slug) if task_slug else None
    if task is None:
        print(f"Idea '{args.slug}' has no linked imported task to quarantine.")
        return 1

    snorkel = task.get("snorkel") or {}
    quarantine = {
        "at": utc_now(),
        "reason": args.reason,
        "evidence": list(dict.fromkeys(args.evidence or [])),
        "source_file": snorkel.get("source_file"),
        "project_id": snorkel.get("project_id"),
        "assignment_id": snorkel.get("assignment_id"),
        "submission_id": snorkel.get("submission_id"),
        "uploaded_at": snorkel.get("uploaded_at"),
    }
    old_status = idea.get("status")
    idea["portfolio_scope"] = "quarantined"
    idea["status"] = "retired"
    idea["quarantine"] = quarantine
    idea["next_action"] = "None; preserve only as historical import provenance."
    add_idea_history(
        idea,
        f"status {old_status} -> retired; quarantined",
        args.reason,
    )

    task["portfolio_scope"] = "quarantined"
    task["quarantine"] = quarantine
    task["next_action"] = "Quarantined from the active portfolio; provenance retained."
    touch(task)
    add_note(task, f"quarantined import: {args.reason}")

    save_registry(reg)
    write_board(reg)
    print(f"Quarantined '{args.slug}' outside the active portfolio; no history was deleted.")
    return 0


def cmd_idea_uniqueness(args: argparse.Namespace) -> int:
    reg = load_registry()
    idea = _get_idea_or_error(reg, args.slug)
    if idea is None:
        return 1
    if args.verdict == "passed":
        eligibility_gaps = _eligibility_gaps(idea, action="idea-uniqueness")
        if eligibility_gaps:
            save_registry(reg)
            write_board(reg)
            _print_eligibility_block(eligibility_gaps)
            return 1
    uniqueness = idea.setdefault("uniqueness", {})
    fingerprint = uniqueness.setdefault("fingerprint", {})

    scopes = _split_csv(args.scope)
    if scopes:
        uniqueness["scope"] = sorted(set(scopes))
    if args.evidence:
        uniqueness["evidence"] = list(dict.fromkeys(args.evidence))
    for field in ("domain", "mechanism", "topology", "verification"):
        value = getattr(args, field)
        if value is not None:
            fingerprint[field] = value
    if args.closest is not None:
        uniqueness["closest_analogue"] = args.closest
    if args.difference is not None:
        uniqueness["differentiator"] = args.difference
    if args.reason is not None:
        uniqueness["reason"] = args.reason
    uniqueness["status"] = args.verdict
    uniqueness["checked_at"] = utc_now() if args.verdict in {"passed", "failed"} else None

    if args.verdict == "passed":
        gaps = _uniqueness_gaps(idea)
        if gaps:
            print("Cannot record uniqueness PASS:")
            for gap in gaps:
                print(f"- {gap}")
            return 1
        idea["next_action"] = "Run Step 2a validation; construction remains blocked until GO."
    elif args.verdict == "failed":
        if not args.reason:
            print("Uniqueness FAIL requires --reason.")
            return 2
        idea["status"] = "rejected"
        idea["next_action"] = "None; rejected because the concept is not sufficiently distinct."

    add_idea_history(
        idea,
        f"uniqueness {args.verdict}",
        args.reason or "Collision-audit evidence updated.",
    )
    save_registry(reg)
    write_board(reg)
    print(f"Idea '{args.slug}' uniqueness set to '{args.verdict}'.")
    return 0


def cmd_idea_validation(args: argparse.Namespace) -> int:
    reg = load_registry()
    idea = _get_idea_or_error(reg, args.slug)
    if idea is None:
        return 1
    if args.verdict == "go":
        eligibility_gaps = _eligibility_gaps(idea, action="step2a-go")
        if eligibility_gaps:
            save_registry(reg)
            write_board(reg)
            _print_eligibility_block(eligibility_gaps)
            return 1
    if args.verdict == "go" and _uniqueness_gaps(idea):
        print("Step 2a GO cannot be recorded before uniqueness PASS is complete.")
        return 1
    if args.verdict == "stop" and not args.reason:
        print("Step 2a STOP requires --reason.")
        return 2
    validation = idea.setdefault("validation", {})
    validation["status"] = args.verdict
    if args.attempt is not None:
        validation["attempt"] = args.attempt
    if args.evidence:
        validation["evidence"] = list(dict.fromkeys(args.evidence))
    if args.reason is not None:
        validation["reason"] = args.reason

    if args.verdict == "in-progress":
        idea["status"] = "validating"
        idea["next_action"] = "Complete Step 2a and record GO or STOP with evidence."
    elif args.verdict == "go":
        if not validation.get("evidence"):
            print("Step 2a GO requires at least one --evidence path.")
            return 1
        idea["status"] = "approved"
        idea["next_action"] = "Approved for construction; create/link the task and execute it."
    elif args.verdict == "stop":
        idea["status"] = "rejected"
        idea["next_action"] = "None; retain the record and rejection reason for collision avoidance."

    add_idea_history(
        idea,
        f"Step 2a {args.verdict}",
        args.reason or "Validation evidence updated.",
    )
    save_registry(reg)
    write_board(reg)
    print(f"Idea '{args.slug}' Step 2a verdict set to '{args.verdict}'.")
    return 0


def cmd_idea_list(args: argparse.Namespace) -> int:
    reg = load_registry()
    scope = None if args.all else "active"
    ideas = [
        idea
        for idea in (reg.get("ideas") or {}).values()
        if scope is None or idea.get("portfolio_scope", "active") == scope
    ]
    if args.status:
        ideas = [idea for idea in ideas if idea.get("status") == args.status]
    if args.json:
        print(json.dumps(ideas, indent=2, sort_keys=True))
    else:
        print("\n".join(_idea_rows(reg, args.status, scope)))
    return 0


def _backfill_idea_for_task(reg: dict[str, Any], slug: str, task: dict[str, Any]) -> bool:
    task["idea_slug"] = slug
    idea = reg["ideas"].get(slug)
    if idea is not None:
        idea["task_slug"] = slug
        if idea.get("status") == "legacy" and idea.get("next_action") == (
            "Complete the novelty fingerprint and collision audit."
        ):
            idea["next_action"] = "Do not reuse without a fresh uniqueness dossier."
        return False

    phase = task.get("phase")
    if phase == "idea":
        status = "captured"
    elif phase == "step2a":
        status = "validating"
    else:
        status = "legacy"
    idea = new_idea_entry(
        reg,
        slug,
        title=task.get("title"),
        category=task.get("category"),
        languages=list(task.get("languages") or []),
        subcategories=list(task.get("subcategories") or []),
        summary="Imported from the existing task registry.",
        status=status,
    )
    idea["task_slug"] = slug
    if status == "validating":
        idea["validation"]["status"] = "in-progress"
        idea["next_action"] = "Complete Step 2a evidence and record GO or STOP."
    reg["ideas"][slug] = idea
    _scaffold_idea_record(idea)
    return True


def cmd_idea_backfill(_args: argparse.Namespace) -> int:
    reg = load_registry()
    added = 0
    for slug, task in sorted(reg["tasks"].items()):
        if _backfill_idea_for_task(reg, slug, task):
            added += 1
    save_registry(reg)
    write_board(reg)
    print(f"Idea backfill complete: {added} added, {len(reg['ideas'])} total.")
    return 0


def cmd_idea_validate(_args: argparse.Namespace) -> int:
    reg = load_registry()
    errors, warnings = validate_idea_registry(reg)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Idea registry: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


def cmd_outcome(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    if args.status in {"accepted", "rejected", "needs-revision"} and not args.reason:
        print(f"Platform status '{args.status}' requires --reason.")
        return 2
    entry["platform_status"] = {
        "status": args.status,
        "source": "explicit",
        "at": utc_now(),
        "reason": args.reason or "Status synchronized from platform evidence.",
        "evidence": list(dict.fromkeys(args.evidence or [])),
    }
    if args.next:
        entry["next_action"] = args.next
    elif args.status == "in-review":
        entry["next_action"] = "Await the platform reviewer decision."
    elif args.status == "in-evaluation":
        entry["next_action"] = "Await the platform evaluation result."
    touch(entry)
    add_note(entry, f"platform outcome -> {args.status}: {args.reason or 'evidence synchronized'}")
    save_registry(reg)
    write_board(reg)
    print(f"'{args.slug}' platform outcome set to '{args.status}'.")
    return 0


def cmd_eligibility(args: argparse.Namespace) -> int:
    reg = load_registry()
    task = get_entry(reg, args.slug)
    idea = (reg.get("ideas") or {}).get(args.slug)
    record = task or idea
    if record is None:
        print(f"No task or idea '{args.slug}' in registry.")
        return 1
    if task is not None:
        source_dir = TASKS_DIR / args.slug
        if source_dir.is_dir():
            enrich_from_source(task, source_dir)
    result = _refresh_eligibility(record, action=args.action)
    save_registry(reg)
    write_board(reg)
    if args.json:
        print(json.dumps(record["eligibility_verdict"], indent=2, sort_keys=True))
    else:
        print(
            f"{args.slug}: official={result.official_status} "
            f"house={result.house_status} blocking={result.blocking}"
        )
        for reason in result.reasons:
            print(f"- {reason}")
    return 1 if result.blocking else 0


def _exemption_effective_date(record: dict[str, Any], rule_id: str) -> str | None:
    for candidate, effective_date in eligibility_policy.applicable_rules(record):
        if candidate == rule_id:
            return effective_date
    return None


def cmd_exemption_capture(args: argparse.Namespace) -> int:
    reg = load_registry()
    task = get_entry(reg, args.slug)
    idea = (reg.get("ideas") or {}).get(args.slug)
    if task is not None:
        source_dir = TASKS_DIR / args.slug
        if source_dir.is_dir():
            enrich_from_source(task, source_dir)
        if idea is not None:
            idea["subcategories"] = list(task.get("subcategories") or [])
    records = [record for record in (idea, task) if record is not None]
    if not records:
        print(f"No task or idea '{args.slug}' in registry.")
        return 1

    effective_date = args.effective_date or _exemption_effective_date(
        task or idea or {}, args.rule_id
    )
    if effective_date is None:
        print(f"Rule {args.rule_id!r} is not applicable to '{args.slug}'.")
        return 2
    exemption_id = args.exemption_id or (
        args.slug
        + "-"
        + re.sub(r"[^a-z0-9]+", "-", args.rule_id.lower()).strip("-")
    )
    exemption = {
        "id": exemption_id,
        "rule_id": args.rule_id,
        "effective_date": effective_date,
        "recorded_at": utc_now(),
        "source": args.source,
        "platform_state": args.platform_state.upper(),
        "evidence": list(dict.fromkeys(args.evidence)),
        "reason": args.reason,
        "status": "active",
    }
    errors = eligibility_policy.exemption_errors(exemption)
    if errors:
        print("Cannot capture exemption:")
        for error in errors:
            print(f"- {error}")
        return 2

    results: list[eligibility_policy.EligibilityResult] = []
    for record in records:
        exemptions = record.setdefault("in_flight_exemptions", [])
        exemptions[:] = [row for row in exemptions if row.get("id") != exemption_id]
        exemptions.append(dict(exemption))
        if args.first_submitted_at:
            record["first_submitted_at"] = args.first_submitted_at
            record["first_submitted_evidence"] = list(dict.fromkeys(args.evidence))
        results.append(_refresh_eligibility(record, action="exemption-capture"))

    if idea is not None:
        add_idea_history(idea, "eligibility exemption captured", args.reason)
    if task is not None:
        touch(task)
        add_note(task, f"eligibility exemption {exemption_id}: {args.reason}")
    save_registry(reg)
    write_board(reg)
    result = results[-1]
    print(
        f"Captured exemption '{exemption_id}' for '{args.slug}': "
        f"official={result.official_status} blocking={result.blocking}"
    )
    if result.blocking:
        for reason in result.reasons:
            print(f"- {reason}")
        return 1
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    reg = load_registry()
    if args.slug:
        entry = get_entry(reg, args.slug)
        if entry is None:
            print(f"No task '{args.slug}' in registry.")
            return 1
        print(json.dumps(entry, indent=2, sort_keys=True))
    else:
        print(json.dumps(reg, indent=2, sort_keys=True))
    return 0


def cmd_board(_args: argparse.Namespace) -> int:
    reg = load_registry()
    write_board(reg)
    print(
        f"Wrote {BOARD_PATH.relative_to(REPO_ROOT)}, "
        f"{IDEA_INDEX_PATH.relative_to(REPO_ROOT)}, and "
        f"{STATUS_PATH.relative_to(REPO_ROOT)} "
        f"({len(reg['ideas'])} ideas, {len(reg['tasks'])} tasks)."
    )
    return 0


def cmd_phase(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry. Run `new` first.")
        return 1
    if args.phase not in PHASES:
        print(f"Unknown phase '{args.phase}'. Valid: {', '.join(PHASES)}")
        return 2

    idea_slug = entry.get("idea_slug") or args.slug
    idea = (reg.get("ideas") or {}).get(idea_slug)
    if idea is None:
        print(
            f"Task '{args.slug}' has no idea record. Run `python3 sudhir_task.py idea backfill` first."
        )
        return 1
    if _phase_index(args.phase) >= _phase_index("construct"):
        gaps = _task_execution_gaps(reg, entry)
        if gaps:
            _print_execution_block(gaps)
            return 1
    source_dir = TASKS_DIR / args.slug
    if source_dir.is_dir():
        enrich_from_source(entry, source_dir)
    if args.phase == "submitted":
        eligibility_gaps = _eligibility_gaps(entry, action="submit")
        if eligibility_gaps:
            save_registry(reg)
            write_board(reg)
            _print_eligibility_block(eligibility_gaps)
            return 1

    entry["phase"] = args.phase
    if args.next:
        entry["next_action"] = args.next
    if source_dir.is_dir():
        enrich_from_source(entry, source_dir)
    if args.phase == "step2a" and idea.get("status") != "legacy":
        idea["status"] = "validating"
        idea.setdefault("validation", {})["status"] = "in-progress"
        idea["next_action"] = "Complete Step 2a and record GO or STOP with evidence."
        add_idea_history(idea, "Step 2a started", "Task phase moved to step2a.")
    touch(entry)
    add_note(entry, f"phase -> {args.phase}")
    save_registry(reg)
    write_board(reg)
    print(f"'{args.slug}' phase set to '{args.phase}'.")
    return 0


def cmd_revise(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    stale_zip = SUBMISSIONS_DIR / f"{args.slug}.zip"
    stale_backup = SUBMISSIONS_DIR / f".{args.slug}.{os.getpid()}.revision-backup"
    stale_backup.unlink(missing_ok=True)
    if stale_zip.exists():
        try:
            root_adapter.ROOTS.assert_writable(stale_zip)
            os.replace(stale_zip, stale_backup)
            from scripts import build_submission_index

            build_submission_index.write_index_atomic(
                SUBMISSIONS_DIR,
                CURRENT_SUBMISSION_INDEX_PATH,
            )
        except Exception as error:
            if stale_backup.exists():
                os.replace(stale_backup, stale_zip)
            print(f"Could not remove stale package {_display_repo_path(stale_zip)}: {error}")
            return 1
        stale_backup.unlink(missing_ok=True)
    entry["revision"] = entry.get("revision", 0) + 1
    # Any task edit invalidates prior gate + package evidence (lifecycle rule).
    entry["gates"] = {}
    entry["package"] = {}
    entry["phase"] = (
        "construct"
        if _phase_index(entry.get("phase", "")) > _phase_index("construct")
        else entry.get("phase", "construct")
    )
    reason = args.reason or "revision opened"
    entry["next_action"] = f"Re-run gates after revision {entry['revision']}: {reason}"
    rev_dir = sudhir_dossier.open_revision_workspace(REVIEWS_DIR, entry, reason=reason)
    touch(entry)
    add_note(entry, f"revision {entry['revision']}: {reason}")
    save_registry(reg)
    write_board(reg)
    print(
        f"Opened revision {entry['revision']} for '{args.slug}' at "
        f"{rev_dir.relative_to(REPO_ROOT)}. "
        "Prior gate and package evidence invalidated; rerun gates."
    )
    return 0


def cmd_gates(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry. Run `new` first.")
        return 1
    execution_gaps = _task_execution_gaps(reg, entry)
    if execution_gaps:
        _print_execution_block(execution_gaps)
        return 1
    source_dir = TASKS_DIR / args.slug
    if not source_dir.is_dir():
        print(f"Task source not found: {source_dir.relative_to(REPO_ROOT)}")
        return 1

    task_arg = str(source_dir)
    gates = {
        "static": ["python3", "run_static_checks.py", "--task-dir", task_arg, "--version", "edition_2"],
        "dockerfile": ["python3", "dockerfile_check.py", task_arg],
        "collapse": ["python3", "collapse_check.py", task_arg],
        "integrity": ["python3", "task_integrity.py", "verify", task_arg],
    }
    results: dict[str, Any] = {}
    overall_ok = True
    for name, cmd in gates.items():
        if not (REPO_ROOT / f"{cmd[1]}").exists() and cmd[1].endswith(".py"):
            results[name] = {"result": "SKIP", "reason": "script missing", "at": utc_now()}
            continue
        res = run_gate(cmd, name)
        results[name] = res
        if res["result"] == "FAIL":
            overall_ok = False

    entry["gates"] = results
    enrich_from_source(entry, source_dir)
    if _phase_index(entry.get("phase", "")) < _phase_index("gates"):
        entry["phase"] = "gates"
    entry["next_action"] = (
        "Run oracle 1x + NOP (needs Docker), then review."
        if overall_ok
        else "Fix failing cheap gate(s), then rerun `sudhir_task.py gates`."
    )
    touch(entry)
    save_registry(reg)
    write_board(reg)
    print(f"\nGate summary for '{args.slug}': "
          + ", ".join(f"{k}={v.get('result')}" for k, v in results.items()))
    return 0 if overall_ok else 1


def cmd_package(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    execution_gaps = _task_execution_gaps(reg, entry)
    if execution_gaps:
        _print_execution_block(execution_gaps)
        return 1
    source_dir = TASKS_DIR / args.slug
    if not source_dir.is_dir():
        print(f"Task source not found: {source_dir.relative_to(REPO_ROOT)}")
        return 1
    enrich_from_source(entry, source_dir)
    eligibility_gaps = _eligibility_gaps(entry, action="package")
    if eligibility_gaps:
        save_registry(reg)
        write_board(reg)
        _print_eligibility_block(eligibility_gaps)
        return 1

    rev = int(entry.get("revision") or 0)
    if rev < 1:
        # First package without revise: open REV-1 workspace for form/checklist storage.
        entry["revision"] = 1
        sudhir_dossier.open_revision_workspace(
            REVIEWS_DIR, entry, reason="package without prior revise"
        )
        rev = 1
    rev_dir = sudhir_dossier.revision_dir(REVIEWS_DIR, args.slug, rev)
    preupload = rev_dir / "PREUPLOAD.md"
    if not args.force:
        ok, detail = sudhir_dossier.preupload_complete(preupload)
        if not ok:
            print(
                f"PREUPLOAD checklist incomplete ({detail}). "
                f"Tick items in {preupload.relative_to(REPO_ROOT)} or pass --force."
            )
            return 1

    SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = SUBMISSIONS_DIR / f"{args.slug}.zip"
    root_adapter.ROOTS.assert_writable(zip_path)
    candidate = SUBMISSIONS_DIR / f".{args.slug}.{os.getpid()}.candidate"
    backup = SUBMISSIONS_DIR / f".{args.slug}.{os.getpid()}.previous"
    candidate.unlink(missing_ok=True)
    backup.unlink(missing_ok=True)
    _build_submission_zip(source_dir, candidate)
    had_previous = zip_path.exists()
    if had_previous:
        os.replace(zip_path, backup)
    os.replace(candidate, zip_path)

    def restore_previous_package() -> None:
        zip_path.unlink(missing_ok=True)
        if had_previous and backup.exists():
            os.replace(backup, zip_path)

    print(f"Built {_display_repo_path(zip_path)}")

    validate = run_gate(
        ["python3", "validate_submission_zip.py", str(zip_path)], "validate-zip"
    )
    sha = sudhir_dossier.sha256_file(zip_path)
    members = sudhir_dossier.zip_member_count(zip_path)
    pkg = {
        "zip": str(_display_repo_path(zip_path)),
        "validated": validate["result"] == "PASS",
        "at": utc_now(),
        "sha256": sha,
        "member_count": members,
    }
    entry["package"] = pkg
    for row in entry.get("revisions") or []:
        if int(row.get("n", -1)) == rev:
            row["zip_sha"] = sha
            break

    if not args.skip_approve:
        approve = run_gate(
            [
                "python3", "approve_task.py", "--task-dir", str(source_dir),
                "--zip", str(zip_path), "--skip-verifier-health",
            ],
            "approve",
        )
        pkg["approved"] = approve["result"] == "PASS"

    package_ok = pkg.get("validated") and (args.skip_approve or pkg.get("approved", False))
    if package_ok:
        try:
            from scripts import build_submission_index

            index = build_submission_index.write_index_atomic(
                SUBMISSIONS_DIR,
                CURRENT_SUBMISSION_INDEX_PATH,
            )
            index_display = (
                CURRENT_SUBMISSION_INDEX_PATH.relative_to(REPO_ROOT)
                if CURRENT_SUBMISSION_INDEX_PATH.is_relative_to(REPO_ROOT)
                else CURRENT_SUBMISSION_INDEX_PATH
            )
            pkg["index"] = str(index_display)
            pkg["index_archive_count"] = index["archive_count"]
        except Exception as exc:
            restore_previous_package()
            print(f"Canonical index refresh failed; package rolled back: {exc}")
            pkg["validated"] = False
            package_ok = False
    else:
        restore_previous_package()
    backup.unlink(missing_ok=True)

    if package_ok and pkg.get("approved", False):
        entry["phase"] = "package"
        entry["next_action"] = (
            "Upload the zip to the Snorkel platform, then "
            "`sudhir_task.py phase <slug> submitted`. Store form paste fields with "
            "`form-capture` if not already in the REV dossier."
        )
    else:
        entry["next_action"] = "Resolve packaging/approval failures, then re-run `package`."
    touch(entry)
    save_registry(reg)
    write_board(reg)
    print(f"package sha256={sha} members={members}")
    return 0 if package_ok else 1


# Exclusion list mirrors commands.md Packaging + scripts/check-task.sh Phase B.
_ZIP_EXCLUDE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".cursor",
    ".aider",
    ".continue",
    ".claude",
}
_ZIP_EXCLUDE_ROOT_FILES = {
    "output_contract.toml",
    "quality_check_adjudication.json",
    "construction_manifest.json",
    "rubric.txt",
    "rubrics.txt",
}
_ZIP_EXCLUDE_ANY_FILES = {"CLAUDE.md", "AGENTS.md", "skills.md"}


def _build_submission_zip(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(source_dir)
            parts = set(rel.parts)
            if parts & _ZIP_EXCLUDE_DIRS:
                continue
            if path.suffix in {".pyc", ".pyo"}:
                continue
            if path.name in _ZIP_EXCLUDE_ANY_FILES:
                continue
            if rel.name.startswith(".") and len(rel.parts) == 1:
                continue  # task-root dotfiles (.step2b-checksum, .dockerignore stays via env dir)
            if len(rel.parts) == 1 and rel.name in _ZIP_EXCLUDE_ROOT_FILES:
                continue
            zf.write(path, rel.as_posix())



def _read_text_arg(path: str | None, use_stdin: bool) -> str:
    if use_stdin:
        return sys.stdin.read()
    if not path:
        raise ValueError("text source required")
    return Path(path).read_text(encoding="utf-8")


def cmd_evidence(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    kind_map = {
        "oracle_1x": args.oracle_1x,
        "nop": args.nop,
        "oracle_10x": args.oracle_10x,
    }
    selected = [(kind, job) for kind, job in kind_map.items() if job]
    if not selected:
        print("Provide one of --oracle-1x / --nop / --oracle-10x JOB_ID")
        return 1
    rev = int(entry.get("revision") or 0)
    if rev < 1:
        entry["revision"] = 1
        sudhir_dossier.open_revision_workspace(
            REVIEWS_DIR, entry, reason="evidence capture"
        )
        rev = 1
    rev_dir = sudhir_dossier.revision_dir(REVIEWS_DIR, args.slug, rev)
    evidence_md = rev_dir / "EVIDENCE.md"
    for kind, job in selected:
        job_dir = sudhir_dossier.resolve_job_dir(REPO_ROOT, JOBS_DIR, job)
        if job_dir is None:
            print(f"Harbor job not found: {job}")
            return 1
        result_path = job_dir / "result.json"
        mean = sudhir_dossier.parse_harbor_mean(result_path)
        if mean is None:
            print(f"Could not parse mean from {result_path}")
            return 1
        try:
            rel_job = str(job_dir.relative_to(REPO_ROOT))
        except ValueError:
            rel_job = str(job_dir)
        record = {"job": job_dir.name, "mean": mean, "at": utc_now(), "path": rel_job}
        entry["evidence"][kind] = record
        with evidence_md.open("a", encoding="utf-8") as handle:
            handle.write(
                f"\n- `{kind}`: job `{record['job']}` mean={mean} at {record['at']} ({rel_job})\n"
            )
        print(f"recorded {kind}: job={record['job']} mean={mean}")
    touch(entry)
    add_note(entry, "recorded Harbor evidence: " + ", ".join(k for k, _ in selected))
    save_registry(reg)
    write_board(reg)
    return 0


def cmd_feedback_capture(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    rev = int(entry.get("revision") or 0)
    if rev < 1:
        entry["revision"] = 1
        sudhir_dossier.open_revision_workspace(
            REVIEWS_DIR, entry, reason="feedback-capture"
        )
        rev = 1
    try:
        body = _read_text_arg(args.text_file, args.stdin)
    except ValueError:
        print("Provide --text-file PATH or --stdin")
        return 1
    rev_dir = sudhir_dossier.revision_dir(REVIEWS_DIR, args.slug, rev)
    sudhir_dossier.write_capture_file(
        rev_dir / "FEEDBACK.md",
        f"REV-{rev} reviewer feedback — {args.slug}",
        body,
    )
    suggestions = sudhir_dossier.suggest_cm_ids(body)
    if suggestions:
        sudhir_dossier.update_revision_cm_ids(entry, suggestions)
        (rev_dir / "CM-SUGGESTIONS.md").write_text(
            "# CM suggestions (keyword map)\n\n"
            + "\n".join(f"- {cm}" for cm in suggestions)
            + "\n\nConfirm and append to COMMON_MISTAKES.md if new; bump Seen if known.\n",
            encoding="utf-8",
        )
        print("CM suggestions:", ", ".join(suggestions))
    entry["platform_status"] = {
        "status": "needs-revision",
        "source": "explicit",
        "at": utc_now(),
        "reason": "Reviewer feedback captured into dossier",
        "evidence": [f"sudhir_reviews/{args.slug}/REV-{rev}/FEEDBACK.md"],
    }
    entry["phase"] = "feedback"
    entry["next_action"] = (
        f"Address REV-{rev} feedback; tick PREUPLOAD; rerun gates and package."
    )
    touch(entry)
    add_note(entry, f"feedback-capture -> REV-{rev}/FEEDBACK.md")
    save_registry(reg)
    write_board(reg)
    print(f"Wrote {rev_dir.relative_to(REPO_ROOT)}/FEEDBACK.md")
    return 0


def cmd_form_capture(args: argparse.Namespace) -> int:
    """Store every Snorkel form paste field for the current revision."""
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    rev = int(entry.get("revision") or 0)
    if rev < 1:
        entry["revision"] = 1
        sudhir_dossier.open_revision_workspace(
            REVIEWS_DIR, entry, reason="form-capture"
        )
        rev = 1
    rev_dir = sudhir_dossier.revision_dir(REVIEWS_DIR, args.slug, rev)
    mapping = {
        "difficulty": args.difficulty_file,
        "solution": args.solution_file,
        "verification": args.verification_file,
        "rubric": args.rubric_file,
    }
    written = []
    for key, file_arg in mapping.items():
        if not file_arg:
            continue
        body = Path(file_arg).read_text(encoding="utf-8")
        filename = sudhir_dossier.FORM_FILES[key]
        sudhir_dossier.write_capture_file(
            rev_dir / filename,
            f"{filename.removesuffix('.md')} — {args.slug} REV-{rev}",
            body,
        )
        written.append(filename)
        rel = f"sudhir_reviews/{args.slug}/REV-{rev}/{filename}"
        entry["learning"].setdefault("form_refs", {})[key] = rel
        for row in entry.get("revisions") or []:
            if int(row.get("n", -1)) == rev:
                row.setdefault("form_refs", {})[key] = rel
                if key == "rubric":
                    row["rubric_ref"] = rel
    if not written:
        print(
            "Provide at least one of --difficulty-file / --solution-file / "
            "--verification-file / --rubric-file"
        )
        return 1
    touch(entry)
    add_note(entry, "form-capture: " + ", ".join(written))
    save_registry(reg)
    write_board(reg)
    print(f"Stored form fields in {rev_dir.relative_to(REPO_ROOT)}: {', '.join(written)}")
    return 0


def cmd_rubric_capture(args: argparse.Namespace) -> int:
    args.difficulty_file = None
    args.solution_file = None
    args.verification_file = None
    # reuse form-capture for rubric only
    ns = argparse.Namespace(
        slug=args.slug,
        difficulty_file=None,
        solution_file=None,
        verification_file=None,
        rubric_file=args.text_file,
    )
    return cmd_form_capture(ns)


def cmd_learn_check(args: argparse.Namespace) -> int:
    reg = load_registry()
    entry = get_entry(reg, args.slug)
    if entry is None:
        print(f"No task '{args.slug}' in registry.")
        return 1
    sudhir_dossier.ensure_task_learning_fields(entry)
    source_dir = TASKS_DIR / args.slug
    prompts = sudhir_dossier.applicable_cm_prompts(
        entry, source_dir if source_dir.is_dir() else None
    )
    print(f"Applicable preventions for {args.slug}:")
    for line in prompts:
        print(f"  - {line}")
    rev = int(entry.get("revision") or 0)
    if rev < 1:
        print("No revision dossier yet; run revise or package will open REV-1.")
        return 1
    preupload = sudhir_dossier.revision_dir(REVIEWS_DIR, args.slug, rev) / "PREUPLOAD.md"
    ok, detail = sudhir_dossier.preupload_complete(preupload)
    print(f"PREUPLOAD: {'PASS' if ok else 'FAIL'} ({detail})")
    return 0 if ok else 1


def cmd_ingest(args: argparse.Namespace) -> int:
    reg = load_registry()
    paths = _iter_export_paths(args.paths)
    if not paths:
        print("No submission exports found (submission_*.json or sudhir_snorkel/inbox/*.json).")
        return 0

    ingested = 0
    unchanged = 0
    unmatched: list[str] = []
    for path in paths:
        if not path.is_file():
            print(f"skip (missing): {path}")
            continue
        parsed = parse_submission_export(path)
        if parsed is None:
            print(f"skip (unparseable): {path.name}")
            continue
        slug = parsed["slug"]
        snorkel = parsed["snorkel"]
        if not slug:
            unmatched.append(path.name)
            print(f"skip (no zip filename in export): {path.name}")
            continue
        entry = get_entry(reg, slug)
        if entry is None:
            entry = new_entry(slug)
            entry["title"] = slug.replace("-", " ").title()
            reg["tasks"][slug] = entry
        sudhir_dossier.ensure_task_learning_fields(entry)
        previous_snorkel = entry.get("snorkel") or {}
        same_export = (
            previous_snorkel.get("submission_id") == snorkel.get("submission_id")
            and previous_snorkel.get("source_file") == snorkel.get("source_file")
            and previous_snorkel.get("source_sha256") in {None, snorkel.get("source_sha256")}
        )
        if same_export and previous_snorkel.get("ingested_at"):
            snorkel["ingested_at"] = previous_snorkel["ingested_at"]
        entry["snorkel"] = snorkel
        entry["phase"] = "feedback"
        verdict = snorkel.get("difficulty") or "?"
        solv = snorkel.get("solvable")
        entry["next_action"] = _feedback_next_action(verdict, solv, snorkel.get("static_outcome"))
        _backfill_idea_for_task(reg, slug, entry)

        explicit_platform = entry.get("platform_status") or {}
        if explicit_platform.get("source") != "explicit":
            inferred = _infer_platform_status(snorkel)
            entry["platform_status"] = {
                "status": inferred,
                "source": "inferred",
                "at": snorkel.get("ingested_at") or utc_now(),
                "reason": "Derived from platform evaluation; not final reviewer acceptance.",
                "evidence": [path.name],
            }

        rev = int(entry.get("revision") or 0)
        if rev < 1:
            entry["revision"] = 1
            sudhir_dossier.open_revision_workspace(
                REVIEWS_DIR, entry, reason=f"ingest {path.name}"
            )
            rev = 1
        rev_dir = sudhir_dossier.revision_dir(REVIEWS_DIR, slug, rev)
        form_fields = sudhir_dossier.extract_export_form_fields(path)
        snapshot = sudhir_dossier.sanitize_platform_snapshot(
            snorkel,
            text_summary=form_fields.get("text_summary", ""),
            quality_summary=form_fields.get("quality_check_summary", ""),
            test_review=form_fields.get("test_review", ""),
            test_rubrics=form_fields.get("test_rubrics", ""),
        )
        (rev_dir / "PLATFORM.md").write_text(snapshot, encoding="utf-8")
        suggest_src = "\n".join(
            [
                form_fields.get("text_summary", ""),
                form_fields.get("quality_check_summary", ""),
                form_fields.get("test_review", ""),
                form_fields.get("test_rubrics", ""),
            ]
        )
        suggestions = sudhir_dossier.suggest_cm_ids(suggest_src)
        if suggestions:
            sudhir_dossier.update_revision_cm_ids(entry, suggestions)
            lines = ["# CM suggestions from ingest (keyword map)", ""]
            lines.extend(f"- {cm}" for cm in suggestions)
            lines.extend(["", "<!-- auto -->", "Confirm Seen bumps in COMMON_MISTAKES.md.", ""])
            (rev_dir / "CM-SUGGESTIONS.md").write_text("\n".join(lines), encoding="utf-8")
        rubric_path = rev_dir / "RUBRIC.md"
        platform_rubric = form_fields.get("test_rubrics", "").strip()
        if platform_rubric:
            existing = rubric_path.read_text(encoding="utf-8") if rubric_path.exists() else ""
            if not existing.strip() or "(empty" in existing[:240]:
                sudhir_dossier.write_capture_file(
                    rubric_path,
                    f"RUBRIC — {slug} REV-{rev} (from platform export)",
                    platform_rubric,
                )

        if same_export:
            unchanged += 1
            print(f"unchanged {slug}: already ingested {path.name}")
        else:
            touch(entry)
            add_note(entry, f"ingested Snorkel feedback from {path.name}")
            ingested += 1
            print(
                f"ingested {slug}: difficulty={verdict} solvable={solv} "
                f"static={snorkel.get('static_outcome')}"
            )

        if SNORKEL_INBOX in path.parents:
            SNORKEL_ARCHIVE.mkdir(parents=True, exist_ok=True)
            dest = SNORKEL_ARCHIVE / path.name
            shutil.move(str(path), str(dest))

    save_registry(reg)
    write_board(reg)
    print(f"\nIngested {ingested} new/changed export(s); {unchanged} unchanged.")
    if unmatched:
        print(f"Unmatched (no slug): {', '.join(unmatched)}")
    return 0


def _feedback_next_action(difficulty: str, solvable: Any, static: str | None) -> str:
    if static and static != "PASS":
        return "Static checks did not pass on platform; fix and resubmit."
    if solvable is False:
        return "Platform marks some tests unsolved by any agent; loosen/repair tests and resubmit."
    if difficulty and difficulty not in ("HARD",):
        return f"Platform rated difficulty {difficulty}; increase hardness or accept and resubmit."
    return "Evaluation passed; await explicit reviewer/platform acceptance before archiving."


def cmd_sync_snorkel(_args: argparse.Namespace) -> int:
    print(
        "Network sync is not configured. The Snorkel 'Terminus-2nd-Edition' "
        "platform serves feedback behind app auth and S3 (daas-blobs); this "
        "repo has no stored API credentials.\n\n"
        "Supported workflow:\n"
        "  1. In the platform UI, open a submission and export/download its "
        "JSON (the 'submission_<id>.json' blob).\n"
        f"  2. Drop it into {SNORKEL_INBOX.relative_to(REPO_ROOT)}/\n"
        "  3. Run: python3 sudhir_task.py ingest\n\n"
        "If a real API endpoint + token become available, set SNORKEL_API_URL "
        "and SNORKEL_API_TOKEN and extend cmd_sync_snorkel to fetch exports "
        "into the inbox, then call cmd_ingest."
    )
    return 0


def cmd_backfill(args: argparse.Namespace) -> int:
    reg = load_registry()
    added = 0

    # 1. Active task sources.
    if TASKS_DIR.is_dir():
        for source_dir in sorted(p for p in TASKS_DIR.iterdir() if p.is_dir()):
            slug = source_dir.name
            entry = get_entry(reg, slug) or new_entry(slug)
            enrich_from_source(entry, source_dir)
            if entry.get("phase") == "idea":
                entry["phase"] = "construct"
                entry["next_action"] = "Run cheap gates: python3 sudhir_task.py gates " + slug
            if slug not in reg["tasks"]:
                reg["tasks"][slug] = entry
                added += 1

    # 2. Existing Snorkel exports (does not move root-level files).
    for path in sorted(REPO_ROOT.glob("submission_*.json")):
        parsed = parse_submission_export(path)
        if parsed is None or not parsed["slug"]:
            continue
        slug = parsed["slug"]
        entry = get_entry(reg, slug)
        if entry is None:
            entry = new_entry(slug)
            reg["tasks"][slug] = entry
            added += 1
        entry["snorkel"] = parsed["snorkel"]
        entry["platform_status"] = {
            "status": _infer_platform_status(parsed["snorkel"]),
            "source": "inferred",
            "at": parsed["snorkel"].get("ingested_at") or utc_now(),
            "reason": "Derived from platform evaluation; not final reviewer acceptance.",
            "evidence": [path.name],
        }
        if _phase_index(entry.get("phase", "")) < _phase_index("feedback"):
            entry["phase"] = "feedback"
        entry["next_action"] = _feedback_next_action(
            parsed["snorkel"].get("difficulty") or "?",
            parsed["snorkel"].get("solvable"),
            parsed["snorkel"].get("static_outcome"),
        )

    for slug, entry in sorted(reg["tasks"].items()):
        if _backfill_idea_for_task(reg, slug, entry):
            added += 1

    save_registry(reg)
    write_board(reg)
    print(f"Backfill complete. Registry now tracks {len(reg['tasks'])} task(s); added {added} new.")
    return 0


# --------------------------------------------------------------------------- #
# CLI wiring
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    idea = sub.add_parser("idea", help="Manage the documented idea portfolio.")
    idea_sub = idea.add_subparsers(dest="idea_command", required=True)

    sp = idea_sub.add_parser("new", help="Capture an idea without starting task execution.")
    sp.add_argument("slug")
    sp.add_argument("--title")
    sp.add_argument("--summary")
    sp.add_argument("--category")
    sp.add_argument("--languages", help="comma-separated")
    sp.add_argument("--subcategories", help="comma-separated")
    sp.add_argument("--skills", help="comma-separated Associated Skills")
    sp.add_argument("--tags", help="comma-separated Task Tags")
    sp.add_argument("--number-of-milestones", type=int, default=0)
    sp.set_defaults(func=cmd_idea_new)

    sp = idea_sub.add_parser(
        "proposal",
        help="Capture Task Idea Proposal fields and the platform Check feedback verdict.",
    )
    sp.add_argument("slug")
    sp.add_argument("verdict", choices=("pending", "passed", "failed"))
    sp.add_argument("--summary")
    sp.add_argument("--summary-file")
    sp.add_argument("--category")
    sp.add_argument("--skills", help="comma-separated; 5-10 values")
    sp.add_argument("--tags", help="comma-separated; 3-6 values")
    sp.add_argument("--evidence", action="append", help="platform evidence; repeatable")
    sp.add_argument("--feedback")
    sp.add_argument("--feedback-file")
    sp.add_argument("--source-type")
    sp.add_argument("--source-reference")
    sp.add_argument("--reuse-boundary")
    sp.set_defaults(func=cmd_idea_proposal)

    sp = idea_sub.add_parser("status", help="Set the idea decision/lifecycle status.")
    sp.add_argument("slug")
    sp.add_argument("status", choices=MANUAL_IDEA_STATUSES)
    sp.add_argument("--reason")
    sp.add_argument("--next")
    sp.set_defaults(func=cmd_idea_status)

    sp = idea_sub.add_parser(
        "quarantine", help="Retire an unrecognized import outside the active portfolio."
    )
    sp.add_argument("slug")
    sp.add_argument("--reason", required=True)
    sp.add_argument("--evidence", action="append", help="provenance evidence; repeatable")
    sp.set_defaults(func=cmd_idea_quarantine)

    sp = idea_sub.add_parser("uniqueness", help="Record the novelty fingerprint and collision audit.")
    sp.add_argument("slug")
    sp.add_argument("verdict", choices=UNIQUENESS_STATUSES)
    sp.add_argument("--scope", help="comma-separated required search scopes")
    sp.add_argument("--evidence", action="append", help="evidence path or URL; repeatable")
    sp.add_argument("--domain")
    sp.add_argument("--mechanism")
    sp.add_argument("--topology")
    sp.add_argument("--verification")
    sp.add_argument("--closest")
    sp.add_argument("--difference")
    sp.add_argument("--reason")
    sp.set_defaults(func=cmd_idea_uniqueness)

    sp = idea_sub.add_parser("validation", help="Record the Step 2a verdict and evidence.")
    sp.add_argument("slug")
    sp.add_argument("verdict", choices=VALIDATION_STATUSES)
    sp.add_argument("--attempt", type=int)
    sp.add_argument("--evidence", action="append", help="evidence path; repeatable")
    sp.add_argument("--reason")
    sp.set_defaults(func=cmd_idea_validation)

    sp = idea_sub.add_parser("list", help="List ideas and their independent status facets.")
    sp.add_argument("--status", choices=IDEA_STATUSES)
    sp.add_argument("--all", action="store_true", help="include quarantined imports")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_idea_list)

    sp = idea_sub.add_parser("backfill", help="Create honest idea records for existing tasks.")
    sp.set_defaults(func=cmd_idea_backfill)

    sp = idea_sub.add_parser("validate", help="Validate idea/task links and approval evidence.")
    sp.set_defaults(func=cmd_idea_validate)

    sp = sub.add_parser("new", help="Register a task and scaffold its idea record.")
    sp.add_argument("slug")
    sp.add_argument("--title")
    sp.add_argument("--category")
    sp.add_argument("--languages", help="comma-separated, e.g. c,rust,fortran")
    sp.add_argument("--subcategories", help="comma-separated")
    sp.add_argument("--skills", help="comma-separated Associated Skills")
    sp.add_argument("--tags", help="comma-separated Task Tags")
    sp.add_argument("--number-of-milestones", type=int)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_new)

    sp = sub.add_parser("status", help="Print the registry as JSON.")
    sp.add_argument("slug", nargs="?")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("board", help="Re-render the Markdown status board.")
    sp.set_defaults(func=cmd_board)

    sp = sub.add_parser("phase", help="Set a task's lifecycle phase.")
    sp.add_argument("slug")
    sp.add_argument("phase", choices=PHASES)
    sp.add_argument("--next", help="next action text")
    sp.set_defaults(func=cmd_phase)

    sp = sub.add_parser("revise", help="Open a revision and invalidate downstream evidence.")
    sp.add_argument("slug")
    sp.add_argument("--reason")
    sp.set_defaults(func=cmd_revise)

    sp = sub.add_parser("gates", help="Run static + dockerfile + collapse + integrity gates.")
    sp.add_argument("slug")
    sp.set_defaults(func=cmd_gates)

    sp = sub.add_parser("package", help="Build the submission zip, validate, and approve.")
    sp.add_argument("slug")
    sp.add_argument("--skip-approve", action="store_true")
    sp.add_argument(
        "--force",
        action="store_true",
        help="skip PREUPLOAD checklist gate (emergency only)",
    )
    sp.set_defaults(func=cmd_package)

    sp = sub.add_parser("evidence", help="Record Harbor oracle/NOP/10x job evidence.")
    sp.add_argument("slug")
    sp.add_argument("--oracle-1x", dest="oracle_1x", help="Harbor job id for oracle 1x")
    sp.add_argument("--nop", help="Harbor job id for NOP")
    sp.add_argument("--oracle-10x", dest="oracle_10x", help="Harbor job id for oracle 10x")
    sp.set_defaults(func=cmd_evidence)

    sp = sub.add_parser("feedback-capture", help="Store reviewer feedback in the REV dossier.")
    sp.add_argument("slug")
    sp.add_argument("--text-file", help="path to feedback text")
    sp.add_argument("--stdin", action="store_true", help="read feedback from stdin")
    sp.set_defaults(func=cmd_feedback_capture)

    sp = sub.add_parser(
        "form-capture",
        help="Store difficulty/solution/verification/rubric paste fields in the REV dossier.",
    )
    sp.add_argument("slug")
    sp.add_argument("--difficulty-file", help="DIFFICULTY explanation paste")
    sp.add_argument("--solution-file", help="SOLUTION explanation paste")
    sp.add_argument("--verification-file", help="VERIFICATION explanation paste")
    sp.add_argument("--rubric-file", help="RUBRIC paste")
    sp.set_defaults(func=cmd_form_capture)

    sp = sub.add_parser("rubric-capture", help="Store UI rubric paste in the REV dossier.")
    sp.add_argument("slug")
    sp.add_argument("--text-file", required=True, help="path to rubric text")
    sp.set_defaults(func=cmd_rubric_capture)

    sp = sub.add_parser("learn-check", help="Print CM preventions and check PREUPLOAD.")
    sp.add_argument("slug")
    sp.set_defaults(func=cmd_learn_check)

    sp = sub.add_parser("ingest", help="Parse Snorkel submission_*.json exports.")
    sp.add_argument("paths", nargs="*", help="explicit export paths (default: auto-discover)")
    sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser("outcome", help="Record explicit platform/reviewer status.")
    sp.add_argument("slug")
    sp.add_argument("status", choices=PLATFORM_STATUSES)
    sp.add_argument("--reason")
    sp.add_argument("--evidence", action="append", help="evidence path or platform URL; repeatable")
    sp.add_argument("--next", help="next action text")
    sp.set_defaults(func=cmd_outcome)

    sp = sub.add_parser("eligibility", help="Evaluate current official/house eligibility.")
    sp.add_argument("slug")
    sp.add_argument(
        "--action",
        choices=(
            "view",
            "idea-uniqueness",
            "step2a-go",
            "task-registration",
            "package",
            "submit",
            "update-submission",
        ),
        default="view",
    )
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_eligibility)

    sp = sub.add_parser(
        "exemption-capture",
        help="Capture source-backed in-flight eligibility evidence.",
    )
    sp.add_argument("slug")
    sp.add_argument("--rule-id", required=True)
    sp.add_argument("--exemption-id")
    sp.add_argument("--effective-date")
    sp.add_argument(
        "--platform-state",
        required=True,
        choices=sorted(eligibility_policy.IN_FLIGHT_PLATFORM_STATES),
    )
    sp.add_argument("--source", required=True)
    sp.add_argument("--evidence", action="append", required=True)
    sp.add_argument("--reason", required=True)
    sp.add_argument("--first-submitted-at")
    sp.set_defaults(func=cmd_exemption_capture)

    sp = sub.add_parser("sync-snorkel", help="Explain/attempt the optional network pull.")
    sp.set_defaults(func=cmd_sync_snorkel)

    sp = sub.add_parser("backfill", help="Seed registry from active tasks + existing exports.")
    sp.set_defaults(func=cmd_backfill)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    with registry_lock():
        return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
