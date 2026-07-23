package io

import (
	"encoding/json"
	"fmt"
	"os"

	"airspace-sim/internal/model"
)

func LoadScenario(path string) (model.Scenario, error) {
	var s model.Scenario
	b, err := os.ReadFile(path)
	if err != nil {
		return s, err
	}
	if err := json.Unmarshal(b, &s); err != nil {
		return s, err
	}
	if s.Name == "" || s.Horizon <= 0 {
		return s, fmt.Errorf("invalid scenario metadata")
	}
	return s, nil
}
