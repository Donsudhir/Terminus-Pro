"""Verifier for musl-sysroot-splice assembly outputs."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

PAYLOAD = Path("/app/output/payload")
REPORT = Path("/app/output/probe_report.json")
BUILD = Path("/app/tools/build_payload.sh")


def _rebuild() -> None:
    subprocess.run(["bash", BUILD.as_posix()], check=True, cwd="/app")


@pytest.fixture(scope="module", autouse=True)
def _built_once() -> None:
    """Rebuild through the public assembly entrypoint once per module."""
    _rebuild()


def _read_report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def _file_digest(path: Path) -> str:
    proc = subprocess.run(
        ["sha256sum", path.as_posix()],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.split()[0]


def _qemu_stdout() -> str:
    qemu = "qemu-x86_64"
    missing = subprocess.run(
        ["bash", "-lc", f"command -v {qemu}"],
        capture_output=True,
    ).returncode
    if missing != 0:
        proc = subprocess.run(
            [PAYLOAD.as_posix()],
            capture_output=True,
            text=True,
            check=False,
        )
    else:
        proc = subprocess.run(
            [qemu, PAYLOAD.as_posix()],
            capture_output=True,
            text=True,
            check=False,
        )
    return proc.stdout


def test_artifact_present() -> None:
    """Payload ELF exists at /app/output/payload and is executable."""
    assert PAYLOAD.is_file(), "payload missing"
    assert PAYLOAD.stat().st_size > 64
    assert os.access(PAYLOAD, os.X_OK)


def test_elf_has_no_interp() -> None:
    """Fully static payload must not carry a PT_INTERP program interpreter."""
    proc = subprocess.run(
        ["readelf", "-l", PAYLOAD.as_posix()],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "INTERP" not in proc.stdout


def test_runtime_marker_match() -> None:
    """qemu-user stdout includes MARKER=CXR-7F from the release contract."""
    out = _qemu_stdout()
    assert "MARKER=CXR-7F" in out


def test_runtime_thread_slot() -> None:
    """qemu-user stdout reports THREAD=7 for the thread-local probe."""
    out = _qemu_stdout()
    assert "THREAD=7" in out


def test_runtime_errno_slot() -> None:
    """qemu-user stdout reports ERRNO=2 after the intentional failed open."""
    out = _qemu_stdout()
    assert "ERRNO=2" in out


def test_summary_all_true() -> None:
    """Ledger settlement is true and every row ok flag is true."""
    report = _read_report()
    assert report["schema_version"] == "1"
    assert report["settlement"] is True
    assert all(row["ok"] is True for row in report["rows"])
    assert all("detail" in row for row in report["rows"])


def test_summary_count() -> None:
    """Ledger contains exactly three rows named marker, thread, errno."""
    report = _read_report()
    assert len(report["rows"]) == 3
    names = [row["name"] for row in report["rows"]]
    assert names == ["marker", "thread", "errno"]


def test_digest_matches_artifact() -> None:
    """payload_digest matches the on-disk artifact; LANE_TAG=BRAVO on stdout."""
    report = _read_report()
    digest = _file_digest(PAYLOAD)
    assert report["payload_digest"] == digest
    out = _qemu_stdout()
    assert "LANE_TAG=BRAVO" in out
