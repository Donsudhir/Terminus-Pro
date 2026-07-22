#!/usr/bin/env bash
set -euo pipefail
cd /app

cat > /app/native/series.c <<'EOF'
#include "include/series.h"

#include <float.h>
#include <math.h>
#include <stddef.h>

int eval_band(const double *a, const double *b, int32_t n, double *c) {
    double sum = 0.0;
    double permanent = 0.0;
    double factor;
    double bound;
    int32_t i;

    if (a == NULL || b == NULL || c == NULL || n <= 0) {
        return SERIES_INVALID;
    }
    for (i = 0; i < n; ++i) {
        if (!isfinite(a[i]) || !isfinite(b[i]) || b[i] < 0.0) {
            *c = 0.0;
            return SERIES_REFINE;
        }
        sum += a[i];
        permanent += b[i];
    }
    *c = sum;
    if (!isfinite(sum) || !isfinite(permanent)) {
        return SERIES_REFINE;
    }
    factor = DBL_EPSILON * (8.0 * (double)n + 32.0);
    if (factor <= 0.0 || permanent > DBL_MAX / factor) {
        return SERIES_REFINE;
    }
    bound = permanent * factor;
    if (fabs(sum) <= bound) {
        return SERIES_REFINE;
    }
    return sum < 0.0 ? SERIES_NEGATIVE : SERIES_POSITIVE;
}
EOF

cat > /app/host/plate.rs <<'EOF'
use crate::model::Frame;

pub(crate) fn map_state(a: i32, b: &mut Frame) -> i8 {
    b.raw_status = a;
    b.needs_refine = false;
    match a {
        -1 => -1,
        1 => 1,
        2 => {
            b.needs_refine = true;
            0
        }
        _ => {
            b.invalid = true;
            0
        }
    }
}
EOF

cat > /app/host/frame.rs <<'EOF'
use crate::model::Frame;

pub(crate) fn clear_frame(a: &mut Frame, b: &[f64]) {
    a.needs_refine = false;
    a.invalid = false;
    a.raw_status = 0;
    a.refined = 0;
    a.armed = false;
    if b.is_empty() {
        a.invalid = true;
        return;
    }
    let mut low = b[0];
    let mut high = b[0];
    for value in b {
        if !value.is_finite() {
            a.invalid = true;
            return;
        }
        if *value < low {
            low = *value;
        }
        if *value > high {
            high = *value;
        }
    }
    if low < i32::MIN as f64 || high > i32::MAX as f64 {
        a.invalid = true;
        return;
    }
    let floor = low.round() as i32;
    let ceiling = high.round() as i32;
    let Some(gain) = ceiling.checked_neg() else {
        a.invalid = true;
        return;
    };
    a.floor = floor;
    a.gain = gain;
    a.armed = true;
}
EOF

cat > /app/analysis/pack.f90 <<'EOF'
integer(c_int) function fold_rows(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  integer(c_int), intent(inout) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int), allocatable :: rows(:, :)
  integer(c_int), allocatable :: faces(:, :)
  integer(c_int) :: candidate(4)
  integer(c_int) :: best(4)
  integer(c_int) :: key4(4)
  integer(c_int) :: key3(3)
  integer(c_int) :: value
  integer :: i
  integer :: j
  integer :: k
  integer :: p1
  integer :: p2
  integer :: p3
  integer :: p4
  integer :: permutation(4)
  integer :: inversions
  integer :: left
  integer :: right
  integer :: omitted
  integer :: cursor
  integer :: face_index
  integer :: run_end
  integer :: run_length
  logical :: have_best
  logical :: better
  logical :: greater
  logical :: equal

  c(1) = 0_c_int
  c(2) = 0_c_int
  c(3) = 0_c_int
  c(4) = 0_c_int
  if (b < 0_c_int) then
    fold_rows = 1_c_int
    return
  end if
  if (b == 0_c_int) then
    fold_rows = 0_c_int
    return
  end if

  allocate(rows(4, b))
  do i = 1, b
    do j = 1, 4
      rows(j, i) = a(4 * (i - 1) + j)
    end do
    have_best = .false.
    do p1 = 1, 4
      do p2 = 1, 4
        if (p2 == p1) cycle
        do p3 = 1, 4
          if (p3 == p1 .or. p3 == p2) cycle
          do p4 = 1, 4
            if (p4 == p1 .or. p4 == p2 .or. p4 == p3) cycle
            permutation = [p1, p2, p3, p4]
            inversions = 0
            do left = 1, 3
              do right = left + 1, 4
                if (permutation(left) > permutation(right)) inversions = inversions + 1
              end do
            end do
            if (mod(inversions, 2) /= 0) cycle
            candidate = [rows(p1, i), rows(p2, i), rows(p3, i), rows(p4, i)]
            if (.not. have_best) then
              best = candidate
              have_best = .true.
            else
              better = .false.
              do k = 1, 4
                if (candidate(k) < best(k)) then
                  better = .true.
                  exit
                else if (candidate(k) > best(k)) then
                  exit
                end if
              end do
              if (better) best = candidate
            end if
          end do
        end do
      end do
    end do
    rows(:, i) = best
  end do

  do i = 2, b
    key4 = rows(:, i)
    j = i - 1
    do while (j >= 1)
      greater = .false.
      do k = 1, 4
        if (rows(k, j) > key4(k)) then
          greater = .true.
          exit
        else if (rows(k, j) < key4(k)) then
          exit
        end if
      end do
      if (.not. greater) exit
      rows(:, j + 1) = rows(:, j)
      j = j - 1
    end do
    rows(:, j + 1) = key4
  end do

  allocate(faces(3, 4 * b))
  face_index = 0
  do i = 1, b
    do omitted = 1, 4
      face_index = face_index + 1
      cursor = 0
      do j = 1, 4
        if (j /= omitted) then
          cursor = cursor + 1
          faces(cursor, face_index) = rows(j, i)
        end if
      end do
      do left = 1, 2
        do right = left + 1, 3
          if (faces(right, face_index) < faces(left, face_index)) then
            value = faces(left, face_index)
            faces(left, face_index) = faces(right, face_index)
            faces(right, face_index) = value
          end if
        end do
      end do
    end do
  end do

  do i = 2, 4 * b
    key3 = faces(:, i)
    j = i - 1
    do while (j >= 1)
      greater = .false.
      do k = 1, 3
        if (faces(k, j) > key3(k)) then
          greater = .true.
          exit
        else if (faces(k, j) < key3(k)) then
          exit
        end if
      end do
      if (.not. greater) exit
      faces(:, j + 1) = faces(:, j)
      j = j - 1
    end do
    faces(:, j + 1) = key3
  end do

  i = 1
  do while (i <= 4 * b)
    run_end = i + 1
    do while (run_end <= 4 * b)
      equal = .true.
      do k = 1, 3
        if (faces(k, run_end) /= faces(k, i)) then
          equal = .false.
          exit
        end if
      end do
      if (.not. equal) exit
      run_end = run_end + 1
    end do
    run_length = run_end - i
    c(1) = c(1) + 1_c_int
    if (run_length == 1) then
      c(2) = c(2) + 1_c_int
    else if (run_length == 2) then
      c(3) = c(3) + 1_c_int
    else
      c(4) = c(4) + 1_c_int
    end if
    i = run_end
  end do

  do i = 1, b
    do j = 1, 4
      a(4 * (i - 1) + j) = rows(j, i)
    end do
  end do
  deallocate(faces)
  deallocate(rows)
  fold_rows = 0_c_int
end function fold_rows
EOF

make clean
make all
mkdir -p /app/output
/app/bin/geomlab
