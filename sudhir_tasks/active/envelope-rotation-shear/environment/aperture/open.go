package aperture

import (
	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func openSet(frame model.Frame, supplied crypto.Scope) []crypto.Scope {
	out := []crypto.Scope{supplied}
	if frame.Axis != model.AxisFor(frame.Item) {
		return out
	}
	routed, err := crypto.ScopeFor(model.RouteAxis(frame.Axis), keyring.Epoch(frame.Epoch))
	if err == nil && routed.Equal(supplied) {
		return out
	}
	derived, err := crypto.ScopeFor(frame.Axis, keyring.Epoch(frame.Epoch))
	if err == nil && !derived.Equal(supplied) {
		out = append(out, derived)
	}
	return out
}

func Read(frame model.Frame, scope crypto.Scope, ring *keyring.Ring) (model.Payload, error) {
	return route_s(frame, scope, ring)
}
