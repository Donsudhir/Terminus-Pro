"""Current Terminus EC eligibility and evidence-backed exemption policy.

Policy snapshots are reviewed facts rather than automatically promoted prose.
Official category/milestone blocks and repository house rules are evaluated
separately so local policy never claims upstream authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

CURRENT_POLICY_SNAPSHOT_ID = "terminus-ec-2026-07-21"
PRE_ADR_POLICY_SNAPSHOT_ID = "pre-ADR-0016"
POLICY_SOURCE_URLS = (
    "https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/category-status.md",
    "https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/reference/changelog.md",
    "https://snorkel-ai.github.io/Terminus-EC-Training-stateful/docs/understanding-tasks/task-subtypes.md",
)

CATEGORY_BLOCKS: dict[str, str] = {
    "debugging": "2026-06-18",
    "software-engineering": "2026-06-18",
    "data-processing": "2026-07-10",
}
MILESTONE_BLOCK_EFFECTIVE_DATE = "2026-06-29"
UI_BUILDING_HOUSE_BLOCK_EFFECTIVE_DATE = "2026-07-21"

IN_FLIGHT_PLATFORM_STATES = frozenset(
    {
        "NEEDS_REVISION",
        "REVISION_REQUESTED",
        "REVIEW_PENDING",
        "IN_REVIEW",
        "UNDER_REVIEW",
    }
)
SHIPPING_ACTIONS = frozenset({"package", "submit", "update-submission"})


@dataclass(frozen=True)
class EligibilityResult:
    official_status: str
    house_status: str
    blocking: bool
    official_blocking: bool
    house_blocking: bool
    official_reasons: tuple[str, ...]
    official_rule_ids: tuple[str, ...]
    official_exemption_ids: tuple[str, ...]
    house_reasons: tuple[str, ...]
    house_rule_ids: tuple[str, ...]
    house_exemption_ids: tuple[str, ...]

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys((*self.official_reasons, *self.house_reasons)))

    @property
    def rule_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys((*self.official_rule_ids, *self.house_rule_ids)))

    @property
    def exemption_ids(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys((*self.official_exemption_ids, *self.house_exemption_ids))
        )

    def to_dict(self, *, action: str, evaluated_at: str) -> dict[str, Any]:
        return {
            "policy_snapshot_id": CURRENT_POLICY_SNAPSHOT_ID,
            "action": action,
            "evaluated_at": evaluated_at,
            "official": {
                "status": self.official_status,
                "blocking": self.official_blocking,
                "reasons": list(self.official_reasons),
                "rule_ids": list(self.official_rule_ids),
                "exemption_ids": list(self.official_exemption_ids),
            },
            "house": {
                "status": self.house_status,
                "blocking": self.house_blocking,
                "reasons": list(self.house_reasons),
                "rule_ids": list(self.house_rule_ids),
                "exemption_ids": list(self.house_exemption_ids),
            },
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def category_rule_id(category: str) -> str:
    return f"official.category.{category}.blocked"


def milestone_rule_id() -> str:
    return "official.structure.milestone-net-new.blocked"


def ui_building_rule_id() -> str:
    return "house.subcategory.ui-building.net-new.blocked"


def applicable_rules(record: dict[str, Any]) -> list[tuple[str, str]]:
    """Return the union of official and house rules for exemption lookup."""
    return list(
        dict.fromkeys((*official_applicable_rules(record), *house_applicable_rules(record)))
    )


def official_applicable_rules(record: dict[str, Any]) -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    category = str(record.get("category") or "").strip().lower()
    if category in CATEGORY_BLOCKS:
        rules.append((category_rule_id(category), CATEGORY_BLOCKS[category]))
    milestone_count = record.get("number_of_milestones", 0)
    if isinstance(milestone_count, int) and milestone_count > 0:
        rules.append((milestone_rule_id(), MILESTONE_BLOCK_EFFECTIVE_DATE))
    return rules


def house_applicable_rules(record: dict[str, Any]) -> list[tuple[str, str]]:
    rules = official_applicable_rules(record)
    subcategories = record.get("subcategories")
    if isinstance(subcategories, list) and any(
        isinstance(value, str) and value.strip().lower() == "ui_building"
        for value in subcategories
    ):
        rules.append((ui_building_rule_id(), UI_BUILDING_HOUSE_BLOCK_EFFECTIVE_DATE))
    return rules


def new_record_policy_fields() -> dict[str, Any]:
    return {
        "policy_snapshot_id": CURRENT_POLICY_SNAPSHOT_ID,
        "first_submitted_at": None,
        "first_submitted_evidence": [],
        "in_flight_exemptions": [],
        "eligibility_verdict": {
            "policy_snapshot_id": CURRENT_POLICY_SNAPSHOT_ID,
            "action": "not-evaluated",
            "evaluated_at": None,
            "official": {
                "status": "not-evaluated",
                "blocking": False,
                "reasons": [],
                "rule_ids": [],
                "exemption_ids": [],
            },
            "house": {
                "status": "not-evaluated",
                "blocking": False,
                "reasons": [],
                "rule_ids": [],
                "exemption_ids": [],
            },
        },
        "number_of_milestones": 0,
        "subcategories": [],
    }


def ensure_record_policy_fields(record: dict[str, Any]) -> bool:
    """Add backward-compatible defaults and report whether anything changed."""
    changed = False
    defaults = {
        "policy_snapshot_id": PRE_ADR_POLICY_SNAPSHOT_ID,
        "first_submitted_at": None,
        "first_submitted_evidence": [],
        "in_flight_exemptions": [],
        "number_of_milestones": 0,
        "subcategories": [],
    }
    for key, value in defaults.items():
        if key not in record:
            record[key] = value.copy() if isinstance(value, list) else value
            changed = True
    if "eligibility_verdict" not in record:
        record["eligibility_verdict"] = {
            "policy_snapshot_id": PRE_ADR_POLICY_SNAPSHOT_ID,
            "action": "migration-default",
            "evaluated_at": None,
            "official": {
                "status": "grandfathered-pending-review",
                "blocking": False,
                "reasons": ["Record predates ADR-0016 eligibility fields."],
                "rule_ids": [],
                "exemption_ids": [],
            },
            "house": {
                "status": "grandfathered-pending-review",
                "blocking": False,
                "reasons": ["Record predates ADR-0016 eligibility fields."],
                "rule_ids": [],
                "exemption_ids": [],
            },
        }
        changed = True
    return changed


def exemption_errors(exemption: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_text = ("id", "rule_id", "effective_date", "recorded_at", "source", "reason")
    for key in required_text:
        if not isinstance(exemption.get(key), str) or not str(exemption[key]).strip():
            errors.append(f"exemption {key} is missing")
    evidence = exemption.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(
        isinstance(item, str) and item.strip() for item in evidence
    ):
        errors.append("exemption evidence must be a non-empty list of references")
    state = str(exemption.get("platform_state") or "").upper()
    if state not in IN_FLIGHT_PLATFORM_STATES:
        errors.append(
            "exemption platform_state must prove active review/revision: "
            + ", ".join(sorted(IN_FLIGHT_PLATFORM_STATES))
        )
    if exemption.get("status", "active") != "active":
        errors.append("exemption status is not active")
    return errors


def _valid_exemption(record: dict[str, Any], rule_id: str) -> dict[str, Any] | None:
    exemptions = record.get("in_flight_exemptions")
    if not isinstance(exemptions, list):
        return None
    for exemption in exemptions:
        if not isinstance(exemption, dict) or exemption.get("rule_id") != rule_id:
            continue
        if not exemption_errors(exemption):
            return exemption
    return None


@dataclass(frozen=True)
class _ProfileResult:
    status: str
    blocking: bool
    reasons: tuple[str, ...]
    rule_ids: tuple[str, ...]
    exemption_ids: tuple[str, ...]


def _evaluate_profile(
    record: dict[str, Any],
    *,
    action: str,
    rules: list[tuple[str, str]],
) -> _ProfileResult:
    if not rules:
        return _ProfileResult("eligible", False, (), (), ())

    missing: list[tuple[str, str]] = []
    exemption_ids: list[str] = []
    for rule_id, effective_date in rules:
        exemption = _valid_exemption(record, rule_id)
        if exemption is None:
            missing.append((rule_id, effective_date))
        else:
            exemption_ids.append(str(exemption["id"]))

    rule_ids = tuple(rule_id for rule_id, _ in rules)
    if not missing:
        reasons = tuple(
            f"In-flight exemption {exemption_id} is evidence-backed."
            for exemption_id in exemption_ids
        )
        return _ProfileResult(
            "exempt-in-flight",
            False,
            reasons,
            rule_ids,
            tuple(exemption_ids),
        )

    snapshot = str(record.get("policy_snapshot_id") or PRE_ADR_POLICY_SNAPSHOT_ID)
    missing_reasons = tuple(
        f"{rule_id} effective {effective_date} has no valid in-flight exemption."
        for rule_id, effective_date in missing
    )
    if snapshot == PRE_ADR_POLICY_SNAPSHOT_ID and action not in SHIPPING_ACTIONS:
        return _ProfileResult(
            "grandfathered-pending-review",
            False,
            missing_reasons,
            rule_ids,
            tuple(exemption_ids),
        )
    if snapshot == PRE_ADR_POLICY_SNAPSHOT_ID:
        return _ProfileResult(
            "grandfathered-pending-review",
            True,
            missing_reasons,
            rule_ids,
            tuple(exemption_ids),
        )
    return _ProfileResult(
        "blocked",
        True,
        missing_reasons,
        rule_ids,
        tuple(exemption_ids),
    )


def evaluate(record: dict[str, Any], *, action: str) -> EligibilityResult:
    official = _evaluate_profile(
        record,
        action=action,
        rules=official_applicable_rules(record),
    )
    house = _evaluate_profile(
        record,
        action=action,
        rules=house_applicable_rules(record),
    )
    return EligibilityResult(
        official.status,
        house.status,
        official.blocking or house.blocking,
        official.blocking,
        house.blocking,
        official.reasons,
        official.rule_ids,
        official.exemption_ids,
        house.reasons,
        house.rule_ids,
        house.exemption_ids,
    )


def policy_field_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(record.get("policy_snapshot_id"), str):
        errors.append("policy_snapshot_id is missing")
    if not isinstance(record.get("first_submitted_evidence"), list):
        errors.append("first_submitted_evidence must be a list")
    exemptions = record.get("in_flight_exemptions")
    if not isinstance(exemptions, list):
        errors.append("in_flight_exemptions must be a list")
    else:
        for index, exemption in enumerate(exemptions):
            if not isinstance(exemption, dict):
                errors.append(f"in_flight_exemptions[{index}] must be an object")
                continue
            errors.extend(
                f"in_flight_exemptions[{index}]: {error}"
                for error in exemption_errors(exemption)
            )
    if not isinstance(record.get("eligibility_verdict"), dict):
        errors.append("eligibility_verdict must be an object")
    milestone_count = record.get("number_of_milestones")
    if not isinstance(milestone_count, int) or milestone_count < 0:
        errors.append("number_of_milestones must be a non-negative integer")
    subcategories = record.get("subcategories")
    if subcategories is not None and (
        not isinstance(subcategories, list)
        or not all(isinstance(value, str) and value.strip() for value in subcategories)
    ):
        errors.append("subcategories must be a list of non-empty strings")
    return errors
