#include "ledge.h"

#include "common.h"

#include <stddef.h>

static uint64_t mix64(uint64_t h, uint64_t v) {
    h ^= v + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
    return h;
}

static uint64_t hash_span(const int32_t *a, int32_t b) {
    uint64_t h = 0xCBF29CE484222325ULL;
    int32_t i;
    for (i = 0; i < b; ++i) {
        h = mix64(h, (uint64_t)(uint32_t)a[i]);
        h *= 0x100000001B3ULL;
    }
    return h;
}

int32_t braid_q(const int32_t *a, int32_t b, uint64_t *c) {
    int32_t mode;
    int32_t count;

    if (a == NULL || c == NULL || b < 2 || b > DHDR_MAX_NODES + 1) {
        return DHDR_INVALID;
    }

    mode = a[0];
    count = b - 1;
    if (count <= 0) {
        return DHDR_INVALID;
    }

    if (mode == 0) {
        *c = hash_span(a + 1, count);
        return DHDR_OK;
    }

    if (mode == 1) {
        *c = 0;
        (void)count;
        return DHDR_OK;
    }

    return DHDR_INVALID;
}
