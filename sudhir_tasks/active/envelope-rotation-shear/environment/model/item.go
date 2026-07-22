package model

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strings"
	"unicode"
)

type ItemID struct {
	Service string `json:"service"`
	Secret  string `json:"secret"`
}

func (i ItemID) Valid() error {
	if len(i.Service) < 2 || len(i.Service) > 96 {
		return fmt.Errorf("invalid service label")
	}
	if len(i.Secret) < 2 || len(i.Secret) > 96 {
		return fmt.Errorf("invalid secret label")
	}
	for _, part := range []string{i.Service, i.Secret} {
		for _, r := range part {
			if unicode.IsControl(r) || unicode.IsSpace(r) || r == '/' || r == '\\' {
				return fmt.Errorf("invalid item label")
			}
		}
	}
	return nil
}

func (i ItemID) Equal(other ItemID) bool {
	return i.Service == other.Service && i.Secret == other.Secret
}

func AxisFor(i ItemID) AxisID {
	return AxisID(i.Service)
}

func RouteAxis(a AxisID) AxisID {
	sum := sha256.Sum256([]byte(strings.ToLower(string(a))))
	return AxisID(hex.EncodeToString(sum[:6]))
}

func (i ItemID) Key() string {
	return i.Service + "\x00" + i.Secret
}
