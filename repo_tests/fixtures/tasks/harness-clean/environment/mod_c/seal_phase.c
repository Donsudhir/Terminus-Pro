#include "seal_phase.h"
#include "../mod_common/common.h"

#include <stdio.h>
#include <string.h>

int seal_phase(const char *a, const char *b, const char *out_path) {
    (void)b;
    size_t n = strlen(out_path);

    if (n > 6 && strcmp(out_path + n - 6, ".flags") == 0) {
        FILE *flags = fopen(out_path, "w");
        if (!flags) {
            return -1;
        }
        fprintf(flags, "-static\n");
        fprintf(flags, "%s/lib/crt1.o\n", a);
        fprintf(flags, "%s/lib/crti.o\n", a);
        fclose(flags);
        return 0;
    }

    if (n > 5 && strcmp(out_path + n - 5, ".json") == 0) {
        FILE *report = fopen(out_path, "w");
        if (!report) {
            return -1;
        }
        fprintf(report,
                "{\n"
                "  \"schema_version\": \"1\",\n"
                "  \"payload_digest\": \"0\",\n"
                "  \"rows\": [],\n"
                "  \"settlement\": false\n"
                "}\n");
        fclose(report);
        return 0;
    }

    return -1;
}
