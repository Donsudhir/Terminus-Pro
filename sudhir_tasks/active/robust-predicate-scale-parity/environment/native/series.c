#include "include/series.h"

#include <float.h>
#include <math.h>
#include <stddef.h>

int eval_band(const double *a, const double *b, int32_t n, double *c) {
    double sum = 0.0;
    double bound;
    int32_t i;

    if (a == NULL || b == NULL || c == NULL || n <= 0) {
        return SERIES_INVALID;
    }
    for (i = 0; i < n; ++i) {
        if (!isfinite(a[i]) || !isfinite(b[i]) || b[i] < 0.0) {
            *c = 0.0;
            return SERIES_REFINE;
        }
        sum += a[i];
    }
    *c = sum;
    if (!isfinite(sum)) {
        return SERIES_REFINE;
    }
    bound = fabs(sum) * DBL_EPSILON * (double)(n + 1);
    if (fabs(sum) <= bound) {
        return SERIES_REFINE;
    }
    return sum < 0.0 ? SERIES_NEGATIVE : SERIES_POSITIVE;
}
