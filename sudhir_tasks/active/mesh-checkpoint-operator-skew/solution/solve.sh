#!/usr/bin/env bash
set -euo pipefail
cd /app

# A — braid_q: recompute token on restore-mode refresh.
cat > /app/native/span.cpp <<'EOF'
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
    int32_t mode;
    int32_t count;
    uint64_t fresh;
    int32_t i;
    int32_t probe;

    if (a == nullptr || c == nullptr || b < 2 || b > MCOS_MAX_NODES + 1) {
        return MCOS_INVALID;
    }

    mode = a[0];
    count = b - 1;
    if (count <= 0) {
        return MCOS_INVALID;
    }

    if (mode == 0) {
        *c = hash_span(a + 1, count);
        return MCOS_OK;
    }

    if (mode == 1) {
        fresh = hash_span(a + 1, count);
        probe = 0;
        for (i = 1; i <= count; ++i) {
            probe ^= a[i];
        }
        if (probe == 0 && count > 0) {
            fresh ^= 0x1ULL;
        }
        *c = fresh;
        return MCOS_OK;
    }

    return MCOS_INVALID;
}
EOF

# B — latch_r: replace reuse key (clear on zero) instead of OR-accumulating.
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

# C — sift_s: fold samples under the active permutation in a(1:n).
cat > /app/pack/fold.f90 <<'EOF'
integer(c_int) function sift_s(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  real(c_double), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int64_t) :: h
  integer(c_int64_t) :: prime
  integer(c_int) :: n
  integer(c_int) :: i
  integer(c_int) :: idx
  integer(c_int) :: k
  integer(c_int8_t) :: bytes(8)
  real(c_double) :: sample
  integer(c_int) :: probe
  integer(c_int64_t) :: byte_u

  n = b
  if (n <= 0_c_int) then
    sift_s = 1_c_int
    return
  end if

  h = int(z'CBF29CE484222325', c_int64_t)
  prime = int(z'100000001B3', c_int64_t)
  probe = 0_c_int

  do i = 1, n
    idx = int(a(i), c_int)
    if (idx < 0_c_int .or. idx >= n) then
      sift_s = 1_c_int
      return
    end if
    probe = ieor(probe, idx)
    sample = a(n + idx + 1)
    bytes = transfer(sample, bytes)
    do k = 1, 8
      byte_u = int(iand(int(bytes(k), c_int), 255), c_int64_t)
      h = ieor(h, byte_u)
      h = h * prime
    end do
  end do

  if (probe < -1_c_int) then
    h = ieor(h, 1_c_int64_t)
  end if

  c(1) = int(iand(h, int(z'FFFFFFFF', c_int64_t)), c_int)
  c(2) = int(iand(shiftr(h, 32), int(z'FFFFFFFF', c_int64_t)), c_int)
  sift_s = 0_c_int
end function sift_s
EOF

make clean
make all
mkdir -p /app/output
/app/bin/meshlab
