package kernel

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os/exec"
)

type Candidate struct {
	FlightID  string `json:"flight_id"`
	Priority  int    `json:"priority"`
	Age       int    `json:"age"`
	ReadyTick int    `json:"ready_tick"`
}

type Request struct {
	Capacity   int         `json:"capacity"`
	Candidates []Candidate `json:"candidates"`
}

type Response struct {
	Accepted []string `json:"accepted"`
}

func Resolve(capacity int, candidates []Candidate) (map[string]bool, error) {
	req := Request{Capacity: capacity, Candidates: candidates}
	payload, err := json.Marshal(req)
	if err != nil {
		return nil, err
	}

	cmd := exec.Command("/usr/local/bin/atc-kernel")
	cmd.Stdin = bytes.NewReader(payload)
	var out bytes.Buffer
	cmd.Stdout = &out
	if err := cmd.Run(); err != nil {
		return nil, fmt.Errorf("kernel run: %w", err)
	}

	var resp Response
	if err := json.Unmarshal(out.Bytes(), &resp); err != nil {
		return nil, fmt.Errorf("kernel decode: %w", err)
	}

	accepted := make(map[string]bool, len(resp.Accepted))
	for _, f := range resp.Accepted {
		accepted[f] = true
	}
	return accepted, nil
}
