module ridge_mod
  use iso_c_binding
  implicit none
contains

  integer(c_int) function ridge_eval(u, x, n, r) bind(C, name="ridge_eval")
    real(c_double), intent(in) :: u(*)
    real(c_double), intent(in) :: x(*)
    integer(c_int), value :: n
    real(c_double), intent(out) :: r(*)
    integer(c_int) :: i
    real(c_double) :: force

    if (n < 2_c_int) then
      ridge_eval = 1_c_int
      return
    end if

    r(1) = 0.0_c_double
    r(n) = 0.0_c_double
    do i = 2, n - 1
      force = 0.15_c_double * sin(x(i) * 3.141592653589793_c_double)
      r(i) = (u(i - 1) - 2.0_c_double * u(i) + u(i + 1)) + force
    end do
    ridge_eval = 0_c_int
  end function ridge_eval

  integer(c_int) function ridge_norm(r, n, out) bind(C, name="ridge_norm")
    real(c_double), intent(in) :: r(*)
    integer(c_int), value :: n
    real(c_double), intent(out) :: out
    integer(c_int) :: i
    real(c_double) :: acc

    if (n <= 0_c_int) then
      ridge_norm = 1_c_int
      return
    end if
    acc = 0.0_c_double
    do i = 1, n
      acc = acc + r(i) * r(i)
    end do
    out = sqrt(acc)
    ridge_norm = 0_c_int
  end function ridge_norm

end module ridge_mod
