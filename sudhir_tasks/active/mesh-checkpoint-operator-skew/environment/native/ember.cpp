#include "span.h"

#include "common.h"

#include <cmath>
#include <cstddef>

int32_t ember_step(double *u, const double *x, int32_t n, double dt) {
    if (u == nullptr || x == nullptr || n < 2 || n > MCOS_MAX_NODES) {
        return MCOS_INVALID;
    }
    double next[MCOS_MAX_NODES];
    for (int32_t i = 0; i < n; ++i) {
        next[i] = u[i];
    }
    for (int32_t i = 1; i < n - 1; ++i) {
        const double left = u[i - 1];
        const double right = u[i + 1];
        const double mid = u[i];
        const double force = 0.15 * std::sin(x[i] * 3.141592653589793);
        next[i] = mid + dt * ((left - 2.0 * mid + right) + force);
    }
    next[0] = u[0];
    next[n - 1] = u[n - 1];
    for (int32_t i = 0; i < n; ++i) {
        u[i] = next[i];
    }
    return MCOS_OK;
}

int32_t ember_remap(const double *u_old, int32_t n_old, double *u_new, int32_t n_new) {
    if (u_old == nullptr || u_new == nullptr || n_old < 2 || n_new < 2 ||
        n_old > MCOS_MAX_NODES || n_new > MCOS_MAX_NODES) {
        return MCOS_INVALID;
    }
    for (int32_t j = 0; j < n_new; ++j) {
        const double t = static_cast<double>(j) / static_cast<double>(n_new - 1);
        const double src = t * static_cast<double>(n_old - 1);
        const int32_t i0 = static_cast<int32_t>(src);
        const int32_t i1 = (i0 + 1 < n_old) ? i0 + 1 : i0;
        const double frac = src - static_cast<double>(i0);
        u_new[j] = u_old[i0] * (1.0 - frac) + u_old[i1] * frac;
    }
    return MCOS_OK;
}
