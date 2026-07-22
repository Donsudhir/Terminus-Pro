"""Official CI coverage matrix and policy fact regressions."""

from __future__ import annotations

from pathlib import Path

import ci_policy

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CHECKS = {
    "check_pinned_images",
    "check_sanctioned_base_images",
    "check_build_context_size",
    "pinned_dependencies",
    "tests_or_solution_in_image",
    "check_dockerfile_references",
    "check_test_sh",
    "check_task_absolute_path",
    "check_privileged_containers",
    "validate_task_fields",
    "ruff",
    "typos",
    "check_task_sizes",
    "check_dockerignore",
    "check_dockerfile_hygiene",
    "check_offline_tests",
    "check_apt_usage",
    "check_reproducible_builds",
    "check_layer_volatility",
    "check_no_build_tools_in_runtime",
    "check_file_extraction",
    "check_heredoc_usage",
    "check_recursive_permissions",
}


def test_every_official_check_has_one_valid_coverage_disposition() -> None:
    rows = ci_policy.OFFICIAL_CHECK_COVERAGE
    ids = [row[0] for row in rows]
    assert set(ids) == EXPECTED_CHECKS
    assert len(ids) == len(set(ids))
    assert all(row[1] in ci_policy.ALLOWED_DISPOSITIONS for row in rows)
    assert all(row[2].strip() for row in rows)


def test_reviewed_build_context_and_sanctioned_image_facts() -> None:
    assert ci_policy.BUILD_CONTEXT_MAX_BYTES == 100 * 1024 * 1024
    assert ci_policy.BUILD_CONTEXT_FILE_MAX_BYTES == 50 * 1024 * 1024
    assert len(ci_policy.SANCTIONED_FINAL_IMAGES) == 11
    assert "scratch" in ci_policy.SANCTIONED_FINAL_IMAGES
    assert all(
        image == "scratch" or "@sha256:" in image
        for image in ci_policy.SANCTIONED_FINAL_IMAGES
    )


def test_human_coverage_document_names_every_check() -> None:
    document = (
        REPO_ROOT / "sudhir_research" / "OFFICIAL-CI-COVERAGE-2026-07-21.md"
    ).read_text(encoding="utf-8")
    for check_id in EXPECTED_CHECKS:
        assert f"`{check_id}`" in document
    assert "delegated-upstream" in document
    assert "New blocking deltas: zero" in document
