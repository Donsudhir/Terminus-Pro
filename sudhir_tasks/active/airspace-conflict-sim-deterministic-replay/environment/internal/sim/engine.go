package sim

import (
	"fmt"
	"sort"

	"airspace-sim/internal/kernel"
	"airspace-sim/internal/model"
	"airspace-sim/internal/util"
)

type flightState struct {
	id          string
	leg         int
	readyTick   int
	queueSince  int
	done        bool
	dropped     bool
	priority    int
	path        []string
	durations   []int
	maxQueue    int
	startDelay  int
	priorityAdj int
}

func RunScenario(s model.Scenario, p model.ControlPlan) (model.ScenarioResult, error) {
	plansByFlight, ok := p.Scenarios[s.Name]
	if !ok {
		return model.ScenarioResult{}, fmt.Errorf("missing scenario plan for %s", s.Name)
	}

	edgeCap := map[string]int{}
	for _, e := range s.Edges {
		edgeCap[e.From+"->"+e.To] = e.Capacity
	}

	states := map[string]*flightState{}
	finishTicks := map[string]int{}
	eventCounts := map[string]int{"grant": 0, "deny": 0, "drop": 0, "finish": 0}
	events := make([]string, 0, 4096)

	for _, f := range s.Flights {
		if len(f.Path) < 2 || len(f.Durations) != len(f.Path)-1 {
			return model.ScenarioResult{}, fmt.Errorf("invalid flight %s shape", f.ID)
		}
		fp := plansByFlight[f.ID]
		states[f.ID] = &flightState{
			id:          f.ID,
			leg:         0,
			readyTick:   f.EntryTick + fp.StartDelay,
			queueSince:  f.EntryTick + fp.StartDelay,
			done:        false,
			dropped:     false,
			priority:    f.Priority,
			path:        f.Path,
			durations:   f.Durations,
			maxQueue:    f.MaxQueue,
			startDelay:  fp.StartDelay,
			priorityAdj: fp.PriorityBias,
		}
	}

	conflicts := 0
	losses := 0
	completed := 0
	completionTickSum := 0

	for tick := 0; tick <= s.Horizon; tick++ {
		edgeCandidates := map[string][]kernel.Candidate{}
		byEdgeOrder := make([]string, 0)

		for _, st := range states {
			if st.done || st.dropped {
				continue
			}
			if tick < st.readyTick {
				continue
			}
			edge := st.path[st.leg] + "->" + st.path[st.leg+1]
			if _, exists := edgeCandidates[edge]; !exists {
				byEdgeOrder = append(byEdgeOrder, edge)
			}
			age := tick - st.queueSince
			edgeCandidates[edge] = append(edgeCandidates[edge], kernel.Candidate{
				FlightID:  st.id,
				Priority:  st.priority + st.priorityAdj,
				Age:       age,
				ReadyTick: st.readyTick,
			})
		}

		sort.Strings(byEdgeOrder)
		for _, edge := range byEdgeOrder {
			cand := edgeCandidates[edge]
			cap, ok := edgeCap[edge]
			if !ok {
				return model.ScenarioResult{}, fmt.Errorf("edge capacity missing for %s", edge)
			}

			accepted := map[string]bool{}
			if len(cand) <= cap {
				for _, c := range cand {
					accepted[c.FlightID] = true
				}
			} else {
				resolved, err := kernel.Resolve(cap, cand)
				if err != nil {
					return model.ScenarioResult{}, err
				}
				accepted = resolved
			}

			for _, c := range cand {
				st := states[c.FlightID]
				if accepted[c.FlightID] {
					st.leg++
					eventCounts["grant"]++
					events = append(events, tickEvent(tick, st.id, "grant:"+edge))
					if st.leg >= len(st.durations) {
						st.done = true
						completed++
						completionTickSum += tick
						finishTicks[st.id] = tick
						eventCounts["finish"]++
						events = append(events, tickEvent(tick, st.id, "finish"))
					} else {
						st.readyTick = tick + st.durations[st.leg]
						st.queueSince = st.readyTick
					}
				} else {
					conflicts++
					eventCounts["deny"]++
					events = append(events, tickEvent(tick, st.id, "deny:"+edge))
					if tick-st.queueSince+1 > st.maxQueue {
						st.dropped = true
						losses++
						eventCounts["drop"]++
						events = append(events, tickEvent(tick, st.id, "drop"))
					}
				}
			}
		}
	}

	result := model.ScenarioResult{
		Scenario:          s.Name,
		FlightsTotal:      len(s.Flights),
		Completed:         completed,
		Losses:            losses,
		Conflicts:         conflicts,
		CompletionTickSum: completionTickSum,
		FinishTicks:       finishTicks,
		EventCounts:       eventCounts,
	}
	result.ThroughputScore = scoreResult(result)
	trajectory := buildTrajectory(events)
	result.TrajectoryHash = util.SHA256Hex(trajectory)
	return result, nil
}
