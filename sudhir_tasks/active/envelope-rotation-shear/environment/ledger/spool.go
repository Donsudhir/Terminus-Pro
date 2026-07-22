package ledger

import "sort"

type SpoolRow struct {
	Bucket string `json:"bucket"`
	Count  int    `json:"count"`
}

func replay_v(index []IndexRow) []SpoolRow {
	counts := make(map[string]int)
	for _, row := range index {
		switch {
		case row.Count <= 1:
			counts["single"]++
		case row.Count == 2:
			counts["paired"]++
		default:
			counts["dense"]++
		}
	}
	names := make([]string, 0, len(counts))
	for name := range counts {
		names = append(names, name)
	}
	sort.Strings(names)
	out := make([]SpoolRow, 0, len(names))
	for _, name := range names {
		out = append(out, SpoolRow{Bucket: name, Count: counts[name]})
	}
	return out
}

func SpoolCounts(journal *Journal) []SpoolRow {
	return replay_v(BuildIndex(journal))
}
