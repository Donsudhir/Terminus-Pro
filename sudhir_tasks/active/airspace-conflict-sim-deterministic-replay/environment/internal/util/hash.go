package util

import (
	"crypto/sha256"
	"encoding/hex"
)

func SHA256Hex(text string) string {
	h := sha256.Sum256([]byte(text))
	return hex.EncodeToString(h[:])
}
