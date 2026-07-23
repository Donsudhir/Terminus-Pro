#ifndef HAZE_LOOM_H
#define HAZE_LOOM_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int loom_stage_set(const char *slot);
void loom_stage_clear(void);

int32_t knit_p(const uint8_t *a, size_t b, uint64_t *c);
int32_t ledge_tally(const uint8_t *a, size_t b, int32_t *c);

#ifdef __cplusplus
}
#endif

#endif
