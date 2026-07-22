.section .interp,"a"
.string "/lib64/ld-linux-x86-64.so.2"

.text
.globl _start
_start:
    xor %edi, %edi
    mov $60, %eax
    syscall
