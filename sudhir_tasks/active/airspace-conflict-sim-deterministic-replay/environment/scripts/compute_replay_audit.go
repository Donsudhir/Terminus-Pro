package main

import (
	"bufio"
	"crypto/sha256"
	"encoding/csv"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

type ManifestRow struct {
	Scenario string
	FlightID string
	BasePri  int
	ETA      int
}

type Track struct {
	EventID   string `json:"event_id"`
	FlightID  string `json:"flight_id"`
	Scenario  string `json:"scenario"`
	Tick      int    `json:"tick"`
	Sector    string `json:"sector"`
	State     string `json:"state"`
	Revision  int    `json:"revision"`
	Source    string
}

type Correction struct {
	EventID  string `json:"event_id"`
	Mode     string `json:"mode"`
	Tick     *int   `json:"tick,omitempty"`
	Sector   string `json:"sector,omitempty"`
	State    string `json:"state,omitempty"`
	Revision *int   `json:"revision,omitempty"`
}

type TSVRow struct {
	Scenario string
	Tick     int
	Sector   string
	WindowID string
	FlightID string
	EffPri   int
	ETA      int
	Rank     int
	Decision string
}

type ScenarioSummary struct {
	Scenario        string `json:"scenario"`
	ConflictWindows int    `json:"conflict_windows"`
	ClearDecisions  int    `json:"clear_decisions"`
	HoldDecisions   int    `json:"hold_decisions"`
	Score           int    `json:"score"`
}

type Report struct {
	SchemaVersion    string            `json:"schema_version"`
	Scenarios        []ScenarioSummary `json:"scenarios"`
	Totals           ScenarioSummary   `json:"totals"`
	DeterministicHash string           `json:"deterministic_hash"`
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func readManifest(path string) map[string]ManifestRow {
	f, err := os.Open(path)
	must(err)
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll()
	must(err)
	out := map[string]ManifestRow{}
	for i, r := range rows {
		if i == 0 {
			continue
		}
		bp, _ := strconv.Atoi(r[2])
		eta, _ := strconv.Atoi(r[3])
		out[r[0]+"|"+r[1]] = ManifestRow{Scenario: r[0], FlightID: r[1], BasePri: bp, ETA: eta}
	}
	return out
}

func readOverrides(path string) map[string]int {
	f, err := os.Open(path)
	must(err)
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll()
	must(err)
	out := map[string]int{}
	for i, r := range rows {
		if i == 0 {
			continue
		}
		delta, _ := strconv.Atoi(r[2])
		out[r[0]+"|"+r[1]] = delta
	}
	return out
}

func readCap(path string) map[string]int {
	f, err := os.Open(path)
	must(err)
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll()
	must(err)
	out := map[string]int{}
	for i, r := range rows {
		if i == 0 {
			continue
		}
		c, _ := strconv.Atoi(r[2])
		out[r[0]+"|"+r[1]] = c
	}
	return out
}

func readCorrections(path string) map[string]Correction {
	f, err := os.Open(path)
	must(err)
	defer f.Close()
	s := bufio.NewScanner(f)
	out := map[string]Correction{}
	for s.Scan() {
		var c Correction
		must(json.Unmarshal([]byte(s.Text()), &c))
		out[c.EventID] = c
	}
	must(s.Err())
	return out
}

func readTracks(dir string) []Track {
	matches, err := filepath.Glob(filepath.Join(dir, "tracks_*.ndjson"))
	must(err)
	sort.Strings(matches)
	out := make([]Track, 0)
	for _, path := range matches {
		f, err := os.Open(path)
		must(err)
		s := bufio.NewScanner(f)
		src := filepath.Base(path)
		for s.Scan() {
			var t Track
			must(json.Unmarshal([]byte(s.Text()), &t))
			t.Source = src
			out = append(out, t)
		}
		must(s.Err())
		f.Close()
	}
	return out
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: compute_replay_audit <output-json> <output-tsv>")
	}
	outJSON := os.Args[1]
	outTSV := os.Args[2]

	base := "/app/environment/data"
	manifest := readManifest(filepath.Join(base, "manifest.csv"))
	overrides := readOverrides(filepath.Join(base, "overrides.csv"))
	caps := readCap(filepath.Join(base, "capacity.csv"))
	corr := readCorrections(filepath.Join(base, "corrections.ndjson"))
	tracks := readTracks(base)

	best := map[string]Track{}
	for _, t := range tracks {
		if c, ok := corr[t.EventID]; ok {
			if c.Mode == "drop" {
				continue
			}
			if c.Mode == "replace" {
				if c.Tick != nil {
					t.Tick = *c.Tick
				}
				if c.Sector != "" {
					t.Sector = c.Sector
				}
				if c.State != "" {
					t.State = c.State
				}
				if c.Revision != nil {
					t.Revision = *c.Revision
				}
			}
		}

		k := t.Scenario + "|" + t.EventID
		prev, ok := best[k]
		if !ok || t.Revision > prev.Revision || (t.Revision == prev.Revision && t.Source > prev.Source) {
			best[k] = t
		}
	}

	windowFlights := map[string]map[string]bool{}
	for _, t := range best {
		if t.State != "in" {
			continue
		}
		wk := fmt.Sprintf("%s|%d|%s", t.Scenario, t.Tick, t.Sector)
		if _, ok := windowFlights[wk]; !ok {
			windowFlights[wk] = map[string]bool{}
		}
		windowFlights[wk][t.FlightID] = true
	}

	tsvRows := make([]TSVRow, 0)
	summary := map[string]*ScenarioSummary{}
	for wk, flightsSet := range windowFlights {
		parts := strings.Split(wk, "|")
		scenario := parts[0]
		tick, _ := strconv.Atoi(parts[1])
		sector := parts[2]
		cap := caps[scenario+"|"+sector]
		flights := make([]string, 0, len(flightsSet))
		for f := range flightsSet {
			flights = append(flights, f)
		}
		if len(flights) <= cap {
			continue
		}
		sort.Slice(flights, func(i, j int) bool {
			li := manifest[scenario+"|"+flights[i]]
			lj := manifest[scenario+"|"+flights[j]]
			pi := li.BasePri + overrides[scenario+"|"+flights[i]]
			pj := lj.BasePri + overrides[scenario+"|"+flights[j]]
			if pi != pj {
				return pi > pj
			}
			if li.ETA != lj.ETA {
				return li.ETA < lj.ETA
			}
			return flights[i] < flights[j]
		})

		if _, ok := summary[scenario]; !ok {
			summary[scenario] = &ScenarioSummary{Scenario: scenario}
		}
		summary[scenario].ConflictWindows++

		windowID := fmt.Sprintf("%s:%s:%d", scenario, sector, tick)
		for i, fid := range flights {
			m := manifest[scenario+"|"+fid]
			eff := m.BasePri + overrides[scenario+"|"+fid]
			decision := "HOLD"
			if i < cap {
				decision = "CLEAR"
				summary[scenario].ClearDecisions++
			} else {
				summary[scenario].HoldDecisions++
			}
			tsvRows = append(tsvRows, TSVRow{
				Scenario: scenario,
				Tick: tick,
				Sector: sector,
				WindowID: windowID,
				FlightID: fid,
				EffPri: eff,
				ETA: m.ETA,
				Rank: i + 1,
				Decision: decision,
			})
		}
	}

	sort.Slice(tsvRows, func(i, j int) bool {
		a, b := tsvRows[i], tsvRows[j]
		if a.Scenario != b.Scenario {
			return a.Scenario < b.Scenario
		}
		if a.Tick != b.Tick {
			return a.Tick < b.Tick
		}
		if a.Sector != b.Sector {
			return a.Sector < b.Sector
		}
		if a.Rank != b.Rank {
			return a.Rank < b.Rank
		}
		return a.FlightID < b.FlightID
	})

	lines := []string{"scenario\ttick\tsector\twindow_id\tflight_id\teffective_priority\teta_tick\trank\tdecision"}
	for _, r := range tsvRows {
		lines = append(lines, fmt.Sprintf("%s\t%d\t%s\t%s\t%s\t%d\t%d\t%d\t%s", r.Scenario, r.Tick, r.Sector, r.WindowID, r.FlightID, r.EffPri, r.ETA, r.Rank, r.Decision))
	}
	tsv := strings.Join(lines, "\n") + "\n"
	must(os.WriteFile(outTSV, []byte(tsv), 0o644))

	h := sha256.Sum256([]byte(tsv))
	hash := hex.EncodeToString(h[:])

	scenarios := make([]ScenarioSummary, 0, len(summary))
	for _, k := range []string{"alpha", "beta", "gamma"} {
		s := summary[k]
		if s == nil {
			s = &ScenarioSummary{Scenario: k}
		}
		s.Score = s.ClearDecisions*4 - s.HoldDecisions*3 - s.ConflictWindows*2
		scenarios = append(scenarios, *s)
	}

	totals := ScenarioSummary{Scenario: "totals"}
	for _, s := range scenarios {
		totals.ConflictWindows += s.ConflictWindows
		totals.ClearDecisions += s.ClearDecisions
		totals.HoldDecisions += s.HoldDecisions
		totals.Score += s.Score
	}

	report := Report{
		SchemaVersion: "airspace-replay-audit-v1",
		Scenarios: scenarios,
		Totals: totals,
		DeterministicHash: hash,
	}
	b, err := json.MarshalIndent(report, "", "  ")
	must(err)
	must(os.WriteFile(outJSON, b, 0o644))
}
