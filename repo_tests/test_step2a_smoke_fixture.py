from __future__ import annotations

import json
from pathlib import Path

import validate_loop

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "step2a" / "valid-evidence.json"


def test_step2a_smoke_fixture_matches_current_schema() -> None:
    evidence = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = validate_loop.validate_evidence(evidence)
    assert result["errors"] == []
    assert result["hard_fail_reasons"] == []
