package ledger

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"

	"vaultlab/aperture"
	"vaultlab/keyring"
	"vaultlab/model"
	"vaultlab/tenant"
)

type RecoveredItem struct {
	Service string `json:"service"`
	Secret  string `json:"secret"`
}

type RecoveryReport struct {
	Recovered []RecoveredItem `json:"recovered"`
}

func storeFrame(entry model.CatalogEntry, frame model.Frame) error {
	path := model.Home("var", "live", entry.File)
	raw, err := os.ReadFile(path)
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
	frames[entry.Slot] = frame
	encoded, err := model.EncodeFrames(frames)
	if err != nil {
		return err
	}
	tmp := path + ".restore"
	if err := os.WriteFile(tmp, append(encoded, '\n'), 0o600); err != nil {
		return err
	}
	return os.Rename(tmp, path)
}

func Recover(catalog []model.CatalogEntry) (RecoveryReport, error) {
	report := RecoveryReport{Recovered: []RecoveredItem{}}
	ring, err := keyring.LoadDefault()
	if err != nil {
		return report, err
	}
	journal, err := LoadJournal()
	if err != nil {
		return report, err
	}
	for _, entry := range catalog {
		raw, err := os.ReadFile(model.Home("var", "live", entry.File))
		if err != nil {
			return report, err
		}
		frames, err := model.DecodeFrames(raw)
		if err != nil {
			return report, err
		}
		if entry.Slot < 0 || entry.Slot >= len(frames) {
			return report, fmt.Errorf("catalog slot out of range")
		}
		current := frames[entry.Slot]
		axis := model.AxisFor(entry.Item)
		scope, err := tenant.ScopeFor(axis, keyring.Epoch(current.Epoch))
		if err == nil {
			if _, openErr := aperture.Read(current, scope, ring); openErr == nil {
				continue
			}
		}
		prior, err := replay_t(journal, entry.Item, axis, ring.Active())
		if err != nil {
			return report, err
		}
		priorScope, err := tenant.ScopeFor(axis, keyring.Epoch(prior.Epoch))
		if err != nil {
			return report, err
		}
		if _, err := aperture.Read(*prior, priorScope, ring); err != nil {
			return report, err
		}
		if err := storeFrame(entry, *prior); err != nil {
			return report, err
		}
		report.Recovered = append(report.Recovered, RecoveredItem{
			Service: entry.Item.Service,
			Secret:  entry.Item.Secret,
		})
	}
	sort.Slice(report.Recovered, func(i, j int) bool {
		if report.Recovered[i].Service == report.Recovered[j].Service {
			return report.Recovered[i].Secret < report.Recovered[j].Secret
		}
		return report.Recovered[i].Service < report.Recovered[j].Service
	})
	return report, nil
}

func WriteReport(report RecoveryReport) error {
	if err := os.MkdirAll(model.Home("output"), 0o755); err != nil {
		return err
	}
	raw, err := json.MarshalIndent(report, "", "  ")
	if err != nil {
		return err
	}
	tmp := model.Home("output", "recovery.json.next")
	if err := os.WriteFile(tmp, append(raw, '\n'), 0o600); err != nil {
		return err
	}
	return os.Rename(tmp, model.Home("output", "recovery.json"))
}
