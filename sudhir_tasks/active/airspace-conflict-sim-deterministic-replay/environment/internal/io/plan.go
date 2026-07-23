package io

import (
	"encoding/json"
	"fmt"
	"os"

	"airspace-sim/internal/model"
)

func LoadPlan(path string) (model.ControlPlan, error) {
	var p model.ControlPlan
	b, err := os.ReadFile(path)
	if err != nil {
		return p, err
	}
	if err := json.Unmarshal(b, &p); err != nil {
		return p, err
	}
	if len(p.Scenarios) == 0 {
		return p, fmt.Errorf("plan.scenarios is empty")
	}
	return p, nil
}

func WriteJSON(path string, v any) error {
	b, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, b, 0o644)
}
