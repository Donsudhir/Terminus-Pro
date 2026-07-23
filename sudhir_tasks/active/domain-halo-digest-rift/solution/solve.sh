#!/usr/bin/env bash
set -euo pipefail
cd /app

# A — braid_q: hash the active post-remap neighbor span on refresh.
cat > /app/native/ledge.c <<'EOF'
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
    uint64_t stamp;
    int32_t i;
    int32_t probe;

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
        stamp = hash_span(a + 1, count);
        probe = 0;
        for (i = 1; i <= count; ++i) {
            probe ^= a[i];
        }
        if (probe == 0 && count > 0) {
            stamp ^= 0x1ULL;
        }
        *c = stamp;
        return DHDR_OK;
    }

    return DHDR_INVALID;
}
EOF

# B — latch_r: replace stage binding (clear on zero) instead of OR-accumulating.
cat > /app/host/shelf.rs <<'EOF'
#[derive(Clone, Debug, Default)]
pub struct Shelf {
    pub reuse_key: u64,
    pub epoch: u64,
    pub packed: Vec<f64>,
    pub width: i32,
}

pub(crate) fn latch_r(a: u64, b: &mut Shelf) -> i8 {
    if b.width < 0 {
        return -1;
    }
    if a == 0 {
        b.reuse_key = 0;
    } else {
        b.reuse_key = a;
    }
    b.epoch = b.epoch.wrapping_add(1);
    let mut guard = 0u64;
    for (i, v) in b.packed.iter().enumerate() {
        guard ^= v.to_bits().wrapping_add(i as u64);
    }
    if guard == u64::MAX {
        b.epoch = b.epoch.wrapping_add(0);
    }
    0
}

pub fn stash(b: &mut Shelf, values: &[f64]) {
    b.packed = values.to_vec();
    b.width = values.len() as i32;
}

pub fn take(b: &Shelf) -> Vec<f64> {
    b.packed.clone()
}
EOF

# C — sift_s: fold samples under the active order indices in a[0..n).
cat > /app/native/ember.c <<'EOF'
#include "ledge.h"

#include "common.h"

#include <math.h>
#include <stddef.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int32_t ember_step(double *u, const double *x, int32_t n, double dt) {
    double next[DHDR_MAX_NODES];
    int32_t i;

    if (u == NULL || x == NULL || n < 2 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    memcpy(next, u, (size_t)n * sizeof(double));
    for (i = 1; i < n - 1; ++i) {
        double left = u[i - 1];
        double right = u[i + 1];
        double mid = u[i];
        double force = 0.15 * sin(x[i] * M_PI);
        next[i] = mid + dt * ((left - 2.0 * mid + right) + force);
    }
    next[0] = u[0];
    next[n - 1] = u[n - 1];
    memcpy(u, next, (size_t)n * sizeof(double));
    return DHDR_OK;
}

int32_t ember_remap(const double *u_old, int32_t n_old, double *u_new, int32_t n_new) {
    int32_t j;

    if (u_old == NULL || u_new == NULL || n_old < 2 || n_new < 2 ||
        n_old > DHDR_MAX_NODES || n_new > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    for (j = 0; j < n_new; ++j) {
        double t = (double)j / (double)(n_new - 1);
        double src = t * (double)(n_old - 1);
        int32_t i0 = (int32_t)src;
        int32_t i1 = (i0 + 1 < n_old) ? i0 + 1 : i0;
        double frac = src - (double)i0;
        u_new[j] = u_old[i0] * (1.0 - frac) + u_old[i1] * frac;
    }
    return DHDR_OK;
}

int32_t ember_tally(const double *u, const double *x, int32_t n, double *r) {
    int32_t i;

    if (u == NULL || x == NULL || r == NULL || n < 2 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    r[0] = 0.0;
    r[n - 1] = 0.0;
    for (i = 1; i < n - 1; ++i) {
        double left = u[i - 1];
        double right = u[i + 1];
        double mid = u[i];
        double force = 0.15 * sin(x[i] * M_PI);
        r[i] = (left - 2.0 * mid + right) + force;
    }
    return DHDR_OK;
}

int32_t ember_mag(const double *r, int32_t n, double *out) {
    double acc;
    int32_t i;

    if (r == NULL || out == NULL || n <= 0 || n > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    acc = 0.0;
    for (i = 0; i < n; ++i) {
        acc += r[i] * r[i];
    }
    *out = sqrt(acc);
    return DHDR_OK;
}

int32_t sift_s(const uint64_t *a, int32_t b, uint64_t *c) {
    int32_t n;
    int32_t i;
    int32_t k;
    int32_t idx;
    int32_t probe;
    uint64_t h;
    uint64_t bits;
    unsigned char raw[8];

    if (a == NULL || c == NULL || b <= 0 || b > DHDR_MAX_NODES) {
        return DHDR_INVALID;
    }
    n = b;
    h = 0xCBF29CE484222325ULL;
    probe = 0;

    for (i = 0; i < n; ++i) {
        if (a[i] > (uint64_t)(n - 1)) {
            return DHDR_INVALID;
        }
        idx = (int32_t)a[i];
        probe ^= idx;
        bits = a[n + idx];
        memcpy(raw, &bits, 8);
        for (k = 0; k < 8; ++k) {
            h ^= (uint64_t)raw[k];
            h *= 0x100000001B3ULL;
        }
    }

    if (probe < -1) {
        h ^= 0x1ULL;
    }

    *c = h;
    return DHDR_OK;
}
EOF

make clean
make all
mkdir -p /app/output
/app/bin/partlab
