#include "open_probe.h"

#include "common.h"

#include <stdio.h>
#include <string.h>

int32_t probe_identity(const char *path, uint64_t *out_id) {
    FILE *fp;
    unsigned char hdr[9];
    uint16_t maj;
    uint16_t min;

    if (path == NULL || out_id == NULL) {
        return HAZE_INVALID;
    }
    fp = fopen(path, "rb");
    if (fp == NULL) {
        return HAZE_IO;
    }
    if (fread(hdr, 1, sizeof(hdr), fp) != sizeof(hdr)) {
        fclose(fp);
        return HAZE_IO;
    }
    fclose(fp);
    if (hdr[0] != HAZE_MAGIC0 || hdr[1] != HAZE_MAGIC1 || hdr[2] != HAZE_MAGIC2 ||
        hdr[3] != HAZE_MAGIC3) {
        return HAZE_REJECT;
    }
    if (hdr[4] != HAZE_KIND_CHAR && hdr[4] != HAZE_KIND_BLOCK) {
        return HAZE_REJECT;
    }
    maj = (uint16_t)hdr[5] | ((uint16_t)hdr[6] << 8);
    min = (uint16_t)hdr[7] | ((uint16_t)hdr[8] << 8);
    *out_id = slot_pack(hdr[4], maj, min);
    return HAZE_OK;
}

int32_t probe_openable(const char *path) {
    FILE *fp;
    if (path == NULL) {
        return HAZE_INVALID;
    }
    fp = fopen(path, "rb");
    if (fp == NULL) {
        return HAZE_IO;
    }
    fclose(fp);
    return HAZE_OK;
}

int32_t probe_kind_ok(uint64_t id) {
    uint8_t kind = slot_kind(id);
    if (kind == HAZE_KIND_CHAR || kind == HAZE_KIND_BLOCK) {
        return HAZE_OK;
    }
    return HAZE_REJECT;
}
