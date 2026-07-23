import json
import os
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
BINARY = APP / "bin" / "partlab"
SCHEMA_DOC = APP / "docs" / "parity-report-schema.md"


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


def _f64_le_bytes(value: float) -> bytes:
    array_mod = __import__("array")
    return array_mod.array("d", [float(value)]).tobytes()


def _fold_samples(values, order):
    h = 0xCBF29CE484222325
    for idx in order:
        raw = _f64_le_bytes(float(values[int(idx)]))
        for b in raw:
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


def _run_env(tmp_path, label, input_path=None):
    output = tmp_path / f"{label}.json"
    env = os.environ.copy()
    if input_path is None:
        env.pop("PARTLAB_INPUT", None)
    else:
        env["PARTLAB_INPUT"] = str(input_path)
    env["PARTLAB_OUTPUT"] = str(output)
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


def _item(document, family, tag, mode):
    matches = [
        row
        for row in document["runs"]
        if row["family"] == family and row["tag"] == tag and row["mode"] == mode
    ]
    assert len(matches) == 1, (family, tag, mode, matches)
    return matches[0]


def _families_source(order_families=None):
    blocks = {
        "alpha": "\n".join(
            [
                "family alpha",
                "nodes 5",
                "values 0.0 0.2 0.5 0.2 0.0",
                "order 0 2 4 1 3",
                "refine 8",
                "tag base",
                "end",
            ]
        ),
        "beta": "\n".join(
            [
                "family beta",
                "nodes 4",
                "values 0.1 0.4 0.4 0.1",
                "order 3 2 1 0",
                "refine 7",
                "tag base",
                "end",
            ]
        ),
        "gamma": "\n".join(
            [
                "family gamma",
                "nodes 6",
                "values 0.0 0.15 0.35 0.35 0.15 0.0",
                "order 1 3 5 0 2 4",
                "refine 9",
                "tag base",
                "end",
            ]
        ),
    }
    names = order_families or ["alpha", "beta", "gamma"]
    return "\n".join(blocks[n] for n in names) + "\n"


def _close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def _pairs_agree(doc):
    for family in ("alpha", "beta", "gamma"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        if twin["field_digest"] != mapped["field_digest"]:
            return False
        if twin["layout_token"] != mapped["layout_token"]:
            return False
    return True


def _folds_agree(doc):
    for row in doc["runs"]:
        if row["field_digest"] != _fold_samples(row["samples"], row["fold_order"]):
            return False
    return True


def test_m01(tmp_path):
    """After rank map change, fold checksums match the steady twin."""
    doc, _ = _run_env(tmp_path, "m01")
    for family in ("alpha", "beta", "gamma"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        assert twin["field_digest"] == mapped["field_digest"]
        assert twin["layout_token"] == mapped["layout_token"]


def test_m02(tmp_path):
    """Pointwise residual samples agree with the twin after map change."""
    doc, _ = _run_env(tmp_path, "m02")
    for family in ("alpha", "beta", "gamma"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        assert len(twin["residual_samples"]) == len(mapped["residual_samples"])
        for a, b in zip(twin["residual_samples"], mapped["residual_samples"]):
            assert _close(a, b, tol=1e-7)


def test_m03(tmp_path):
    """Sample contracts stay consistent with twin under stage metadata."""
    doc, _ = _run_env(tmp_path, "m03")
    for family in ("beta", "gamma"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        assert _close(twin["residual_norm"], mapped["residual_norm"], tol=1e-7)
        for a, b in zip(twin["residual_samples"], mapped["residual_samples"]):
            assert _close(a, b, tol=1e-7)
        assert mapped["reuse_mark"] != 0


def test_m04(tmp_path):
    """Emitted fold fields match an independent fold under fold_order."""
    doc, _ = _run_env(tmp_path, "m04")
    assert _folds_agree(doc)
    assert doc["summary"]["digest_match"]


def test_m05(tmp_path):
    """Sequential map-change families do not inherit prior stage identity."""
    doc, _ = _run_env(tmp_path, "m05")
    marks = [
        _item(doc, family, "base", "mapped")["reuse_mark"]
        for family in ("alpha", "beta", "gamma")
    ]
    assert marks[0] != 0 and marks[1] != 0 and marks[2] != 0
    assert len(set(marks)) == 3
    assert (marks[1] & marks[0]) != marks[0]
    assert (marks[2] & marks[1]) != marks[1]


def test_m06(tmp_path):
    """Combined twin parity under map change for pack and authority."""
    doc, _ = _run_env(tmp_path, "m06")
    assert _pairs_agree(doc)
    assert doc["summary"]["twin_agree"]
    for family in ("alpha", "beta"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        for a, b in zip(twin["residual_samples"], mapped["residual_samples"]):
            assert _close(a, b, tol=1e-7)


def test_m07(tmp_path):
    """Local-norm plausibility does not mask fold disagreement after repair."""
    doc, _ = _run_env(tmp_path, "m07")
    for family in ("alpha", "beta", "gamma"):
        twin = _item(doc, family, "base", "twin")
        mapped = _item(doc, family, "base", "mapped")
        assert mapped["iterations"] == twin["iterations"]
        assert mapped["residual_norm"] > 0.0
        assert mapped["residual_norm"] == mapped["residual_norm"]
        assert abs(mapped["residual_norm"]) != float("inf")
        assert twin["field_digest"] == mapped["field_digest"]


def test_m08(tmp_path):
    """Mapped trajectories fold under post-map ordering, not identity."""
    doc, _ = _run_env(tmp_path, "m08")
    for family in ("alpha", "beta", "gamma"):
        row = _item(doc, family, "base", "mapped")
        assert row["fold_order"]
        assert len(row["fold_order"]) == len(row["samples"])
        identity = list(range(len(row["fold_order"])))
        assert row["fold_order"] != identity
        assert row["field_digest"] == _fold_samples(row["samples"], row["fold_order"])
    assert _folds_agree(doc)


def test_m09(tmp_path):
    """Summary flags agree with emitted digests and schema_version."""
    doc, _ = _run_env(tmp_path, "m09")
    assert _pairs_agree(doc)
    assert _folds_agree(doc)
    assert doc["schema_version"] == _expected_schema_version()
    assert doc["summary"]["twin_agree"]
    assert doc["summary"]["digest_match"]


def test_m10(tmp_path):
    """Reordered family execution remains byte-identical for twin parity."""
    src_a = tmp_path / "order_a.case"
    src_b = tmp_path / "order_b.case"
    src_a.write_text(_families_source(["alpha", "beta", "gamma"]), encoding="utf-8")
    src_b.write_text(_families_source(["gamma", "beta", "alpha"]), encoding="utf-8")
    doc_a, raw_a = _run_env(tmp_path, "m10a", input_path=src_a)
    doc_b, raw_b = _run_env(tmp_path, "m10b", input_path=src_b)
    assert raw_a == raw_b
    assert doc_a["digest"] == doc_b["digest"]
    assert _pairs_agree(doc_a)


def test_m11(tmp_path):
    """Healthy steady control stays byte-identical with a clear reuse mark."""
    doc1, raw1 = _run_env(tmp_path, "m11a")
    doc2, raw2 = _run_env(tmp_path, "m11b")
    assert raw1 == raw2
    for family in ("alpha", "beta", "gamma"):
        control = _item(doc1, family, "base", "control")
        assert control["reuse_mark"] == 0
    assert doc1["summary"]["control_stable"]
    assert doc2["summary"]["control_stable"]


def test_m12(tmp_path):
    """Clean rebuild byte identity and report digest match the FNV contract."""
    doc1, raw1 = _run_env(tmp_path, "m12a")
    doc2, raw2 = _run_env(tmp_path, "m12b")
    assert raw1 == raw2
    assert doc1["digest"] == doc2["digest"]
    assert _folds_agree(doc1)
    marker = ',"digest":"'
    assert marker in raw1
    head, _, tail = raw1.rpartition(marker)
    digest_hex = tail[:16]
    assert tail[16:18] == '"}'
    payload = head + "}"
    assert _fnv1a64(payload.encode("utf-8")) == digest_hex
    assert digest_hex == doc1["digest"]
