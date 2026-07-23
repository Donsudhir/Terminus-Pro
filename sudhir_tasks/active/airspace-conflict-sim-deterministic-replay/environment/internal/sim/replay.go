package sim

import (
	"fmt"
	"sort"
	"strings"
)

func buildTrajectory(events []string) string {
	sorted := make([]string, len(events))
	copy(sorted, events)
	sort.Strings(sorted)
	return strings.Join(sorted, "\n")
}

func tickEvent(tick int, flightID string, event string) string {
	return fmt.Sprintf("t=%03d|f=%s|e=%s", tick, flightID, event)
}
