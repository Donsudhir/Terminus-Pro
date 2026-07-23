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
  integer(c_int) :: k
  integer(c_int8_t) :: bytes(8)
  real(c_double) :: sample
  integer(c_int64_t) :: byte_u

  n = b
  if (n <= 0_c_int) then
    sift_s = 1_c_int
    return
  end if

  h = int(z'CBF29CE484222325', c_int64_t)
  prime = int(z'100000001B3', c_int64_t)

  do i = 1, n
    sample = a(n + i)
    bytes = transfer(sample, bytes)
    do k = 1, 8
      byte_u = int(iand(int(bytes(k), c_int), 255), c_int64_t)
      h = ieor(h, byte_u)
      h = h * prime
    end do
  end do

  c(1) = int(iand(h, int(z'FFFFFFFF', c_int64_t)), c_int)
  c(2) = int(iand(shiftr(h, 32), int(z'FFFFFFFF', c_int64_t)), c_int)
  sift_s = 0_c_int
end function sift_s
