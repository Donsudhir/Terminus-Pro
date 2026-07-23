#ifndef HAZE_OPEN_PROBE_H
#define HAZE_OPEN_PROBE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Read project special header; returns HAZE_OK and fills *out_id. */
int32_t probe_identity(const char *path, uint64_t *out_id);

/* Confirm the target is openable under the project contract. */
int32_t probe_openable(const char *path);

/* Validate kind is an accepted special kind (char/block). */
int32_t probe_kind_ok(uint64_t id);

#ifdef __cplusplus
}
#endif

#endif
