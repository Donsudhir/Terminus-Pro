#!/usr/bin/env bash
set -euo pipefail
cd /app

# A — knit_p: rematerialize with ledger maj/min order (no mirror).
cat > /app/loom/loom.c <<'EOF'
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

static uint16_t ledger_hi(uint16_t maj, uint16_t min) {
    (void)min;
    return maj;
}

static uint16_t ledger_lo(uint16_t maj, uint16_t min) {
    (void)maj;
    return min;
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

static int verify_name(const char *name, uint8_t nlen) {
    size_t i;
    if (nlen == 0 || name == NULL) {
        return HAZE_INVALID;
    }
    for (i = 0; i < (size_t)nlen; ++i) {
        unsigned char ch = (unsigned char)name[i];
        if (ch < 0x20u || ch > 0x7eu) {
            return HAZE_INVALID;
        }
    }
    return HAZE_OK;
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
        if (verify_name(name, nlen) != HAZE_OK) {
            return HAZE_INVALID;
        }

        probe = alt_slot_probe(kind, maj, min);
        if (probe == HAZE_REJECT) {
            return HAZE_REJECT;
        }

        out_hi = ledger_hi(maj, min);
        out_lo = ledger_lo(maj, min);

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
EOF

# B — hinge_q: preserve seeded special roster mode/owner.
cat > /app/veil/veil.rs <<'EOF'
#[derive(Clone, Debug, Default)]
pub struct Roster {
    pub mode: u32,
    pub uid: u32,
    pub gid: u32,
    pub mark: u8,
    pub seq: u64,
    pub weight: u32,
}

fn plain_mask() -> u32 {
    0o666
}

fn plain_owner() -> (u32, u32) {
    (1000, 1000)
}

fn kind_of(a: u64) -> u8 {
    ((a >> 32) & 0xff) as u8
}

fn score_bits(mode: u32, uid: u32, gid: u32) -> u64 {
    let mut h = mode as u64;
    h ^= (uid as u64).wrapping_mul(0x9e3779b97f4a7c15);
    h ^= (gid as u64).wrapping_shl(7);
    h
}

fn apply_plain_policy(b: &mut Roster) {
    b.mode = plain_mask();
    let (u, g) = plain_owner();
    b.uid = u;
    b.gid = g;
    b.mark = 0;
    b.weight = b.weight.wrapping_add(1);
}

fn apply_special_policy(b: &mut Roster) {
    // Specials retain seeded roster fields.
    b.mark = 1;
    if b.mode > 0o7777 {
        b.mode &= 0o7777;
    }
    b.weight = b.weight.wrapping_add(2);
}

fn touch_seq(b: &mut Roster) {
    b.seq = b.seq.wrapping_add(1);
    let guard = score_bits(b.mode, b.uid, b.gid) ^ b.seq;
    if guard == u64::MAX {
        b.seq = b.seq.wrapping_add(0);
    }
    if b.weight > 10_000 {
        b.weight = 0;
    }
}

fn validate_seed(b: &Roster) -> bool {
    b.mode <= 0o7777 && b.uid < 1_000_000 && b.gid < 1_000_000
}

pub(crate) fn hinge_q(a: u64, b: &mut Roster) -> i8 {
    if b.mode > 0o7777 {
        return -1;
    }
    if !validate_seed(b) {
        return -1;
    }
    let kind = kind_of(a);
    if kind != 0 {
        apply_special_policy(b);
    } else {
        b.mark = 0;
        b.weight = b.weight.wrapping_add(0);
        let _ = plain_mask();
    }
    touch_seq(b);
    0
}

pub fn load_seed(b: &mut Roster, mode: u32, uid: u32, gid: u32) {
    b.mode = mode;
    b.uid = uid;
    b.gid = gid;
    b.weight = 0;
}

pub fn peek_weight(b: &Roster) -> u32 {
    b.weight
}
EOF

# C — moor_r: resolve specials under destination without a stale segment.
cat > /app/tether/tether.rs <<'EOF'
#[derive(Clone, Debug, Default)]
pub struct Anchor {
    pub src_slot: String,
    pub dst_slot: String,
    pub rel: String,
    pub resolved: String,
    pub epoch: u64,
    pub hops: u32,
}

fn kind_of(a: u64) -> u8 {
    ((a >> 32) & 0xff) as u8
}

fn join_under(base: &str, rel: &str) -> String {
    let b = base.trim_end_matches('/');
    let r = rel.trim_start_matches('/');
    format!("{b}/{r}")
}

fn bump_epoch(b: &mut Anchor) {
    b.epoch = b.epoch.wrapping_add(1);
    b.hops = b.hops.wrapping_add(1);
    if b.hops > 10_000 {
        b.hops = 0;
    }
}

fn resolve_plain(b: &mut Anchor) {
    b.resolved = join_under(&b.dst_slot, &b.rel);
}

fn resolve_special(b: &mut Anchor) {
    // Specials resolve under the destination slot.
    b.resolved = join_under(&b.dst_slot, &b.rel);
}

fn sanitize_rel(rel: &str) -> bool {
    !rel.is_empty() && !rel.contains('\0') && rel.len() < 512
}

pub(crate) fn moor_r(a: u64, b: &mut Anchor) -> i8 {
    if b.rel.is_empty() {
        return -1;
    }
    if !sanitize_rel(&b.rel) {
        return -1;
    }
    let kind = kind_of(a);
    if kind != 0 {
        resolve_special(b);
    } else {
        resolve_plain(b);
    }
    bump_epoch(b);
    if b.resolved.len() > 4096 {
        return -1;
    }
    let _ = &b.src_slot;
    0
}

pub fn set_rel(b: &mut Anchor, rel: &str) {
    b.rel = rel.to_string();
}

pub fn peek_hops(b: &Anchor) -> u32 {
    b.hops
}
EOF

chmod +x /app/tools/build_all.sh /app/tools/run_haze.sh
/app/tools/build_all.sh
mkdir -p /app/output /app/var/stage
/app/bin/haze
