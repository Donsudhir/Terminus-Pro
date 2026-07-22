#!/usr/bin/env bash
set -euo pipefail
cd /app

cat > /app/conductor/arc.go <<'EOF'
package conductor

import (
	"bytes"
	"fmt"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func trace_q(a model.ItemID, b model.AxisID, c keyring.Epoch, d model.Payload) (model.Frame, error) {
	if err := a.Valid(); err != nil {
		return model.Frame{}, fmt.Errorf("invalid item: %w", err)
	}
	if b == "" || b != model.AxisFor(a) {
		return model.Frame{}, fmt.Errorf("axis mismatch")
	}
	if c == 0 || len(d) == 0 || len(d) > 1<<20 {
		return model.Frame{}, fmt.Errorf("invalid frame input")
	}
	x, err := keyring.LoadDefault()
	if err != nil {
		return model.Frame{}, fmt.Errorf("load ring: %w", err)
	}
	if !x.Has(c) {
		return model.Frame{}, fmt.Errorf("epoch unavailable")
	}
	y, err := crypto.ScopeFor(b, c)
	if err != nil {
		return model.Frame{}, fmt.Errorf("build scope: %w", err)
	}
	if err := y.Valid(); err != nil {
		return model.Frame{}, err
	}
	z, err := crypto.Seal(a, b, c, d, x)
	if err != nil {
		return model.Frame{}, fmt.Errorf("seal frame: %w", err)
	}
	if err := z.StructuralValid(); err != nil {
		return model.Frame{}, err
	}
	if !z.Item.Equal(a) || z.Axis != b || z.Epoch != uint32(c) {
		return model.Frame{}, fmt.Errorf("frame header mismatch")
	}
	p, err := crypto.Open(z, y, x)
	if err != nil {
		return model.Frame{}, fmt.Errorf("verify frame: %w", err)
	}
	if !bytes.Equal(p, d) {
		return model.Frame{}, fmt.Errorf("frame verification mismatch")
	}
	return z, nil
}
EOF

cat > /app/tenant/spine.go <<'EOF'
package tenant

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"unicode"
	"unicode/utf8"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func settle_r(a model.AxisID, b keyring.Epoch) (crypto.Scope, error) {
	x := []byte(a)
	if len(x) < 2 || len(x) > 96 || b == 0 {
		return crypto.Scope{}, fmt.Errorf("invalid scope input")
	}
	if !utf8.Valid(x) {
		return crypto.Scope{}, fmt.Errorf("invalid axis encoding")
	}
	for _, r := range string(a) {
		if unicode.IsControl(r) || unicode.IsSpace(r) || r == '/' || r == '\\' {
			return crypto.Scope{}, fmt.Errorf("invalid axis label")
		}
	}
	var y bytes.Buffer
	if _, err := y.Write([]byte("scope-v1")); err != nil {
		return crypto.Scope{}, err
	}
	if err := binary.Write(&y, binary.BigEndian, uint32(len(x))); err != nil {
		return crypto.Scope{}, err
	}
	if _, err := y.Write(x); err != nil {
		return crypto.Scope{}, err
	}
	if err := binary.Write(&y, binary.BigEndian, uint32(b)); err != nil {
		return crypto.Scope{}, err
	}
	z := crypto.Scope{Bytes: append([]byte(nil), y.Bytes()...)}
	if err := z.Valid(); err != nil {
		return crypto.Scope{}, err
	}
	q, err := crypto.ScopeFor(a, b)
	if err != nil {
		return crypto.Scope{}, err
	}
	if !z.Equal(q) {
		return crypto.Scope{}, fmt.Errorf("scope encoding mismatch")
	}
	return z, nil
}
EOF

cat > /app/aperture/sill.go <<'EOF'
package aperture

import (
	"fmt"

	"vaultlab/crypto"
	"vaultlab/keyring"
	"vaultlab/model"
)

func route_s(a model.Frame, b crypto.Scope, c *keyring.Ring) (model.Payload, error) {
	if c == nil {
		return nil, fmt.Errorf("ring unavailable")
	}
	if err := a.StructuralValid(); err != nil {
		return nil, err
	}
	if !c.Has(keyring.Epoch(a.Epoch)) {
		return nil, fmt.Errorf("epoch unavailable")
	}
	x := model.AxisFor(a.Item)
	if x == "" || a.Axis != x {
		return nil, fmt.Errorf("frame authority mismatch")
	}
	if err := b.Valid(); err != nil {
		return nil, err
	}
	y, err := crypto.ScopeFor(x, keyring.Epoch(a.Epoch))
	if err != nil {
		return nil, err
	}
	if !b.Equal(y) {
		return nil, fmt.Errorf("scope mismatch")
	}
	z, err := crypto.Open(a, y, c)
	if err != nil {
		return nil, fmt.Errorf("protected open: %w", err)
	}
	if len(z) == 0 {
		return nil, fmt.Errorf("empty payload")
	}
	return append(model.Payload(nil), z...), nil
}
EOF

cat > /app/ledger/reel.go <<'EOF'
package ledger

import (
	"fmt"

	"vaultlab/keyring"
	"vaultlab/model"
)

func replay_t(a *Journal, b model.ItemID, c model.AxisID, d keyring.Epoch) (*model.Frame, error) {
	if a == nil {
		return nil, fmt.Errorf("journal unavailable")
	}
	if err := b.Valid(); err != nil {
		return nil, err
	}
	if c == "" || c != model.AxisFor(b) || d == 0 {
		return nil, fmt.Errorf("invalid journal query")
	}
	seen := make(map[uint64]bool)
	var best *model.Frame
	for _, x := range a.Frames() {
		if err := x.StructuralValid(); err != nil {
			return nil, err
		}
		if seen[x.Seq] {
			return nil, fmt.Errorf("duplicate journal sequence")
		}
		seen[x.Seq] = true
		if !x.Item.Equal(b) {
			continue
		}
		if x.Axis != c || x.Axis != model.AxisFor(x.Item) {
			continue
		}
		e := keyring.Epoch(x.Epoch)
		if e == 0 || e > d {
			continue
		}
		if best == nil || x.Seq > best.Seq {
			y := x.Clone()
			best = &y
			continue
		}
		if best.Seq == x.Seq {
			return nil, fmt.Errorf("ambiguous journal sequence")
		}
	}
	if best == nil {
		return nil, fmt.Errorf("no prior frame")
	}
	if !best.Item.Equal(b) || best.Axis != c {
		return nil, fmt.Errorf("journal selection mismatch")
	}
	if keyring.Epoch(best.Epoch) > d {
		return nil, fmt.Errorf("journal epoch out of range")
	}
	out := best.Clone()
	return &out, nil
}
EOF

gofmt -w /app/conductor/arc.go /app/tenant/spine.go /app/aperture/sill.go /app/ledger/reel.go
make build
