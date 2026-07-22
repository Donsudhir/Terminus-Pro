"""Task Idea Proposal form contract and validation helpers."""

from __future__ import annotations

import re
from typing import Any

PROPOSAL_STATUSES = ("pending", "passed", "failed", "not-recorded")

CATEGORY_LABEL_TO_SLUG: dict[str, str] = {
    "System / Environment Setup & Configuration": "system-administration",
    "Build / Compilation / Dependency Management": "build-and-dependency-management",
    "Data / File Processing / ETL / Scripting": "data-processing",
    "Machine Learning / Model Training / Inference": "machine-learning",
    "Security / Cryptography / Vulnerability Demonstration": "security",
    "Scientific Computing": "scientific-computing",
    "Interactive / Simulation Tasks / Games": "games",
}
CATEGORY_SLUG_TO_LABEL = {slug: label for label, slug in CATEGORY_LABEL_TO_SLUG.items()}


def normalize_category(value: str | None) -> tuple[str, str] | None:
    cleaned = str(value or "").strip()
    if cleaned in CATEGORY_LABEL_TO_SLUG:
        return cleaned, CATEGORY_LABEL_TO_SLUG[cleaned]
    lowered = cleaned.lower()
    for slug, label in CATEGORY_SLUG_TO_LABEL.items():
        if lowered == slug:
            return label, slug
    return None


def sentence_count(summary: str) -> int:
    chunks = re.split(r"(?<=[.!?])(?:\s+|$)", summary.strip())
    return len([chunk for chunk in chunks if chunk.strip()])


def field_errors(
    *,
    summary: str,
    category: str,
    skills: list[str],
    tags: list[str],
) -> list[str]:
    errors: list[str] = []
    count = sentence_count(summary)
    if not 2 <= count <= 5:
        errors.append(f"Task Idea Summary must contain 2-5 sentences, found {count}")
    if normalize_category(category) is None:
        errors.append("Idea Category must be one exact platform label or normalized local slug")
    if not 5 <= len(skills) <= 10:
        errors.append(f"Associated Skills must contain 5-10 values, found {len(skills)}")
    if not 3 <= len(tags) <= 6:
        errors.append(f"Task Tags must contain 3-6 values, found {len(tags)}")
    for label, values in (("Associated Skills", skills), ("Task Tags", tags)):
        if any(not isinstance(value, str) or not value.strip() for value in values):
            errors.append(f"{label} must contain only non-empty strings")
        normalized = [value.strip().lower() for value in values if isinstance(value, str)]
        if len(normalized) != len(set(normalized)):
            errors.append(f"{label} must not contain duplicates")
    return errors


def new_proposal_check(
    *,
    summary: str = "",
    category: str | None = None,
    skills: list[str] | None = None,
    tags: list[str] | None = None,
    status: str = "pending",
) -> dict[str, Any]:
    normalized = normalize_category(category)
    return {
        "status": status,
        "summary": summary,
        "category_label": normalized[0] if normalized else str(category or ""),
        "category_slug": normalized[1] if normalized else "",
        "associated_skills": list(skills or []),
        "task_tags": list(tags or []),
        "checked_at": None,
        "evidence": [],
        "feedback": "",
        "inspiration": {
            "source_type": "",
            "source_reference": "",
            "reuse_boundary": "",
        },
    }


def render_proposal(slug: str, proposal: dict[str, Any], *, generated_at: str) -> str:
    evidence = proposal.get("evidence") or []
    evidence_text = ", ".join(str(item) for item in evidence) or "PENDING"
    feedback = str(proposal.get("feedback") or "PENDING")
    inspiration = proposal.get("inspiration") or {}
    skills = ", ".join(str(item) for item in proposal.get("associated_skills") or [])
    tags = ", ".join(str(item) for item in proposal.get("task_tags") or [])
    return "\n".join(
        [
            f"# Task Idea Proposal — {slug}",
            "",
            f"Generated: {generated_at}",
            f"Platform check: {str(proposal.get('status') or 'pending').upper()}",
            f"Evidence: {evidence_text}",
            "",
            "## Paste-ready fields",
            "",
            "### Task Idea Summary",
            "",
            str(proposal.get("summary") or ""),
            "",
            "### Idea Category",
            "",
            str(proposal.get("category_label") or ""),
            "",
            f"Normalized local category: `{proposal.get('category_slug') or ''}`",
            "",
            "### Associated Skills",
            "",
            skills,
            "",
            "### Task Tags",
            "",
            tags,
            "",
            "## Check feedback",
            "",
            feedback,
            "",
            "## Inspiration provenance",
            "",
            f"- Source type: {inspiration.get('source_type') or 'PENDING'}",
            f"- Source reference: {inspiration.get('source_reference') or 'PENDING'}",
            f"- Reuse boundary: {inspiration.get('reuse_boundary') or 'PENDING'}",
            "",
        ]
    )
