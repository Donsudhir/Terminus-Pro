module ridge_mod
  use iso_c_binding
  implicit none
contains

  integer(c_int) function ridge_eval(coeff, rows, cols, nnz, row_ptr, col_idx, x, r) bind(C)
    use iso_c_binding
    implicit none
    real(c_double), intent(in) :: coeff(*)
    integer(c_int), value :: rows
    integer(c_int), value :: cols
    integer(c_int), value :: nnz
    integer(c_int), intent(in) :: row_ptr(*)
    integer(c_int), intent(in) :: col_idx(*)
    real(c_double), intent(in) :: x(*)
    real(c_double), intent(out) :: r(*)
    integer :: i
    integer :: j
    integer :: p
    integer :: p_lo
    integer :: p_hi

    if (nnz < 0) then
      ridge_eval = 1_c_int
      return
    end if

    do i = 1, rows
      r(i) = 0.0_c_double
    end do
    do j = 1, cols
      p_lo = row_ptr(j) + 1
      p_hi = row_ptr(j + 1)
      do p = p_lo, p_hi
        i = col_idx(p) + 1
        r(i) = r(i) + coeff(p) * x(j)
      end do
    end do
    ridge_eval = 0_c_int
  end function ridge_eval

  integer(c_int) function ridge_companion(coeff, rows, cols, nnz, row_ptr, col_idx, v, out) bind(C)
    use iso_c_binding
    implicit none
    real(c_double), intent(in) :: coeff(*)
    integer(c_int), value :: rows
    integer(c_int), value :: cols
    integer(c_int), value :: nnz
    integer(c_int), intent(in) :: row_ptr(*)
    integer(c_int), intent(in) :: col_idx(*)
    real(c_double), intent(in) :: v(*)
    real(c_double), intent(out) :: out(*)
    integer :: i
    integer :: j
    integer :: p
    integer :: p_lo
    integer :: p_hi

    if (nnz < 0) then
      ridge_companion = 1_c_int
      return
    end if

    do i = 1, rows
      out(i) = 0.0_c_double
    end do
    do j = 1, cols
      p_lo = row_ptr(j) + 1
      p_hi = row_ptr(j + 1)
      do p = p_lo, p_hi
        i = col_idx(p) + 1
        out(i) = out(i) + coeff(p) * v(j)
      end do
    end do
    ridge_companion = 0_c_int
  end function ridge_companion

end module ridge_mod
