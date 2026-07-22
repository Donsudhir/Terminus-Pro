package keyring

import (
	"crypto/sha256"
	"encoding/hex"
	"sort"
)

type Entry struct {
	Epoch       Epoch
	Fingerprint string
	Active      bool
}

func (r *Ring) Catalog() []Entry {
	epochs := make([]int, 0, len(r.keys))
	for epoch := range r.keys {
		epochs = append(epochs, int(epoch))
	}
	sort.Ints(epochs)
	out := make([]Entry, 0, len(epochs))
	for _, n := range epochs {
		epoch := Epoch(n)
		sum := sha256.Sum256(r.keys[epoch])
		out = append(out, Entry{
			Epoch:       epoch,
			Fingerprint: hex.EncodeToString(sum[:6]),
			Active:      epoch == r.active,
		})
	}
	return out
}
