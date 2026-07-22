import json
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
LOAM = "/app/bin/loam"
BUILD = "/app/tools/build-all"
RESET = "/app/tools/reset-lab"
MIXED = APP / "data" / "archive" / "mixed.store"
CURRENT = APP / "data" / "archive" / "current.store"
HEALTHY = APP / "data" / "archive" / "healthy.store"
VAULT = APP / "data" / "archive" / "vault.store"


@pytest.fixture(scope="session", autouse=True)
def _build_once() -> None:
    subprocess.run([RESET], check=True, cwd=APP)
    subprocess.run([BUILD], check=True, cwd=APP)


def _run_case(
    tmp_path: Path,
    case_id: str,
    store: Path,
    op: str,
    x: int | str,
    y: int,
    lane: str,
    skipping: bool,
) -> dict:
    case_dir = tmp_path / f"cases-{case_id}"
    case_dir.mkdir()
    line = f"{case_id}|{store}|{op}|{x}|{y}|{lane}|{int(skipping)}|probe\n"
    (case_dir / "incident.case").write_text(line, encoding="utf-8")
    report = tmp_path / f"{case_id}.json"
    subprocess.run([LOAM, "audit", str(case_dir), str(report)], check=True, cwd=APP)
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "complete"
    assert isinstance(payload["digest"], str) and payload["digest"]
    return payload["cases"][0]


def _ingest(tmp_path: Path, source: Path, name: str) -> Path:
    target_dir = tmp_path / name
    subprocess.run([LOAM, "ingest", str(source), str(target_dir)], check=True, cwd=APP)
    target = target_dir / "data.store"
    assert target.is_file()
    return target


def _write_csv(tmp_path: Path, name: str, first: bool) -> Path:
    path = tmp_path / f"{name}.csv"
    if first:
        lines = [
            "origin,presence,amount,region",
            "0,1,-937,east",
            "2,1,17,east",
            "2,1,29,west",
            "2,1,43,west",
            "2,1,107,north",
            "2,0,881,north",
            "2,1,137,south",
            "2,1,151,south",
        ]
    else:
        lines = [
            "origin,presence,amount,region",
            "2,1,-911,east",
            "2,1,7,east",
            "2,0,863,west",
            "2,1,19,west",
            "0,1,-883,north",
            "2,1,211,north",
            "2,1,223,south",
            "2,1,227,south",
        ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _write_gamma_csv(tmp_path: Path, name: str) -> Path:
    path = tmp_path / f"{name}.csv"
    lines = [
        "origin,presence,amount,region",
        "2,1,-999,east",
        "2,1,12,east",
        "2,1,25,west",
        "2,1,31,west",
        "0,1,401,north",
        "2,0,412,north",
        "0,0,423,south",
        "0,1,434,south",
        "2,1,55,east",
        "2,1,61,west",
        "2,0,700,north",
        "2,1,73,south",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _parse_store(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    pages: list[dict] = []
    index = 1
    while index < len(lines):
        header = lines[index].split("|")
        assert header[0] == "P" and len(header) == 9
        row_count = int(header[8])
        for raw in lines[index + 1 : index + 1 + row_count]:
            fields = raw.split("|")
            assert fields[0] == "R" and len(fields) == 5
        pages.append(
            {
                "generation": int(header[2]),
                "low": int(header[3]),
                "high": int(header[4]),
                "has_absent": int(header[5]),
            }
        )
        index += 1 + row_count
    return pages


def _assert_markers(path: Path, expected: list[tuple[int, int, int]]) -> list[dict]:
    pages = _parse_store(path)
    assert len(pages) == len(expected)
    for page, markers in zip(pages, expected, strict=True):
        assert (page["low"], page["high"], page["has_absent"]) == markers
    return pages


def _assert_tally(row: dict, count: int, total: int) -> None:
    assert row["row_count"] == count
    assert row["sum_amount"] == total


def test_p01(tmp_path: Path) -> None:
    """Fresh numeric ingestion keeps its recorded value domain faithful."""
    source = _write_csv(tmp_path, "alpha-01", True)
    produced = _ingest(tmp_path, source, "a1")
    _assert_markers(produced, [(17, 43, 1), (107, 151, 1)])


def test_p02(tmp_path: Path) -> None:
    """Archived selective row execution returns the complete invoice window."""
    row = _run_case(tmp_path, "p02", MIXED, "range", 10, 40, "row", True)
    _assert_tally(row, 4, 100)
    assert row["pages_read"] < row["pages_total"]


def test_p03(tmp_path: Path) -> None:
    """Fresh artifact evidence and archived selective answers agree together."""
    source = _write_csv(tmp_path, "alpha-03", True)
    produced = _ingest(tmp_path, source, "a3")
    _assert_markers(produced, [(17, 43, 1), (107, 151, 1)])
    row = _run_case(tmp_path, "p03", MIXED, "range", 10, 40, "row", True)
    _assert_tally(row, 4, 100)


def test_p04(tmp_path: Path) -> None:
    """Batch execution counts every absent archived entry exactly once."""
    row = _run_case(tmp_path, "p04", MIXED, "isnull", 0, 0, "batch", False)
    _assert_tally(row, 2, 0)


def test_p05(tmp_path: Path) -> None:
    """Fresh artifact evidence composes with archived batch absence handling."""
    source = _write_csv(tmp_path, "alpha-05", True)
    produced = _ingest(tmp_path, source, "a5")
    _assert_markers(produced, [(17, 43, 1), (107, 151, 1)])
    row = _run_case(tmp_path, "p05", MIXED, "isnull", 0, 0, "batch", False)
    _assert_tally(row, 2, 0)


def test_p06(tmp_path: Path) -> None:
    """The mixed selective-batch window preserves all qualifying values."""
    row = _run_case(tmp_path, "p06", MIXED, "range", -1000, 25, "batch", True)
    _assert_tally(row, 3, 25)


def test_p07(tmp_path: Path) -> None:
    """A fresh sparse range avoids irrelevant data without widening markers."""
    source = _write_csv(tmp_path, "beta-07", False)
    produced = _ingest(tmp_path, source, "b7")
    _assert_markers(produced, [(-911, 19, 1), (211, 227, 1)])
    row = _run_case(tmp_path, "p07", produced, "range", 500, 600, "row", True)
    _assert_tally(row, 0, 0)
    assert row["pages_read"] < row["pages_total"]


def test_p08(tmp_path: Path) -> None:
    """Selective archived and healthy controls retain correct work avoidance."""
    row = _run_case(tmp_path, "p08", MIXED, "range", 10, 20, "row", True)
    _assert_tally(row, 2, 30)
    assert row["pages_read"] < row["pages_total"]
    control = _run_case(tmp_path, "p08c", HEALTHY, "range", 100, 130, "batch", True)
    _assert_tally(control, 4, 460)
    assert control["pages_read"] < control["pages_total"]


def test_p09(tmp_path: Path) -> None:
    """Batch range execution excludes archived absent entries."""
    row = _run_case(tmp_path, "p09", MIXED, "range", -1000, -1, "batch", False)
    _assert_tally(row, 1, -5)


def test_p10(tmp_path: Path) -> None:
    """Equivalent fresh ingests produce faithful and byte-stable artifacts."""
    source = _write_csv(tmp_path, "alpha-10", True)
    first = _ingest(tmp_path, source, "a10-first")
    second = _ingest(tmp_path, source, "a10-second")
    _assert_markers(first, [(17, 43, 1), (107, 151, 1)])
    assert first.read_bytes() == second.read_bytes()
    report = tmp_path / "audit.json"
    subprocess.run([LOAM, "audit", str(APP / "data" / "cases"), str(report)], check=True, cwd=APP)
    first_bytes = report.read_bytes()
    subprocess.run([LOAM, "audit", str(APP / "data" / "cases"), str(report)], check=True, cwd=APP)
    assert first_bytes == report.read_bytes()


def test_p11(tmp_path: Path) -> None:
    """Neighboring generations preserve the same selective numeric answer."""
    row = _run_case(tmp_path, "p11", MIXED, "range", 10, 20, "row", True)
    _assert_tally(row, 2, 30)
    control = _run_case(tmp_path, "p11c", CURRENT, "range", 10, 20, "row", True)
    _assert_tally(control, 2, 30)


def test_p12(tmp_path: Path) -> None:
    """Full archived batch totals coexist with an active healthy fast path."""
    row = _run_case(tmp_path, "p12", MIXED, "all", 0, 0, "batch", False)
    _assert_tally(row, 10, 2095)
    control = _run_case(tmp_path, "p12c", HEALTHY, "range", 100, 130, "batch", True)
    _assert_tally(control, 4, 460)
    assert control["path"] == "batch"
    assert control["pages_read"] < control["pages_total"]


def test_p13(tmp_path: Path) -> None:
    """Selective absence probes agree across lanes on neighboring generations."""
    row = _run_case(tmp_path, "p13", VAULT, "isnull", 0, 0, "row", True)
    _assert_tally(row, 2, 0)
    assert row["pages_read"] < row["pages_total"]
    batch = _run_case(tmp_path, "p13b", VAULT, "isnull", 0, 0, "batch", True)
    _assert_tally(batch, 2, 0)
    assert batch["pages_read"] < batch["pages_total"]


def test_p14(tmp_path: Path) -> None:
    """Selective text-code probes stay complete on neighboring generations."""
    row = _run_case(tmp_path, "p14", VAULT, "region_eq", "east", 0, "row", True)
    _assert_tally(row, 2, 49)
    assert row["pages_read"] < row["pages_total"]


def test_p15(tmp_path: Path) -> None:
    """Sparse fresh chunks keep faithful markers and consistent answers."""
    source = _write_gamma_csv(tmp_path, "gamma-15")
    produced = _ingest(tmp_path, source, "g15")
    _assert_markers(produced, [(-999, 31, 0), (0, 0, 1), (55, 73, 1)])
    row = _run_case(tmp_path, "p15", produced, "range", 50, 80, "row", True)
    _assert_tally(row, 3, 189)
    assert row["pages_read"] < row["pages_total"]
    batch = _run_case(tmp_path, "p15b", produced, "range", 50, 80, "batch", True)
    _assert_tally(batch, 3, 189)
    assert batch["pages_read"] < batch["pages_total"]
    probe = _run_case(tmp_path, "p15c", produced, "eq", -999, 0, "batch", True)
    _assert_tally(probe, 1, -999)
    assert probe["pages_read"] < probe["pages_total"]
    absent = _run_case(tmp_path, "p15d", produced, "isnull", 0, 0, "batch", False)
    _assert_tally(absent, 5, 0)
