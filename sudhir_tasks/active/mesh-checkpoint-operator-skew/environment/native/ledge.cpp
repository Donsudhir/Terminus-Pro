#include "span.h"

#include "common.h"

#include <cstddef>

int32_t ledge_stats(const int32_t *a, int32_t b, int32_t *c) {
    if (a == nullptr || c == nullptr || b <= 0 || b > MCOS_MAX_NODES) {
        return MCOS_INVALID;
    }
    int32_t lo = a[0];
    int32_t hi = a[0];
    int64_t sum = 0;
    for (int32_t i = 0; i < b; ++i) {
        if (a[i] < lo) {
            lo = a[i];
        }
        if (a[i] > hi) {
            hi = a[i];
        }
        sum += a[i];
    }
    c[0] = lo;
    c[1] = hi;
    c[2] = static_cast<int32_t>(sum / b);
    c[3] = b;
    return MCOS_OK;
}
