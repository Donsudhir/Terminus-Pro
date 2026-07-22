from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

APP = Path(os.environ.get("ERS_APP_ROOT", "/app"))
BIN = Path(os.environ.get("ERS_BIN_ROOT", str(APP / "bin")))


def _cleanup_local() -> None:
    if APP != Path("/app"):
        shutil.rmtree(APP / "var", ignore_errors=True)
        shutil.rmtree(APP / "output", ignore_errors=True)


def cleanup_local() -> None:
    _cleanup_local()


def _env() -> dict[str, str]:
    env = os.environ.copy()
    if APP != Path("/app"):
        env["VAULT_HOME"] = str(APP)
    return env


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(BIN / "vaultctl"), *args],
        check=check,
        capture_output=True,
        text=True,
        env=_env(),
    )


def reset() -> None:
    subprocess.run(
        [str(APP / "scripts" / "reset-fixture.sh")],
        check=True,
        capture_output=True,
        text=True,
        env=_env(),
    )


def value_for(service: str, secret: str) -> str:
    folded = sum((index + 1) * ord(ch) for index, ch in enumerate(service + secret))
    return f"{secret}-{folded % 997:03d}"


def _keys() -> tuple[int, dict[int, bytes]]:
    active = 0
    keys: dict[int, bytes] = {}
    for raw in (APP / "config" / "ring.toml").read_text().splitlines():
        line = raw.strip()
        if not line:
            continue
        name, text = (part.strip() for part in line.split("=", 1))
        if name == "active":
            active = int(text)
        elif name.startswith("epoch_"):
            keys[int(name.removeprefix("epoch_"))] = bytes.fromhex(text.strip('"'))
    return active, keys


def active_epoch() -> int:
    active, _ = _keys()
    return active


def _case_tool() -> Path:
    folder = Path(os.environ.get("TMPDIR", "/tmp")) / Path(__file__).stem
    source = folder / Path(__file__).with_suffix(".go").name
    binary = source.with_suffix("")
    if binary.exists():
        return binary
    folder.mkdir(parents=True, exist_ok=True)
    source.write_text(
        """package main

import (
    "encoding/json"
    "fmt"
    "os"
    "strconv"

    "vaultlab/crypto"
    "vaultlab/keyring"
    "vaultlab/model"
)

func fold(a, b string) string {
    n := 0
    for i, r := range a + b {
        n += (i + 1) * int(r)
    }
    return fmt.Sprintf("%s-%03d", b, n%997)
}

func main() {
    if len(os.Args) != 6 {
        os.Exit(2)
    }
    e, err := strconv.ParseUint(os.Args[3], 10, 32)
    if err != nil {
        panic(err)
    }
    q, err := strconv.ParseUint(os.Args[4], 10, 64)
    if err != nil {
        panic(err)
    }
    ring, err := keyring.LoadDefault()
    if err != nil {
        panic(err)
    }
    item := model.ItemID{Service: os.Args[1], Secret: os.Args[2]}
    frame, err := crypto.SealAt(
        item,
        model.AxisFor(item),
        keyring.Epoch(e),
        model.Payload(fold(os.Args[1], os.Args[2])),
        q,
        ring,
    )
    if err != nil {
        panic(err)
    }
    if os.Args[5] == "1" {
        if frame.Tag[0] == 'A' {
            frame.Tag = "B" + frame.Tag[1:]
        } else {
            frame.Tag = "A" + frame.Tag[1:]
        }
    }
    if err := json.NewEncoder(os.Stdout).Encode(frame); err != nil {
        panic(err)
    }
}
"""
    )
    subprocess.run(
        [
            "go",
            "build",
            "-buildvcs=false",
            "-trimpath",
            "-o",
            str(binary),
            str(source),
        ],
        cwd=APP,
        check=True,
        capture_output=True,
        text=True,
        env=_env(),
    )
    return binary


def make_frame(
    service: str,
    secret: str,
    epoch: int,
    seq: int,
    *,
    damage: bool = False,
) -> dict[str, Any]:
    result = subprocess.run(
        [
            str(_case_tool()),
            service,
            secret,
            str(epoch),
            str(seq),
            "1" if damage else "0",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=_env(),
    )
    return json.loads(result.stdout)


def catalog() -> list[dict[str, Any]]:
    return json.loads((APP / "var" / "live" / "catalog.json").read_text())


def write_catalog(rows: list[dict[str, Any]]) -> None:
    path = APP / "var" / "live" / "catalog.json"
    path.write_text(json.dumps(rows, indent=2) + "\n")


def retain(*pairs: tuple[str, str]) -> None:
    wanted = set(pairs)
    rows = [
        row
        for row in catalog()
        if (row["item"]["service"], row["item"]["secret"]) in wanted
    ]
    write_catalog(rows)


def add_case(
    service: str,
    secret: str,
    *,
    damage: bool = False,
    history: bool = False,
    epoch: int | None = None,
) -> tuple[str, str]:
    rows = catalog()
    index = len(rows) + 1
    active, _ = _keys()
    selected_epoch = active if epoch is None else epoch
    name = f"case-{index:03d}.bin"
    current = make_frame(service, secret, selected_epoch, 6000 + index, damage=damage)
    (APP / "var" / "live" / name).write_text(json.dumps([current], indent=2) + "\n")
    rows.append(
        {
            "item": {"service": service, "secret": secret},
            "file": name,
            "slot": 0,
        }
    )
    write_catalog(rows)
    if history:
        path = APP / "var" / "segments" / "chunk-03.bin"
        frames = json.loads(path.read_text())
        frames.append(make_frame(service, secret, active - 1, 4000 + index * 2))
        peer = f"peer-{index:03d}"
        frames.append(make_frame(peer, secret, active - 1, 4001 + index * 2))
        path.write_text(json.dumps(frames, indent=2) + "\n")
    return service, secret


def generated_pairs(count: int, seed: str) -> list[tuple[str, str]]:
    pairs = []
    for index in range(count):
        token = (index * 7919 + len(seed) * 101 + sum(map(ord, seed))) % 10_000_019
        pairs.append((f"unit-{index:02d}-{token}", f"slot-{(index * 7 + 3) % 29:02d}"))
    return pairs


def entry(pair: tuple[str, str]) -> dict[str, Any]:
    service, secret = pair
    for row in catalog():
        if row["item"] == {"service": service, "secret": secret}:
            return row
    raise KeyError(pair)


def live_path(pair: tuple[str, str]) -> Path:
    return APP / "var" / "live" / entry(pair)["file"]


def substitute(target: tuple[str, str], source: tuple[str, str]) -> None:
    live_path(target).write_bytes(live_path(source).read_bytes())


def tamper(pair: tuple[str, str]) -> None:
    path = live_path(pair)
    frames = json.loads(path.read_text())
    body = frames[0]["body"]
    frames[0]["body"] = ("A" if body[0] != "A" else "B") + body[1:]
    path.write_text(json.dumps(frames, indent=2) + "\n")


def digest_tree() -> tuple[tuple[str, bytes], ...]:
    snapshot = []
    for path in sorted((APP / "var").rglob("*")):
        if path.is_file():
            snapshot.append(
                (path.relative_to(APP / "var").as_posix(), path.read_bytes())
            )
    return tuple(snapshot)


def digest_file(pair: tuple[str, str]) -> bytes:
    return live_path(pair).read_bytes()


def report() -> dict[str, Any]:
    return json.loads((APP / "output" / "recovery.json").read_text())
