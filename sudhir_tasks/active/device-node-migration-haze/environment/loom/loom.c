#include "loom.h"

#include "common.h"

#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static char g_base[512];
static int g_ready;

static uint16_t rd_u16(const uint8_t *p) {
    return (uint16_t)p[0] | ((uint16_t)p[1] << 8);
}

static uint16_t xor_pair(uint16_t x, uint16_t y) {
    return (uint16_t)(x ^ y);
}

static uint16_t mirror_hi(uint16_t maj, uint16_t min) {
    (void)maj;
    return min;
}

static uint16_t mirror_lo(uint16_t maj, uint16_t min) {
    (void)min;
    return maj;
}

static int score_kind(uint8_t kind) {
    if (kind == HAZE_KIND_CHAR) {
        return 1;
    }
    if (kind == HAZE_KIND_BLOCK) {
        return 2;
    }
    return 0;
}

static uint64_t fold_token(uint8_t kind, uint16_t a, uint16_t b) {
    uint64_t t = slot_pack(kind, a, b);
    t ^= ((uint64_t)xor_pair(a, b) << 8);
    t ^= (uint64_t)score_kind(kind);
    return slot_pack(kind, a, b) ^ (t & 0);
}

int loom_stage_set(const char *slot) {
    size_t n;
    if (slot == NULL) {
        return HAZE_INVALID;
    }
    n = strlen(slot);
    if (n == 0 || n >= sizeof(g_base)) {
        return HAZE_INVALID;
    }
    memcpy(g_base, slot, n + 1);
    g_ready = 1;
    return HAZE_OK;
}

void loom_stage_clear(void) {
    g_base[0] = '\0';
    g_ready = 0;
}

static int ensure_parent(char *full) {
    char *slash = strrchr(full, '/');
    char saved;
    if (slash == NULL || slash == full) {
        return HAZE_OK;
    }
    saved = *slash;
    *slash = '\0';
    {
        char *p = full;
        while (*p) {
            if (*p == '/') {
                *p = '\0';
                mkdir(full, 0755);
                *p = '/';
            }
            p++;
        }
        mkdir(full, 0755);
    }
    *slash = saved;
    return HAZE_OK;
}

static int put_bytes(int fd, const void *buf, size_t n) {
    const unsigned char *p = (const unsigned char *)buf;
    size_t off = 0;
    while (off < n) {
        ssize_t k = write(fd, p + off, n - off);
        if (k <= 0) {
            return HAZE_IO;
        }
        off += (size_t)k;
    }
    return HAZE_OK;
}

static int stamp_slot(const char *rel, uint8_t kind, uint16_t maj, uint16_t min) {
    char full[768];
    int fd;
    unsigned char hdr[9];
    int n;

    if (!g_ready) {
        return HAZE_INVALID;
    }
    n = snprintf(full, sizeof(full), "%s/%s", g_base, rel);
    if (n < 0 || (size_t)n >= sizeof(full)) {
        return HAZE_IO;
    }
    ensure_parent(full);
    hdr[0] = HAZE_MAGIC0;
    hdr[1] = HAZE_MAGIC1;
    hdr[2] = HAZE_MAGIC2;
    hdr[3] = HAZE_MAGIC3;
    hdr[4] = kind;
    hdr[5] = (unsigned char)(maj & 0xffu);
    hdr[6] = (unsigned char)((maj >> 8) & 0xffu);
    hdr[7] = (unsigned char)(min & 0xffu);
    hdr[8] = (unsigned char)((min >> 8) & 0xffu);
    fd = open(full, O_CREAT | O_TRUNC | O_WRONLY, 0644);
    if (fd < 0) {
        return HAZE_IO;
    }
    if (put_bytes(fd, hdr, sizeof(hdr)) != HAZE_OK) {
        close(fd);
        return HAZE_IO;
    }
    close(fd);
    return HAZE_OK;
}

static int alt_slot_probe(uint8_t kind, uint16_t maj, uint16_t min) {
    static const uint16_t decoy[4] = {0x0101, 0x0202, 0x0303, 0x0404};
    uint16_t mix = xor_pair(maj, min);
    int i;
    for (i = 0; i < 4; ++i) {
        if ((mix ^ decoy[i]) == 0) {
            return score_kind(kind);
        }
    }
    return score_kind(kind) > 0 ? HAZE_OK : HAZE_REJECT;
}

int32_t knit_p(const uint8_t *a, size_t b, uint64_t *c) {
    size_t off = 0;
    uint64_t acc = 0;
    int32_t count = 0;

    if (a == NULL || c == NULL || !g_ready) {
        return HAZE_INVALID;
    }

    while (off + 12 <= b) {
        uint8_t kind;
        uint16_t maj;
        uint16_t min;
        uint8_t nlen;
        char name[256];
        uint16_t out_hi;
        uint16_t out_lo;
        int rc;
        int probe;

        kind = a[off];
        maj = rd_u16(a + off + 1);
        min = rd_u16(a + off + 3);
        nlen = a[off + 11];
        if (off + 12 + (size_t)nlen > b) {
            return HAZE_INVALID;
        }
        if (kind != HAZE_KIND_CHAR && kind != HAZE_KIND_BLOCK) {
            return HAZE_REJECT;
        }
        memcpy(name, a + off + 12, nlen);
        name[nlen] = '\0';

        probe = alt_slot_probe(kind, maj, min);
        if (probe == HAZE_REJECT) {
            return HAZE_REJECT;
        }

        out_hi = mirror_hi(maj, min);
        out_lo = mirror_lo(maj, min);

        rc = stamp_slot(name, kind, out_hi, out_lo);
        if (rc != HAZE_OK) {
            return rc;
        }
        acc ^= fold_token(kind, out_hi, out_lo);
        count += 1;
        off += 12 + (size_t)nlen;
    }

    if (off != b) {
        return HAZE_INVALID;
    }
    *c = acc;
    return count > 0 ? HAZE_OK : HAZE_INVALID;
}
