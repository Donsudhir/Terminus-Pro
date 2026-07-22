#ifndef SJCC_RIDGE_H
#define SJCC_RIDGE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int ridge_eval(const double *coeff, int32_t rows, int32_t cols, int32_t nnz,
               const int32_t *row_ptr, const int32_t *col_idx, const double *x,
               double *r);

int ridge_companion(const double *coeff, int32_t rows, int32_t cols, int32_t nnz,
                    const int32_t *row_ptr, const int32_t *col_idx, const double *v,
                    double *out);

#ifdef __cplusplus
}
#endif

#endif
