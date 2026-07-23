#ifndef DHDR_LEDGE_H
#define DHDR_LEDGE_H

#include <stdint.h>

int32_t braid_q(const int32_t *a, int32_t b, uint64_t *c);
int32_t brim_banner(const double *u, int32_t n, double *out);
int32_t ember_step(double *u, const double *x, int32_t n, double dt);
int32_t ember_remap(const double *u_old, int32_t n_old, double *u_new, int32_t n_new);
int32_t ember_tally(const double *u, const double *x, int32_t n, double *r);
int32_t ember_mag(const double *r, int32_t n, double *out);
int32_t sift_s(const uint64_t *a, int32_t b, uint64_t *c);

#endif
