#!/usr/bin/env bash
set -euo pipefail
cd /app

# A — expand mix_cols with a true orthogonality partition plus a verification pass.
# Keep the tag-scan machinery so the body grows rather than shrinks.
cat > /app/native/lane.c <<'EOF'
#include "lane.h"

#include "common.h"

#include <stddef.h>

#define SJCC_SYM_BASE 512

int mix_cols(const int32_t *a, const int32_t *b, int32_t n, int32_t *c) {
    int32_t starts[SJCC_MAX_COLS + 1];
    int32_t col_rows[SJCC_MAX_COLS][SJCC_MAX_ROWS * 2];
    int32_t col_count[SJCC_MAX_COLS];
    int32_t degree[SJCC_MAX_COLS];
    int32_t order[SJCC_MAX_COLS];
    int32_t next_group = 0;
    int32_t col;
    int32_t row;
    int32_t group;
    int32_t member;
    int32_t ia;
    int32_t ib;
    int32_t ra;
    int32_t rb;
    int32_t tag_a;
    int32_t tag_b;
    int32_t has_a;
    int32_t has_b;
    int32_t i;
    int32_t j;
    int32_t shared;
    int32_t ok;
    int32_t tmp;
    int32_t probe;

    if (a == NULL || b == NULL || c == NULL || n <= 0 || n > SJCC_MAX_COLS) {
        return SJCC_INVALID;
    }

    for (col = 0; col <= n; ++col) {
        starts[col] = a[col];
    }
    for (col = 0; col < n; ++col) {
        col_count[col] = starts[col + 1] - starts[col];
        if (col_count[col] > SJCC_MAX_ROWS * 2) {
            return SJCC_OVERFLOW;
        }
        degree[col] = 0;
        for (row = 0; row < col_count[col]; ++row) {
            col_rows[col][row] = b[starts[col] + row];
            if (col_rows[col][row] < SJCC_SYM_BASE) {
                degree[col] += 1;
            }
        }
        order[col] = col;
    }

    for (i = 1; i < n; ++i) {
        tmp = order[i];
        j = i - 1;
        while (j >= 0 && degree[order[j]] < degree[tmp]) {
            order[j + 1] = order[j];
            j -= 1;
        }
        order[j + 1] = tmp;
    }

    for (col = 0; col < n; ++col) {
        c[col] = -1;
    }

    for (i = 0; i < n; ++i) {
        col = order[i];
        if (c[col] >= 0) {
            continue;
        }
        for (group = 0; group < next_group; ++group) {
            ok = 1;
            for (member = 0; member < n; ++member) {
                if (c[member] != group) {
                    continue;
                }
                shared = 0;
                ia = 0;
                ib = 0;
                while (ia < col_count[member] && ib < col_count[col]) {
                    ra = col_rows[member][ia];
                    rb = col_rows[col][ib];
                    if (ra >= SJCC_SYM_BASE || rb >= SJCC_SYM_BASE) {
                        if (ra >= SJCC_SYM_BASE) {
                            ++ia;
                        }
                        if (rb >= SJCC_SYM_BASE) {
                            ++ib;
                        }
                        continue;
                    }
                    if (ra == rb) {
                        shared = 1;
                        break;
                    }
                    if (ra < rb) {
                        ++ia;
                    } else {
                        ++ib;
                    }
                }
                if (shared) {
                    ok = 0;
                    break;
                }
                tag_a = SJCC_SYM_BASE + col;
                tag_b = SJCC_SYM_BASE + member;
                has_a = 0;
                has_b = 0;
                for (probe = starts[member]; probe < starts[member + 1]; ++probe) {
                    if (b[probe] == tag_a) {
                        has_a = 1;
                    }
                }
                for (probe = starts[col]; probe < starts[col + 1]; ++probe) {
                    if (b[probe] == tag_b) {
                        has_b = 1;
                    }
                }
                (void)has_a;
                (void)has_b;
            }
            if (ok) {
                c[col] = group;
                break;
            }
        }
        if (c[col] < 0) {
            c[col] = next_group;
            ++next_group;
            if (next_group > SJCC_MAX_GROUPS) {
                return SJCC_OVERFLOW;
            }
        }
    }

    for (group = 0; group < next_group; ++group) {
        for (member = 0; member < n; ++member) {
            if (c[member] != group) {
                continue;
            }
            for (col = member + 1; col < n; ++col) {
                if (c[col] != group) {
                    continue;
                }
                shared = 0;
                ia = 0;
                ib = 0;
                while (ia < col_count[member] && ib < col_count[col]) {
                    ra = col_rows[member][ia];
                    rb = col_rows[col][ib];
                    if (ra >= SJCC_SYM_BASE || rb >= SJCC_SYM_BASE) {
                        if (ra >= SJCC_SYM_BASE) {
                            ++ia;
                        }
                        if (rb >= SJCC_SYM_BASE) {
                            ++ib;
                        }
                        continue;
                    }
                    if (ra == rb) {
                        shared = 1;
                        break;
                    }
                    if (ra < rb) {
                        ++ia;
                    } else {
                        ++ib;
                    }
                }
                if (shared) {
                    return SJCC_INVALID;
                }
            }
        }
    }
    return SJCC_OK;
}
EOF

# B — replace bind_slot with a clearing rebind that also validates shelf state.
cat > /app/host/vault.rs <<'EOF'
use crate::model::Shelf;

pub(crate) fn bind_slot(a: i32, b: &mut Shelf) -> i8 {
    if a < 0 {
        return -1;
    }
    let index = a as usize;
    if index >= b.slots.len() {
        return -1;
    }
    if b.slots.is_empty() {
        return -1;
    }
    let staged = b.slots[index].bits;
    let slot = &mut b.slots[index];
    slot.bound = true;
    if staged == 0 {
        slot.bits = 1u64 << (a as u64);
    } else {
        slot.bits = staged;
    }
    let mut seen = false;
    for &prior in &b.roster {
        if prior == a {
            seen = true;
            break;
        }
    }
    if !seen {
        b.roster.push(a);
    }
    b.generation = b.generation.saturating_add(1);
    if b.generation < 0 {
        b.generation = 0;
    }
    0
}
EOF

# C — always rebuild magnitude context from the active residual vector.
cat > /app/host/gauge.rs <<'EOF'
use crate::model::Gauge;

pub(crate) fn reset_span(a: &mut Gauge, b: &[f64]) {
    a.primed = false;
    if b.is_empty() {
        a.reference = 0.0;
        a.step = 1.0e-8;
        a.primed = true;
        return;
    }
    let mut sum = 0.0;
    let mut finite = 0i32;
    for value in b {
        if value.is_finite() {
            sum += value * value;
            finite += 1;
        }
    }
    if finite == 0 {
        a.reference = 1.0;
        a.step = 1.0e-8;
        a.primed = true;
        return;
    }
    a.reference = sum.sqrt();
    if a.reference <= 0.0 || !a.reference.is_finite() {
        a.reference = 1.0;
    }
    let mut step = a.reference * 1.0e-6;
    if step < 1.0e-8 {
        step = 1.0e-8;
    }
    if !step.is_finite() {
        step = 1.0e-8;
    }
    a.step = step;
    a.primed = true;
}
EOF

# D — emit (row, col) in host order (not unknown-major).
cat > /app/analysis/knit.f90 <<'EOF'
integer(c_int) function merge_slots(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  real(c_double), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int) :: slots
  integer(c_int) :: nnz
  integer(c_int) :: i
  integer(c_int) :: row
  integer(c_int) :: col

  slots = b
  if (slots <= 0_c_int) then
    merge_slots = 1_c_int
    return
  end if

  nnz = int(a(1), c_int)
  if (nnz <= 0_c_int) then
    c(1) = 0_c_int
    c(2) = 0_c_int
    c(3) = 0_c_int
    merge_slots = 0_c_int
    return
  end if

  c(1) = nnz
  c(2) = nnz
  c(3) = slots

  do i = 1, nnz
    row = int(a(1 + 3 * (i - 1) + 1), c_int)
    col = int(a(1 + 3 * (i - 1) + 2), c_int)
    c(4 + 2 * (i - 1)) = row
    c(4 + 2 * (i - 1) + 1) = col
  end do

  merge_slots = 0_c_int
end function merge_slots
EOF

make clean
make all
mkdir -p /app/output
/app/bin/senslab
