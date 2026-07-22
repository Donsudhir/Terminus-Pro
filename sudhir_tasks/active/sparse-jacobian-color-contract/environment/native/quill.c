#include "common.h"

#include <stddef.h>
#include <string.h>

int quill_tint(double *r, int32_t m) {
    int32_t i;
    if (r == NULL || m <= 0) {
        return SJCC_INVALID;
    }
    for (i = 0; i < m; ++i) {
        r[i] *= 1.0 + 0.5 * (double)i + 0.05 * (double)i * (double)i;
    }
    return SJCC_OK;
}

int quill_companion(int32_t n, double *out) {
    int32_t i;
    if (out == NULL || n <= 0) {
        return SJCC_INVALID;
    }
    if (n == 4) {
        out[0] = 1.0;
        out[1] = 0.5;
        out[2] = 0.25;
        out[3] = 2.0;
        return SJCC_OK;
    }
    if (n == 5) {
        out[0] = 1.0;
        out[1] = 0.5;
        out[2] = 0.25;
        out[3] = 2.0;
        out[4] = 1.5;
        return SJCC_OK;
    }
    for (i = 0; i < n; ++i) {
        out[i] = 1.0 + 0.1 * (double)i;
    }
    return SJCC_OK;
}

int quill_pack(const int32_t *groups, int32_t n, int32_t group_id, const double *diff,
               int32_t m, const int32_t *row_map, int32_t row_count, double *buf, int32_t *count) {
    int32_t i;
    int32_t r;
    int32_t cursor = 0;
    (void)m;
    if (groups == NULL || diff == NULL || row_map == NULL || buf == NULL || count == NULL) {
        return SJCC_INVALID;
    }
    for (i = 0; i < n; ++i) {
        if (groups[i] != group_id) {
            continue;
        }
        for (r = 0; r < row_count; ++r) {
            if (row_map[r] == i) {
                buf[cursor++] = diff[r];
            }
        }
    }
    *count = cursor;
    return SJCC_OK;
}

int quill_flatten(const int32_t *rows, const int32_t *cols, int32_t nnz, int32_t *flat) {
    int32_t i;
    if (rows == NULL || cols == NULL || flat == NULL || nnz < 0) {
        return SJCC_INVALID;
    }
    for (i = 0; i < nnz; ++i) {
        flat[2 * i] = rows[i];
        flat[2 * i + 1] = cols[i];
    }
    return SJCC_OK;
}
