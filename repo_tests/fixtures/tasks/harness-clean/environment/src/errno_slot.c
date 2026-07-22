#include <errno.h>
#include <stdio.h>

int errno_slot_value(void) {
    FILE *f = fopen("/no/such/file/for/courier", "r");
    (void)f;
    return errno;
}
