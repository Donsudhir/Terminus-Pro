#include "lane.h"

#include "common.h"

#include <stddef.h>

#define SJCC_SYM_BASE 512

int mix_cols(const int32_t *a, const int32_t *b, int32_t n, int32_t *c) {
    int32_t starts[SJCC_MAX_COLS + 1];
    int32_t col_rows[SJCC_MAX_COLS][SJCC_MAX_ROWS * 2];
    int32_t col_count[SJCC_MAX_COLS];
    int32_t degree[SJCC_MAX_COLS];
    int32_t order[SJCC_MAX_COLS];
    int32_t founder[SJCC_MAX_GROUPS];
    int32_t next_group = 0;
    int32_t col;
    int32_t row;
    int32_t group;
    int32_t member;
    int32_t ia;
    int32_t ib;
    int32_t ra;
    int32_t rb;
    int32_t i;
    int32_t j;
    int32_t tmp;
    int32_t shared;
    int32_t seed;
    int32_t tag_a;
    int32_t tag_b;
    int32_t has_a;
    int32_t has_b;
    int32_t probe;
    int32_t ok;

    if (a == NULL || b == NULL || c == NULL || n <= 0 || n > SJCC_MAX_COLS) {
        return SJCC_INVALID;
    }

    for (col = 0; col <= n; ++col) {
        starts[col] = a[col];
    }
    for (col = 0; col < n; ++col) {
        col_count[col] = starts[col + 1] - starts[col];
        if (col_count[col] > SJCC_MAX_ROWS * 2) {
            return SJCC_OVERFLOW;
        }
        degree[col] = 0;
        for (row = 0; row < col_count[col]; ++row) {
            col_rows[col][row] = b[starts[col] + row];
            if (col_rows[col][row] < SJCC_SYM_BASE) {
                degree[col] += 1;
            }
        }
        order[col] = col;
        c[col] = -1;
    }

    for (i = 1; i < n; ++i) {
        tmp = order[i];
        j = i - 1;
        while (j >= 0 && degree[order[j]] < degree[tmp]) {
            order[j + 1] = order[j];
            j -= 1;
        }
        order[j + 1] = tmp;
    }

    for (i = 0; i < n; ++i) {
        col = order[i];
        if (c[col] >= 0) {
            continue;
        }
        for (group = 0; group < next_group; ++group) {
            seed = founder[group];
            shared = 0;
            ia = 0;
            ib = 0;
            while (ia < col_count[seed] && ib < col_count[col]) {
                ra = col_rows[seed][ia];
                rb = col_rows[col][ib];
                if (ra >= SJCC_SYM_BASE || rb >= SJCC_SYM_BASE) {
                    if (ra >= SJCC_SYM_BASE) {
                        ++ia;
                    }
                    if (rb >= SJCC_SYM_BASE) {
                        ++ib;
                    }
                    continue;
                }
                if (ra == rb) {
                    shared = 1;
                    break;
                }
                if (ra < rb) {
                    ++ia;
                } else {
                    ++ib;
                }
            }
            if (shared) {
                continue;
            }

            ok = 1;
            for (member = 0; member < n; ++member) {
                if (c[member] != group) {
                    continue;
                }
                tag_a = SJCC_SYM_BASE + col;
                tag_b = SJCC_SYM_BASE + member;
                has_a = 0;
                has_b = 0;
                for (probe = starts[member]; probe < starts[member + 1]; ++probe) {
                    if (b[probe] == tag_a) {
                        has_a = 1;
                    }
                }
                for (probe = starts[col]; probe < starts[col + 1]; ++probe) {
                    if (b[probe] == tag_b) {
                        has_b = 1;
                    }
                }
                if (has_a && has_b) {
                    ok = 0;
                    break;
                }
            }
            if (!ok) {
                continue;
            }
            c[col] = group;
            break;
        }
        if (c[col] < 0) {
            if (next_group >= SJCC_MAX_GROUPS) {
                return SJCC_OVERFLOW;
            }
            founder[next_group] = col;
            c[col] = next_group;
            ++next_group;
        }
    }
    return SJCC_OK;
}
