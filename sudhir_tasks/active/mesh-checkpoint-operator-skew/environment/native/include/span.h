#ifndef MCOS_SPAN_H
#define MCOS_SPAN_H

#include <cstdint>

extern "C" {
int32_t braid_q(const int32_t *a, int32_t b, uint64_t *c);
int32_t ledge_stats(const int32_t *a, int32_t b, int32_t *c);
int32_t ember_step(double *u, const double *x, int32_t n, double dt);
int32_t ember_remap(const double *u_old, int32_t n_old, double *u_new, int32_t n_new);
}

#endif
