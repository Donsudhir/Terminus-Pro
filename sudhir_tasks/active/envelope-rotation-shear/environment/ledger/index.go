package ledger

import (
	"fmt"
	"sort"

	"vaultlab/model"
)

type IndexRow struct {
	Item   model.ItemID
	Oldest uint64
	Newest uint64
	Count  int
}

func BuildIndex(journal *Journal) []IndexRow {
	rows := make(map[string]IndexRow)
	for _, frame := range journal.frames {
		key := frame.Item.Key()
		row, ok := rows[key]
		if !ok {
			row = IndexRow{Item: frame.Item, Oldest: frame.Seq, Newest: frame.Seq}
		}
		if frame.Seq < row.Oldest {
			row.Oldest = frame.Seq
		}
		if frame.Seq > row.Newest {
			row.Newest = frame.Seq
		}
		row.Count++
		rows[key] = row
	}
	keys := make([]string, 0, len(rows))
	for key := range rows {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	out := make([]IndexRow, 0, len(keys))
	for _, key := range keys {
		out = append(out, rows[key])
	}
	return out
}

func CheckSegments(journal *Journal) (int, error) {
	seen := make(map[uint64]bool)
	for _, frame := range journal.frames {
		if err := frame.StructuralValid(); err != nil {
			return 0, err
		}
		if frame.Axis != model.AxisFor(frame.Item) {
			return 0, fmt.Errorf("segment authority mismatch")
		}
		if seen[frame.Seq] {
			return 0, fmt.Errorf("duplicate segment sequence")
		}
		seen[frame.Seq] = true
	}
	return len(journal.frames), nil
}
