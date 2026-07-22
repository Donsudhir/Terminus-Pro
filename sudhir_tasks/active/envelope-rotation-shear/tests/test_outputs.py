from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
cases = __import__("case_factory")


def teardown_module() -> None:
    cases.cleanup_local()


def _pairs() -> list[tuple[str, str]]:
    return [
        (row["item"]["service"], row["item"]["secret"])
        for row in cases.catalog()
    ]


def _read(pair: tuple[str, str], *, check: bool = True):
    return cases.run_cli("get", *pair, check=check)


def test_e01() -> None:
    """Checks one isolated public transition and its neighboring control."""
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first, third)
    control = cases.digest_file(third)
    cases.run_cli("maintain")
    assert _read(first).stdout.strip() == cases.value_for(*first)
    assert _read(third).stdout.strip() == cases.value_for(*third)
    assert cases.digest_file(third) == control


def test_e02() -> None:
    """Checks a neutral set of public reads created for this case."""
    cases.reset()
    cases.retain()
    pairs = cases.generated_pairs(5, "elm")
    for pair in pairs:
        cases.add_case(*pair)
    for pair in pairs:
        assert _read(pair).stdout.strip() == cases.value_for(*pair)


def test_e03() -> None:
    """Checks matching reads and one mismatched placement."""
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first, third)
    assert _read(first).stdout.strip() == cases.value_for(*first)
    assert _read(third).stdout.strip() == cases.value_for(*third)
    cases.substitute(first, third)
    assert _read(first, check=False).returncode != 0


def test_e04() -> None:
    """Checks one reset and recovery through the public workflow."""
    cases.reset()
    _, second, _ = _pairs()
    cases.retain(second)
    cases.run_cli("recover")
    assert _read(second).stdout.strip() == cases.value_for(*second)


def test_e05() -> None:
    """Checks exact repeated-run stability over an isolated live set."""
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first, third)
    cases.run_cli("maintain")
    once = cases.digest_tree()
    cases.run_cli("maintain")
    assert cases.digest_tree() == once


def test_e06() -> None:
    """Checks a wider neutral matrix of public identities."""
    cases.reset()
    cases.retain()
    pairs = cases.generated_pairs(14, "pine")
    for pair in pairs:
        cases.add_case(*pair)
    observed = {_read(pair).stdout.strip() for pair in pairs}
    wanted = {cases.value_for(*pair) for pair in pairs}
    assert observed == wanted
    assert len(observed) == len(pairs)


def test_e07() -> None:
    """Checks refusal under two independent protected-input changes."""
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first)
    cases.tamper(first)
    assert cases.run_cli("audit", check=False).returncode != 0
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first, third)
    cases.substitute(first, third)
    assert cases.run_cli("audit", check=False).returncode != 0


def test_e08() -> None:
    """Checks the public report and preservation around one recovery."""
    cases.reset()
    _, second, third = _pairs()
    cases.retain(second, third)
    control = cases.digest_file(third)
    cases.run_cli("recover")
    report = cases.report()
    assert set(report) == {"recovered"}
    assert report["recovered"] == [
        {"service": second[0], "secret": second[1]}
    ]
    assert set(report["recovered"][0]) == {"service", "secret"}
    assert _read(second).stdout.strip() == cases.value_for(*second)
    assert cases.digest_file(third) == control


def test_e09() -> None:
    """Checks the complete public workflow after an independent reset."""
    cases.reset()
    _, second, third = _pairs()
    cases.retain(second, third)
    control = cases.digest_file(third)
    cases.run_cli("recover")
    assert _read(second).stdout.strip() == cases.value_for(*second)
    cases.run_cli("maintain")
    once = cases.digest_tree()
    cases.run_cli("maintain")
    assert cases.digest_tree() == once
    assert cases.digest_file(third) == control
    cases.substitute(third, second)
    assert cases.run_cli("audit", check=False).returncode != 0


def test_e10() -> None:
    """Checks several generated identities through one recovery."""
    cases.reset()
    cases.retain()
    pairs = cases.generated_pairs(4, "cedar")
    for pair in pairs:
        cases.add_case(*pair, damage=True, history=True)
    cases.run_cli("recover")
    recovered = {
        (item["service"], item["secret"]) for item in cases.report()["recovered"]
    }
    assert recovered == set(pairs)
    for pair in pairs:
        assert _read(pair).stdout.strip() == cases.value_for(*pair)


def test_e11() -> None:
    """Checks strict public access without invoking recovery."""
    cases.reset()
    first, _, third = _pairs()
    cases.retain(first, third)
    assert cases.run_cli("audit").returncode == 0
    cases.substitute(third, first)
    assert _read(third, check=False).returncode != 0
    assert cases.run_cli("audit", check=False).returncode != 0


def test_e12() -> None:
    """Checks generated identities across two later transitions."""
    cases.reset()
    cases.retain()
    pairs = cases.generated_pairs(6, "birch")
    epoch = cases.active_epoch() - 1
    for pair in pairs:
        cases.add_case(*pair, epoch=epoch)
    cases.run_cli("maintain")
    once = cases.digest_tree()
    cases.run_cli("maintain")
    assert cases.digest_tree() == once
    for pair in pairs:
        assert _read(pair).stdout.strip() == cases.value_for(*pair)
