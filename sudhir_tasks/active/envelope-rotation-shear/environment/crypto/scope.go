package crypto

import (
	"bytes"
	"encoding/binary"
	"fmt"

	"vaultlab/keyring"
	"vaultlab/model"
)

type Scope struct {
	Bytes []byte
}

func ScopeFor(a model.AxisID, b keyring.Epoch) (Scope, error) {
	if a == "" || b == 0 {
		return Scope{}, fmt.Errorf("invalid scope input")
	}
	raw := []byte(a)
	var out bytes.Buffer
	_, _ = out.Write([]byte("scope-v1"))
	_ = binary.Write(&out, binary.BigEndian, uint32(len(raw)))
	_, _ = out.Write(raw)
	_ = binary.Write(&out, binary.BigEndian, uint32(b))
	return Scope{Bytes: out.Bytes()}, nil
}

func (s Scope) Valid() error {
	if len(s.Bytes) < 17 {
		return fmt.Errorf("short scope")
	}
	if !bytes.HasPrefix(s.Bytes, []byte("scope-v1")) {
		return fmt.Errorf("scope domain mismatch")
	}
	return nil
}

func (s Scope) Equal(other Scope) bool {
	return Equal(s.Bytes, other.Bytes)
}
