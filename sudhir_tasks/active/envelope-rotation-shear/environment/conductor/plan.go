package conductor

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"

	"vaultlab/model"
)

type PlanEntry struct {
	Catalog model.CatalogEntry
	Frame   model.Frame
}

func LoadPlan() ([]PlanEntry, error) {
	raw, err := os.ReadFile(model.Home("var", "live", "catalog.json"))
	if err != nil {
		return nil, err
	}
	var catalog []model.CatalogEntry
	if err := json.Unmarshal(raw, &catalog); err != nil {
		return nil, err
	}
	sort.Slice(catalog, func(i, j int) bool {
		return catalog[i].Item.Key() < catalog[j].Item.Key()
	})
	out := make([]PlanEntry, 0, len(catalog))
	for _, entry := range catalog {
		bundleRaw, err := os.ReadFile(model.Home("var", "live", entry.File))
		if err != nil {
			return nil, err
		}
		frames, err := model.DecodeFrames(bundleRaw)
		if err != nil {
			return nil, err
		}
		if entry.Slot < 0 || entry.Slot >= len(frames) {
			return nil, fmt.Errorf("catalog slot out of range")
		}
		out = append(out, PlanEntry{Catalog: entry, Frame: frames[entry.Slot]})
	}
	return out, nil
}
