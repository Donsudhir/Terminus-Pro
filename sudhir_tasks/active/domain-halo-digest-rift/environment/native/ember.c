#include "ledge.h"

#include "common.h"

#include <math.h>
#include <stddef.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int32_t ember_step(double *u, const double *x, int32_t n, double dt) {
    double next[DHDR_MAX_NODES];
    int32_t i;

    if (u == NULL || x == NULL || n < 2 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    memcpy(next, u, (size_t)n * sizeof(double));
    for (i = 1; i < n - 1; ++i) {
        double left = u[i - 1];
        double right = u[i + 1];
        double mid = u[i];
        double force = 0.15 * sin(x[i] * M_PI);
        next[i] = mid + dt * ((left - 2.0 * mid + right) + force);
    }
    next[0] = u[0];
    next[n - 1] = u[n - 1];
    memcpy(u, next, (size_t)n * sizeof(double));
    return DHDR_OK;
}

int32_t ember_remap(const double *u_old, int32_t n_old, double *u_new, int32_t n_new) {
    int32_t j;

    if (u_old == NULL || u_new == NULL || n_old < 2 || n_new < 2 ||
        n_old > DHDR_MAX_NODES || n_new > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    for (j = 0; j < n_new; ++j) {
        double t = (double)j / (double)(n_new - 1);
        double src = t * (double)(n_old - 1);
        int32_t i0 = (int32_t)src;
        int32_t i1 = (i0 + 1 < n_old) ? i0 + 1 : i0;
        double frac = src - (double)i0;
        u_new[j] = u_old[i0] * (1.0 - frac) + u_old[i1] * frac;
    }
    return DHDR_OK;
}

int32_t ember_tally(const double *u, const double *x, int32_t n, double *r) {
    int32_t i;

    if (u == NULL || x == NULL || r == NULL || n < 2 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    r[0] = 0.0;
    r[n - 1] = 0.0;
    for (i = 1; i < n - 1; ++i) {
        double left = u[i - 1];
        double right = u[i + 1];
        double mid = u[i];
        double force = 0.15 * sin(x[i] * M_PI);
        r[i] = (left - 2.0 * mid + right) + force;
    }
    return DHDR_OK;
}

int32_t ember_mag(const double *r, int32_t n, double *out) {
    double acc;
    int32_t i;

    if (r == NULL || out == NULL || n <= 0 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    acc = 0.0;
    for (i = 0; i < n; ++i) {
        acc += r[i] * r[i];
    }
    *out = sqrt(acc);
    return DHDR_OK;
}

int32_t sift_s(const uint64_t *a, int32_t b, uint64_t *c) {
    int32_t n;
    int32_t i;
    int32_t k;
    uint64_t h;
    uint64_t bits;
    unsigned char raw[8];

    if (a == NULL || c == NULL || b <= 0 || b > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    n = b;
    h = 0xCBF29CE484222325ULL;

    for (i = 0; i < n; ++i) {
        bits = a[n + i];
        memcpy(raw, &bits, 8);
        for (k = 0; k < 8; ++k) {
            h ^= (uint64_t)raw[k];
            h *= 0x100000001B3ULL;
        }
    }

    *c = h;
    return DHDR_OK;
}
