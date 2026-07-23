package sim

import "airspace-sim/internal/model"

func scoreResult(r model.ScenarioResult) int {
	return r.Completed*120 - r.Losses*400 - r.Conflicts*8 - r.CompletionTickSum
}
