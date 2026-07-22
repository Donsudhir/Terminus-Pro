#include "include/window.h"

#include <math.h>
#include <stddef.h>

int eval_frame(const double *a, int32_t b, double *c, double *d) {
    int32_t i;
    double low;
    double high;

    if (a == NULL || c == NULL || d == NULL || b <= 0) {
        return -1;
    }
    low = a[0];
    high = a[0];
    if (!isfinite(low)) {
        return -1;
    }
    for (i = 1; i < b; ++i) {
        if (!isfinite(a[i])) {
            return -1;
        }
        if (a[i] < low) {
            low = a[i];
        }
        if (a[i] > high) {
            high = a[i];
        }
    }
    *c = low;
    *d = high;
    return 0;
}
