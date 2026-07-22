from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import dockerfile_check

REPO_ROOT = Path(__file__).resolve().parents[1]
CLASSIFIER_TASK = REPO_ROOT / "tasks" / "classifier-robustness-gate"
RANK_SPIKE_TASK = REPO_ROOT / "tasks" / "rank-spike-remediation"
TENSOR_RETENTION_TASK = REPO_ROOT / "tasks" / "tensor-retention-gate"
TRANSFORMER_LATENCY_TASK = REPO_ROOT / "tasks" / "transformer-inference-latency"
ANN_FOOTPRINT_TASK = REPO_ROOT / "tasks" / "ann-footprint-gate"
CLUSTER_RECOVERY_TASK = REPO_ROOT / "tasks" / "cluster-recovery-gate"
SESSION_GATE_DASHBOARD_TASK = REPO_ROOT / "tasks" / "session-gate-dashboard"
CV_DATASET_REPAIR_TASK = REPO_ROOT / "tasks" / "cv-dataset-repair"
BUSINESS_KPI_DRIFT_TASK = REPO_ROOT / "tasks" / "business-kpi-drift"
GROUNDED_CONTEXT_BENCH_TASK = REPO_ROOT / "tasks" / "grounded-context-bench"
ANN_QUERY_SCHEDULER_TASK = REPO_ROOT / "tasks" / "ann-query-scheduler"
ANN_INCREMENTAL_REINDEX_TASK = REPO_ROOT / "tasks" / "ann-incremental-reindex"
SEMANTIC_SEARCH_RECOVERY_TASK = REPO_ROOT / "tasks" / "semantic-search-recovery"
PARALLEL_EMBED_COMPRESS_TASK = REPO_ROOT / "tasks" / "parallel-embed-compress"
FAISS_INDEX_REGRESSION_TASK = REPO_ROOT / "tasks" / "faiss-index-regression"
HYBRID_SEARCH_LATENCY_TASK = REPO_ROOT / "tasks" / "hybrid-search-latency"
TOKENIZER_REGRESSION_TASK = REPO_ROOT / "tasks" / "tokenizer-regression-reproduction"
LABEL_NOISE_TASK = REPO_ROOT / "tasks" / "label-noise-isolation"
LORA_VRAM_TASK = REPO_ROOT / "tasks" / "lora-vram-pipeline"
CROSS_SERVICE_EMBEDDING_MISMATCH_TASK = REPO_ROOT / "tasks" / "cross-service-embedding-mismatch"


def write_minimal_task(
    root: Path,
    *,
    dockerfile: str,
    task_toml: str | None = None,
    dockerignore: str | None = None,
) -> Path:
    task_dir = root / "sample-task"
    env = task_dir / "environment"
    env.mkdir(parents=True)
    (env / "Dockerfile").write_text(dockerfile, encoding="utf-8")
    if dockerignore is not None:
        (env / ".dockerignore").write_text(dockerignore, encoding="utf-8")
    default_toml = """
version = "2.0"

[metadata]
author_name = "anonymous"
author_email = "anonymous"
difficulty = "hard"
category = "software-engineering"
subcategories = []
codebase_size = "small"
number_of_milestones = 0
languages = ["python"]
tags = ["a", "b", "c"]
expert_time_estimate_min = 30
junior_time_estimate_min = 120

[agent]
timeout_sec = 900

[verifier]
timeout_sec = 300

[environment]
allow_internet = false
build_timeout_sec = 600
cpus = 1
memory_mb = 2048
storage_mb = 10240
"""
    (task_dir / "task.toml").write_text(task_toml or default_toml, encoding="utf-8")
    return task_dir


GOOD_DOCKERFILE = """\
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

LABEL org.opencontainers.image.source="https://example.com/task"
LABEL org.opencontainers.image.revision="deadbeef"

WORKDIR /app

RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        tmux=3.3a-3 \\
        asciinema=2.2.0-1 \\
    && asciinema --version \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest==8.4.1

COPY src/ /app/src/
"""


class DockerfileCheckTest(unittest.TestCase):
    def test_compliant_task_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
            report = dockerfile_check.build_report(task_dir)
        self.assertEqual(report["fails"], 0)
        self.assertEqual(dockerfile_check.exit_code(report), 0)

    def test_missing_digest_fails(self) -> None:
        bad = GOOD_DOCKERFILE.replace(
            "@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb",
            "",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        self.assertGreater(report["fails"], 0)
        messages = json.dumps(report)
        self.assertIn("pin_base_digest", messages)
        self.assertIn("@sha256", messages)

    def test_non_sanctioned_final_image_fails_but_builder_is_allowed(self) -> None:
        custom = GOOD_DOCKERFILE.replace(
            GOOD_DOCKERFILE.splitlines()[0],
            "FROM example.invalid/custom@sha256:" + "a" * 64,
        )
        builder_then_canonical = (
            "FROM example.invalid/custom@sha256:" + "a" * 64 + " AS builder\n"
            + GOOD_DOCKERFILE
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            bad_task = write_minimal_task(root / "bad", dockerfile=custom)
            good_task = write_minimal_task(root / "good", dockerfile=builder_then_canonical)
            bad = dockerfile_check.build_report(bad_task)
            good = dockerfile_check.build_report(good_task)
        self.assertIn("check_sanctioned_base_images", json.dumps(bad))
        self.assertGreater(bad["fails"], 0)
        self.assertEqual(good["fails"], 0, json.dumps(good, indent=2))

    def test_scratch_is_sanctioned_without_digest(self) -> None:
        dockerfile = "FROM scratch\nWORKDIR /app\n# tmux asciinema\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=dockerfile)
            report = dockerfile_check.build_report(task_dir)
        sanctioned = next(
            row for row in report["results"] if row["check"] == "check_sanctioned_base_images"
        )
        pinned = next(row for row in report["results"] if row["check"] == "pin_base_digest")
        self.assertEqual(sanctioned["severity"], "PASS")
        self.assertEqual(pinned["severity"], "PASS")

    def test_build_context_size_limits_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
            oversized = task_dir / "environment" / "oversized.bin"
            with oversized.open("wb") as file_handle:
                file_handle.truncate(50 * 1024 * 1024 + 1)
            outside = Path(tmpdir) / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            (task_dir / "environment" / "escape").symlink_to(outside)
            report = dockerfile_check.build_report(task_dir)
        text = json.dumps(report)
        self.assertIn("exceeds 50 MiB", text)
        self.assertIn("symlink escapes", text)

    def test_compose_unsafe_capabilities_and_oracle_mount_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
            (task_dir / "environment" / "docker-compose.yaml").write_text(
                "services:\n  app:\n    cap_add:\n      - NET_ADMIN\n"
                "    volumes:\n      - ./oracle:/oracle\n",
                encoding="utf-8",
            )
            report = dockerfile_check.build_report(task_dir)
        text = json.dumps(report)
        self.assertIn("NET_ADMIN", text)
        self.assertIn("/oracle", text)

    def test_archive_must_be_extracted_and_removed_in_same_stage(self) -> None:
        bad = GOOD_DOCKERFILE + "\nCOPY fixtures.tar.gz /tmp/fixtures.tar.gz\n"
        good = bad + (
            "RUN tar -xzf /tmp/fixtures.tar.gz -C /app "
            "&& rm /tmp/fixtures.tar.gz\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_task = write_minimal_task(Path(tmpdir) / "bad", dockerfile=bad)
            good_task = write_minimal_task(Path(tmpdir) / "good", dockerfile=good)
            bad_report = dockerfile_check.build_report(bad_task)
            good_report = dockerfile_check.build_report(good_task)
        extraction_bad = next(
            row for row in bad_report["results"] if row["check"] == "check_file_extraction"
        )
        extraction_good = next(
            row for row in good_report["results"] if row["check"] == "check_file_extraction"
        )
        self.assertEqual(extraction_bad["severity"], "WARN")
        self.assertEqual(extraction_good["severity"], "PASS")

    def test_layer_volatility_warns_for_copy_before_dependency_install(self) -> None:
        bad = GOOD_DOCKERFILE + "\nCOPY . /app\nRUN pip install requests==2.32.4\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(
                Path(tmpdir),
                dockerfile=bad,
                dockerignore=".git\n__pycache__/\n",
            )
            report = dockerfile_check.build_report(task_dir)
        volatility = next(
            row for row in report["results"] if row["check"] == "check_layer_volatility"
        )
        self.assertEqual(volatility["severity"], "WARN")

    def test_unjustified_runtime_build_tool_warns(self) -> None:
        bad = GOOD_DOCKERFILE.replace(
            "asciinema=2.2.0-1 \\\n",
            "asciinema=2.2.0-1 \\\n        build-essential \\\n",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        runtime = next(
            row
            for row in report["results"]
            if row["check"] == "check_no_build_tools_in_runtime"
        )
        self.assertEqual(runtime["severity"], "WARN")

    def test_direct_download_requires_checksum(self) -> None:
        bad = GOOD_DOCKERFILE + "\nRUN curl -fsSL https://example.com/tool -o /tmp/tool\n"
        good = GOOD_DOCKERFILE + (
            "\nRUN curl -fsSL https://example.com/tool -o /tmp/tool "
            "&& echo 'abc  /tmp/tool' | sha256sum -c -\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_task = write_minimal_task(Path(tmpdir) / "bad", dockerfile=bad)
            good_task = write_minimal_task(Path(tmpdir) / "good", dockerfile=good)
            bad_report = dockerfile_check.build_report(bad_task)
            good_report = dockerfile_check.build_report(good_task)
        self.assertGreater(bad_report["fails"], 0)
        self.assertEqual(good_report["fails"], 0, json.dumps(good_report, indent=2))

    def test_node_dependency_needs_exact_pin_or_lockfile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
            package = task_dir / "environment" / "package.json"
            package.write_text(
                '{"dependencies":{"left-pad":"^1.3.0"}}\n', encoding="utf-8"
            )
            bad = dockerfile_check.build_report(task_dir)
            (task_dir / "environment" / "package-lock.json").write_text(
                '{"lockfileVersion":3}\n', encoding="utf-8"
            )
            good = dockerfile_check.build_report(task_dir)
        self.assertIn("left-pad", json.dumps(bad))
        self.assertEqual(good["fails"], 0, json.dumps(good, indent=2))

    def test_cargo_go_maven_and_gradle_unpinned_dependencies_fail(self) -> None:
        cases = (
            (
                "Cargo.toml",
                '[package]\nname="x"\nversion="0.1.0"\n[dependencies]\nserde = "^1"\n',
                "serde",
            ),
            (
                "go.mod",
                "module example.invalid/x\ngo 1.24\nrequire example.invalid/dep v1.2.3\n",
                "go.sum",
            ),
            (
                "pom.xml",
                "<project><dependencies><dependency><groupId>x</groupId>"
                "<artifactId>dep</artifactId></dependency></dependencies></project>",
                "dep",
            ),
            (
                "build.gradle",
                "dependencies { implementation 'com.example:dep:+' }\n",
                "dynamic versions",
            ),
        )
        for filename, content, expected in cases:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmpdir:
                task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
                (task_dir / "environment" / filename).write_text(content, encoding="utf-8")
                report = dockerfile_check.build_report(task_dir)
            self.assertGreater(report["fails"], 0, json.dumps(report, indent=2))
            self.assertIn(expected, json.dumps(report))

    def test_direct_npm_cargo_and_go_installs_require_versions(self) -> None:
        bad = GOOD_DOCKERFILE + (
            "\nRUN npm install left-pad\n"
            "RUN cargo install ripgrep\n"
            "RUN go install example.invalid/tool\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        text = json.dumps(report)
        self.assertIn("left-pad", text)
        self.assertIn("cargo install requires", text)
        self.assertIn("go install requires", text)

    def test_missing_session_tools_fails(self) -> None:
        bad = GOOD_DOCKERFILE.replace("tmux=3.3a-3 \\\n        asciinema=2.2.0-1 \\\n", "")
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        self.assertGreater(report["fails"], 0)
        self.assertIn("agent_session_tools", json.dumps(report))

    def test_copy_solution_fails(self) -> None:
        bad = GOOD_DOCKERFILE + "\nCOPY solution/ /app/solution/\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        self.assertGreater(report["fails"], 0)
        self.assertIn("solution/", json.dumps(report))

    def test_allow_internet_must_be_false(self) -> None:
        toml = """
version = "2.0"
[environment]
allow_internet = true
build_timeout_sec = 600
cpus = 1
memory_mb = 2048
storage_mb = 10240
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE, task_toml=toml)
            report = dockerfile_check.build_report(task_dir)
        self.assertGreater(report["fails"], 0)
        self.assertIn("allow_internet", json.dumps(report))

    def test_cli_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = write_minimal_task(Path(tmpdir), dockerfile=GOOD_DOCKERFILE)
            exit_code = dockerfile_check.main([str(task_dir), "--json"])
        self.assertEqual(exit_code, 0)

    def test_classifier_robustness_gate_task_passes(self) -> None:
        if not CLASSIFIER_TASK.is_dir():
            self.skipTest("classifier-robustness-gate task directory is not present")
        report = dockerfile_check.build_report(CLASSIFIER_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        # WARN-only (exit 2) is acceptable for real tasks missing optional .dockerignore/OCI labels.
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_rank_spike_remediation_task_passes(self) -> None:
        if not RANK_SPIKE_TASK.is_dir():
            self.skipTest("rank-spike-remediation task directory is not present")
        report = dockerfile_check.build_report(RANK_SPIKE_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_tensor_retention_gate_task_passes(self) -> None:
        if not TENSOR_RETENTION_TASK.is_dir():
            self.skipTest("tensor-retention-gate task directory is not present")
        report = dockerfile_check.build_report(TENSOR_RETENTION_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_transformer_inference_latency_task_passes(self) -> None:
        if not TRANSFORMER_LATENCY_TASK.is_dir():
            self.skipTest("transformer-inference-latency task directory is not present")
        report = dockerfile_check.build_report(TRANSFORMER_LATENCY_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_ann_footprint_gate_task_passes(self) -> None:
        if not ANN_FOOTPRINT_TASK.is_dir():
            self.skipTest("ann-footprint-gate task directory is not present")
        report = dockerfile_check.build_report(ANN_FOOTPRINT_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_cluster_recovery_gate_task_passes(self) -> None:
        if not CLUSTER_RECOVERY_TASK.is_dir():
            self.skipTest("cluster-recovery-gate task directory is not present")
        report = dockerfile_check.build_report(CLUSTER_RECOVERY_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_session_gate_dashboard_task_passes(self) -> None:
        if not SESSION_GATE_DASHBOARD_TASK.is_dir():
            self.skipTest("session-gate-dashboard task directory is not present")
        report = dockerfile_check.build_report(SESSION_GATE_DASHBOARD_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_cv_dataset_repair_task_passes(self) -> None:
        if not CV_DATASET_REPAIR_TASK.is_dir():
            self.skipTest("cv-dataset-repair task directory is not present")
        report = dockerfile_check.build_report(CV_DATASET_REPAIR_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_business_kpi_drift_task_passes(self) -> None:
        if not BUSINESS_KPI_DRIFT_TASK.is_dir():
            self.skipTest("business-kpi-drift task directory is not present")
        report = dockerfile_check.build_report(BUSINESS_KPI_DRIFT_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_grounded_context_bench_task_passes(self) -> None:
        if not GROUNDED_CONTEXT_BENCH_TASK.is_dir():
            self.skipTest("grounded-context-bench task directory is not present")
        report = dockerfile_check.build_report(GROUNDED_CONTEXT_BENCH_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_ann_query_scheduler_task_passes(self) -> None:
        if not ANN_QUERY_SCHEDULER_TASK.is_dir():
            self.skipTest("ann-query-scheduler task directory is not present")
        report = dockerfile_check.build_report(ANN_QUERY_SCHEDULER_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_ann_incremental_reindex_task_passes(self) -> None:
        if not ANN_INCREMENTAL_REINDEX_TASK.is_dir():
            self.skipTest("ann-incremental-reindex task directory is not present")
        report = dockerfile_check.build_report(ANN_INCREMENTAL_REINDEX_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_semantic_search_recovery_task_passes(self) -> None:
        if not SEMANTIC_SEARCH_RECOVERY_TASK.is_dir():
            self.skipTest("semantic-search-recovery task directory is not present")
        report = dockerfile_check.build_report(SEMANTIC_SEARCH_RECOVERY_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_parallel_embed_compress_task_passes(self) -> None:
        if not PARALLEL_EMBED_COMPRESS_TASK.is_dir():
            self.skipTest("parallel-embed-compress task directory is not present")
        report = dockerfile_check.build_report(PARALLEL_EMBED_COMPRESS_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_faiss_index_regression_task_passes(self) -> None:
        if not FAISS_INDEX_REGRESSION_TASK.is_dir():
            self.skipTest("faiss-index-regression task directory is not present")
        report = dockerfile_check.build_report(FAISS_INDEX_REGRESSION_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_hybrid_search_latency_task_passes(self) -> None:
        if not HYBRID_SEARCH_LATENCY_TASK.is_dir():
            self.skipTest("hybrid-search-latency task directory is not present")
        report = dockerfile_check.build_report(HYBRID_SEARCH_LATENCY_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_tokenizer_regression_reproduction_task_passes(self) -> None:
        if not TOKENIZER_REGRESSION_TASK.is_dir():
            self.skipTest("tokenizer-regression-reproduction task directory is not present")
        report = dockerfile_check.build_report(TOKENIZER_REGRESSION_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_label_noise_isolation_task_passes(self) -> None:
        if not LABEL_NOISE_TASK.is_dir():
            self.skipTest("label-noise-isolation task directory is not present")
        report = dockerfile_check.build_report(LABEL_NOISE_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_lora_vram_pipeline_task_passes(self) -> None:
        if not LORA_VRAM_TASK.is_dir():
            self.skipTest("lora-vram-pipeline task directory is not present")
        report = dockerfile_check.build_report(LORA_VRAM_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_cross_service_embedding_mismatch_task_passes(self) -> None:
        if not CROSS_SERVICE_EMBEDDING_MISMATCH_TASK.is_dir():
            self.skipTest("cross-service-embedding-mismatch task directory is not present")
        report = dockerfile_check.build_report(CROSS_SERVICE_EMBEDDING_MISMATCH_TASK)
        self.assertEqual(
            report["fails"],
            0,
            json.dumps(report["results"], indent=2),
        )
        self.assertIn(dockerfile_check.exit_code(report), (0, 2))

    def test_python_interpreter_hygiene_fails_on_usr_bin_python3_symlink(self) -> None:
        bad = """\
FROM python:3.13-slim-bookworm@sha256:abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789
WORKDIR /app
RUN apt-get update \\
    && apt-get install -y --no-install-recommends asciinema=2.2.0-1 tmux=3.3a-3 \\
    && rm -rf /var/lib/apt/lists/* \\
    && asciinema --version
RUN ln -sf /usr/local/bin/python3.13 /usr/bin/python3 \\
    && ln -sf /usr/local/bin/python3.13 /usr/bin/python
"""
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = write_minimal_task(Path(tmp), dockerfile=bad)
            report = dockerfile_check.build_report(task_dir)
        hygiene = next(r for r in report["results"] if r["check"] == "python_interpreter_hygiene")
        self.assertEqual(hygiene["severity"], "FAIL", json.dumps(hygiene, indent=2))
        self.assertTrue(
            any(issue["rule"] == "python_interpreter_hygiene" for issue in hygiene["issues"])
        )

    def test_python_interpreter_hygiene_passes_without_usr_bin_repoint(self) -> None:
        good = """\
FROM python:3.13-slim-bookworm@sha256:abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789
WORKDIR /app
RUN apt-get update \\
    && apt-get install -y --no-install-recommends asciinema=2.2.0-1 tmux=3.3a-3 \\
    && rm -rf /var/lib/apt/lists/* \\
    && asciinema --version \\
    && python3 -m pytest --version
"""
        result = dockerfile_check.check_python_interpreter_hygiene(
            good,
            dockerfile_check.normalize_dockerfile_lines(good),
        )
        self.assertEqual(result.severity, "PASS", result.detail or result.issues)


if __name__ == "__main__":
    unittest.main()
