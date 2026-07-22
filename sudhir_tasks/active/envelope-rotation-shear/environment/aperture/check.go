package aperture

import (
	"encoding/json"
	"fmt"
	"os"

	"vaultlab/keyring"
	"vaultlab/model"
	"vaultlab/tenant"
)

func Audit() (int, error) {
	raw, err := os.ReadFile(model.Home("var", "live", "catalog.json"))
	if err != nil {
		return 0, err
	}
	var catalog []model.CatalogEntry
	if err := json.Unmarshal(raw, &catalog); err != nil {
		return 0, err
	}
	ring, err := keyring.LoadDefault()
	if err != nil {
		return 0, err
	}
	seen := make(map[string]bool)
	for _, entry := range catalog {
		if err := entry.Item.Valid(); err != nil {
			return 0, err
		}
		if seen[entry.Item.Key()] {
			return 0, fmt.Errorf("duplicate catalog identity")
		}
		seen[entry.Item.Key()] = true
		bundleRaw, err := os.ReadFile(model.Home("var", "live", entry.File))
		if err != nil {
			return 0, err
		}
		frames, err := model.DecodeFrames(bundleRaw)
		if err != nil {
			return 0, err
		}
		if entry.Slot < 0 || entry.Slot >= len(frames) {
			return 0, fmt.Errorf("catalog slot out of range")
		}
		frame := frames[entry.Slot]
		scope, err := tenant.ScopeFor(model.AxisFor(entry.Item), keyring.Epoch(frame.Epoch))
		if err != nil {
			return 0, err
		}
		if _, err := route_s(frame, scope, ring); err != nil {
			return 0, err
		}
	}
	return len(catalog), nil
}
