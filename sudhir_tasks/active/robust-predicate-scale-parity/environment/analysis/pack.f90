integer(c_int) function fold_rows(a, b, c) bind(C)
  use iso_c_binding
  implicit none
  integer(c_int), intent(inout) :: a(*)
  integer(c_int), value :: b
  integer(c_int), intent(out) :: c(*)
  integer(c_int), allocatable :: rows(:, :)
  integer(c_int) :: key(4)
  integer(c_int) :: value
  integer :: i
  integer :: j
  integer :: k
  integer :: left
  integer :: right
  logical :: greater

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
    do left = 1, 3
      do right = left + 1, 4
        if (rows(right, i) < rows(left, i)) then
          value = rows(left, i)
          rows(left, i) = rows(right, i)
          rows(right, i) = value
        end if
      end do
    end do
  end do

  do i = 2, b
    key = rows(:, i)
    j = i - 1
    do while (j >= 1)
      greater = .false.
      do k = 1, 4
        if (rows(k, j) > key(k)) then
          greater = .true.
          exit
        else if (rows(k, j) < key(k)) then
          exit
        end if
      end do
      if (.not. greater) then
        exit
      end if
      rows(:, j + 1) = rows(:, j)
      j = j - 1
    end do
    rows(:, j + 1) = key
  end do

  do i = 1, b
    do j = 1, 4
      a(4 * (i - 1) + j) = rows(j, i)
    end do
  end do
  c(1) = 4_c_int * b
  c(2) = 4_c_int * b
  c(3) = 0_c_int
  c(4) = 0_c_int
  deallocate(rows)
  fold_rows = 0_c_int
end function fold_rows
