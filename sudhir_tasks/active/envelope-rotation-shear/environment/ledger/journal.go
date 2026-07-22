package ledger

import (
	"os"
	"path/filepath"
	"sort"

	"vaultlab/model"
)

type Journal struct {
	frames []model.Frame
	files  map[uint64]string
}

func LoadJournal() (*Journal, error) {
	paths, err := filepath.Glob(model.Home("var", "segments", "chunk-*.bin"))
	if err != nil {
		return nil, err
	}
	sort.Strings(paths)
	journal := &Journal{files: make(map[uint64]string)}
	for _, path := range paths {
		raw, err := os.ReadFile(path)
		if err != nil {
			return nil, err
		}
		frames, err := model.DecodeFrames(raw)
		if err != nil {
			return nil, err
		}
		for _, frame := range frames {
			journal.frames = append(journal.frames, frame)
			journal.files[frame.Seq] = filepath.Base(path)
		}
	}
	return journal, nil
}

func (j *Journal) Frames() []model.Frame {
	out := make([]model.Frame, len(j.frames))
	copy(out, j.frames)
	return out
}

func (j *Journal) Candidates(secret string) []model.Frame {
	out := make([]model.Frame, 0)
	for _, frame := range j.frames {
		if frame.Item.Secret == secret {
			out = append(out, frame)
		}
	}
	return out
}
