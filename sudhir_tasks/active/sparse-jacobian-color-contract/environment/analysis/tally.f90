integer(c_int) function tally_marks(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  real(c_double), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int) :: i
  integer(c_int) :: count

  count = b
  c(1) = 0_c_int
  c(2) = 0_c_int
  do i = 1, count
    if (a(i) > 0.0_c_double) then
      c(1) = c(1) + 1_c_int
    else if (a(i) < 0.0_c_double) then
      c(2) = c(2) + 1_c_int
    end if
  end do
  tally_marks = 0_c_int
end function tally_marks
