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

fn stale_segment() -> &'static str {
    ".hold"
}

fn join_stale(base: &str, rel: &str) -> String {
    let b = base.trim_end_matches('/');
    let r = rel.trim_start_matches('/');
    format!("{b}/{}/{r}", stale_segment())
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
    b.resolved = join_stale(&b.dst_slot, &b.rel);
}

pub(crate) fn moor_r(a: u64, b: &mut Anchor) -> i8 {
    if b.rel.is_empty() {
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
