"""Versioned frontier-model identifiers used by local TERMINUS tooling.

This module intentionally separates current run targets from historical parser
support. Updating the current pair must not make old job artifacts unreadable,
and an unknown future model identifier must remain visible rather than being
silently discarded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

CURRENT_MODEL_EFFECTIVE_DATE = "2026-06-12"
UNKNOWN_MODEL_PREFIX = "unknown:"


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    label: str
    provider: str
    harbor_flag: str
    quality_check_flag: str
    sdk_name: str | None
    match_pattern: str
    effective_date: str
    current: bool


CURRENT_MODELS: tuple[ModelSpec, ...] = (
    ModelSpec(
        model_id="gpt-5.5",
        label="GPT-5.5",
        provider="openai",
        harbor_flag="@openai/gpt-5.5",
        quality_check_flag="openai/@openai/gpt-5.5",
        sdk_name=None,
        match_pattern=r"gpt-5\.5",
        effective_date=CURRENT_MODEL_EFFECTIVE_DATE,
        current=True,
    ),
    ModelSpec(
        model_id="claude-opus-4.8",
        label="Claude Opus 4.8",
        provider="anthropic",
        harbor_flag="@anthropic/claude-opus-4-8",
        quality_check_flag="anthropic/@anthropic/claude-opus-4-8",
        sdk_name="claude-opus-4-8",
        match_pattern=r"claude-opus-4(?:[.-])8",
        effective_date=CURRENT_MODEL_EFFECTIVE_DATE,
        current=True,
    ),
)

LEGACY_MODELS: tuple[ModelSpec, ...] = (
    ModelSpec(
        model_id="gpt-5.2",
        label="GPT-5.2 (legacy)",
        provider="openai",
        harbor_flag="@openai/gpt-5.2",
        quality_check_flag="openai/@openai/gpt-5.2",
        sdk_name=None,
        match_pattern=r"gpt-5\.2",
        effective_date="2026-01-01",
        current=False,
    ),
    ModelSpec(
        model_id="claude-opus-4.6",
        label="Claude Opus 4.6 (legacy)",
        provider="anthropic",
        harbor_flag="@anthropic/claude-opus-4-6",
        quality_check_flag="anthropic/@anthropic/claude-opus-4-6",
        sdk_name="claude-opus-4-6",
        match_pattern=r"claude-opus-4(?:[.-])6",
        effective_date="2026-01-01",
        current=False,
    ),
)

ALL_MODELS: tuple[ModelSpec, ...] = CURRENT_MODELS + LEGACY_MODELS
MODEL_BY_ID: dict[str, ModelSpec] = {spec.model_id: spec for spec in ALL_MODELS}
CURRENT_MODEL_IDS: tuple[str, ...] = tuple(spec.model_id for spec in CURRENT_MODELS)

CURRENT_OPENAI_MODEL = next(spec for spec in CURRENT_MODELS if spec.provider == "openai")
CURRENT_ANTHROPIC_MODEL = next(
    spec for spec in CURRENT_MODELS if spec.provider == "anthropic"
)
QUALITY_CHECK_MODEL = CURRENT_OPENAI_MODEL.quality_check_flag
RUBRIC_REVIEW_MODEL = CURRENT_ANTHROPIC_MODEL.sdk_name or CURRENT_ANTHROPIC_MODEL.model_id

_MODELISH_PATTERN = re.compile(
    r"(?:@[A-Za-z0-9_.-]+/|\b(?:openai|anthropic|google|gpt|claude|gemini)[/:_-])",
    re.IGNORECASE,
)


def current_agent_model_map() -> dict[str, dict[str, str]]:
    """Return the current-only shape consumed by ``agent_test.run``."""
    return {
        spec.model_id: {
            "label": spec.label,
            "harbor_flag": spec.harbor_flag,
            "match": spec.match_pattern,
        }
        for spec in CURRENT_MODELS
    }


def identify_model(raw: str, *, preserve_unknown: bool = True) -> str | None:
    """Identify current/legacy models and retain model-shaped unknown values."""
    value = str(raw or "").strip()
    if not value:
        return None
    for spec in ALL_MODELS:
        if re.search(spec.match_pattern, value, re.IGNORECASE):
            return spec.model_id
    if preserve_unknown and _MODELISH_PATTERN.search(value):
        normalized = " ".join(value.split())[:180]
        return UNKNOWN_MODEL_PREFIX + normalized
    return None


def label_for(model_id: str | None) -> str:
    if not model_id:
        return "Unknown model"
    spec = MODEL_BY_ID.get(model_id)
    if spec is not None:
        return spec.label
    if model_id.startswith(UNKNOWN_MODEL_PREFIX):
        return f"Unknown model ({model_id[len(UNKNOWN_MODEL_PREFIX):]})"
    return model_id


def is_current(model_id: str | None) -> bool:
    return bool(model_id in CURRENT_MODEL_IDS)


def reporting_sort_key(model_id: str) -> tuple[int, int | str]:
    if model_id in CURRENT_MODEL_IDS:
        return (0, CURRENT_MODEL_IDS.index(model_id))
    legacy_ids = tuple(spec.model_id for spec in LEGACY_MODELS)
    if model_id in legacy_ids:
        return (1, legacy_ids.index(model_id))
    return (2, model_id)


def current_pair_label() -> str:
    return " + ".join(spec.label for spec in CURRENT_MODELS)
