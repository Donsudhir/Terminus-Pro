#!/usr/bin/env bash
set -euo pipefail
cd /app

# Fix locus A: stage alpha includes (ABI overlay) + bravo CRT.
cat > /app/mod_a/op_knit.c <<'EOF'
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

    snprintf(cmd, sizeof(cmd), "cp -a '%s/include/.' '%s/include/'", alpha, out_dir);
    if (run_cmd(cmd) != 0) {
        return -1;
    }

    snprintf(cmd, sizeof(cmd),
             "cp -f '%s/lib/crt1.o' '%s/lib/crti.o' '%s/lib/crtn.o' '%s/lib/'",
             bravo, bravo, bravo, out_dir);
    if (run_cmd(cmd) != 0) {
        return -1;
    }

    return 0;
}
EOF

# Fix locus B: prefer bravo slots, embed BRAVO tag.
cat > /app/mod_b/step_lane.c <<'EOF'
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

    (void)charlie;
    if (!f) {
        return -1;
    }

    fprintf(f, "-L%s/lib\n", bravo);
    fprintf(f, "-lslots\n");
    fprintf(f, "-lc\n");
    fclose(f);

    snprintf(tag_path, sizeof(tag_path), "%s.tag.c", out_path);
    tag = fopen(tag_path, "w");
    if (!tag) {
        return -1;
    }
    fprintf(tag, "const char lane_tag_bytes[] = \"BRAVO\";\n");
    fclose(tag);

    snprintf(cmd, sizeof(cmd), "gcc -c -o '%s.tag.o' '%s'", out_path, tag_path);
    if (run_cmd(cmd) != 0) {
        return -1;
    }
    return 0;
}
EOF

# Fix locus C: flags without dynamic linker; json mode builds live ledger.
cat > /app/mod_c/seal_phase.c <<'EOF'
#include "seal_phase.h"
#include "../mod_common/common.h"

#include <ctype.h>
#include <stdio.h>
#include <string.h>

static int write_flags(const char *stage, const char *out_path) {
    FILE *flags = fopen(out_path, "w");
    if (!flags) {
        return -1;
    }
    fprintf(flags, "-static\n");
    fprintf(flags, "%s/lib/crt1.o\n", stage);
    fprintf(flags, "%s/lib/crti.o\n", stage);
    fclose(flags);
    return 0;
}

static int hex_digest_file(const char *path, char *out_hex, size_t out_sz) {
    char cmd[768];
    FILE *p;
    if (out_sz < 65) {
        return -1;
    }
    snprintf(cmd, sizeof(cmd), "sha256sum '%s'", path);
    p = popen(cmd, "r");
    if (!p) {
        return -1;
    }
    if (fscanf(p, "%64s", out_hex) != 1) {
        pclose(p);
        return -1;
    }
    pclose(p);
    out_hex[64] = '\0';
    return 0;
}

static int line_has(const char *buf, const char *prefix, const char *expect) {
    size_t n = strlen(prefix);
    if (strncmp(buf, prefix, n) != 0) {
        return 0;
    }
    return strcmp(buf + n, expect) == 0;
}

static int write_report(const char *payload, const char *stdout_path, const char *out_path) {
    char digest[65];
    char line[256];
    int ok_marker = 0, ok_thread = 0, ok_errno = 0, ok_lane = 0;
    FILE *in;
    FILE *report;
    int settlement;

    if (hex_digest_file(payload, digest, sizeof(digest)) != 0) {
        return -1;
    }

    in = fopen(stdout_path, "r");
    if (!in) {
        return -1;
    }
    while (fgets(line, sizeof(line), in)) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) {
            line[--len] = '\0';
        }
        if (line_has(line, "MARKER=", "CXR-7F")) {
            ok_marker = 1;
        } else if (line_has(line, "THREAD=", "7")) {
            ok_thread = 1;
        } else if (line_has(line, "ERRNO=", "2")) {
            ok_errno = 1;
        } else if (line_has(line, "LANE_TAG=", "BRAVO")) {
            ok_lane = 1;
        }
    }
    fclose(in);

    (void)ok_lane;
    settlement = ok_marker && ok_thread && ok_errno;

    report = fopen(out_path, "w");
    if (!report) {
        return -1;
    }
    fprintf(report,
            "{\n"
            "  \"schema_version\": \"1\",\n"
            "  \"payload_digest\": \"%s\",\n"
            "  \"rows\": [\n"
            "    {\"name\": \"marker\", \"ok\": %s, \"detail\": \"MARKER\"},\n"
            "    {\"name\": \"thread\", \"ok\": %s, \"detail\": \"THREAD\"},\n"
            "    {\"name\": \"errno\", \"ok\": %s, \"detail\": \"ERRNO\"}\n"
            "  ],\n"
            "  \"settlement\": %s\n"
            "}\n",
            digest,
            ok_marker ? "true" : "false",
            ok_thread ? "true" : "false",
            ok_errno ? "true" : "false",
            settlement ? "true" : "false");
    fclose(report);
    return 0;
}

int seal_phase(const char *a, const char *b, const char *out_path) {
    size_t n = strlen(out_path);
    if (n > 6 && strcmp(out_path + n - 6, ".flags") == 0) {
        return write_flags(a, out_path);
    }
    if (n > 5 && strcmp(out_path + n - 5, ".json") == 0) {
        return write_report(a, b, out_path);
    }
    return -1;
}
EOF

make -C /app/mod_common
/app/tools/build_payload.sh
