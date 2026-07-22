"""Reviewed official CI policy facts and local coverage dispositions."""

from __future__ import annotations

from typing import Final

POLICY_ID: Final = "terminus-ec-ci-2026-07-21"
SOURCE_URL: Final = (
    "https://snorkel-ai.github.io/Terminus-EC-Training-stateful/"
    "docs/creating-tasks/ci-checks.md"
)

BUILD_CONTEXT_MAX_BYTES: Final = 100 * 1024 * 1024
BUILD_CONTEXT_FILE_MAX_BYTES: Final = 50 * 1024 * 1024

SANCTIONED_FINAL_IMAGES: Final = frozenset(
    {
        "public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb",
        "public.ecr.aws/docker/library/node:22-bookworm-slim@sha256:f3a68cf41a855d227d1b0ab832bed9749469ef38cf4f58182fb8c893bc462383",
        "public.ecr.aws/docker/library/golang:1.24-bookworm@sha256:1a6d4452c65dea36aac2e2d606b01b4a029ec90cc1ae53890540ce6173ea77ac",
        "public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe9e7d8e37ceb96ed907265a3a0df7f44e3737d0b100e7907a679acb36",
        "public.ecr.aws/docker/library/eclipse-temurin:21-jdk-jammy@sha256:25d1276565738d3c805e632a4542c3a7598866ef967f4def6544c15de3a74b14",
        "public.ecr.aws/docker/library/gcc:13-bookworm@sha256:930f2ebe239275fa67226654cb79273ea34eee672ae61c8a39f689c37fb7ac5c",
        "public.ecr.aws/docker/library/ruby:3.3-slim-bookworm@sha256:e76733e94b3a5893e4a141024ef3a583dc10781dc24becebf74f9c9f9a33e3df",
        "public.ecr.aws/docker/library/maven:3.9.9-eclipse-temurin-21@sha256:3a4ab3276a087bf276f79cae96b1af04f53731bec53fb2e651aca79e4b10211e",
        "public.ecr.aws/docker/library/debian:bookworm-slim@sha256:4724b8cc51e33e398f0e2e15e18d5ec2851ff0c2280647e1310bc1642182655d",
        "public.ecr.aws/docker/library/ubuntu:24.04@sha256:0d39fcc8335d6d74d5502f6df2d30119ff4790ebbb60b364818d5112d9e3e932",
        "scratch",
    }
)

# Custom final images may be added only by a reviewed ADR-backed framework
# change. Task-authored files cannot self-exempt a base image.
SANCTIONED_BASE_EXEMPTIONS: Final[dict[str, str]] = {}

UNSAFE_CAPABILITIES: Final = frozenset(
    {
        "SYS_ADMIN",
        "NET_ADMIN",
        "SYS_MODULE",
        "SYS_PTRACE",
        "DAC_READ_SEARCH",
        "DAC_OVERRIDE",
        "MKNOD",
    }
)

OFFICIAL_CHECK_COVERAGE: Final = (
    ("check_pinned_images", "locally-enforced", "dockerfile_check.check_pin_base_digest"),
    ("check_sanctioned_base_images", "locally-enforced", "dockerfile_check.check_sanctioned_base_image"),
    ("check_build_context_size", "locally-enforced", "dockerfile_check.check_build_context_size"),
    ("pinned_dependencies", "locally-enforced", "dockerfile_check.check_dependency_pinning"),
    ("tests_or_solution_in_image", "locally-enforced", "dockerfile_check.check_silo_and_reserved"),
    ("check_dockerfile_references", "locally-enforced", "run_static_checks.check_dockerfile_copy_sources"),
    ("check_test_sh", "locally-enforced", "run_static_checks.check_test_sh"),
    ("check_task_absolute_path", "locally-enforced", "run_static_checks.check_absolute_paths"),
    ("check_privileged_containers", "locally-enforced", "dockerfile_check.check_compose_safety"),
    ("validate_task_fields", "locally-enforced", "run_static_checks.check_task_toml"),
    ("ruff", "locally-enforced", "run_static_checks.check_python_verifier_layout"),
    ("typos", "delegated-upstream", "required pre-submission quality check; semantic spellcheck"),
    ("check_task_sizes", "delegated-upstream", "platform limit not numerically published"),
    ("check_dockerignore", "locally-enforced", "dockerfile_check.check_dockerignore_and_copy"),
    ("check_dockerfile_hygiene", "locally-enforced", "run_static_checks.check_package_hygiene"),
    ("check_offline_tests", "locally-enforced", "run_static_checks.check_test_sh"),
    ("check_apt_usage", "locally-enforced", "dockerfile_check.check_apt_hygiene"),
    ("check_reproducible_builds", "locally-enforced", "dockerfile_check.check_reproducible_builds"),
    ("check_layer_volatility", "locally-enforced", "dockerfile_check.check_layer_volatility"),
    ("check_no_build_tools_in_runtime", "locally-enforced", "dockerfile_check.check_no_build_tools_in_runtime"),
    ("check_file_extraction", "locally-enforced", "dockerfile_check.check_file_extraction"),
    ("check_heredoc_usage", "locally-enforced", "dockerfile_check.check_source_as_files"),
    ("check_recursive_permissions", "locally-enforced", "dockerfile_check.check_copy_metadata"),
)

ALLOWED_DISPOSITIONS: Final = frozenset(
    {
        "locally-enforced",
        "delegated-upstream",
        "mandatory-human-review",
        "house-override",
        "not-applicable",
    }
)
