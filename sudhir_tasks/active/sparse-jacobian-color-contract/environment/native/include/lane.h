#ifndef SJCC_LANE_H
#define SJCC_LANE_H

#include <stdint.h>

int mix_cols(const int32_t *a, const int32_t *b, int32_t n, int32_t *c);
int ledge_stats(const int32_t *a, const int32_t *b, int32_t n, int32_t *c);

#endif
