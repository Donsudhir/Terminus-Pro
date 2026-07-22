import json
import os
import subprocess
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

import pytest

APP = Path("/app")
BINARY = APP / "bin" / "geomlab"

POINTS_A = [
    (11, (0, 0, 0)),
    (12, (7, 1, 2)),
    (13, (1, 8, 3)),
    (14, (2, 1, 9)),
    (15, (6, 5, 4)),
    (16, (-3, 4, 2)),
    (17, (3, -2, 5)),
]
POINTS_B = [
    (21, (-4, -3, 1)),
    (22, (5, -2, 0)),
    (23, (-1, 6, 2)),
    (24, (2, 1, 8)),
    (25, (7, 4, 5)),
    (26, (-5, 3, 6)),
    (27, (4, -6, 3)),
    (28, (0, 2, -4)),
]
POINTS_C = [
    (31, (0, 0, 0)),
    (32, (9, 2, 4)),
    (33, (2, 7, 6)),
    (34, (3, 4, 10)),
    (35, (10, 6, 7)),
    (36, (-6, 5, 4)),
    (37, (7, -5, 6)),
]
VARIANTS = [
    ("base", 0, ((0, 0), (0, 0), (0, 0))),
    ("upper", 420, ((1, 500), (-3, 490), (5, 480))),
    ("lower", -420, ((-7, -300), (2, -310), (9, -320))),
]


@pytest.fixture(scope="session", autouse=True)
def compiled_pipeline():
    """Build the mixed-language executable once for the verifier session."""
    subprocess.run(
        [os.fspath(APP / "scripts" / "build.sh")],
        cwd=APP,
        check=True,
        text=True,
        capture_output=True,
        timeout=240,
    )
    assert BINARY.is_file()


def _determinant(matrix):
    total = 0
    size = len(matrix)
    for order in permutations(range(size)):
        inversions = sum(
            order[left] > order[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = 1
        for row, column in enumerate(order):
            term *= matrix[row][column]
        total += -term if inversions % 2 else term
    return total


def _orientation(a, b, c, d):
    matrix = [
        [a[axis] - d[axis] for axis in range(3)],
        [b[axis] - d[axis] for axis in range(3)],
        [c[axis] - d[axis] for axis in range(3)],
    ]
    return _determinant(matrix)


def _sphere(a, b, c, d, e):
    matrix = []
    for point in (a, b, c, d):
        row = [point[axis] - e[axis] for axis in range(3)]
        matrix.append(row + [sum(value * value for value in row)])
    return _determinant(matrix)


def _expected_cells(points):
    coordinates = [value for _, value in points]
    identities = [identity for identity, _ in points]
    result = []
    for indices in combinations(range(len(points)), 4):
        ordered = list(indices)
        sign = _orientation(*(coordinates[index] for index in ordered))
        assert sign != 0
        if sign < 0:
            ordered[0], ordered[1] = ordered[1], ordered[0]
        occupied = False
        for query in range(len(points)):
            if query in indices:
                continue
            relation = _sphere(
                *(coordinates[index] for index in ordered),
                coordinates[query],
            )
            assert relation != 0
            if relation > 0:
                occupied = True
                break
        if not occupied:
            result.append(tuple(sorted(identities[index] for index in indices)))
    return sorted(result)


def _face(row, opposite):
    return tuple(sorted(value for index, value in enumerate(row) if index != opposite))


def _expected_adjacency(cells):
    owners = {}
    for cell_index, row in enumerate(cells):
        for opposite in range(4):
            owners.setdefault(_face(row, opposite), []).append((cell_index, opposite))
    result = [[-1, -1, -1, -1] for _ in cells]
    for entries in owners.values():
        assert len(entries) in (1, 2)
        if len(entries) == 2:
            (left, left_face), (right, right_face) = entries
            result[left][left_face] = right
            result[right][right_face] = left
    return result


def _topology(points, cells):
    edges = set()
    faces = Counter()
    for row in cells:
        for edge in combinations(row, 2):
            edges.add(tuple(sorted(edge)))
        for face in combinations(row, 3):
            faces[tuple(sorted(face))] += 1
    assert all(value in (1, 2) for value in faces.values())
    boundary = sum(value == 1 for value in faces.values())
    return {
        "vertices": len(points),
        "edges": len(edges),
        "faces": len(faces),
        "cells": len(cells),
        "boundary_faces": boundary,
        "euler": len(points) - len(edges) + len(faces) - len(cells),
    }


def _dyadic(value):
    if isinstance(value, tuple):
        return f"{value[0]}@{value[1]}"
    return f"{value}@0"


def _source(families):
    lines = []
    for family in families:
        lines.append(f"family {family['name']}")
        for identity, xyz in family["points"]:
            lines.append(
                f"point {identity} {_dyadic(xyz[0])} {_dyadic(xyz[1])} {_dyadic(xyz[2])}"
            )
        for name, scale, shift in family["variants"]:
            lines.append(
                f"variant {name} {scale} {_dyadic(shift[0])} {_dyadic(shift[1])} {_dyadic(shift[2])}"
            )
        lines.append("end")
    return "\n".join(lines) + "\n"


def _run_case(tmp_path, families, label, binary=BINARY):
    source = tmp_path / f"{label}.geom"
    output = tmp_path / f"{label}.json"
    source.write_text(_source(families), encoding="utf-8")
    environment = os.environ.copy()
    environment["GEOMLAB_INPUT"] = str(source)
    environment["GEOMLAB_OUTPUT"] = str(output)
    command = [os.fspath(binary)]
    completed = subprocess.run(
        command,
        cwd=APP,
        env=environment,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr
    raw = output.read_text(encoding="utf-8")
    return json.loads(raw), raw


def _run_bundled(tmp_path, label):
    output = tmp_path / f"{label}.json"
    environment = os.environ.copy()
    environment.pop("GEOMLAB_INPUT", None)
    environment["GEOMLAB_OUTPUT"] = str(output)
    completed = subprocess.run(
        [os.fspath(BINARY)],
        cwd=APP,
        env=environment,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stderr
    raw = output.read_text(encoding="utf-8")
    return json.loads(raw), raw


def _batch(document, family, variant):
    matches = [
        item
        for item in document["batches"]
        if item["identity"]["family"] == family and item["identity"]["variant"] == variant
    ]
    assert len(matches) == 1
    return matches[0]


def _assert_batch(item, points):
    expected = _expected_cells(points)
    actual = item["cells"]
    coordinates = dict(points)
    assert item["identity"]["point_ids"] == [identity for identity, _ in points]
    assert sorted(tuple(sorted(row)) for row in actual) == expected
    assert all(_orientation(*(coordinates[identity] for identity in row)) > 0 for row in actual)
    assert item["adjacency"] == _expected_adjacency(actual)
    assert item["orientation"] == {"positive": len(actual), "negative": 0, "zero": 0}
    assert item["validity"] == {
        "checks": len(actual) * (len(points) - 4),
        "violations": 0,
    }
    assert item["topology"] == _topology(points, actual)


def _assert_unoriented_batch(item, points):
    expected = sorted(tuple(sorted(row)) for row in _expected_cells(points))
    actual = sorted(tuple(sorted(row)) for row in item["cells"])
    assert item["identity"]["point_ids"] == [identity for identity, _ in points]
    assert actual == expected


def _probe_series(binary, exact, terms):
    command = [os.fspath(binary), "--inspect-series", str(exact)]
    command.extend(format(term, ".17g") for term in terms)
    completed = subprocess.run(command, cwd=APP, text=True, capture_output=True, check=True, timeout=30)
    return json.loads(completed.stdout)


def _probe_state(binary, raw):
    command = [os.fspath(binary), "--inspect-status", str(raw)]
    completed = subprocess.run(
        command,
        cwd=APP,
        text=True,
        capture_output=True,
        check=True,
        timeout=30,
    )
    return json.loads(completed.stdout)


def _binary_sign(values):
    ratios = [value.as_integer_ratio() for value in values]
    denominator = max(item[1] for item in ratios)
    total = sum(numerator * (denominator // divisor) for numerator, divisor in ratios)
    return (total > 0) - (total < 0)


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


def test_r01():
    """Cancellation must refine; a well-conditioned series must still certify."""
    cancel = [1.0e16, 1.0, -1.0e16, -0.5]
    exact_cancel = _binary_sign(cancel)
    assert exact_cancel == 1
    row = _probe_series(BINARY, exact_cancel, cancel)
    assert row["raw"] == 2
    assert row["final"] == exact_cancel

    stable = [1.0, 2.0, 3.0, 4.0]
    exact_stable = _binary_sign(stable)
    assert exact_stable == 1
    stable_row = _probe_series(BINARY, exact_stable, stable)
    assert stable_row["raw"] == exact_stable
    assert stable_row["final"] == exact_stable


def test_r02():
    """Opposite-polarity cancellation refines; well-conditioned negative certifies."""
    cancel = [-1.0e16, -1.0, 1.0e16, 0.5] + [value for _ in range(10) for value in (8.0, -8.0)]
    exact_cancel = _binary_sign(cancel)
    assert exact_cancel == -1
    row = _probe_series(BINARY, exact_cancel, cancel)
    assert row["raw"] == 2
    assert row["final"] == exact_cancel

    stable = [-5.0, -1.0, -2.0]
    exact_stable = _binary_sign(stable)
    assert exact_stable == -1
    stable_row = _probe_series(BINARY, exact_stable, stable)
    assert stable_row["raw"] == exact_stable
    assert stable_row["final"] == exact_stable


def test_r03():
    """The foreign refinement state remains distinct when it crosses the host boundary."""
    row = _probe_state(BINARY, 2)
    assert row["raw"] == 2
    assert row["refine"] is True
    assert row["mapped"] not in (-1, 1)


def test_r04(tmp_path):
    """Generated positive-scale and translated views retain one canonical complex."""
    family = {"name": "generated_a", "points": POINTS_A, "variants": VARIANTS}
    document, _ = _run_case(tmp_path, [family], "r04")
    cells = []
    for name, _, _ in VARIANTS:
        item = _batch(document, "generated_a", name)
        _assert_unoriented_batch(item, POINTS_A)
        cells.append(item["cells"])
    assert cells[0] == cells[1] == cells[2]


def test_r05(tmp_path):
    """Independent family results do not depend on mixed-scale source ordering."""
    first = {"name": "order_a", "points": POINTS_A, "variants": VARIANTS}
    second = {"name": "order_b", "points": POINTS_B, "variants": list(reversed(VARIANTS))}
    left, left_raw = _run_case(tmp_path, [first, second], "r05_left")
    right, right_raw = _run_case(tmp_path, [second, first], "r05_right")
    assert left == right
    assert left_raw == right_raw


def test_r06():
    """Native-to-host chain refines cancellations and certifies stable signs."""
    positive = [1.0e16, 1.0, -1.0e16, -0.5]
    negative = [-1.0e16, -1.0, 1.0e16, 0.5]
    pos = _probe_series(BINARY, 1, positive)
    neg = _probe_series(BINARY, -1, negative)
    assert pos["raw"] == 2 and pos["final"] == 1
    assert neg["raw"] == 2 and neg["final"] == -1
    assert _probe_series(BINARY, 1, [2.0, 3.0, 5.0])["raw"] == 1
    assert _probe_series(BINARY, -1, [-2.0, -3.0, -5.0])["raw"] == -1


def test_r07(tmp_path):
    """A refined run reaches the analysis layer and retains its oriented row contract."""
    assert _probe_state(BINARY, 2)["refine"] is True
    family = {"name": "analysis_b", "points": POINTS_B, "variants": [VARIANTS[0]]}
    document, _ = _run_case(tmp_path, [family], "r07")
    _assert_batch(_batch(document, "analysis_b", "base"), POINTS_B)


def test_r08(tmp_path):
    """Every emitted row has positive exact handedness after canonical ordering."""
    family = {"name": "hand_a", "points": POINTS_A, "variants": [VARIANTS[0]]}
    document, _ = _run_case(tmp_path, [family], "r08")
    item = _batch(document, "hand_a", "base")
    coordinates = dict(POINTS_A)
    assert item["cells"]
    for row in item["cells"]:
        assert _orientation(*(coordinates[identity] for identity in row)) > 0
    assert item["orientation"]["negative"] == 0
    assert item["orientation"]["zero"] == 0


def test_r09(tmp_path):
    """Face links, incidence totals, and Euler accounting agree with emitted rows."""
    family = {"name": "links_b", "points": POINTS_B, "variants": [VARIANTS[0]]}
    document, _ = _run_case(tmp_path, [family], "r09")
    item = _batch(document, "links_b", "base")
    _assert_batch(item, POINTS_B)


def test_r10(tmp_path):
    """A clean strict build preserves certified decisions and report semantics."""
    build_dir = tmp_path / f"{tmp_path.name}-build"
    bin_dir = tmp_path / f"{tmp_path.name}-bin"
    subprocess.run(
        [
            os.fspath(APP / "scripts" / "strict-build.sh"),
            os.fspath(build_dir),
            os.fspath(bin_dir),
        ],
        cwd=APP,
        text=True,
        capture_output=True,
        check=True,
        timeout=240,
    )
    strict = bin_dir / "geomlab"
    family = {"name": "strict_a", "points": POINTS_A, "variants": VARIANTS}
    default_document, _ = _run_case(tmp_path, [family], "r10_default")
    strict_document, _ = _run_case(tmp_path, [family], "r10_strict", strict)
    assert strict_document == default_document
    terms = [1.0e16, 1.0, -1.0e16, -0.5]
    cancel = _probe_series(strict, 1, terms)
    assert cancel["raw"] == 2 and cancel["final"] == 1
    assert _probe_series(strict, 1, [1.0, 4.0, 5.0])["raw"] == 1
    assert _probe_state(strict, 2)["refine"] is True


def test_r11(tmp_path):
    """Repeated multi-family runs are byte-stable and malformed input fails closed."""
    first = {"name": "repeat_a", "points": POINTS_A, "variants": VARIANTS}
    second = {"name": "repeat_b", "points": POINTS_B, "variants": VARIANTS}
    document, left = _run_case(tmp_path, [first, second], "r11_left")
    repeated, right = _run_case(tmp_path, [first, second], "r11_right")
    for name, _, _ in VARIANTS:
        _assert_unoriented_batch(_batch(document, "repeat_a", name), POINTS_A)
        _assert_unoriented_batch(_batch(document, "repeat_b", name), POINTS_B)
    assert repeated == document
    assert left == right
    bundled, _ = _run_bundled(tmp_path, "r11_bundled")
    bundled_families = {
        "aurora": (POINTS_A, ("base", "upper", "lower")),
        "meridian": (POINTS_B, ("base", "far", "near")),
        "prism": (POINTS_C, ("base", "raised", "reduced")),
    }
    assert len(bundled["batches"]) == 9
    for family, (points, variants) in bundled_families.items():
        for name in variants:
            _assert_unoriented_batch(_batch(bundled, family, name), points)
    malformed = tmp_path / f"{tmp_path.name}-malformed.geom"
    output = tmp_path / f"{tmp_path.name}-malformed.json"
    malformed.write_text("family bad\npoint 1 0@0 0@0 0@0\nend\n", encoding="utf-8")
    environment = os.environ.copy()
    environment["GEOMLAB_INPUT"] = str(malformed)
    environment["GEOMLAB_OUTPUT"] = str(output)
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


def test_r12(tmp_path):
    """Transformed canonical output and its reproducibility digest stay coherent."""
    family = {"name": "digest_a", "points": POINTS_A, "variants": VARIANTS}
    document, raw = _run_case(tmp_path, [family], "r12")
    cells = []
    for name, _, _ in VARIANTS:
        item = _batch(document, "digest_a", name)
        _assert_batch(item, POINTS_A)
        cells.append(item["cells"])
    assert cells[0] == cells[1] == cells[2]
    _assert_digest(document, raw)
