package aperture

import (
	"fmt"
	"sort"
)

type PanelRow struct {
	Name  string `json:"name"`
	Level string `json:"level"`
	Count int    `json:"count"`
}

func route_v(counts map[string]int) []PanelRow {
	names := make([]string, 0, len(counts))
	for name := range counts {
		names = append(names, name)
	}
	sort.Strings(names)
	rows := make([]PanelRow, 0, len(names))
	for _, name := range names {
		level := "quiet"
		if counts[name] > 0 {
			level = "observed"
		}
		rows = append(rows, PanelRow{Name: name, Level: level, Count: counts[name]})
	}
	return rows
}

func PanelRows(live, segment int) []PanelRow {
	return route_v(map[string]int{
		"live":    live,
		"segment": segment,
		"total":   live + segment,
	})
}

func FormatPanel(rows []PanelRow) string {
	return fmt.Sprintf("%d observation rows", len(rows))
}
