#ifndef STAGE_COMMON_H
#define STAGE_COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <errno.h>

static inline int ensure_dir(const char *path) {
    if (mkdir(path, 0755) == 0 || errno == EEXIST) {
        return 0;
    }
    return -1;
}

static inline int run_cmd(const char *cmd) {
    int rc = system(cmd);
    if (rc != 0) {
        fprintf(stderr, "command failed (%d): %s\n", rc, cmd);
        return -1;
    }
    return 0;
}

#endif
