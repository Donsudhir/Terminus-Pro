integer(c_int) function merge_slots(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  real(c_double), intent(in) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int) :: slots
  integer(c_int) :: nnz
  integer(c_int) :: i
  integer(c_int) :: eq
  integer(c_int) :: unk

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
    eq = int(a(1 + 3 * (i - 1) + 1), c_int)
    unk = int(a(1 + 3 * (i - 1) + 2), c_int)
    c(4 + 2 * (i - 1)) = unk
    c(4 + 2 * (i - 1) + 1) = eq
  end do

  merge_slots = 0_c_int
end function merge_slots
