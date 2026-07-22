"""Recoverable regression cases for the current harness baseline.

The original full task fixtures referenced by ``repo_tests.cases`` were never
tracked and cannot be recovered from Git or submission archives.  This module
pins current behavior against an immutable snapshot of a complete local task.
Focused synthetic tests continue to cover individual failure modes.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_TASKS_DIR = REPO_ROOT / "repo_tests" / "fixtures" / "tasks"
CLEAN_FIXTURE_NAME = "harness-clean"

COMMON_STATIC_PASS_MESSAGES = (
    "required task files present",
    "no legacy canary strings found",
    "task.toml Edition 2 gate passed",
    "task structure aligns with Edition 2 expectations",
    "tests/test.sh reward.txt block matches Edition 2 expectation",
    "tests/test.sh pre-pytest block preserves the standard non-UI semantics",
    "tests/test.sh CM-007 pytest cwd-shadow hardening present",
    "Dockerfile Edition 2 gate passed",
    "docker-compose checks skipped (no environment/docker-compose.yaml)",
    "instruction.md uses absolute in-container path references",
    "output contract matches the declared user-visible outputs and schema checks",
    "environment/ contains no hidden-instruction patterns",
)

STATIC_CHECK_EXPECTATIONS = {
    CLEAN_FIXTURE_NAME: {"warnings": []},
}

COLLAPSE_CHECK_EXPECTATIONS = {
    CLEAN_FIXTURE_NAME: {
        "exit_code": 2,
        "fails": 0,
        "warns": 2,
        "oracle_targets": [
            "mod_a/op_knit.c",
            "mod_b/step_lane.c",
            "mod_c/seal_phase.c",
        ],
        "dominant_root": "mod_a",
        "severities": {
            "rc1_oracle_simplification": "WARN",
            "rc2_oracle_predictability": "PASS",
            "rc3_verifier_shallowness": "PASS",
            "rc4_tamper_surface": "PASS",
            "rc5_reference_artifacts": "PASS",
            "rc6_instruction_specificity": "PASS",
            "rc7_oracle_triviality": "PASS",
            "rc8_frontier_concentration": "PASS",
            "cr1_symbol_table_compliance": "WARN",
            "cr2_flipping_point_contract": "PASS",
            "cr7_grep_resistance": "PASS",
            "cr8_no_central_orchestration": "PASS",
            "cr9_test_contract_traceability": "PASS",
            "gx1_oracle_comment_leakage": "PASS",
            "gx2_oracle_real_diff": "PASS",
            "gx3_oracle_edit_distance": "PASS",
            "gx4_no_op_rewrite": "PASS",
            "gx5_instruction_test_overlap": "PASS",
            "gx6_causal_connective_density": "PASS",
            "gx7_test_literals_homed": "PASS",
            "gx8_test_import_consistency": "PASS",
            "gx9_instruction_contract_saturation": "PASS",
            "gx10_instruction_polarity_contradiction": "PASS",
        },
        "issue_counts": {
            "rc4_tamper_surface": 0,
            "rc5_reference_artifacts": 0,
        },
        "net_deltas": {"rc1_oracle_simplification": 69},
        "predict_ratios": {"rc2_oracle_predictability": 0.0},
        "issue_paths": {},
        "rc6_classification": {
            "level": "symptoms-only",
            "trigger_count": 0,
            "strong_count": 0,
        },
        "rc7_band": {
            "band": "substantive",
            "oracle_loc": 170,
        },
    },
}
