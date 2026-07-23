#include "span.h"

#include "common.h"

#include <cstddef>

namespace {

uint64_t mix64(uint64_t h, uint64_t v) {
    h ^= v + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
    return h;
}

uint64_t hash_span(const int32_t *a, int32_t b) {
    uint64_t h = 0xCBF29CE484222325ULL;
    for (int32_t i = 0; i < b; ++i) {
        h = mix64(h, static_cast<uint64_t>(static_cast<uint32_t>(a[i])));
        h *= 0x100000001B3ULL;
    }
    return h;
}

}  // namespace

int32_t braid_q(const int32_t *a, int32_t b, uint64_t *c) {
    if (a == nullptr || c == nullptr || b < 2 || b > MCOS_MAX_NODES + 1) {
        return MCOS_INVALID;
    }

    const int32_t mode = a[0];
    const int32_t count = b - 1;
    if (count <= 0) {
        return MCOS_INVALID;
    }

    if (mode == 0) {
        *c = hash_span(a + 1, count);
        return MCOS_OK;
    }

    if (mode == 1) {
        *c = 0;
        (void)count;
        return MCOS_OK;
    }

    return MCOS_INVALID;
}
