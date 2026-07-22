package main

import (
	"encoding/json"
	"fmt"
	"os"

	"vaultlab/aperture"
	"vaultlab/conductor"
	"vaultlab/keyring"
	"vaultlab/ledger"
	"vaultlab/model"
	"vaultlab/tenant"
)

func loadCatalog() ([]model.CatalogEntry, error) {
	raw, err := os.ReadFile(model.Home("var", "live", "catalog.json"))
	if err != nil {
		return nil, err
	}
	var catalog []model.CatalogEntry
	if err := json.Unmarshal(raw, &catalog); err != nil {
		return nil, err
	}
	return catalog, nil
}

func readItem(service, secret string) error {
	catalog, err := loadCatalog()
	if err != nil {
		return err
	}
	want := model.ItemID{Service: service, Secret: secret}
	for _, entry := range catalog {
		if !entry.Item.Equal(want) {
			continue
		}
		raw, err := os.ReadFile(model.Home("var", "live", entry.File))
		if err != nil {
			return err
		}
		frames, err := model.DecodeFrames(raw)
		if err != nil {
			return err
		}
		if entry.Slot < 0 || entry.Slot >= len(frames) {
			return fmt.Errorf("catalog slot out of range")
		}
		frame := frames[entry.Slot]
		ring, err := keyring.LoadDefault()
		if err != nil {
			return err
		}
		scope, err := tenant.ScopeFor(model.AxisFor(want), keyring.Epoch(frame.Epoch))
		if err != nil {
			return err
		}
		payload, err := aperture.Read(frame, scope, ring)
		if err != nil {
			return err
		}
		_, err = os.Stdout.Write(append(payload, '\n'))
		return err
	}
	return fmt.Errorf("item not found")
}

func recoverAll() error {
	_ = os.Remove(model.Home("output", "recovery.json"))
	catalog, err := loadCatalog()
	if err != nil {
		return err
	}
	report, err := ledger.Recover(catalog)
	if err != nil {
		return err
	}
	return ledger.WriteReport(report)
}

func auditAll() error {
	live, err := aperture.Audit()
	if err != nil {
		return err
	}
	journal, err := ledger.LoadJournal()
	if err != nil {
		return err
	}
	segments, err := ledger.CheckSegments(journal)
	if err != nil {
		return err
	}
	fmt.Printf("checked %d live and %d historical frames\n", live, segments)
	return nil
}

func usage() {
	fmt.Fprintln(os.Stderr, "usage: vaultctl get <service> <secret> | recover | maintain | audit")
}

func main() {
	var err error
	switch {
	case len(os.Args) == 4 && os.Args[1] == "get":
		err = readItem(os.Args[2], os.Args[3])
	case len(os.Args) == 2 && os.Args[1] == "recover":
		err = recoverAll()
	case len(os.Args) == 2 && os.Args[1] == "maintain":
		err = conductor.Maintain()
	case len(os.Args) == 2 && os.Args[1] == "audit":
		err = auditAll()
	default:
		usage()
		os.Exit(2)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
