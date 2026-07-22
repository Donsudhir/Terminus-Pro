import json
import os
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
BINARY = APP / "bin" / "senslab"

AURORA_TERMS = [
    (1, 1, 1.0),
    (1, 2, 2.0),
    (2, 1, 1.0),
    (2, 2, 3.0),
    (2, 3, 1.0),
    (3, 3, 1.0),
    (3, 4, 4.0),
]
MERIDIAN_TERMS = [
    (1, 1, 2.0),
    (1, 2, 1.0),
    (2, 1, 1.0),
    (2, 2, 2.0),
    (2, 3, 3.0),
    (3, 2, 1.0),
    (3, 3, 1.0),
    (3, 4, 2.0),
    (4, 1, 1.0),
    (4, 5, 1.0),
]
PRISM_TERMS = [
    (1, 1, 1.5),
    (1, 2, 0.5),
    (2, 1, 2.0),
    (2, 2, 1.0),
    (2, 3, 2.0),
    (3, 3, 1.0),
    (3, 4, 3.0),
]
# Dense overlapping support — incomplete group conflict checks tend to fail here.
CLUSTER_TERMS = [
    (1, 1, 1.0),
    (1, 2, 1.0),
    (1, 3, 1.0),
    (2, 2, 2.0),
    (2, 3, 1.0),
    (2, 4, 1.0),
    (3, 1, 1.0),
    (3, 4, 3.0),
    (3, 5, 1.0),
    (4, 3, 1.0),
    (4, 5, 2.0),
]


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


def _row_weight(row_zero_based: int) -> float:
    """Match native/quill.c quill_tint diagonal participation (0-based i)."""
    i = float(row_zero_based)
    return 1.0 + 0.5 * i + 0.05 * i * i


def _companion_direction(cols: int):
    if cols == 4:
        return [1.0, 0.5, 0.25, 2.0]
    if cols == 5:
        return [1.0, 0.5, 0.25, 2.0, 1.5]
    return [1.0 + 0.1 * idx for idx in range(cols)]


def _min_probe_groups(cols: int, terms) -> int:
    """Exact chromatic number of the column conflict graph (small n)."""
    from collections import defaultdict
    import itertools

    rows = defaultdict(set)
    for eq, col, _coeff in terms:
        rows[eq].add(col - 1)
    adj = [set() for _ in range(cols)]
    for members in rows.values():
        for a in members:
            for b in members:
                if a != b:
                    adj[a].add(b)
    for colors in range(1, cols + 1):
        for assign in itertools.product(range(colors), repeat=cols):
            if all(assign[i] != assign[j] for i in range(cols) for j in adj[i]):
                return colors
    return cols


def _expected_jacobian(rows, cols, terms):
    dense = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for eq, col, coeff in terms:
        dense[eq - 1][col - 1] += coeff * _row_weight(eq - 1)
    entries = []
    for row in range(rows):
        for col in range(cols):
            if dense[row][col] != 0.0:
                entries.append((row, col, dense[row][col]))
    return dense, entries


def _direction(rows, cols, terms, direction):
    dense, _ = _expected_jacobian(rows, cols, terms)
    out = [0.0 for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            out[row] += dense[row][col] * direction[col]
    return out


def _source(families):
    lines = []
    for family in families:
        lines.append(f"family {family['name']}")
        lines.append(f"dim {family['dim']}")
        lines.append(f"eq {family['rows']}")
        for eq, col, coeff in family["terms"]:
            lines.append(f"term {eq} {col} {coeff}")
        lines.append("base " + " ".join(str(v) for v in family["base"]))
        for tag in family["tags"]:
            lines.append(
                "tag "
                + tag["name"]
                + f" {tag['scale']} "
                + " ".join(str(v) for v in tag["shift"])
            )
        for perm in family.get("perms", []):
            lines.append("perm " + perm["name"] + " " + " ".join(str(v) for v in perm["order"]))
        lines.append("end")
    return "\n".join(lines) + "\n"


def _run_case(tmp_path, families, label, binary=BINARY):
    source = tmp_path / f"{label}.resid"
    output = tmp_path / f"{label}.json"
    source.write_text(_source(families), encoding="utf-8")
    env = os.environ.copy()
    env["SENSLAB_INPUT"] = str(source)
    env["SENSLAB_OUTPUT"] = str(output)
    completed = subprocess.run(
        [os.fspath(binary)],
        cwd=APP,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr
    raw = output.read_text(encoding="utf-8")
    return json.loads(raw), raw


def _run_bundled(tmp_path, label):
    output = tmp_path / f"{label}.json"
    env = os.environ.copy()
    env.pop("SENSLAB_INPUT", None)
    env["SENSLAB_OUTPUT"] = str(output)
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


def _run(subcommand):
    completed = subprocess.run(
        [os.fspath(BINARY), subcommand] if subcommand else [os.fspath(BINARY)],
        cwd=APP,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout


def _item(document, family, tag):
    matches = [
        run
        for run in document["runs"]
        if run["label"]["family"] == family and run["label"]["tag"] == tag
    ]
    assert len(matches) == 1
    return matches[0]


def _pairs(item):
    values = item["values"]
    indices = item["indices"]
    out = {}
    for pos in range(0, len(indices), 2):
        key = (indices[pos], indices[pos + 1])
        out[key] = values[pos // 2]
    return out


def _fnv1a(payload):
    value = 0xCBF29CE484222325
    for byte in payload:
        value ^= byte
        value = (value * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return value


def _assert_digest(document, raw):
    digest = document["digest"]
    suffix = f',"digest":"{digest}"}}\n'
    assert raw.endswith(suffix)
    payload = (raw[: -len(suffix)] + "}").encode()
    assert digest == f"{_fnv1a(payload):016x}"


def _affine_state(base, scale, shift):
    return [value * scale + delta for value, delta in zip(base, shift)]


def _residual_l2(rows, cols, terms, state):
    dense, _ = _expected_jacobian(rows, cols, terms)
    residual = [
        sum(dense[row][col] * state[col] for col in range(cols)) for row in range(rows)
    ]
    return sum(value * value for value in residual) ** 0.5


def _expected_span(rows, cols, terms, base, scale, shift, step_floor=1.0e-8, step_gain=0.5):
    """Match host gauge: ref = ||r||_2, step = max(ref*1e-6, floor) then *gain floor."""
    state = _affine_state(base, scale, shift)
    reference = _residual_l2(rows, cols, terms, state)
    if reference <= 0.0 or reference != reference or reference == float("inf"):
        reference = 1.0
    step = max(reference * 1.0e-6, step_floor)
    step = max(step * step_gain, step_floor)
    return reference, step


def _assert_ids(item, cols):
    assert item["ids"] == list(range(1, cols + 1))


def test_k01(tmp_path):
    """Permutation-equivalent batches agree on packed support and values."""
    # Column remap: new_index = inv[old_index] for swap 0↔1, 2↔3.
    inv = [1, 0, 3, 2]
    perm_terms = [(eq, inv[col - 1] + 1, coeff) for eq, col, coeff in AURORA_TERMS]
    base_family = {
        "name": "perm_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [1.0, 2.0, 3.0, 4.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    perm_family = {
        "name": "perm_a",
        "dim": 4,
        "rows": 3,
        "terms": perm_terms,
        "base": [2.0, 1.0, 4.0, 3.0],
        "tags": [{"name": "swap", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    _, entries = _expected_jacobian(3, 4, AURORA_TERMS)
    base_doc, _ = _run_case(tmp_path, [base_family], "k01_base")
    perm_doc, _ = _run_case(tmp_path, [perm_family], "k01_perm")
    base_pairs = _pairs(_item(base_doc, "perm_a", "base"))
    perm_pairs = _pairs(_item(perm_doc, "perm_a", "swap"))
    expected_keys = {(row, col) for row, col, _ in entries}
    assert set(base_pairs) == expected_keys
    for row, col, value in entries:
        assert base_pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)
    for (row, col), value in base_pairs.items():
        assert perm_pairs[(row, inv[col])] == pytest.approx(value, rel=0, abs=1e-4)


def test_k02(tmp_path):
    """Held-out column probes match retained packed entries."""
    family = {
        "name": "probe_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [1.0, 2.0, 3.0, 4.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    document, _ = _run_case(tmp_path, [family], "k02")
    item = _item(document, "probe_a", "base")
    _, entries = _expected_jacobian(3, 4, AURORA_TERMS)
    pairs = _pairs(item)
    direction = _companion_direction(4)
    expected = _direction(3, 4, AURORA_TERMS, direction)
    assert item["products"] == pytest.approx(expected, rel=0, abs=1e-4)
    for row, col, value in entries:
        assert pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)

    dense = {
        "name": "probe_cluster",
        "dim": 5,
        "rows": 4,
        "terms": CLUSTER_TERMS,
        "base": [1.0, 1.5, 2.0, 2.5, 1.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0, 0.0]}],
    }
    dense_doc, _ = _run_case(tmp_path, [dense], "k02_cluster")
    dense_item = _item(dense_doc, "probe_cluster", "base")
    _, dense_entries = _expected_jacobian(4, 5, CLUSTER_TERMS)
    dense_pairs = _pairs(dense_item)
    dense_direction = _companion_direction(5)
    dense_expected = _direction(4, 5, CLUSTER_TERMS, dense_direction)
    assert set(dense_pairs) == {(row, col) for row, col, _ in dense_entries}
    for row, col, value in dense_entries:
        assert dense_pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)
    assert dense_item["products"] == pytest.approx(dense_expected, rel=0, abs=1e-4)
    assert dense_item["ledger"]["groups"] == _min_probe_groups(5, CLUSTER_TERMS)
    assert item["ledger"]["groups"] == _min_probe_groups(4, AURORA_TERMS)


def test_k03():
    """Resume-from-saved-plan matches cold start."""
    payload = json.loads(_run("--mode-echo"))
    assert payload["same"] is True


def test_k04(tmp_path):
    """Scale-equivalent batch preserves directional products and operator sensitivities."""
    family = {
        "name": "scale_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [1.0, 2.0, 3.0, 4.0],
        "tags": [
            {"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]},
            {"name": "wide", "scale": 2.0, "shift": [0.0, 0.0, 0.0, 0.0]},
            {"name": "narrow", "scale": 0.5, "shift": [0.0, 0.0, 0.0, 0.0]},
        ],
    }
    document, _ = _run_case(tmp_path, [family], "k04")
    direction = _companion_direction(4)
    expected = _direction(3, 4, AURORA_TERMS, direction)
    _, entries = _expected_jacobian(3, 4, AURORA_TERMS)
    base_item = _item(document, "scale_a", "base")
    wide_item = _item(document, "scale_a", "wide")
    narrow_item = _item(document, "scale_a", "narrow")
    assert base_item["products"] == pytest.approx(expected, rel=0, abs=1e-4)
    assert wide_item["products"] == pytest.approx(expected, rel=0, abs=1e-4)
    assert narrow_item["products"] == pytest.approx(expected, rel=0, abs=1e-4)
    base_pairs = _pairs(base_item)
    wide_pairs = _pairs(wide_item)
    narrow_pairs = _pairs(narrow_item)
    assert set(base_pairs) == set(wide_pairs) == set(narrow_pairs)
    for row, col, value in entries:
        assert base_pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)
        assert wide_pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)
        assert narrow_pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)


def test_k05(tmp_path):
    """Sequential mixed-scale batches do not inherit prior magnitude."""
    family_a = {
        "name": "order_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [1.0, 2.0, 3.0, 4.0],
        "tags": [{"name": "wide", "scale": 100.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    family_b = {
        "name": "order_b",
        "dim": 5,
        "rows": 4,
        "terms": MERIDIAN_TERMS,
        "base": [2.0, 1.0, 3.0, 2.0, 1.0],
        "tags": [{"name": "near", "scale": 0.01, "shift": [0.0, 0.0, 0.0, 0.0, 0.0]}],
    }
    family_c = {
        "name": "order_c",
        "dim": 4,
        "rows": 3,
        "terms": PRISM_TERMS,
        "base": [0.5, 1.5, 2.5, 1.0],
        "tags": [{"name": "mid", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    document, _ = _run_case(tmp_path, [family_a, family_b, family_c], "k05")
    near = _item(document, "order_b", "near")
    wide = _item(document, "order_a", "wide")
    mid = _item(document, "order_c", "mid")
    _assert_ids(wide, 4)
    _assert_ids(near, 5)
    _assert_ids(mid, 4)
    wide_ref, wide_step = _expected_span(
        3, 4, AURORA_TERMS, family_a["base"], 100.0, family_a["tags"][0]["shift"]
    )
    near_ref, near_step = _expected_span(
        4, 5, MERIDIAN_TERMS, family_b["base"], 0.01, family_b["tags"][0]["shift"]
    )
    mid_ref, mid_step = _expected_span(
        3, 4, PRISM_TERMS, family_c["base"], 1.0, family_c["tags"][0]["shift"]
    )
    assert wide["span_info"]["ref"] == pytest.approx(wide_ref, rel=0, abs=1e-6)
    assert wide["span_info"]["step"] == pytest.approx(wide_step, rel=0, abs=1e-12)
    assert near["span_info"]["ref"] == pytest.approx(near_ref, rel=0, abs=1e-6)
    assert near["span_info"]["step"] == pytest.approx(near_step, rel=0, abs=1e-12)
    assert mid["span_info"]["ref"] == pytest.approx(mid_ref, rel=0, abs=1e-6)
    assert mid["span_info"]["step"] == pytest.approx(mid_step, rel=0, abs=1e-12)
    assert near["span_info"]["ref"] < wide["span_info"]["ref"] / 10.0
    assert near["span_info"]["step"] <= wide["span_info"]["step"] / 100.0
    assert mid["span_info"]["ref"] < wide["span_info"]["ref"] / 10.0


def test_k06(tmp_path):
    """Combined permutation and resume parity."""
    payload = json.loads(_run("--mode-echo"))
    family = {
        "name": "combo_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [2.0, 1.0, 4.0, 3.0],
        "tags": [{"name": "swap", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    document, _ = _run_case(tmp_path, [family], "k06")
    _, entries = _expected_jacobian(3, 4, AURORA_TERMS)
    pairs = _pairs(_item(document, "combo_a", "swap"))
    assert len(pairs) == len(entries)
    assert payload["same"] is True


def test_k07(tmp_path):
    """Packed layout agrees with audit support counts."""
    document, _ = _run_bundled(tmp_path, "k07")
    for run in document["runs"]:
        assert run["ledger"]["active"] == len(run["values"])
        assert run["ledger"]["total"] == run["dims"]["nnz"]
        assert len(run["indices"]) == 2 * len(run["values"])
        _assert_ids(run, run["dims"]["cols"])
    item = _item(document, "aurora", "base")
    pairs = _pairs(item)
    _, entries = _expected_jacobian(3, 4, AURORA_TERMS)
    assert len(pairs) == len(entries)
    for row, col, value in entries:
        assert pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-3)


def test_k08(tmp_path):
    """Unpack orientation preserves independent dense probes on retained indices."""
    family = {
        "name": "dense_b",
        "dim": 5,
        "rows": 4,
        "terms": MERIDIAN_TERMS,
        "base": [2.0, 1.0, 3.0, 2.0, 1.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0, 0.0]}],
    }
    document, _ = _run_case(tmp_path, [family], "k08")
    item = _item(document, "dense_b", "base")
    _, entries = _expected_jacobian(4, 5, MERIDIAN_TERMS)
    pairs = _pairs(item)
    direction = _companion_direction(5)
    expected = _direction(4, 5, MERIDIAN_TERMS, direction)
    for row, col, value in entries:
        assert pairs[(row, col)] == pytest.approx(value, rel=0, abs=1e-4)
    assert item["products"] == pytest.approx(expected, rel=0, abs=1e-4)
    assert item["ledger"]["groups"] == _min_probe_groups(5, MERIDIAN_TERMS)


def test_k09(tmp_path):
    """Summary fields agree with emitted packed structure and probe grouping."""
    document, _ = _run_bundled(tmp_path, "k09")
    expected_groups = {
        "aurora": _min_probe_groups(4, AURORA_TERMS),
        "meridian": _min_probe_groups(5, MERIDIAN_TERMS),
        "prism": _min_probe_groups(4, PRISM_TERMS),
    }
    for run in document["runs"]:
        assert run["ledger"]["groups"] >= 1
        assert run["ledger"]["total"] == run["ledger"]["active"]
        assert run["dims"]["nnz"] == run["ledger"]["total"]
        family = run["label"]["family"]
        if family in expected_groups:
            assert run["ledger"]["groups"] == expected_groups[family]


def test_k10(tmp_path):
    """Reordered execution of the same family is deterministic."""
    family_a = {
        "name": "repeat_a",
        "dim": 4,
        "rows": 3,
        "terms": AURORA_TERMS,
        "base": [1.0, 2.0, 3.0, 4.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]}],
    }
    family_b = {
        "name": "repeat_b",
        "dim": 5,
        "rows": 4,
        "terms": MERIDIAN_TERMS,
        "base": [2.0, 1.0, 3.0, 2.0, 1.0],
        "tags": [{"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0, 0.0]}],
    }
    left, left_raw = _run_case(tmp_path, [family_a, family_b], "k10_left")
    right, right_raw = _run_case(tmp_path, [family_b, family_a], "k10_right")
    assert len(left["runs"]) == 2
    assert len(right["runs"]) == 2
    labels = [(run["label"]["family"], run["label"]["tag"]) for run in left["runs"]]
    assert labels == sorted(labels)
    assert left == right
    assert left_raw == right_raw
    _assert_ids(_item(left, "repeat_a", "base"), 4)
    _assert_ids(_item(left, "repeat_b", "base"), 5)


def test_k11(tmp_path):
    """Scale summary matches the active batch, not a prior cache."""
    family = {
        "name": "span_a",
        "dim": 4,
        "rows": 3,
        "terms": PRISM_TERMS,
        "base": [0.5, 1.5, 2.5, 1.0],
        "tags": [
            {"name": "raised", "scale": 50.0, "shift": [0.0, 0.0, 0.0, 0.0]},
            {"name": "reduced", "scale": 0.02, "shift": [0.0, 0.0, 0.0, 0.0]},
        ],
    }
    document, _ = _run_case(tmp_path, [family], "k11")
    raised = _item(document, "span_a", "raised")
    reduced = _item(document, "span_a", "reduced")
    _assert_ids(raised, 4)
    _assert_ids(reduced, 4)
    raised_ref, raised_step = _expected_span(
        3, 4, PRISM_TERMS, family["base"], 50.0, family["tags"][0]["shift"]
    )
    reduced_ref, reduced_step = _expected_span(
        3, 4, PRISM_TERMS, family["base"], 0.02, family["tags"][1]["shift"]
    )
    assert raised["span_info"]["ref"] == pytest.approx(raised_ref, rel=0, abs=1e-6)
    assert raised["span_info"]["step"] == pytest.approx(raised_step, rel=0, abs=1e-12)
    assert reduced["span_info"]["ref"] == pytest.approx(reduced_ref, rel=0, abs=1e-6)
    assert reduced["span_info"]["step"] == pytest.approx(reduced_step, rel=0, abs=1e-12)
    assert raised["span_info"]["ref"] > reduced["span_info"]["ref"]
    assert raised["span_info"]["step"] > reduced["span_info"]["step"]


def test_k12(tmp_path):
    """Byte-identical report across clean rebuilds after scale and unpack path."""
    family = {
        "name": "digest_a",
        "dim": 4,
        "rows": 3,
        "terms": PRISM_TERMS,
        "base": [0.5, 1.5, 2.5, 1.0],
        "tags": [
            {"name": "base", "scale": 1.0, "shift": [0.0, 0.0, 0.0, 0.0]},
            {"name": "raised", "scale": 4.0, "shift": [0.0, 0.0, 0.0, 0.0]},
        ],
    }
    document, raw = _run_case(tmp_path, [family], "k12_first")
    repeated, raw2 = _run_case(tmp_path, [family], "k12_second")
    assert document == repeated
    assert raw == raw2
    _assert_digest(document, raw)
    for run in document["runs"]:
        _assert_ids(run, 4)
        assert run["ledger"]["active"] == len(run["values"])


def test_k13(tmp_path):
    """Malformed input exits nonzero without writing a partial report."""
    malformed = tmp_path / "k13_bad.resid"
    output = tmp_path / "k13_bad.json"
    malformed.write_text("family bad\ndim not-a-number\nend\n", encoding="utf-8")
    environment = os.environ.copy()
    environment["SENSLAB_INPUT"] = str(malformed)
    environment["SENSLAB_OUTPUT"] = str(output)
    completed = subprocess.run(
        [os.fspath(BINARY)],
        cwd=APP,
        env=environment,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert completed.returncode != 0
    assert not output.exists()
