package conductor

import (
	"fmt"
	"os"
	"path/filepath"

	"vaultlab/aperture"
	"vaultlab/keyring"
	"vaultlab/model"
	"vaultlab/tenant"
)

func replaceFrame(entry model.CatalogEntry, frame model.Frame) error {
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
	tmp := path + ".next"
	if err := os.WriteFile(tmp, append(encoded, '\n'), 0o600); err != nil {
		return err
	}
	return os.Rename(tmp, path)
}

func Maintain() error {
	ring, err := keyring.LoadDefault()
	if err != nil {
		return err
	}
	plan, err := LoadPlan()
	if err != nil {
		return err
	}
	for _, entry := range plan {
		axis := model.AxisFor(entry.Catalog.Item)
		scope, err := tenant.ScopeFor(axis, keyring.Epoch(entry.Frame.Epoch))
		if err != nil {
			return err
		}
		payload, err := aperture.Read(entry.Frame, scope, ring)
		if err != nil {
			return fmt.Errorf("read %s: %w", filepath.Base(entry.Catalog.File), err)
		}
		if entry.Frame.Epoch == uint32(ring.Active()) && entry.Frame.Axis == axis {
			continue
		}
		next, err := trace_q(entry.Catalog.Item, axis, ring.Active(), payload)
		if err != nil {
			return err
		}
		if err := replaceFrame(entry.Catalog, next); err != nil {
			return err
		}
	}
	return nil
}
