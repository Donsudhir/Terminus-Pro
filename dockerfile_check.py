#!/usr/bin/env python3
"""
Dockerfile and image best-practices checks for Terminal-Bench tasks.

Validates environment/Dockerfile and related task.toml [environment] settings
against the Terminal-Bench Dockerfile & Image Best Practices policy.

Usage:
    python3 dockerfile_check.py tasks/<task-name>
    python3 dockerfile_check.py tasks/<task-name> --json

Exit codes: 0 = PASS, 1 = FAIL, 2 = WARN-only
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import ci_policy

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

RESERVED_PATHS = ("/tests", "/solution", "/oracle")
PIP_UNPINNED_ALLOWLIST = {"pip", "setuptools", "wheel"}
REQUIRED_ENVIRONMENT_KEYS = ("cpus", "memory_mb", "storage_mb", "build_timeout_sec")
OCI_LABEL_PREFIX = "org.opencontainers.image."
DOCKER_COMPOSE_NAMES = {"docker-compose.yaml", "docker-compose.yml"}
ENV_FILE_EXCLUDE = {"dockerfile"} | {name.lower() for name in DOCKER_COMPOSE_NAMES}
ARCHIVE_SUFFIXES = (".tar", ".tar.gz", ".tgz", ".zip")
BUILD_TOOL_PACKAGES = {
    "build-essential",
    "gcc",
    "g++",
    "clang",
    "cmake",
    "make",
    "cargo",
    "rustc",
    "golang-go",
    "maven",
    "gradle",
}


@dataclass
class Issue:
    rule: str
    severity: str
    message: str
    line: int | None = None


@dataclass
class CheckResult:
    check: str
    severity: str
    issues: list[Issue] = field(default_factory=list)
    detail: str = ""

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)
        if issue.severity == "FAIL":
            self.severity = "FAIL"
        elif issue.severity == "WARN" and self.severity == "PASS":
            self.severity = "WARN"


def load_task_toml(task_dir: Path) -> dict:
    path = task_dir / "task.toml"
    if not path.exists() or tomllib is None:
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def dockerfile_path(task_dir: Path) -> Path:
    return task_dir / "environment" / "Dockerfile"


def normalize_dockerfile_lines(content: str) -> list[tuple[int, str]]:
    """Return (source_line_number, logical_line) pairs with continuations merged."""
    logical: list[tuple[int, str]] = []
    buffer = ""
    start_line = 0
    for line_no, raw in enumerate(content.splitlines(), start=1):
        stripped = raw.rstrip()
        if not buffer:
            start_line = line_no
            buffer = stripped
        else:
            buffer = f"{buffer} {stripped.lstrip()}"
        if stripped.endswith("\\"):
            buffer = buffer[:-1].rstrip()
            continue
        logical.append((start_line, buffer))
        buffer = ""
    if buffer:
        logical.append((start_line, buffer))
    return logical


def from_image(text: str) -> str | None:
    try:
        tokens = shlex.split(text)
    except ValueError:
        return None
    if not tokens or tokens[0].upper() != "FROM":
        return None
    for token in tokens[1:]:
        if token.startswith("--"):
            continue
        return token
    return None


def docker_stages(logical: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    stages: list[list[tuple[int, str]]] = []
    for item in logical:
        if re.match(r"^\s*FROM\b", item[1], re.I):
            stages.append([])
        if stages:
            stages[-1].append(item)
    return stages


def env_file_count(task_dir: Path) -> int:
    env_dir = task_dir / "environment"
    if not env_dir.is_dir():
        return 0
    return sum(
        1
        for path in env_dir.rglob("*")
        if path.is_file() and path.name.lower() not in ENV_FILE_EXCLUDE
    )


def check_dockerfile_exists(task_dir: Path) -> CheckResult:
    result = CheckResult(check="dockerfile_present", severity="PASS")
    if not dockerfile_path(task_dir).is_file():
        result.add(
            Issue(
                rule="dockerfile_present",
                severity="FAIL",
                message="Missing environment/Dockerfile",
            )
        )
    return result


def check_pin_base_digest(content: str, logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="pin_base_digest", severity="PASS")
    from_lines = [(line_no, text) for line_no, text in logical if re.match(r"^\s*FROM\b", text, re.I)]
    if not from_lines:
        result.add(
            Issue(
                rule="pin_base_digest",
                severity="FAIL",
                message="environment/Dockerfile must contain at least one FROM instruction",
            )
        )
        return result
    for line_no, text in from_lines:
        image = from_image(text)
        if image != "scratch" and "@sha256:" not in text:
            result.add(
                Issue(
                    rule="pin_base_digest",
                    severity="FAIL",
                    message=f"Every FROM stage must be pinned by digest (@sha256:...): {text.strip()}",
                    line=line_no,
                )
            )
        if re.search(r":latest\b", text, re.I) and "@sha256:" not in text:
            result.add(
                Issue(
                    rule="pin_base_digest",
                    severity="FAIL",
                    message=f"Do not use floating :latest tags; pin by digest: {text.strip()}",
                    line=line_no,
                )
            )
    return result


def check_sanctioned_base_image(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="check_sanctioned_base_images", severity="PASS")
    from_lines = [item for item in logical if re.match(r"^\s*FROM\b", item[1], re.I)]
    if not from_lines:
        return result
    line_no, text = from_lines[-1]
    image = from_image(text)
    if image not in ci_policy.SANCTIONED_FINAL_IMAGES and image not in ci_policy.SANCTIONED_BASE_EXEMPTIONS:
        result.add(
            Issue(
                rule="check_sanctioned_base_images",
                severity="FAIL",
                message=(
                    "Final runtime stage must use an exact sanctioned image or an "
                    f"ADR-approved image added to the reviewed policy list; found {image!r}"
                ),
                line=line_no,
            )
        )
    return result


def check_build_context_size(task_dir: Path) -> CheckResult:
    result = CheckResult(check="check_build_context_size", severity="PASS")
    environment = task_dir / "environment"
    if not environment.is_dir():
        return result
    total = 0
    for path in sorted(environment.rglob("*")):
        if path.is_symlink():
            resolved = path.resolve(strict=False)
            if not resolved.is_relative_to(environment.resolve()):
                result.add(
                    Issue(
                        rule="check_build_context_size",
                        severity="FAIL",
                        message=f"Build-context symlink escapes environment/: {path.relative_to(task_dir)}",
                    )
                )
            continue
        if not path.is_file():
            continue
        size = path.stat().st_size
        total += size
        if size > ci_policy.BUILD_CONTEXT_FILE_MAX_BYTES:
            result.add(
                Issue(
                    rule="check_build_context_size",
                    severity="FAIL",
                    message=(
                        f"Build-context file exceeds 50 MiB: {path.relative_to(task_dir)} "
                        f"({size} bytes)"
                    ),
                )
            )
    if total > ci_policy.BUILD_CONTEXT_MAX_BYTES:
        result.add(
            Issue(
                rule="check_build_context_size",
                severity="FAIL",
                message=f"environment/ exceeds 100 MiB build-context limit ({total} bytes)",
            )
        )
    result.detail = f"environment build context: {total} bytes"
    return result


def check_workdir(content: str) -> CheckResult:
    result = CheckResult(check="workdir", severity="PASS")
    if not re.search(r"^\s*WORKDIR\b", content, re.I | re.M):
        result.add(
            Issue(
                rule="workdir",
                severity="FAIL",
                message="environment/Dockerfile must set WORKDIR explicitly",
            )
        )
    return result


def check_reproducible_builds(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="reproducible_builds", severity="PASS")
    curl_pipe_sh = re.compile(
        r"(?:curl|wget)\b[^\n|]*\|\s*(?:\s*(?:bash|sh)\b|(?:\s*\\)?\s*(?:bash|sh)\b)",
        re.I,
    )
    for line_no, text in logical:
        if curl_pipe_sh.search(text):
            result.add(
                Issue(
                    rule="reproducible_builds",
                    severity="FAIL",
                    message="Avoid curl|sh or wget|sh installers; pin release tarballs with checksum verification",
                    line=line_no,
                )
            )
        if re.search(r"\bapt(?:-get)?\s+upgrade\b", text, re.I):
            result.add(
                Issue(
                    rule="reproducible_builds",
                    severity="FAIL",
                    message="Do not run apt-get upgrade in task images",
                    line=line_no,
                )
            )
        if re.search(r"\bdate\b", text) and re.search(r"\bRUN\b", text, re.I):
            result.add(
                Issue(
                    rule="reproducible_builds",
                    severity="WARN",
                    message="RUN invokes date; avoid embedding wall-clock time in image layers",
                    line=line_no,
                )
            )
        if re.search(r"^\s*RUN\b[^\n]*\b(?:curl|wget)\b", text, re.I) and not re.search(
            r"\b(?:sha256sum|shasum\s+-a\s+256)\b", text, re.I
        ):
            result.add(
                Issue(
                    rule="reproducible_builds",
                    severity="FAIL",
                    message="Direct curl/wget downloads must verify a SHA-256 checksum in the same RUN",
                    line=line_no,
                )
            )
        if re.search(r"^\s*RUN\b[^\n]*\bgit\s+clone\b", text, re.I) and not re.search(
            r"\bgit\s+(?:-C\s+\S+\s+)?checkout\s+[0-9a-f]{40}\b", text, re.I
        ):
            result.add(
                Issue(
                    rule="reproducible_builds",
                    severity="FAIL",
                    message="git clone must check out an exact 40-character commit in the same RUN",
                    line=line_no,
                )
            )
    return result


def check_apt_hygiene(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="apt_hygiene", severity="PASS")
    update_counts: list[int] = []
    current_updates = 0
    for line_no, text in logical:
        if re.match(r"^\s*FROM\b", text, re.I):
            if update_counts or current_updates:
                update_counts.append(current_updates)
            current_updates = 0
        if re.search(r"\bapt(?:-get)?\s+update\b", text, re.I):
            current_updates += 1
        if re.search(r"\bapt(?:-get)?\s+install\b", text, re.I):
            if "rm -rf /var/lib/apt/lists" not in text:
                result.add(
                    Issue(
                        rule="apt_hygiene",
                        severity="FAIL",
                        message="apt install must end with rm -rf /var/lib/apt/lists/* in the same RUN layer",
                        line=line_no,
                    )
                )
            if "--no-install-recommends" not in text:
                result.add(
                    Issue(
                        rule="apt_hygiene",
                        severity="WARN",
                        message="Prefer apt-get install -y --no-install-recommends",
                        line=line_no,
                    )
                )
    update_counts.append(current_updates)
    for stage_number, update_count in enumerate(update_counts, start=1):
        if update_count > 1:
            result.add(
                Issue(
                    rule="apt_hygiene",
                    severity="WARN",
                    message=(
                        f"Stage {stage_number} has {update_count} apt-get update calls; "
                        "consolidate into one apt transaction per stage"
                    ),
                )
            )
    return result


def check_agent_session_tools(content: str) -> CheckResult:
    result = CheckResult(check="agent_session_tools", severity="PASS")
    lowered = content.lower()
    missing = [tool for tool in ("tmux", "asciinema") if tool not in lowered]
    if missing:
        result.add(
            Issue(
                rule="agent_session_tools",
                severity="FAIL",
                message=(
                    "Agent runtime requires tmux and asciinema in the image; "
                    f"missing: {', '.join(missing)}"
                ),
            )
        )
    return result


def check_python_interpreter_hygiene(content: str, logical: list[tuple[int, str]]) -> CheckResult:
    """Fail when /usr/bin/python3 is repointed over Debian asciinema's interpreter.

    CM-001: ln -sf …/python3.X /usr/bin/python3 after apt-installing asciinema
    breaks `#!/usr/bin/python3` at runtime while earlier-layer version checks still pass.
    """
    result = CheckResult(check="python_interpreter_hygiene", severity="PASS")
    lowered = content.lower()
    installs_asciinema = bool(re.search(r"\basciinema\b", lowered))
    if not installs_asciinema:
        return result

    symlink_re = re.compile(
        r"ln\s+(-[a-zA-Z]+\s+)*\S*python3(?:\.\d+)?\s+/usr/bin/python3\b",
        re.I,
    )
    for line_no, text in logical:
        if symlink_re.search(text):
            result.add(
                Issue(
                    rule="python_interpreter_hygiene",
                    severity="FAIL",
                    message=(
                        "Do not symlink /usr/bin/python3 onto the image Python when "
                        "asciinema is installed (CM-001). Debian asciinema uses "
                        "#!/usr/bin/python3 and its modules live on the distro "
                        "interpreter; repointing breaks agent session setup. Prefer "
                        "PATH ordering and keep `asciinema --version` in the final RUN."
                    ),
                    line=line_no,
                )
            )

    # Soft guard: if asciinema is installed, require a version check somewhere so
    # runtime breakage is not hidden behind an earlier-layer probe alone.
    if "asciinema --version" not in lowered and "asciinema -v" not in lowered:
        result.add(
            Issue(
                rule="python_interpreter_hygiene",
                severity="WARN",
                message=(
                    "asciinema is installed but no `asciinema --version` appears in "
                    "the Dockerfile; add a final-layer check so interpreter breakage "
                    "fails the image build (CM-001)."
                ),
            )
        )
    return result


def check_silo_and_reserved(content: str, logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="silo_and_reserved", severity="PASS")
    forbidden_copy = re.findall(
        r"^\s*(?:ADD|COPY)\b.*\b(?:solution/|tests/)",
        content,
        flags=re.I | re.M,
    )
    for match in forbidden_copy:
        result.add(
            Issue(
                rule="silo_and_reserved",
                severity="FAIL",
                message=f"Do not copy solution/ or tests/ into the image: {match.strip()}",
            )
        )

    for path in RESERVED_PATHS:
        hits = re.findall(
            rf"^\s*(?:WORKDIR|VOLUME|ADD|COPY)\b.*\s{re.escape(path)}(?:\s|$|/)",
            content,
            flags=re.I | re.M,
        )
        hits.extend(
            re.findall(
                rf"^\s*RUN\b.*\b(?:mkdir|install\s+-d|ln\s+-s|cp|mv|touch)\b.*{re.escape(path)}(?:\s|$|/)",
                content,
                flags=re.I | re.M,
            )
        )
        for hit in hits:
            result.add(
                Issue(
                    rule="silo_and_reserved",
                    severity="FAIL",
                    message=f"Reserved Harbor mount path must not be created or targeted: {hit.strip()}",
                )
            )

    for line_no, text in logical:
        unsafe_names = "|".join(re.escape(value) for value in ci_policy.UNSAFE_CAPABILITIES)
        if re.search(
            rf"(?:--privileged|--cap-add|{unsafe_names}|docker\.sock)",
            text,
            re.I,
        ):
            result.add(
                Issue(
                    rule="silo_and_reserved",
                    severity="FAIL",
                    message="Do not use privileged mode, unsafe capabilities, or docker.sock mounts",
                    line=line_no,
                )
            )
    return result


def check_compose_safety(task_dir: Path) -> CheckResult:
    result = CheckResult(check="check_privileged_containers", severity="PASS")
    compose = next(
        (
            task_dir / "environment" / name
            for name in DOCKER_COMPOSE_NAMES
            if (task_dir / "environment" / name).is_file()
        ),
        None,
    )
    if compose is None:
        return result
    content = compose.read_text(encoding="utf-8", errors="replace")
    unsafe_names = "|".join(re.escape(value) for value in ci_policy.UNSAFE_CAPABILITIES)
    for line_no, line in enumerate(content.splitlines(), start=1):
        if re.search(
            rf"(?:privileged:\s*true|cap_add:|{unsafe_names}|docker\.sock)",
            line,
            re.I,
        ):
            result.add(
                Issue(
                    rule="check_privileged_containers",
                    severity="FAIL",
                    message=f"Unsafe compose privilege/capability: {line.strip()}",
                    line=line_no,
                )
            )
        if re.search(
            r":\s*(?:/logs/artifacts|/logs/verifier|/tests|/solution|/oracle)(?:/|\s|$)",
            line,
        ) or re.search(
            r"target:\s*(?:/logs/artifacts|/logs/verifier|/tests|/solution|/oracle)(?:/|\s|$)",
            line,
        ):
            result.add(
                Issue(
                    rule="check_privileged_containers",
                    severity="FAIL",
                    message=f"Compose overrides a Harbor-reserved mount: {line.strip()}",
                    line=line_no,
                )
            )
    return result


def check_dockerignore_and_copy(task_dir: Path, logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="dockerignore_and_copy", severity="PASS")
    env_dir = task_dir / "environment"
    dockerignore = env_dir / ".dockerignore"
    copy_dot = [
        (line_no, text)
        for line_no, text in logical
        if re.search(r"^\s*(?:COPY|ADD)\s+\.\s", text, re.I)
        or re.search(r"^\s*(?:COPY|ADD)\s+\.\s+/", text, re.I)
        or re.search(r"^\s*(?:COPY|ADD)\s+\.\s+\S", text, re.I)
    ]

    if env_file_count(task_dir) >= 5 and not dockerignore.is_file():
        result.add(
            Issue(
                rule="dockerignore_and_copy",
                severity="WARN",
                message="Non-trivial tasks should include environment/.dockerignore",
            )
        )

    if copy_dot and not dockerignore.is_file():
        for line_no, text in copy_dot:
            result.add(
                Issue(
                    rule="dockerignore_and_copy",
                    severity="FAIL",
                    message=f"COPY . requires a strict environment/.dockerignore: {text.strip()}",
                    line=line_no,
                )
            )

    for line_no, text in logical:
        if re.search(r"^\s*(?:COPY|ADD)\b.*\b(?:\.git|\.env)\b", text, re.I):
            result.add(
                Issue(
                    rule="dockerignore_and_copy",
                    severity="FAIL",
                    message=f"Do not copy secrets or VCS metadata into the image: {text.strip()}",
                    line=line_no,
                )
            )
    return result


def check_source_as_files(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="source_as_files", severity="PASS")
    heredoc_run = re.compile(
        r"^\s*RUN\b.*(?:<<-?\s*['\"]?[A-Za-z0-9_]+['\"]?|cat\s+>\s|cat\s+>>\s|tee\s+>)",
        re.I,
    )
    for line_no, text in logical:
        if heredoc_run.search(text):
            result.add(
                Issue(
                    rule="source_as_files",
                    severity="FAIL",
                    message="Store source as COPY'd files, not RUN heredocs or inline cat/tee writes",
                    line=line_no,
                )
            )
    return result


def check_copy_metadata(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="copy_metadata", severity="PASS")
    for line_no, text in logical:
        if re.search(r"\bchmod\s+-R\b.*/app\b", text, re.I) or re.search(
            r"\bchown\s+-R\b.*/app\b", text, re.I
        ):
            result.add(
                Issue(
                    rule="copy_metadata",
                    severity="WARN",
                    message="Avoid recursive chmod/chown across /app; use COPY --chmod/--chown on specific paths",
                    line=line_no,
                )
            )
    return result


def check_lazy_pull(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="lazy_pull", severity="PASS")
    run_text = "\n".join(text for _, text in logical)
    for line_no, text in logical:
        if re.search(r"^\s*(?:COPY|ADD)\b.*\.(?:tar|tar\.gz|tgz|zip)\b", text, re.I):
            if not re.search(r"\btar\s+-x", run_text, re.I) and not re.search(
                r"\bunzip\b", run_text, re.I
            ):
                result.add(
                    Issue(
                        rule="lazy_pull",
                        severity="WARN",
                        message=(
                            "Archive copied into the image without an extract step; "
                            "extract at build time and remove the archive for lazy-pull locality"
                        ),
                        line=line_no,
                    )
                )
    return result


def check_file_extraction(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="check_file_extraction", severity="PASS")
    for stage in docker_stages(logical):
        stage_text = "\n".join(text for _line, text in stage)
        for line_no, text in stage:
            if not re.match(r"^\s*(?:COPY|ADD)\b", text, re.I):
                continue
            archive_tokens = [
                token.strip('"\'')
                for token in text.split()
                if token.lower().endswith(ARCHIVE_SUFFIXES)
            ]
            for archive in archive_tokens:
                basename = Path(archive).name
                extracted = bool(
                    re.search(rf"(?:tar\s+[^\n]*|unzip\s+[^\n]*){re.escape(basename)}", stage_text, re.I)
                )
                removed = bool(
                    re.search(rf"\brm\b[^\n]*{re.escape(basename)}", stage_text, re.I)
                )
                if not (extracted and removed):
                    result.add(
                        Issue(
                            rule="check_file_extraction",
                            severity="WARN",
                            message=(
                                f"Archive {basename} must be extracted and removed in the same "
                                "Docker stage"
                            ),
                            line=line_no,
                        )
                    )
    return result


def check_layer_volatility(logical: list[tuple[int, str]]) -> CheckResult:
    result = CheckResult(check="check_layer_volatility", severity="PASS")
    dependency_install = re.compile(
        r"\b(?:pip(?:3)?\s+install|npm\s+(?:ci|install)|cargo\s+fetch|go\s+mod\s+download|mvn\b|gradle\b)",
        re.I,
    )
    for stage in docker_stages(logical):
        broad_copy_index: int | None = None
        for index, (line_no, text) in enumerate(stage):
            if re.search(r"^\s*(?:COPY|ADD)\s+(?:--\S+\s+)*\.\s+", text, re.I):
                broad_copy_index = index
                broad_copy_line = line_no
                break
        if broad_copy_index is None:
            continue
        if any(dependency_install.search(text) for _line, text in stage[broad_copy_index + 1 :]):
            result.add(
                Issue(
                    rule="check_layer_volatility",
                    severity="WARN",
                    message=(
                        "COPY/ADD . appears before dependency installation; copy manifests and "
                        "install dependencies before volatile source"
                    ),
                    line=broad_copy_line,
                )
            )
    return result


def check_no_build_tools_in_runtime(
    logical: list[tuple[int, str]], task_data: dict
) -> CheckResult:
    result = CheckResult(check="check_no_build_tools_in_runtime", severity="PASS")
    stages = docker_stages(logical)
    if not stages:
        return result
    metadata = task_data.get("metadata") or {}
    languages = {
        str(value).strip().lower()
        for value in (metadata.get("languages") or [])
        if isinstance(value, str)
    }
    compilation_expected = bool(
        languages
        & {
            "c",
            "c++",
            "cpp",
            "rust",
            "go",
            "golang",
            "java",
            "fortran",
            "zig",
            "ada",
            "haskell",
            "ocaml",
        }
    )
    if compilation_expected:
        return result
    for line_no, text in stages[-1]:
        if not re.search(r"\bapt(?:-get)?\s+install\b", text, re.I):
            continue
        installed = sorted(
            package
            for package in BUILD_TOOL_PACKAGES
            if re.search(rf"(?<![\w-]){re.escape(package)}(?![\w-])", text)
        )
        if installed:
            result.add(
                Issue(
                    rule="check_no_build_tools_in_runtime",
                    severity="WARN",
                    message=(
                        "Final runtime installs build tools not justified by agent-facing "
                        f"languages: {installed}"
                    ),
                    line=line_no,
                )
            )
    return result


def check_oci_labels(content: str) -> CheckResult:
    result = CheckResult(check="oci_labels", severity="PASS")
    if OCI_LABEL_PREFIX not in content:
        result.add(
            Issue(
                rule="oci_labels",
                severity="WARN",
                message=(
                    "Consider OpenContainers audit labels "
                    "(org.opencontainers.image.source, .revision, .created, .version, .licenses)"
                ),
            )
        )
    return result


def _exact_version(value: str) -> bool:
    cleaned = value.strip()
    return bool(re.fullmatch(r"(?:v?\d+)(?:\.\d+)*(?:[-+][0-9A-Za-z.-]+)?", cleaned))


def check_dependency_pinning(
    task_dir: Path, logical: list[tuple[int, str]]
) -> CheckResult:
    result = CheckResult(check="dependency_pinning", severity="PASS")
    unpinned_pip: list[str] = []

    for line_no, text in logical:
        if re.search(r"\bpip(?:3)?\b.*\binstall\b", text, re.I):
            try:
                tokens = shlex.split(text)
            except ValueError:
                continue
            try:
                install_index = next(i for i, t in enumerate(tokens) if t in {"install", "install."})
            except StopIteration:
                continue
            for token in tokens[install_index + 1 :]:
                if token.startswith("-") or token.startswith("$") or token.startswith("."):
                    continue
                if token in PIP_UNPINNED_ALLOWLIST:
                    continue
                if token.endswith((".txt", ".in")):
                    continue
                if any(op in token for op in ("==", ">=", "<=", "~=", "!=")) or token.startswith(
                    "git+"
                ):
                    continue
                unpinned_pip.append(token)

        if re.search(r"\bnpm\s+install\b", text, re.I) and not re.search(
            r"\bnpm\s+install\s+(?:--\S+\s+)*(?:\.\s*)?$", text, re.I
        ):
            try:
                tokens = shlex.split(text)
            except ValueError:
                tokens = []
            try:
                npm_install_index = tokens.index("install")
            except ValueError:
                npm_install_index = len(tokens)
            for token in tokens[npm_install_index + 1 :]:
                if token.startswith("-"):
                    continue
                if token.startswith(("&&", "||")):
                    break
                if token.startswith("@"):
                    pinned = token.count("@") >= 2 and _exact_version(token.rsplit("@", 1)[1])
                else:
                    pinned = "@" in token and _exact_version(token.rsplit("@", 1)[1])
                if not pinned:
                    result.add(
                        Issue(
                            rule="dependency_pinning",
                            severity="FAIL",
                            message=f"Pin npm install package exactly: {token}",
                            line=line_no,
                        )
                    )

        if re.search(r"\bcargo\s+install\b", text) and not re.search(
            r"\bcargo\s+install\b[^\n]*(?:--version\s+\S+|--locked\b)", text
        ):
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message="cargo install requires --version or --locked",
                    line=line_no,
                )
            )
        if re.search(r"\bgo\s+install\s+\S+", text) and not re.search(
            r"\bgo\s+install\s+\S+@v?\d", text
        ):
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message="go install requires an explicit @version",
                    line=line_no,
                )
            )

    if unpinned_pip:
        result.add(
            Issue(
                rule="dependency_pinning",
                severity="FAIL",
                message=f"Pin pip packages when installed directly: {sorted(set(unpinned_pip))}",
            )
        )

    environment = task_dir / "environment"
    for package_json in environment.rglob("package.json"):
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message=f"Invalid package.json {package_json.relative_to(task_dir)}: {exc}",
                )
            )
            continue
        dependencies = {
            **(data.get("dependencies") or {}),
            **(data.get("devDependencies") or {}),
        }
        lock_present = any(
            (package_json.parent / name).is_file()
            for name in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock")
        )
        if dependencies and not lock_present:
            unpinned = sorted(
                name
                for name, version in dependencies.items()
                if not isinstance(version, str) or not _exact_version(version)
            )
            if unpinned:
                result.add(
                    Issue(
                        rule="dependency_pinning",
                        severity="FAIL",
                        message=(
                            f"Node dependencies need exact versions or a lockfile in "
                            f"{package_json.parent.relative_to(task_dir)}: {unpinned}"
                        ),
                    )
                )

    for cargo_toml in environment.rglob("Cargo.toml"):
        text = cargo_toml.read_text(encoding="utf-8", errors="replace")
        if "[dependencies]" in text and not (cargo_toml.parent / "Cargo.lock").is_file():
            non_exact = re.findall(
                r"(?m)^\s*([A-Za-z0-9_-]+)\s*=\s*[\"'](?:\^|~|\*|>=|<=|>|<)",
                text,
            )
            if non_exact:
                result.add(
                    Issue(
                        rule="dependency_pinning",
                        severity="FAIL",
                        message=(
                            f"Cargo dependencies need exact versions or Cargo.lock in "
                            f"{cargo_toml.parent.relative_to(task_dir)}: {sorted(non_exact)}"
                        ),
                    )
                )

    for go_mod in environment.rglob("go.mod"):
        text = go_mod.read_text(encoding="utf-8", errors="replace")
        has_requirements = bool(re.search(r"(?m)^\s*require(?:\s|\()", text))
        if has_requirements and not (go_mod.parent / "go.sum").is_file():
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message=f"go.mod with requirements needs go.sum in {go_mod.parent.relative_to(task_dir)}",
                )
            )

    for pom in environment.rglob("pom.xml"):
        try:
            tree = ET.fromstring(pom.read_text(encoding="utf-8"))
        except ET.ParseError as exc:
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message=f"Invalid pom.xml {pom.relative_to(task_dir)}: {exc}",
                )
            )
            continue
        dependencies = [node for node in tree.iter() if node.tag.endswith("dependency")]
        missing_versions = [
            next(
                (child.text or "?" for child in node if child.tag.endswith("artifactId")),
                "?",
            )
            for node in dependencies
            if not any(child.tag.endswith("version") and (child.text or "").strip() for child in node)
        ]
        if missing_versions:
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message=f"Maven dependencies need versions in {pom.relative_to(task_dir)}: {missing_versions}",
                )
            )

    for gradle in [*environment.rglob("build.gradle"), *environment.rglob("build.gradle.kts")]:
        text = gradle.read_text(encoding="utf-8", errors="replace")
        dynamic = re.findall(r"[\"'][^\"']+:(?:\+|latest[^\"']*)[\"']", text, re.I)
        if dynamic:
            result.add(
                Issue(
                    rule="dependency_pinning",
                    severity="FAIL",
                    message=f"Gradle dependencies use dynamic versions in {gradle.relative_to(task_dir)}",
                )
            )
    return result


def check_task_environment(task_dir: Path, task_data: dict) -> CheckResult:
    result = CheckResult(check="task_environment", severity="PASS")
    environment = task_data.get("environment")
    if not isinstance(environment, dict):
        result.add(
            Issue(
                rule="task_environment",
                severity="FAIL",
                message="task.toml must define [environment] with cpus, memory_mb, storage_mb, build_timeout_sec",
            )
        )
        return result

    missing = [key for key in REQUIRED_ENVIRONMENT_KEYS if key not in environment]
    if missing:
        result.add(
            Issue(
                rule="task_environment",
                severity="FAIL",
                message=f"task.toml [environment] missing required keys: {missing}",
            )
        )

    allow_internet = environment.get("allow_internet")
    if allow_internet is not False:
        result.add(
            Issue(
                rule="task_environment",
                severity="FAIL",
                message=f"task.toml [environment].allow_internet must be false, found {allow_internet!r}",
            )
        )

    for key in ("cpus", "memory_mb", "storage_mb"):
        value = environment.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            result.add(
                Issue(
                    rule="task_environment",
                    severity="FAIL",
                    message=f"task.toml [environment].{key} must be a positive number",
                )
            )

    build_timeout = environment.get("build_timeout_sec")
    if not isinstance(build_timeout, (int, float)) or build_timeout <= 0:
        result.add(
            Issue(
                rule="task_environment",
                severity="FAIL",
                message="task.toml [environment].build_timeout_sec must be a positive number",
            )
        )
    return result


def run_checks(task_dir: Path) -> list[CheckResult]:
    task_data = load_task_toml(task_dir)
    results: list[CheckResult] = [
        check_task_environment(task_dir, task_data),
        check_build_context_size(task_dir),
        check_compose_safety(task_dir),
    ]

    present = check_dockerfile_exists(task_dir)
    results.append(present)
    if present.severity == "FAIL":
        return results

    content = dockerfile_path(task_dir).read_text(encoding="utf-8")
    logical = normalize_dockerfile_lines(content)

    results.extend(
        [
            check_pin_base_digest(content, logical),
            check_sanctioned_base_image(logical),
            check_workdir(content),
            check_reproducible_builds(logical),
            check_apt_hygiene(logical),
            check_agent_session_tools(content),
            check_python_interpreter_hygiene(content, logical),
            check_silo_and_reserved(content, logical),
            check_dockerignore_and_copy(task_dir, logical),
            check_source_as_files(logical),
            check_copy_metadata(logical),
            check_file_extraction(logical),
            check_layer_volatility(logical),
            check_no_build_tools_in_runtime(logical, task_data),
            check_oci_labels(content),
            check_dependency_pinning(task_dir, logical),
        ]
    )
    return results


def build_report(task_dir: Path) -> dict:
    results = run_checks(task_dir)
    fails = sum(1 for r in results if r.severity == "FAIL")
    warns = sum(1 for r in results if r.severity == "WARN")
    return {
        "task_dir": str(task_dir),
        "results": [
            {
                "check": r.check,
                "severity": r.severity,
                "detail": r.detail or _result_detail(r),
                "issues": [
                    {
                        "rule": issue.rule,
                        "severity": issue.severity,
                        "message": issue.message,
                        "line": issue.line,
                    }
                    for issue in r.issues
                ],
            }
            for r in results
        ],
        "fails": fails,
        "warns": warns,
    }


def _result_detail(result: CheckResult) -> str:
    if not result.issues:
        return "OK"
    return "; ".join(issue.message for issue in result.issues[:3])


def exit_code(report: dict) -> int:
    if report["fails"]:
        return 1
    if report["warns"]:
        return 2
    return 0


def format_text_report(task_dir: Path, report: dict) -> str:
    lines = [
        "",
        "=" * 70,
        f"  Dockerfile Check: {task_dir}",
        "=" * 70,
        "",
    ]
    for entry in report["results"]:
        icon = {"PASS": "✓", "WARN": "!", "FAIL": "✗"}.get(entry["severity"], "?")
        lines.append(f"  [{icon}] {entry['check']}: {entry['severity']}")
        for issue in entry["issues"]:
            loc = f" (line {issue['line']})" if issue.get("line") else ""
            lines.append(f"      - {issue['message']}{loc}")
        lines.append("")

    if report["fails"]:
        lines.append(f"  RESULT: FAIL ({report['fails']} check(s) failed)")
    elif report["warns"]:
        lines.append(f"  RESULT: WARN ({report['warns']} check(s) need review)")
    else:
        lines.append("  RESULT: PASS")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Terminal-Bench task Dockerfiles against image best practices."
    )
    parser.add_argument("task_dir", type=Path, help="Path to tasks/<task-name>")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    task_dir = args.task_dir
    if not task_dir.is_dir():
        print(f"ERROR: {task_dir} is not a directory", file=sys.stderr)
        return 1

    report = build_report(task_dir)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_text_report(task_dir, report))
    return exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())
