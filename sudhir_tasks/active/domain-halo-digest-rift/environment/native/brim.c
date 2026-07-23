#include "ledge.h"

#include "common.h"

#include <math.h>
#include <stddef.h>

/* Decoy: local norm banner for diagnostic lines only. */
int32_t brim_banner(const double *u, int32_t n, double *out) {
    double acc;
    int32_t i;

    if (u == NULL || out == NULL || n <= 0 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    acc = 0.0;
    for (i = 0; i < n; ++i) {
        acc += u[i] * u[i];
    }
    *out = sqrt(acc);
    return DHDR_OK;
}
