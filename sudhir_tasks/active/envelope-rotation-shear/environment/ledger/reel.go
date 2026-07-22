package ledger

import (
	"fmt"

	"vaultlab/keyring"
	"vaultlab/model"
)

func replay_t(a *Journal, b model.ItemID, c model.AxisID, d keyring.Epoch) (*model.Frame, error) {
	var best *model.Frame
	for _, frame := range a.Candidates(b.Secret) {
		if keyring.Epoch(frame.Epoch) > d {
			continue
		}
		if best == nil || frame.Seq > best.Seq {
			copyFrame := frame
			best = &copyFrame
		}
	}
	if best == nil {
		return nil, fmt.Errorf("no prior frame")
	}
	return best, nil
}
