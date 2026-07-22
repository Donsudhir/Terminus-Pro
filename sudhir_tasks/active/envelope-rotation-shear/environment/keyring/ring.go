package keyring

import (
	"bufio"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

type Ring struct {
	active Epoch
	keys   map[Epoch][]byte
}

func home(parts ...string) string {
	root := os.Getenv("VAULT_HOME")
	if root == "" {
		root = "/app"
	}
	return filepath.Join(append([]string{root}, parts...)...)
}

func LoadDefault() (*Ring, error) {
	f, err := os.Open(home("config", "ring.toml"))
	if err != nil {
		return nil, err
	}
	defer f.Close()
	r := &Ring{keys: make(map[Epoch][]byte)}
	scan := bufio.NewScanner(f)
	for scan.Scan() {
		line := strings.TrimSpace(scan.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		parts := strings.SplitN(line, "=", 2)
		if len(parts) != 2 {
			return nil, fmt.Errorf("invalid ring line")
		}
		name := strings.TrimSpace(parts[0])
		raw := strings.Trim(strings.TrimSpace(parts[1]), "\"")
		if name == "active" {
			n, err := strconv.ParseUint(raw, 10, 32)
			if err != nil {
				return nil, fmt.Errorf("invalid active epoch: %w", err)
			}
			r.active = Epoch(n)
			continue
		}
		if !strings.HasPrefix(name, "epoch_") {
			continue
		}
		n, err := strconv.ParseUint(strings.TrimPrefix(name, "epoch_"), 10, 32)
		if err != nil {
			return nil, fmt.Errorf("invalid epoch name: %w", err)
		}
		key, err := hex.DecodeString(raw)
		if err != nil {
			return nil, fmt.Errorf("invalid epoch material: %w", err)
		}
		r.keys[Epoch(n)] = key
	}
	if err := scan.Err(); err != nil {
		return nil, err
	}
	if r.active == 0 || len(r.keys[r.active]) == 0 {
		return nil, fmt.Errorf("active epoch unavailable")
	}
	return r, nil
}

func (r *Ring) Active() Epoch {
	return r.active
}

func (r *Ring) Key(e Epoch) ([]byte, error) {
	key, ok := r.keys[e]
	if !ok {
		return nil, fmt.Errorf("epoch unavailable")
	}
	copyKey := append([]byte(nil), key...)
	return copyKey, nil
}

func (r *Ring) Has(e Epoch) bool {
	_, ok := r.keys[e]
	return ok
}
