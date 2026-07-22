#include "step_lane.h"
#include "../mod_common/common.h"

#include <stdio.h>

int step_lane(const char *a, const char *b, const char *out_path) {
    const char *bravo = a;
    const char *charlie = b;
    FILE *f = fopen(out_path, "w");
    char tag_path[512];
    FILE *tag;
    char cmd[768];

    (void)bravo;
    if (!f) {
        return -1;
    }

    fprintf(f, "-L%s/lib\n", charlie);
    fprintf(f, "-lslots\n");
    fprintf(f, "-L%s/lib\n", bravo);
    fprintf(f, "-lc\n");
    fclose(f);

    snprintf(tag_path, sizeof(tag_path), "%s.tag.c", out_path);
    tag = fopen(tag_path, "w");
    if (!tag) {
        return -1;
    }
    fprintf(tag, "const char lane_tag_bytes[] = \"CHARLIE\";\n");
    fclose(tag);

    snprintf(cmd, sizeof(cmd), "gcc -c -o '%s.tag.o' '%s'", out_path, tag_path);
    if (run_cmd(cmd) != 0) {
        return -1;
    }
    return 0;
}
