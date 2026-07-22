package tenant

import (
	"strings"
	"unicode"
)

func settle_v(raw string) string {
	var out strings.Builder
	space := false
	for _, r := range strings.TrimSpace(raw) {
		if unicode.IsSpace(r) || r == '_' || r == '-' {
			space = out.Len() > 0
			continue
		}
		if space {
			out.WriteByte(' ')
			space = false
		}
		out.WriteRune(unicode.ToLower(r))
	}
	return out.String()
}

func RelayLabel(raw string) string {
	label := settle_v(raw)
	if label == "" {
		return "unlabeled"
	}
	return label
}
