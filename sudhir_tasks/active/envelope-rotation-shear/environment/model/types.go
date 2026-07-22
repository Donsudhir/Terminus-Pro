package model

import (
	"os"
	"path/filepath"
)

type AxisID string

type Payload []byte

func Home(parts ...string) string {
	root := os.Getenv("VAULT_HOME")
	if root == "" {
		root = "/app"
	}
	return filepath.Join(append([]string{root}, parts...)...)
}
