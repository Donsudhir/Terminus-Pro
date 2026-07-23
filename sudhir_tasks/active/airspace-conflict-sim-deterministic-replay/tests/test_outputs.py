import csv
import hashlib
import json
from pathlib import Path

ROOT = Path("/app")
DATA = ROOT / "environment" / "data"
OUT_JSON = ROOT / "output" / "conflict_windows.json"
OUT_TSV = ROOT / "output" / "replay_manifest.tsv"


def _read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _read_ndjson(path: Path):
    out = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _compute_expected():
    manifest_rows = _read_csv(DATA / "manifest.csv")
    override_rows = _read_csv(DATA / "overrides.csv")
    capacity_rows = _read_csv(DATA / "capacity.csv")
    corrections = {
        row["event_id"]: row
        for row in _read_ndjson(DATA / "corrections.ndjson")
    }

    manifest = {}
    for row in manifest_rows:
        manifest[(row["scenario"], row["flight_id"])] = {
            "base_priority": int(row["base_priority"]),
            "eta_tick": int(row["eta_tick"]),
        }

    overrides = {}
    for row in override_rows:
        overrides[(row["scenario"], row["flight_id"])] = int(row["priority_delta"])

    capacity = {}
    for row in capacity_rows:
        capacity[(row["scenario"], row["sector"])] = int(row["capacity"])

    best = {}
    for path in sorted(DATA.glob("tracks_*.ndjson")):
        source = path.name
        for rec in _read_ndjson(path):
            corr = corrections.get(rec["event_id"])
            if corr:
                if corr["mode"] == "drop":
                    continue
                if corr["mode"] == "replace":
                    for key in ("tick", "sector", "state", "revision"):
                        if key in corr:
                            rec[key] = corr[key]

            key = (rec["scenario"], rec["event_id"])
            cur = best.get(key)
            cand = {
                "scenario": rec["scenario"],
                "event_id": rec["event_id"],
                "flight_id": rec["flight_id"],
                "tick": int(rec["tick"]),
                "sector": rec["sector"],
                "state": rec["state"],
                "revision": int(rec["revision"]),
                "source": source,
            }
            if cur is None:
                best[key] = cand
                continue
            if cand["revision"] > cur["revision"]:
                best[key] = cand
                continue
            if cand["revision"] == cur["revision"] and cand["source"] > cur["source"]:
                best[key] = cand

    windows = {}
    for rec in best.values():
        if rec["state"] != "in":
            continue
        wk = (rec["scenario"], rec["sector"], rec["tick"])
        windows.setdefault(wk, set()).add(rec["flight_id"])

    rows = []
    scenario_summary = {}
    for (scenario, sector, tick), flights_set in windows.items():
        cap = capacity[(scenario, sector)]
        flights = sorted(flights_set)
        if len(flights) <= cap:
            continue

        scored = []
        for fid in flights:
            info = manifest[(scenario, fid)]
            eff = info["base_priority"] + overrides.get((scenario, fid), 0)
            scored.append((fid, eff, info["eta_tick"]))
        scored.sort(key=lambda x: (-x[1], x[2], x[0]))

        summary = scenario_summary.setdefault(
            scenario,
            {"conflict_windows": 0, "clear_decisions": 0, "hold_decisions": 0, "score": 0},
        )
        summary["conflict_windows"] += 1

        window_id = f"{scenario}:{sector}:{tick}"
        for idx, (fid, eff, eta) in enumerate(scored, start=1):
            decision = "CLEAR" if idx <= cap else "HOLD"
            if decision == "CLEAR":
                summary["clear_decisions"] += 1
            else:
                summary["hold_decisions"] += 1
            rows.append(
                {
                    "scenario": scenario,
                    "tick": tick,
                    "sector": sector,
                    "window_id": window_id,
                    "flight_id": fid,
                    "effective_priority": eff,
                    "eta_tick": eta,
                    "rank": idx,
                    "decision": decision,
                }
            )

    for scenario in ("alpha", "beta", "gamma"):
        scenario_summary.setdefault(
            scenario,
            {"conflict_windows": 0, "clear_decisions": 0, "hold_decisions": 0, "score": 0},
        )

    for v in scenario_summary.values():
        v["score"] = v["clear_decisions"] * 4 - v["hold_decisions"] * 3 - v["conflict_windows"] * 2

    rows.sort(key=lambda r: (r["scenario"], r["tick"], r["sector"], r["rank"], r["flight_id"]))
    header = "scenario\ttick\tsector\twindow_id\tflight_id\teffective_priority\teta_tick\trank\tdecision"
    lines = [header]
    for r in rows:
        lines.append(
            "\t".join(
                [
                    r["scenario"],
                    str(r["tick"]),
                    r["sector"],
                    r["window_id"],
                    r["flight_id"],
                    str(r["effective_priority"]),
                    str(r["eta_tick"]),
                    str(r["rank"]),
                    r["decision"],
                ]
            )
        )
    tsv_text = "\n".join(lines) + "\n"
    digest = hashlib.sha256(tsv_text.encode("utf-8")).hexdigest()

    scenarios = []
    totals = {"scenario": "totals", "conflict_windows": 0, "clear_decisions": 0, "hold_decisions": 0, "score": 0}
    for scenario in ("alpha", "beta", "gamma"):
        s = {"scenario": scenario, **scenario_summary[scenario]}
        scenarios.append(s)
        totals["conflict_windows"] += s["conflict_windows"]
        totals["clear_decisions"] += s["clear_decisions"]
        totals["hold_decisions"] += s["hold_decisions"]
        totals["score"] += s["score"]

    report = {
        "schema_version": "airspace-replay-audit-v1",
        "scenarios": scenarios,
        "totals": totals,
        "deterministic_hash": digest,
    }
    return report, tsv_text


def test_required_outputs_exist():
    """Ensure both required output artifacts are present."""
    assert OUT_JSON.exists(), "missing /app/output/conflict_windows.json"
    assert OUT_TSV.exists(), "missing /app/output/replay_manifest.tsv"


def test_replay_manifest_exact_content_and_order():
    """Validate replay_manifest.tsv matches fully recomputed canonical ordering."""
    _, expected_tsv = _compute_expected()
    got_tsv = OUT_TSV.read_text()
    assert got_tsv == expected_tsv


def test_conflict_windows_report_matches_expected_aggregation():
    """Check scenario and totals aggregation against independent recomputation."""
    expected_report, _ = _compute_expected()
    got = json.loads(OUT_JSON.read_text())

    assert got["schema_version"] == "airspace-replay-audit-v1"
    assert got["deterministic_hash"] == expected_report["deterministic_hash"]
    assert got["totals"] == expected_report["totals"]

    got_rows = sorted(got["scenarios"], key=lambda x: x["scenario"])
    exp_rows = sorted(expected_report["scenarios"], key=lambda x: x["scenario"])
    assert got_rows == exp_rows


def test_hash_matches_manifest_bytes_not_recomputed_structure():
    """Ensure deterministic hash is derived from exact manifest bytes."""
    got = json.loads(OUT_JSON.read_text())
    digest = hashlib.sha256(OUT_TSV.read_bytes()).hexdigest()
    assert got["deterministic_hash"] == digest


def test_subtle_requirements_are_enforced():
    """Assert tie-break and per-window dedup semantics from task requirements."""
    rows = OUT_TSV.read_text().splitlines()
    assert rows[0].split("\t") == [
        "scenario",
        "tick",
        "sector",
        "window_id",
        "flight_id",
        "effective_priority",
        "eta_tick",
        "rank",
        "decision",
    ]

    # Flight G302 appears from two events in gamma tick 30 after correction.
    # The window must still contain that flight once because counting is by unique flight.
    gamma_30 = [r for r in rows[1:] if r.startswith("gamma\t30\tC1\t")]
    g302_count = sum(1 for r in gamma_30 if "\tG302\t" in r)
    assert g302_count == 1

    # Override-driven ranking check: A102 must rank above A101 in alpha tick 10.
    alpha_10 = [r.split("\t") for r in rows[1:] if r.startswith("alpha\t10\tX1\t")]
    by_rank = sorted(alpha_10, key=lambda parts: int(parts[7]))
    assert by_rank[0][4] == "A102"
