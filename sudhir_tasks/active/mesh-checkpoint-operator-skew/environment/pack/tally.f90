integer(c_int) function tally_marks(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  real(c_double), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int) :: i
  real(c_double) :: acc

  if (b <= 0_c_int) then
    tally_marks = 1_c_int
    return
  end if

  acc = 0.0_c_double
  do i = 1, b
    acc = acc + a(i)
  end do
  c(1) = b
  c(2) = int(acc, c_int)
  c(3) = int(acc * 1000.0_c_double, c_int)
  tally_marks = 0_c_int
end function tally_marks
