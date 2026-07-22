package conductor

import (
	"fmt"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func trace_q(a model.ItemID, b model.AxisID, c keyring.Epoch, d model.Payload) (model.Frame, error) {
	if err := a.Valid(); err != nil {
		return model.Frame{}, err
	}
	r, err := keyring.LoadDefault()
	if err != nil {
		return model.Frame{}, fmt.Errorf("load ring: %w", err)
	}
	x := model.RouteAxis(b)
	return crypto.Seal(a, x, c, d, r)
}
