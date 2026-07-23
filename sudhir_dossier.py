"""Per-revision task dossier helpers (ADR-0012).

Keeps review artifacts, platform feedback, Harbor evidence, and every Snorkel
form paste field (difficulty / solution / verification / rubric) under
``sudhir_reviews/<slug>/REV-<n>/``.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import dsv_humanizer

# Keyword → CM id suggestions (propose only; do not invent new CM rows).
CM_KEYWORD_MAP: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("CM-007", ("pytest.py", "sys.path", "confcutdir", "pythonsafepath", "/conftest.py", "cwd-shadow")),
    ("CM-006", ("no interp", "helper-name", "span_info", "malformed-input", "off-domain rubric", "process-heavy")),
    ("CM-001", ("asciinema", "moduleNotFoundError", "/usr/bin/python3")),
    ("CM-002", ("solvable=false", "behavior_in_task_description", "inspect-status", "probe cli")),
    ("CM-005", ("collapse cr1", "stem-match", "map_state")),
)

FORM_FILES: dict[str, str] = {
    "difficulty": "DIFFICULTY.md",
    "solution": "SOLUTION.md",
    "verification": "VERIFICATION.md",
    "rubric": "RUBRIC.md",
}
DSV_AUDIT_FILE = dsv_humanizer.AUDIT_FILENAME


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_task_learning_fields(entry: dict[str, Any]) -> None:
    entry.setdefault("evidence", {})
    entry.setdefault("revisions", [])
    learning = entry.setdefault("learning", {})
    learning.setdefault("cm_hits", [])
    learning.setdefault("patterns_applied", [])
    learning.setdefault("form_refs", {})


def revision_dir(reviews_dir: Path, slug: str, revision: int) -> Path:
    return reviews_dir / slug / f"REV-{revision}"


def current_revision_dir(reviews_dir: Path, entry: dict[str, Any]) -> Path:
    rev = int(entry.get("revision") or 0)
    if rev < 1:
        rev = 1
    return revision_dir(reviews_dir, entry["slug"], rev)


def suggest_cm_ids(text: str) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for cm_id, keywords in CM_KEYWORD_MAP:
        if any(keyword in lowered for keyword in keywords):
            hits.append(cm_id)
    return hits


def preupload_complete(path: Path) -> tuple[bool, str]:
    if not path.is_file():
        return False, f"missing {path.name}"
    text = path.read_text(encoding="utf-8")
    if dsv_humanizer.REQUIRED_MARKER in text:
        ok, detail = strict_dsv_complete(path.parent)
        if not ok:
            return False, detail
    unchecked = re.findall(r"^\s*[-*]\s+\[\s+\]\s+", text, flags=re.MULTILINE)
    if unchecked:
        return False, f"{len(unchecked)} unchecked item(s) in {path.name}"
    if "READY_FOR_PACKAGE: yes" not in text and not re.search(r"^\s*[-*]\s+\[[xX]\]\s+", text, flags=re.MULTILINE):
        return False, f"{path.name} has no checked items and no READY_FOR_PACKAGE: yes"
    return True, "ok"


def dsv_form_paths(rev_dir: Path) -> dict[str, Path]:
    return {
        field: rev_dir / FORM_FILES[field]
        for field in dsv_humanizer.FIELD_ORDER
    }


def strict_dsv_complete(rev_dir: Path) -> tuple[bool, str]:
    """Verify that current DSV files match a strict content-addressed audit."""
    return dsv_humanizer.verify_audit(
        rev_dir / DSV_AUDIT_FILE,
        dsv_form_paths(rev_dir),
    )


def require_strict_dsv(preupload: Path) -> None:
    """Activate the non-bypassable DSV gate for an existing revision."""
    text = preupload.read_text(encoding="utf-8") if preupload.is_file() else ""
    if dsv_humanizer.REQUIRED_MARKER in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += (
        "\n- [ ] Strict Humanizer DSV audit stored and current\n\n"
        f"{dsv_humanizer.REQUIRED_MARKER}\n"
    )
    preupload.write_text(text, encoding="utf-8")


def preupload_template(revision: int, reason: str) -> str:
    return f"""# Pre-upload checklist (REV-{revision})

Reason: {reason}

Walk COMMON_MISTAKES and WHAT_WORKED before packaging. Tick every item (`[x]`)
or mark N/A with `[x]` and a note. `sudhir_task.py package` refuses unchecked
`- [ ]` lines unless `--force`.

- [ ] COMMON_MISTAKES preventions reviewed for this task type
- [ ] CM-007: test.sh uses `cd /tests` + PYTHONSAFEPATH + `--confcutdir` (or N/A)
- [ ] CM-006: behavioral tests / rubric cover claimed contracts (or N/A)
- [ ] Harbor evidence recorded (`sudhir_task.py evidence …`)
- [ ] Platform feedback captured in FEEDBACK.md when Needs Revision
- [ ] Form paste fields stored (DIFFICULTY.md, SOLUTION.md, VERIFICATION.md, RUBRIC.md)
- [ ] Strict Humanizer DSV audit stored and current
- [ ] Zip SHA will be recorded by package

{dsv_humanizer.REQUIRED_MARKER}
READY_FOR_PACKAGE: no
"""


def open_revision_workspace(
    reviews_dir: Path,
    entry: dict[str, Any],
    *,
    reason: str,
) -> Path:
    """Create REV-<n>/ stubs and append EDIT_LEDGER. Returns the revision dir."""
    ensure_task_learning_fields(entry)
    rev = int(entry["revision"])
    slug = entry["slug"]
    rev_dir = revision_dir(reviews_dir, slug, rev)
    rev_dir.mkdir(parents=True, exist_ok=True)

    notes = rev_dir / "NOTES.md"
    if not notes.exists():
        notes.write_text(
            f"# REV-{rev} notes — {slug}\n\nOpened: {utc_now()}\n\nReason: {reason}\n",
            encoding="utf-8",
        )

    feedback = rev_dir / "FEEDBACK.md"
    if not feedback.exists():
        platform = entry.get("platform_status") or {}
        snorkel = entry.get("snorkel") or {}
        chunks = [
            f"# REV-{rev} reviewer feedback — {slug}\n",
            f"Captured stub: {utc_now()}\n",
            "Paste platform Reviewer Feedback below, or run "
            "`sudhir_task.py feedback-capture`.\n",
        ]
        if platform:
            chunks.append("\n## Prior platform_status\n")
            chunks.append("```json\n" + json.dumps(platform, indent=2) + "\n```\n")
        if snorkel.get("status_line") or snorkel.get("difficulty"):
            chunks.append("\n## Prior snorkel scalars\n")
            chunks.append(
                f"- difficulty: {snorkel.get('difficulty')}\n"
                f"- solvable: {snorkel.get('solvable')}\n"
                f"- status_line: {snorkel.get('status_line')}\n"
                f"- static_outcome: {snorkel.get('static_outcome')}\n"
            )
        feedback.write_text("".join(chunks), encoding="utf-8")

    for filename in FORM_FILES.values():
        path = rev_dir / filename
        if not path.exists():
            label = path.stem
            path.write_text(
                f"# {label} — {slug} REV-{rev}\n\n"
                f"(empty — run `sudhir_task.py form-capture {slug} "
                f"--{label.lower()}-file …` or paste here before upload)\n",
                encoding="utf-8",
            )

    preupload = rev_dir / "PREUPLOAD.md"
    if not preupload.exists():
        preupload.write_text(preupload_template(rev, reason), encoding="utf-8")

    evidence = rev_dir / "EVIDENCE.md"
    if not evidence.exists():
        evidence.write_text(
            f"# REV-{rev} Harbor evidence — {slug}\n\n"
            "Recorded by `sudhir_task.py evidence`.\n",
            encoding="utf-8",
        )

    review_root = reviews_dir / slug
    review_root.mkdir(parents=True, exist_ok=True)
    ledger = review_root / "EDIT_LEDGER.md"
    if not ledger.exists():
        ledger.write_text(f"# {slug} Edit Ledger\n", encoding="utf-8")
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {utc_now()} — Revision {rev}\n\n- {reason}\n")

    rel = f"sudhir_reviews/{slug}/REV-{rev}"
    revisions: list[dict[str, Any]] = list(entry.get("revisions") or [])
    revisions = [row for row in revisions if int(row.get("n", -1)) != rev]
    revisions.append(
        {
            "n": rev,
            "reason": reason,
            "opened_at": utc_now(),
            "feedback_ref": f"{rel}/FEEDBACK.md",
            "rubric_ref": f"{rel}/RUBRIC.md",
            "form_refs": {
                key: f"{rel}/{name}" for key, name in FORM_FILES.items()
            },
            "zip_sha": None,
            "cm_ids": [],
        }
    )
    entry["revisions"] = sorted(revisions, key=lambda row: int(row["n"]))
    return rev_dir


def write_capture_file(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = body if body.endswith("\n") else body + "\n"
    if not text.lstrip().startswith("#"):
        text = f"# {title}\n\n{text}"
    path.write_text(text, encoding="utf-8")


def update_revision_cm_ids(entry: dict[str, Any], cm_ids: list[str]) -> None:
    ensure_task_learning_fields(entry)
    rev = int(entry.get("revision") or 0)
    for row in entry["revisions"]:
        if int(row.get("n", -1)) == rev:
            merged = sorted(set(row.get("cm_ids") or []) | set(cm_ids))
            row["cm_ids"] = merged
            break
    hits = list(entry["learning"].get("cm_hits") or [])
    for cm_id in cm_ids:
        if cm_id not in hits:
            hits.append(cm_id)
    entry["learning"]["cm_hits"] = hits


def resolve_job_dir(repo_root: Path, jobs_dir: Path, job: str) -> Path | None:
    candidates = [
        repo_root / "jobs" / job,
        jobs_dir / job,
        Path(job),
    ]
    for candidate in candidates:
        if (candidate / "result.json").is_file():
            return candidate
        if candidate.name == "result.json" and candidate.is_file():
            return candidate.parent
    return None


def parse_harbor_mean(result_path: Path) -> float | None:
    data = json.loads(result_path.read_text(encoding="utf-8"))
    stats = data.get("stats") or {}
    evals = stats.get("evals") or {}
    for _name, payload in evals.items():
        metrics = payload.get("metrics") or []
        if metrics and isinstance(metrics[0], dict) and "mean" in metrics[0]:
            return float(metrics[0]["mean"])
    return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zip_member_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return len(archive.namelist())


def sanitize_platform_snapshot(
    snorkel: dict[str, Any],
    *,
    text_summary: str = "",
    quality_summary: str = "",
    test_review: str = "",
    test_rubrics: str = "",
    max_chars: int = 12000,
) -> str:
    lines = [
        "# Platform snapshot (sanitized)",
        "",
        f"Captured: {utc_now()}",
        "",
        "## Scalars",
        f"- difficulty: {snorkel.get('difficulty')}",
        f"- solvable: {snorkel.get('solvable')}",
        f"- status_line: {snorkel.get('status_line')}",
        f"- static_outcome: {snorkel.get('static_outcome')}",
        f"- submission_id: {snorkel.get('submission_id')}",
        f"- zip_filename: {snorkel.get('zip_filename')}",
        f"- uploaded_at: {snorkel.get('uploaded_at')}",
        f"- source_file: {snorkel.get('source_file')}",
        "",
        "## Agent performance",
    ]
    perf = snorkel.get("agent_performance") or {}
    if perf:
        for name, pct in sorted(perf.items()):
            lines.append(f"- {name}: {pct}")
    else:
        lines.append("- (none parsed)")
    lines.append("")

    def _clip(label: str, body: str) -> None:
        body = (body or "").strip()
        if not body:
            return
        lines.append(f"## {label}")
        lines.append("")
        if len(body) > max_chars:
            body = body[:max_chars] + "\n\n…[truncated]…\n"
        lines.append("```")
        lines.append(body)
        lines.append("```")
        lines.append("")

    _clip("text_summary", text_summary)
    _clip("quality_check_summary", quality_summary)
    _clip("test_review", test_review)
    _clip("test_rubrics (from platform export)", test_rubrics)
    return "\n".join(lines) + "\n"


def extract_export_form_fields(path: Path) -> dict[str, str]:
    """Pull sanitize-safe form/feedback fields from a Snorkel export JSON."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    docs = data.get("task_documents") or []
    if not docs or not isinstance(docs[0], dict):
        return {}
    sd = docs[0].get("submission_document") or {}
    out: dict[str, str] = {}
    for key in (
        "text_summary",
        "quality_check_summary",
        "test_review",
        "test_rubrics",
        "test_quality_judge_report",
    ):
        value = sd.get(key)
        if isinstance(value, str) and value.strip():
            out[key] = value
    # Opaque textareas sometimes hold author paste fields.
    for key, value in sd.items():
        if key.startswith("textarea") and isinstance(value, str) and value.strip():
            out[key] = value
    return out


def applicable_cm_prompts(entry: dict[str, Any], source_dir: Path | None) -> list[str]:
    prompts = [
        "CM-001: Dockerfile must not break Debian asciinema via /usr/bin/python3 symlink",
        "CM-006: Prefer behavioral checks over string/ELF proxies; rubric must be domain-correct",
    ]
    languages = {str(x).lower() for x in (entry.get("languages") or [])}
    test_sh = None
    if source_dir is not None:
        candidate = source_dir / "tests" / "test.sh"
        if candidate.is_file():
            test_sh = candidate.read_text(encoding="utf-8", errors="replace")
    if test_sh and "pytest" in test_sh:
        prompts.append(
            "CM-007: test.sh must use cd /tests + PYTHONSAFEPATH + --confcutdir"
        )
    if languages & {"c", "rust", "fortran", "go"}:
        prompts.append("CM-006/scientific: output contracts must be enforced by tests")
    return prompts
