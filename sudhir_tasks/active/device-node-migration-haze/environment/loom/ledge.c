#include "loom.h"

#include "common.h"

#include <stddef.h>

/* Decoy: count ordinary-looking ledger bytes for diagnostic banners. */
int32_t ledge_tally(const uint8_t *a, size_t b, int32_t *c) {
    size_t i;
    int32_t zeros = 0;
    int32_t nonzero = 0;

    if (a == NULL || c == NULL) {
        return HAZE_INVALID;
    }
    for (i = 0; i < b; ++i) {
        if (a[i] == 0) {
            zeros += 1;
        } else {
            nonzero += 1;
        }
    }
    c[0] = zeros;
    c[1] = nonzero;
    c[2] = (int32_t)b;
    return HAZE_OK;
}
