#ifndef SJCC_COMMON_H
#define SJCC_COMMON_H

#include <stdint.h>

#define SJCC_OK 0
#define SJCC_INVALID -1
#define SJCC_OVERFLOW -2

#define SJCC_MAX_COLS 64
#define SJCC_MAX_ROWS 64
#define SJCC_MAX_GROUPS 32

int quill_tint(double *r, int32_t m);
int quill_companion(int32_t n, double *out);

#endif
