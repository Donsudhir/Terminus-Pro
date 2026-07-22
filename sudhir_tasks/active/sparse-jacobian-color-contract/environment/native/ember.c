#include "common.h"

#include <math.h>
#include <stddef.h>
#include <stdint.h>

int ember_apply(const double *base, double *work, int32_t n, const int32_t *groups, int32_t target,
                uint64_t seed_bits, double step) {
    int32_t i;
    (void)groups;
    (void)target;
    if (base == NULL || work == NULL || n <= 0) {
        return SJCC_INVALID;
    }
    for (i = 0; i < n; ++i) {
        work[i] = base[i];
        if (((seed_bits >> (uint64_t)i) & 1ull) != 0ull) {
            work[i] += step;
        }
    }
    return SJCC_OK;
}

int ember_diff(const double *plus, const double *minus, double *out, int32_t m, double inv_step) {
    int32_t i;
    if (plus == NULL || minus == NULL || out == NULL || m <= 0) {
        return SJCC_INVALID;
    }
    for (i = 0; i < m; ++i) {
        out[i] = (plus[i] - minus[i]) * inv_step;
    }
    return SJCC_OK;
}
