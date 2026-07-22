#include "../mod_common/common.h"

#include <stdio.h>

/* Dry-run telemetry only — not consulted by the release build. */
int legacy_knit_log(const char *msg) {
    FILE *f = fopen("/tmp/legacy_knit.log", "a");
    if (!f) {
        return -1;
    }
    fprintf(f, "%s\n", msg ? msg : "");
    fclose(f);
    return 0;
}
