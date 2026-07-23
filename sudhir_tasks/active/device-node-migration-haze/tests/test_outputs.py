import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
BINARY = APP / "bin" / "haze"
SCHEMA_DOC = APP / "docs" / "cutover-report-schema.md"
TREES = APP / "fixtures" / "trees"


@pytest.fixture(scope="session", autouse=True)
def compiled_pipeline():
    subprocess.run(
        [os.fspath(APP / "tools" / "build_all.sh")],
        cwd=APP,
        check=True,
        text=True,
        capture_output=True,
        timeout=240,
    )
    assert BINARY.is_file()


def _fnv1a64(data: bytes) -> str:
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{h:016x}"


def _expected_schema_version():
    text = SCHEMA_DOC.read_text(encoding="utf-8")
    for line in text.splitlines():
        if "currently" in line and "`" in line:
            for token in line.replace("`", " ").split():
                if token.isdigit():
                    return int(token)
    return 1


def _run_env(tmp_path, label, trees_root=None):
    output = tmp_path / f"{label}.json"
    env = os.environ.copy()
    if trees_root is None:
        env.pop("HAZE_TREES", None)
    else:
        env["HAZE_TREES"] = str(trees_root)
    env["HAZE_OUTPUT"] = str(output)
    completed = subprocess.run(
        [os.fspath(BINARY)],
        cwd=APP,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr
    raw = output.read_text(encoding="utf-8")
    return json.loads(raw), raw


def _item(document, family, tag="base", mode=None):
    matches = [
        row
        for row in document["runs"]
        if row["family"] == family and row["tag"] == tag and (mode is None or row["mode"] == mode)
    ]
    assert len(matches) == 1, (family, tag, mode, matches)
    return matches[0]


def _failing(doc):
    return _item(doc, "failing_alpha", mode="cutover")


def _control(doc):
    return _item(doc, "control_plain", mode="control")


def _reject(doc):
    return _item(doc, "reject_delta", mode="reject")


def _digest_ok(raw: str, doc: dict) -> bool:
    marker = ',"digest":"'
    if marker not in raw:
        return False
    head, _, tail = raw.rpartition(marker)
    digest_hex = tail[:16]
    if tail[16:18] != '"}':
        return False
    payload = head + "}"
    return _fnv1a64(payload.encode("utf-8")) == digest_hex == doc["digest"]


def _special_probes(row):
    return [p for p in row["probes"] if p["name"] in ("ttyS0", "null", "loop0")]


def _clone_trees(tmp_path, order):
    root = tmp_path / "trees"
    for name in order:
        src = TREES / name
        dst = root / name
        shutil.copytree(src, dst)
    return root


def test_h01(tmp_path):
    """Post-cutover major/minor identity matches pre-cutover contract."""
    doc, _ = _run_env(tmp_path, "h01")
    row = _failing(doc)
    specs = _special_probes(row)
    assert specs
    assert row["identity_ok"] and all(p["identity_ok"] for p in specs)


def test_h02(tmp_path):
    """Post-cutover node kind / openability matches pre-cutover contract."""
    doc, _ = _run_env(tmp_path, "h02")
    row = _failing(doc)
    specs = _special_probes(row)
    assert specs
    assert row["open_ok"] and all(p["open_ok"] for p in specs)
    for probe in specs:
        assert int(probe["id_hex"], 16) != 0


def test_h03(tmp_path):
    """Mode/owner fidelity on special entries matches pre-cutover contract."""
    doc, _ = _run_env(tmp_path, "h03")
    row = _failing(doc)
    specs = _special_probes(row)
    assert specs
    assert row["mode_ok"] and all(p["mode_ok"] for p in specs)


def test_h04(tmp_path):
    """Post-cutover open paths resolve to required nodes on failing fixture."""
    doc, _ = _run_env(tmp_path, "h04")
    row = _failing(doc)
    specs = _special_probes(row)
    assert specs
    assert row["path_ok"] and all(p["path_ok"] for p in specs)


def test_h05(tmp_path):
    """Sequential cutover families do not inherit prior roster fidelity mistakes."""
    doc, _ = _run_env(tmp_path, "h05")
    failing = _failing(doc)
    control = _control(doc)
    assert failing["mode_ok"] and all(p["mode_ok"] for p in _special_probes(failing))
    assert control["exit_code"] == 0
    assert control["open_ok"] and all(p["open_ok"] for p in control["probes"])
    assert not control["rejected"]


def test_h06(tmp_path):
    """Combined open+identity under cutover with materialization+fidelity interaction."""
    doc, _ = _run_env(tmp_path, "h06")
    row = _failing(doc)
    specs = _special_probes(row)
    assert row["open_ok"] and row["identity_ok"] and row["mode_ok"]
    assert all(p["open_ok"] and p["identity_ok"] and p["mode_ok"] for p in specs)
    assert doc["summary"]["failing_ok"]


def test_h07(tmp_path):
    """Count/exit plausibility does not mask identity disagreement after repair."""
    doc, _ = _run_env(tmp_path, "h07")
    row = _failing(doc)
    assert row["entry_count"] > 0
    assert row["exit_code"] == 0
    assert row["identity_ok"] and row["mode_ok"]
    assert all(p["identity_ok"] and p["mode_ok"] for p in _special_probes(row))


def test_h08(tmp_path):
    """Rebinding uses post-swap relative anchors on failing fixtures."""
    doc, _ = _run_env(tmp_path, "h08")
    row = _failing(doc)
    specs = _special_probes(row)
    assert row["path_ok"] and row["open_ok"]
    assert all(p["path_ok"] and p["open_ok"] for p in specs)


def test_h09(tmp_path):
    """Report summary fields agree with emitted open/identity probe results."""
    doc, raw = _run_env(tmp_path, "h09")
    assert doc["schema_version"] == _expected_schema_version()
    failing = _failing(doc)
    assert failing["open_ok"] == all(p["open_ok"] for p in failing["probes"])
    assert failing["identity_ok"] == all(p["identity_ok"] for p in _special_probes(failing))
    assert doc["summary"]["failing_ok"]
    assert doc["summary"]["reject_stable"]
    assert _digest_ok(raw, doc)


def test_h10(tmp_path):
    """Reordered execution of the same family is deterministic for identity probes."""
    order_a = _clone_trees(tmp_path / "a", ["failing_alpha", "control_plain", "reject_delta"])
    order_b = _clone_trees(tmp_path / "b", ["reject_delta", "control_plain", "failing_alpha"])
    doc_a, raw_a = _run_env(tmp_path, "h10a", trees_root=order_a)
    doc_b, raw_b = _run_env(tmp_path, "h10b", trees_root=order_b)
    fa = _failing(doc_a)
    fb = _failing(doc_b)
    assert fa["identity_ok"] and fb["identity_ok"]
    assert doc_a["digest"] == doc_b["digest"]
    assert raw_a == raw_b


def test_h11(tmp_path):
    """File-only healthy control remains successful and byte-identical across rebuilds."""
    doc1, raw1 = _run_env(tmp_path, "h11a")
    doc2, raw2 = _run_env(tmp_path, "h11b")
    assert raw1 == raw2
    c1 = _control(doc1)
    c2 = _control(doc2)
    assert c1["exit_code"] == 0 and c2["exit_code"] == 0
    assert c1["open_ok"] and c2["open_ok"]
    assert not c1["rejected"] and not c2["rejected"]
    assert doc1["summary"]["control_stable"] and doc2["summary"]["control_stable"]


def test_h12(tmp_path):
    """Deliberately invalid fixtures remain rejected; report stays consistent."""
    doc1, raw1 = _run_env(tmp_path, "h12a")
    doc2, raw2 = _run_env(tmp_path, "h12b")
    b1 = _reject(doc1)
    b2 = _reject(doc2)
    assert b1["rejected"] and b2["rejected"]
    assert b1["exit_code"] != 0
    assert doc1["summary"]["reject_stable"]
    assert raw1 == raw2
    assert _digest_ok(raw1, doc1)
