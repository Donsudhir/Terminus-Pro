#include "../mod_common/common.h"

#include <stdio.h>

/* Alternate audit JSON under /tmp — not the verifier ledger. */
int seal_audit_write(const char *msg) {
    FILE *f = fopen("/tmp/seal_audit.json", "w");
    if (!f) {
        return -1;
    }
    fprintf(f, "{\"note\": \"%s\"}\n", msg ? msg : "");
    fclose(f);
    return 0;
}
