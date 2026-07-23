#ifndef HAZE_COMMON_H
#define HAZE_COMMON_H

#include <stdint.h>

enum {
    HAZE_OK = 0,
    HAZE_INVALID = 1,
    HAZE_REJECT = 2,
    HAZE_IO = 3
};

enum {
    HAZE_KIND_ORD = 0,
    HAZE_KIND_CHAR = 1,
    HAZE_KIND_BLOCK = 2
};

#define HAZE_MAGIC0 'H'
#define HAZE_MAGIC1 'Z'
#define HAZE_MAGIC2 'S'
#define HAZE_MAGIC3 'P'

static inline uint64_t slot_pack(uint8_t kind, uint16_t maj, uint16_t min) {
    return ((uint64_t)kind << 32) | ((uint64_t)maj << 16) | (uint64_t)min;
}

static inline uint8_t slot_kind(uint64_t id) {
    return (uint8_t)((id >> 32) & 0xffu);
}

static inline uint16_t slot_maj(uint64_t id) {
    return (uint16_t)((id >> 16) & 0xffffu);
}

static inline uint16_t slot_min(uint64_t id) {
    return (uint16_t)(id & 0xffffu);
}

#endif
