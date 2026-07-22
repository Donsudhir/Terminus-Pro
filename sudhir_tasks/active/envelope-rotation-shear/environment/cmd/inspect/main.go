package main

import (
	"encoding/json"
	"fmt"
	"os"

	"vaultlab/aperture"
	"vaultlab/conductor"
	"vaultlab/keyring"
	"vaultlab/ledger"
	"vaultlab/tenant"
)

type observations struct {
	Dial    conductor.DialRow   `json:"dial"`
	Label   string              `json:"label"`
	Panel   []aperture.PanelRow `json:"panel"`
	Spool   []ledger.SpoolRow   `json:"spool"`
	Keysets []keyring.Entry     `json:"keysets"`
}

func main() {
	ring, err := keyring.LoadDefault()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	journal, err := ledger.LoadJournal()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	dial, err := conductor.DialSummary()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	rows := ledger.SpoolCounts(journal)
	view := observations{
		Dial:    dial,
		Label:   tenant.RelayLabel("Store Observation"),
		Panel:   aperture.PanelRows(dial.Entries, len(journal.Frames())),
		Spool:   rows,
		Keysets: ring.Catalog(),
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(view); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
