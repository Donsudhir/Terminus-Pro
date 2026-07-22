package tenant

import (
	"fmt"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func ScopeFor(axis model.AxisID, epoch keyring.Epoch) (crypto.Scope, error) {
	scope, err := settle_r(axis, epoch)
	if err != nil {
		return crypto.Scope{}, fmt.Errorf("scope unavailable: %w", err)
	}
	if err := scope.Valid(); err != nil {
		return crypto.Scope{}, err
	}
	return scope, nil
}
