#!/usr/bin/env python3
"""Build or verify the compact regression index for submission archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import root_adapter  # noqa: E402
import validate_submission_zip  # noqa: E402

DEFAULT_SUBMISSION_DIR = root_adapter.ROOTS.submissions
DEFAULT_INDEX = root_adapter.ROOTS.current_submission_index


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def build_entry(zip_path: Path) -> dict[str, object]:
    report = validate_submission_zip.build_report(zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        names = sorted(
            info.filename.replace("\\", "/").lstrip("./")
            for info in archive.infolist()
            if not info.is_dir()
        )
        instruction_names = (
            sorted(
                name
                for name in names
                if name.startswith("steps/") and name.endswith("/instruction.md")
            )
            if report["layout"] == "milestone"
            else ["instruction.md"]
        )
        instruction_hashes = {
            name: sha256_bytes(archive.read(name)) for name in instruction_names
        }
        task_toml_sha256 = sha256_bytes(archive.read("task.toml"))

    return {
        "sha256": sha256_bytes(zip_path.read_bytes()),
        "bytes": zip_path.stat().st_size,
        "layout": report["layout"],
        "milestones": report["milestones"],
        "member_count": report["member_count"],
        "task_toml_sha256": task_toml_sha256,
        "instruction_sha256": instruction_hashes,
        "validator_valid": report["valid"],
    }


def build_index(submission_dir: Path) -> dict[str, object]:
    archives = {
        path.name: build_entry(path)
        for path in sorted(submission_dir.glob("*.zip"))
    }
    return {
        "schema_version": 1,
        "submission_directory": submission_dir.name,
        "archive_count": len(archives),
        "archives": archives,
    }


def write_index_atomic(submission_dir: Path, index_path: Path) -> dict[str, object]:
    payload = build_index(submission_dir.resolve())
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    resolved_index = index_path.resolve()
    root_adapter.ROOTS.assert_writable(resolved_index)
    resolved_index.parent.mkdir(parents=True, exist_ok=True)
    temporary = resolved_index.with_name(f".{resolved_index.name}.{os.getpid()}.tmp")
    try:
        temporary.write_text(rendered, encoding="utf-8")
        os.replace(temporary, resolved_index)
    finally:
        temporary.unlink(missing_ok=True)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission-dir", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument(
        "--historical",
        action="store_true",
        help="index immutable Task_Ready_To_Submit instead of current submissions",
    )
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.historical:
        default_dir = root_adapter.ROOTS.historical_submissions
        default_index = root_adapter.ROOTS.historical_submission_index
    else:
        default_dir = DEFAULT_SUBMISSION_DIR
        default_index = DEFAULT_INDEX
    submission_dir = (args.submission_dir or default_dir).resolve()
    index_path = (args.index or default_index).resolve()

    if args.check:
        payload = build_index(submission_dir)
        if not index_path.is_file():
            print(f"submission index missing: {index_path}", file=sys.stderr)
            return 1
        try:
            expected = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"submission index is invalid JSON: {exc}", file=sys.stderr)
            return 1
        if expected != payload:
            print("submission index is stale; rebuild it with scripts/build_submission_index.py", file=sys.stderr)
            return 1
        print(f"submission index current: {payload['archive_count']} archives")
        return 0

    payload = write_index_atomic(submission_dir, index_path)
    print(f"wrote {index_path}: {payload['archive_count']} archives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
