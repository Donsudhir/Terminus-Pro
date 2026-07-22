package aperture

import (
	"fmt"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func route_s(a model.Frame, b crypto.Scope, c *keyring.Ring) (model.Payload, error) {
	for _, x := range openSet(a, b) {
		payload, err := crypto.Open(a, x, c)
		if err == nil {
			return payload, nil
		}
	}
	return nil, fmt.Errorf("no candidate opened")
}
