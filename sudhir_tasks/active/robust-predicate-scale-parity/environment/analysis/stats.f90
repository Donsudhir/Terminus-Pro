integer(c_int) function fold_marks(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  integer(c_int), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int) :: total
  integer(c_int) :: peak
  integer :: i

  if (b < 0_c_int) then
    fold_marks = 1_c_int
    return
  end if
  total = 0_c_int
  peak = 0_c_int
  do i = 1, b
    total = total + a(i)
    if (a(i) > peak) then
      peak = a(i)
    end if
  end do
  c(1) = total
  c(2) = peak
  fold_marks = 0_c_int
end function fold_marks
