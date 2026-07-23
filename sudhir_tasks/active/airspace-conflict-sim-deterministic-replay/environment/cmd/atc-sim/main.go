package main

import (
	"flag"
	"fmt"
	"os"

	"airspace-sim/internal/io"
	"airspace-sim/internal/sim"
)

func main() {
	scenarioPath := flag.String("scenario", "", "scenario JSON path")
	planPath := flag.String("plan", "", "control plan JSON path")
	reportPath := flag.String("report", "", "result JSON path")
	flag.Parse()

	if *scenarioPath == "" || *planPath == "" || *reportPath == "" {
		fmt.Fprintln(os.Stderr, "usage: atc-sim --scenario <path> --plan <path> --report <path>")
		os.Exit(2)
	}

	scenario, err := io.LoadScenario(*scenarioPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load scenario: %v\n", err)
		os.Exit(1)
	}

	plan, err := io.LoadPlan(*planPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "load plan: %v\n", err)
		os.Exit(1)
	}

	result, err := sim.RunScenario(scenario, plan)
	if err != nil {
		fmt.Fprintf(os.Stderr, "run scenario: %v\n", err)
		os.Exit(1)
	}

	if err := io.WriteJSON(*reportPath, result); err != nil {
		fmt.Fprintf(os.Stderr, "write report: %v\n", err)
		os.Exit(1)
	}
}
