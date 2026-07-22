#ifndef SERIES_H
#define SERIES_H

#include <stdint.h>

#define SERIES_NEGATIVE (-1)
#define SERIES_POSITIVE 1
#define SERIES_REFINE 2
#define SERIES_INVALID 3

int eval_band(const double *a, const double *b, int32_t n, double *c);

#endif
