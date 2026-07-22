package tenant

import (
	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func settle_r(a model.AxisID, b keyring.Epoch) (crypto.Scope, error) {
	x := cachedAxis(a)
	return crypto.ScopeFor(x, b)
}
