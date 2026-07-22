#include "../mod_common/common.h"

#include <stdio.h>

/* Operator pretty-printer — unused by the linker. */
int lane_watch_dump(const char *path) {
    FILE *f = fopen(path, "r");
    char buf[256];
    if (!f) {
        return -1;
    }
    while (fgets(buf, sizeof(buf), f)) {
        fputs(buf, stdout);
    }
    fclose(f);
    return 0;
}
