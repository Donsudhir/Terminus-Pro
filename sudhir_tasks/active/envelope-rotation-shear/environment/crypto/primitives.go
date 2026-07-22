package crypto

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
)

func Mac(key []byte, parts ...[]byte) []byte {
	h := hmac.New(sha256.New, key)
	for _, part := range parts {
		_, _ = h.Write(part)
	}
	return h.Sum(nil)
}

func Equal(a, b []byte) bool {
	return hmac.Equal(a, b)
}

func EncodeText(raw []byte) string {
	return base64.RawStdEncoding.EncodeToString(raw)
}

func DecodeText(raw string) ([]byte, error) {
	out, err := base64.RawStdEncoding.DecodeString(raw)
	if err != nil {
		return nil, fmt.Errorf("invalid protected text: %w", err)
	}
	return out, nil
}

func Xor(a, b []byte) ([]byte, error) {
	if len(a) != len(b) {
		return nil, fmt.Errorf("length mismatch")
	}
	out := make([]byte, len(a))
	for i := range a {
		out[i] = a[i] ^ b[i]
	}
	return out, nil
}

func Stream(key, nonce []byte, n int) []byte {
	out := make([]byte, 0, n)
	for counter := uint32(0); len(out) < n; counter++ {
		block := Mac(key, []byte("stream-v1"), nonce, []byte{
			byte(counter >> 24), byte(counter >> 16), byte(counter >> 8), byte(counter),
		})
		out = append(out, block...)
	}
	return out[:n]
}
