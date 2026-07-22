package conductor

import (
	"fmt"
	"time"
)

type DialRow struct {
	Entries int   `json:"entries"`
	Micros  int64 `json:"estimated_micros"`
}

func pace_q(entries int, unit time.Duration) DialRow {
	if entries < 0 {
		entries = 0
	}
	if unit < 0 {
		unit = 0
	}
	return DialRow{
		Entries: entries,
		Micros:  (time.Duration(entries) * unit).Microseconds(),
	}
}

func DialSummary() (DialRow, error) {
	plan, err := LoadPlan()
	if err != nil {
		return DialRow{}, fmt.Errorf("plan telemetry: %w", err)
	}
	return pace_q(len(plan), 175*time.Microsecond), nil
}
