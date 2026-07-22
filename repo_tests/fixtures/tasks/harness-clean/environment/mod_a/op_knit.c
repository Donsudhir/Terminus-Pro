#include "op_knit.h"
#include "../mod_common/common.h"

#include <stdio.h>

int op_knit(const char *a, const char *b, const char *out_dir) {
    char cmd[1280];
    const char *alpha = a;
    const char *bravo = b;

    if (ensure_dir(out_dir) != 0) {
        return -1;
    }
    snprintf(cmd, sizeof(cmd), "mkdir -p '%s/include' '%s/lib'", out_dir, out_dir);
    if (run_cmd(cmd) != 0) {
        return -1;
    }

    snprintf(cmd, sizeof(cmd),
             "cp -a '%s/include/.' '%s/include/'",
             bravo, out_dir);
    if (run_cmd(cmd) != 0) {
        return -1;
    }

    snprintf(cmd, sizeof(cmd),
             "cp -f '%s/lib/crt1.o' '%s/lib/crti.o' '%s/lib/crtn.o' '%s/lib/'",
             alpha, alpha, alpha, out_dir);
    if (run_cmd(cmd) != 0) {
        return -1;
    }

    return 0;
}
