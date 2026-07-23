package model

type Edge struct {
	From     string `json:"from"`
	To       string `json:"to"`
	Capacity int    `json:"capacity"`
}

type Flight struct {
	ID        string   `json:"id"`
	EntryTick int      `json:"entry_tick"`
	Priority  int      `json:"priority"`
	MaxQueue  int      `json:"max_queue"`
	Path      []string `json:"path"`
	Durations []int    `json:"durations"`
}

type Scenario struct {
	Name    string   `json:"name"`
	Horizon int      `json:"horizon"`
	Edges   []Edge   `json:"edges"`
	Flights []Flight `json:"flights"`
}

type FlightPlan struct {
	StartDelay   int `json:"start_delay"`
	PriorityBias int `json:"priority_bias"`
}

type ControlPlan struct {
	Scenarios map[string]map[string]FlightPlan `json:"scenarios"`
}

type ScenarioResult struct {
	Scenario          string            `json:"scenario"`
	FlightsTotal      int               `json:"flights_total"`
	Completed         int               `json:"completed"`
	Losses            int               `json:"losses"`
	Conflicts         int               `json:"conflicts"`
	CompletionTickSum int               `json:"completion_tick_sum"`
	ThroughputScore   int               `json:"throughput_score"`
	TrajectoryHash    string            `json:"trajectory_hash"`
	FinishTicks       map[string]int    `json:"finish_ticks"`
	EventCounts       map[string]int    `json:"event_counts"`
}
