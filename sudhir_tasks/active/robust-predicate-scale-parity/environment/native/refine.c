#include "include/refine.h"

#include <stddef.h>

static int sign_wide(__int128 a) {
    if (a < 0) {
        return -1;
    }
    if (a > 0) {
        return 1;
    }
    return 0;
}

int refine_orient3d(const int64_t *a) {
    __int128 ax;
    __int128 ay;
    __int128 az;
    __int128 bx;
    __int128 by;
    __int128 bz;
    __int128 cx;
    __int128 cy;
    __int128 cz;
    __int128 value;

    if (a == NULL) {
        return 0;
    }
    ax = (__int128)a[0] - (__int128)a[9];
    ay = (__int128)a[1] - (__int128)a[10];
    az = (__int128)a[2] - (__int128)a[11];
    bx = (__int128)a[3] - (__int128)a[9];
    by = (__int128)a[4] - (__int128)a[10];
    bz = (__int128)a[5] - (__int128)a[11];
    cx = (__int128)a[6] - (__int128)a[9];
    cy = (__int128)a[7] - (__int128)a[10];
    cz = (__int128)a[8] - (__int128)a[11];
    value = ax * (by * cz - bz * cy)
          - ay * (bx * cz - bz * cx)
          + az * (bx * cy - by * cx);
    return sign_wide(value);
}

int refine_insphere(const int64_t *a) {
    __int128 matrix[4][4];
    __int128 determinant = 0;
    int permutation[4];
    int row;
    int i;
    int j;
    int k;
    int l;

    if (a == NULL) {
        return 0;
    }
    for (row = 0; row < 4; ++row) {
        __int128 x = (__int128)a[row * 3] - (__int128)a[12];
        __int128 y = (__int128)a[row * 3 + 1] - (__int128)a[13];
        __int128 z = (__int128)a[row * 3 + 2] - (__int128)a[14];
        matrix[row][0] = x;
        matrix[row][1] = y;
        matrix[row][2] = z;
        matrix[row][3] = x * x + y * y + z * z;
    }
    for (i = 0; i < 4; ++i) {
        for (j = 0; j < 4; ++j) {
            if (j == i) {
                continue;
            }
            for (k = 0; k < 4; ++k) {
                int inversions = 0;
                __int128 term = 1;
                if (k == i || k == j) {
                    continue;
                }
                for (l = 0; l < 4; ++l) {
                    if (l == i || l == j || l == k) {
                        continue;
                    }
                    permutation[0] = i;
                    permutation[1] = j;
                    permutation[2] = k;
                    permutation[3] = l;
                    for (row = 0; row < 4; ++row) {
                        int right;
                        term *= matrix[row][permutation[row]];
                        for (right = row + 1; right < 4; ++right) {
                            if (permutation[row] > permutation[right]) {
                                ++inversions;
                            }
                        }
                    }
                    if ((inversions & 1) == 0) {
                        determinant += term;
                    } else {
                        determinant -= term;
                    }
                }
            }
        }
    }
    return sign_wide(determinant);
}
