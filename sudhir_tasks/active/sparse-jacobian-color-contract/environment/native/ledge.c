#include "lane.h"

#include "common.h"

#include <stddef.h>

int ledge_stats(const int32_t *a, const int32_t *b, int32_t n, int32_t *c) {
    int32_t col;
    int32_t row;
    int32_t total = 0;
    int32_t max_degree = 0;

    if (a == NULL || b == NULL || c == NULL || n <= 0) {
        return SJCC_INVALID;
    }

    for (col = 0; col < n; ++col) {
        int32_t degree = a[col + 1] - a[col];
        if (degree > max_degree) {
            max_degree = degree;
        }
        for (row = a[col]; row < a[col + 1]; ++row) {
            total += b[row];
        }
    }
    c[0] = total;
    c[1] = max_degree;
    c[2] = n;
    return SJCC_OK;
}
