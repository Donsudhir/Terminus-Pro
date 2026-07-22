import json
import subprocess
from pathlib import Path

APP = Path("/app")
REBUILD = APP / "bin" / "rebuild-forge"
FORGE = APP / "bin" / "forge"
LOCK = APP / "output" / "workspace.lock"
BUILD_REPORT = APP / "output" / "build-report.json"
ALPHA = ("alder", "1.1.0-alpha.1", "alder-preview-110a")
BETA = ("birch", "2.1.0", "birch-retained-210")

BASE_ROWS = [
    {
        "name": "alder",
        "version": "1.0.0",
        "code": 100,
        "source": "alder-main-100",
        "preview": False,
        "withdrawn": False,
        "needs": "birch:200:220:stable:200",
        "payload": "alder/1.0.0",
        "api": "alder_api",
    },
    {
        "name": "alder",
        "version": "1.1.0-alpha.1",
        "code": 110,
        "source": "alder-preview-110a",
        "preview": True,
        "withdrawn": False,
        "needs": "birch:200:220:stable:-",
        "payload": "alder/1.1.0-alpha.1",
        "api": "alpha_api",
    },
    {
        "name": "alder",
        "version": "1.1.0",
        "code": 120,
        "source": "alder-main-110",
        "preview": False,
        "withdrawn": False,
        "needs": "birch:200:220:stable:200",
        "payload": "alder/1.1.0",
        "api": "alder_api",
    },
    {
        "name": "birch",
        "version": "2.0.0",
        "code": 200,
        "source": "birch-main-200",
        "preview": False,
        "withdrawn": False,
        "needs": "elm:400:410:stable:400",
        "payload": "birch/2.0.0",
        "api": "birch_api",
    },
    {
        "name": "birch",
        "version": "2.1.0",
        "code": 210,
        "source": "birch-retained-210",
        "preview": False,
        "withdrawn": True,
        "needs": "elm:400:410:stable:400",
        "payload": "birch/2.1.0",
        "api": "beta_api",
    },
    {
        "name": "cedar",
        "version": "3.0.0",
        "code": 300,
        "source": "cedar-main-300",
        "preview": False,
        "withdrawn": False,
        "needs": "",
        "payload": "cedar/3.0.0",
        "api": "cedar_api",
    },
    {
        "name": "cedar",
        "version": "3.1.0",
        "code": 310,
        "source": "cedar-main-310",
        "preview": False,
        "withdrawn": False,
        "needs": "birch:200:220:stable:210;elm:400:410:stable:400",
        "payload": "cedar/3.1.0",
        "api": "cedar_next_api",
    },
    {
        "name": "elm",
        "version": "4.0.0",
        "code": 400,
        "source": "elm-main-400",
        "preview": False,
        "withdrawn": False,
        "needs": "",
        "payload": "elm/4.0.0",
        "api": "elm_api",
    },
]


def constraint(
    key: str,
    low: int,
    high: int,
    channel: str = "stable",
    exact: int | None = None,
) -> str:
    return f"{key}:{low}:{high}:{channel}:{exact if exact is not None else '-'}"


def generated(
    key: str,
    release: str,
    code: int,
    source: str,
    *,
    preview: bool,
    withdrawn: bool,
    api: str,
) -> dict:
    return {
        "name": key,
        "version": release,
        "code": code,
        "source": source,
        "preview": preview,
        "withdrawn": withdrawn,
        "needs": "",
        "payload": f"{key}/{release}",
        "api": api,
    }


def parse_constraint(value: str) -> dict:
    key, low, high, channel, exact = value.split(":")
    return {
        "key": key,
        "low": int(low),
        "high": int(high),
        "preview": channel == "preview",
        "exact": None if exact == "-" else int(exact),
    }


def accepts(specification: dict, row: dict) -> bool:
    return (
        row["name"] == specification["key"]
        and specification["low"] <= row["code"] < specification["high"]
        and (
            specification["exact"] is None
            or row["code"] == specification["exact"]
        )
        and (specification["preview"] or not row["preview"])
    )


def write_archive(root: Path, rows: list[dict]) -> Path:
    archive = root / "archive"
    archive.mkdir(parents=True)
    body = ",\n".join(
        json.dumps(row, separators=(",", ":"), sort_keys=False) for row in rows
    )
    (archive / "catalog.json").write_text(f"[\n{body}\n]\n", encoding="utf-8")
    for row in rows:
        payload = archive / row["payload"]
        (payload / "src").mkdir(parents=True)
        (payload / "Cargo.toml").write_text(
            "[package]\n"
            f'name = "{row["name"]}"\n'
            f'version = "{row["version"]}"\n'
            'edition = "2021"\n\n'
            "[lib]\n"
            'path = "src/lib.rs"\n',
            encoding="utf-8",
        )
        (payload / "src/lib.rs").write_text(
            f'pub fn {row["api"]}() -> u32 {{ {row["code"]} }}\n',
            encoding="utf-8",
        )
    return archive / "catalog.json"


def write_project(
    path: Path,
    *,
    profile: str,
    catalog: Path,
    roots: list[str],
    apis: list[str],
    seed: int,
) -> None:
    root_text = ", ".join(f'"{item}"' for item in roots)
    api_text = ", ".join(f'"{item}"' for item in apis)
    path.write_text(
        f'title = "{path.stem}"\n'
        f'profile = "{profile}"\n'
        f'catalog = "{catalog}"\n'
        f"roots = [{root_text}]\n"
        f"apis = [{api_text}]\n"
        f'seed = "{seed}"\n',
        encoding="utf-8",
    )


def clean_outputs() -> None:
    for path in (LOCK, BUILD_REPORT, APP / "output" / "resolve.log"):
        if path.exists():
            path.unlink()


def rebuild() -> None:
    result = subprocess.run(
        [REBUILD.as_posix()],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr


def parse_lock(payload: bytes) -> list[tuple[str, str, str]]:
    text = payload.decode("utf-8")
    assert text.endswith("\n")
    assert not text.endswith("\n\n")
    lines = text.removesuffix("\n").split("\n")
    assert all(line and line.count(" ") == 2 for line in lines)
    tuples = [tuple(line.split(" ")) for line in lines]
    assert tuples == sorted(tuples)
    assert len(tuples) == len(set(tuples))
    return tuples


def validate_closure(
    tuples: list[tuple[str, str, str]],
    roots: list[str],
    rows: list[dict],
) -> None:
    chosen = {row[0]: row for row in tuples}
    by_identity = {
        (row["name"], row["version"], row["source"]): row for row in rows
    }
    for root in roots:
        specification = parse_constraint(root)
        assert specification["key"] in chosen
        assert accepts(specification, by_identity[chosen[specification["key"]]])
    reachable = {parse_constraint(root)["key"] for root in roots}
    pending = list(reachable)
    while pending:
        key = pending.pop()
        row = by_identity[chosen[key]]
        for value in filter(None, row["needs"].split(";")):
            specification = parse_constraint(value)
            child = specification["key"]
            assert child in chosen
            assert accepts(specification, by_identity[chosen[child]])
            if child not in reachable:
                reachable.add(child)
                pending.append(child)
    assert set(chosen) == reachable


def run_case(
    tmp_path: Path,
    *,
    profile: str,
    roots: list[str],
    apis: list[str],
    seed: int = 0,
    extras: list[dict] | None = None,
    reverse_archive: bool = False,
    label: str = "case",
) -> tuple[bytes, list[tuple[str, str, str]]]:
    rows = [dict(row) for row in BASE_ROWS] + list(extras or [])
    if reverse_archive:
        rows.reverse()
    case_root = tmp_path / label
    case_root.mkdir()
    catalog = write_archive(case_root, rows)
    project = case_root / f"p{seed}.toml"
    write_project(
        project,
        profile=profile,
        catalog=catalog,
        roots=roots,
        apis=apis,
        seed=seed,
    )
    clean_outputs()
    rebuild()
    result = subprocess.run(
        [FORGE.as_posix(), "solve", project.as_posix()],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    payload = LOCK.read_bytes()
    tuples = parse_lock(payload)
    validate_closure(tuples, roots, rows)
    report = json.loads(BUILD_REPORT.read_text(encoding="utf-8"))
    assert report["success"] is True
    assert report["members"] == len(tuples)
    return payload, tuples


def run_failure(
    tmp_path: Path,
    *,
    profile: str,
    roots: list[str],
    apis: list[str],
    extras: list[dict] | None = None,
) -> None:
    rows = [dict(row) for row in BASE_ROWS] + list(extras or [])
    catalog = write_archive(tmp_path, rows)
    project = tmp_path / f"p{len(rows)}.toml"
    write_project(
        project,
        profile=profile,
        catalog=catalog,
        roots=roots,
        apis=apis,
        seed=0,
    )
    clean_outputs()
    rebuild()
    result = subprocess.run(
        [FORGE.as_posix(), "solve", project.as_posix()],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode != 0
    assert not LOCK.exists()


def test_r01(tmp_path: Path) -> None:
    """Keep the alpha parent selection and compile its closure."""
    _, tuples = run_case(
        tmp_path,
        profile="alpha",
        roots=[constraint("alder", 100, 130, "preview", 110)],
        apis=["alder:alpha_api", "birch:birch_api", "elm:elm_api"],
    )
    assert next(row for row in tuples if row[0] == "alder") == ALPHA


def test_r02(tmp_path: Path) -> None:
    """Keep the beta parent selection and compile its closure."""
    _, tuples = run_case(
        tmp_path,
        profile="beta",
        roots=[constraint("birch", 200, 220, exact=210)],
        apis=["birch:beta_api", "elm:elm_api"],
    )
    assert next(row for row in tuples if row[0] == "birch") == BETA


def test_r03(tmp_path: Path) -> None:
    """Exercise both parent outcomes in one complete graph."""
    _, tuples = run_case(
        tmp_path,
        profile="mixed",
        roots=[
            constraint("alder", 100, 130, "preview", 110),
            constraint("birch", 200, 220, exact=210),
        ],
        apis=["alder:alpha_api", "birch:beta_api", "elm:elm_api"],
    )
    assert next(row for row in tuples if row[0] == "alder") == ALPHA
    assert next(row for row in tuples if row[0] == "birch") == BETA


def test_r04(tmp_path: Path) -> None:
    """Classify a nearby generated preview without a name shortcut."""
    extra = generated(
        "juniper",
        "5.1.0-alpha.1",
        510,
        "j-prev",
        preview=True,
        withdrawn=False,
        api="j_api",
    )
    _, tuples = run_case(
        tmp_path,
        profile="alpha",
        roots=[constraint("juniper", 500, 520, "preview", 510)],
        apis=["juniper:j_api"],
        extras=[extra],
    )
    assert next(row for row in tuples if row[0] == extra["name"]) == (
        extra["name"],
        extra["version"],
        extra["source"],
    )


def test_r05(tmp_path: Path) -> None:
    """Keep bytes stable across equivalent archive permutations."""
    roots = [
        constraint("alder", 100, 130, exact=120),
        constraint("cedar", 300, 320, exact=300),
    ]
    apis = [
        "alder:alder_api",
        "birch:birch_api",
        "elm:elm_api",
        "cedar:cedar_api",
    ]
    first, _ = run_case(tmp_path, profile="plain", roots=roots, apis=apis, label="a")
    second, _ = run_case(
        tmp_path,
        profile="plain",
        roots=roots,
        apis=apis,
        reverse_archive=True,
        label="b",
    )
    assert first == second


def test_r06(tmp_path: Path) -> None:
    """Keep clean equivalent invocations byte-identical."""
    roots = [
        constraint("alder", 100, 130, exact=120),
        constraint("cedar", 300, 320, exact=300),
    ]
    apis = [
        "alder:alder_api",
        "birch:birch_api",
        "elm:elm_api",
        "cedar:cedar_api",
    ]
    first, _ = run_case(tmp_path, profile="plain", roots=roots, apis=apis, label="a")
    second, _ = run_case(
        tmp_path,
        profile="plain",
        roots=roots,
        apis=apis,
        seed=1,
        label="b",
    )
    assert first == second


def test_r07(tmp_path: Path) -> None:
    """Preserve generated stable and preview request distinctions."""
    preview = generated(
        "juniper",
        "5.1.0-alpha.1",
        510,
        "j-prev",
        preview=True,
        withdrawn=False,
        api="j_preview",
    )
    stable = generated(
        "juniper",
        "5.1.0",
        520,
        "j-main",
        preview=False,
        withdrawn=False,
        api="j_stable",
    )
    _, alpha_rows = run_case(
        tmp_path,
        profile="alpha",
        roots=[constraint("juniper", 500, 530, "preview", 510)],
        apis=[f"juniper:{preview['api']}"],
        extras=[preview, stable],
        label="a",
    )
    _, plain_rows = run_case(
        tmp_path,
        profile="plain",
        roots=[constraint("juniper", 500, 530, exact=520)],
        apis=[f"juniper:{stable['api']}"],
        extras=[preview, stable],
        label="b",
    )
    assert alpha_rows != plain_rows


def test_r08(tmp_path: Path) -> None:
    """Limit beta admission to its supported exact context."""
    _, tuples = run_case(
        tmp_path,
        profile="beta",
        roots=[constraint("birch", 200, 220, exact=210)],
        apis=["birch:beta_api", "elm:elm_api"],
        label="supported",
    )
    assert BETA in tuples
    run_failure(
        tmp_path / f"x{len(tuples)}",
        profile="plain",
        roots=[constraint("birch", 200, 220, exact=210)],
        apis=["birch:beta_api", "elm:elm_api"],
    )


def test_r09(tmp_path: Path) -> None:
    """Commit one tuple sequence across root and traversal permutations."""
    roots = [
        constraint("cedar", 300, 320, exact=300),
        constraint("alder", 100, 130, exact=120),
    ]
    apis = [
        "cedar:cedar_api",
        "alder:alder_api",
        "birch:birch_api",
        "elm:elm_api",
    ]
    first, first_rows = run_case(
        tmp_path,
        profile="plain",
        roots=roots,
        apis=apis,
        label="a",
    )
    second, second_rows = run_case(
        tmp_path,
        profile="plain",
        roots=list(reversed(roots)),
        apis=apis,
        seed=1,
        label="b",
    )
    assert first == second
    assert first_rows == second_rows


def test_r10(tmp_path: Path) -> None:
    """Commit generated classification into a deterministic graph."""
    preview = generated(
        "juniper",
        "5.1.0-alpha.1",
        510,
        "j-prev",
        preview=True,
        withdrawn=False,
        api="j_api",
    )
    run_case(
        tmp_path,
        profile="alpha",
        roots=[
            constraint("juniper", 500, 520, "preview", 510),
            constraint("cedar", 300, 320, exact=300),
        ],
        apis=["juniper:j_api", "cedar:cedar_api"],
        extras=[preview],
        seed=1,
    )


def test_r11(tmp_path: Path) -> None:
    """Compile a policy-sensitive transitive API from a stable graph."""
    _, tuples = run_case(
        tmp_path,
        profile="mixed",
        roots=[constraint("cedar", 300, 320, exact=310)],
        apis=[f"cedar:{'cedar_next_api'}", "birch:beta_api", "elm:elm_api"],
        seed=1,
    )
    assert next(row for row in tuples if row[0] == "birch") == BETA


def test_r12(tmp_path: Path) -> None:
    """Apply beta policy across generated names without broad admission."""
    for position, key in enumerate(("juniper", "larch")):
        stable = generated(
            key,
            "5.0.0",
            500,
            f"s{position}",
            preview=False,
            withdrawn=False,
            api="stable_api",
        )
        retained = generated(
            key,
            "5.1.0",
            510,
            f"h{position}",
            preview=False,
            withdrawn=True,
            api="held_api",
        )
        _, tuples = run_case(
            tmp_path,
            profile="beta",
            roots=[constraint(key, 500, 520, exact=510)],
            apis=[f"{key}:held_api"],
            extras=[stable, retained],
            label=f"p{position}",
        )
        assert next(row for row in tuples if row[0] == key) == (
            key,
            "5.1.0",
            f"h{position}",
        )
