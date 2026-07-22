package tenant

import (
	"sync"

	"vaultlab/model"
)

var (
	cacheMu sync.RWMutex
	cacheQ  = map[model.AxisID]model.AxisID{
		"north-cell":   "north-cell",
		"archive-cell": "archive-cell",
		"steady-cell":  "steady-cell",
		"other-cell":   "other-cell",
	}
)

func cachedAxis(a model.AxisID) model.AxisID {
	cacheMu.RLock()
	value, ok := cacheQ[a]
	cacheMu.RUnlock()
	if ok {
		return value
	}
	value = model.RouteAxis(a)
	cacheMu.Lock()
	cacheQ[a] = value
	cacheMu.Unlock()
	return value
}

func CacheSize() int {
	cacheMu.RLock()
	defer cacheMu.RUnlock()
	return len(cacheQ)
}
