package crypto

import "fmt"

func WrapKey(a, b []byte, c Scope) ([]byte, error) {
	if len(a) != 32 || len(b) < 24 {
		return nil, fmt.Errorf("invalid key material")
	}
	if err := c.Valid(); err != nil {
		return nil, err
	}
	mask := Mac(b, []byte("wrap-v1"), c.Bytes)
	return Xor(a, mask[:32])
}

func UnwrapKey(a, b []byte, c Scope) ([]byte, error) {
	return WrapKey(a, b, c)
}
