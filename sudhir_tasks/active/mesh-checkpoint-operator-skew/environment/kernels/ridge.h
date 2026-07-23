#ifndef MCOS_RIDGE_H
#define MCOS_RIDGE_H

#ifdef __cplusplus
extern "C" {
#endif

int ridge_eval(const double *u, const double *x, int n, double *r);
int ridge_norm(const double *r, int n, double *out);

#ifdef __cplusplus
}
#endif

#endif
