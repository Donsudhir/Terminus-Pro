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
    let keep_mode = b.mode;
    let keep_uid = b.uid;
    let keep_gid = b.gid;
    apply_plain_policy(b);
    let _ = (keep_mode, keep_uid, keep_gid);
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

pub(crate) fn hinge_q(a: u64, b: &mut Roster) -> i8 {
    if b.mode > 0o7777 {
        return -1;
    }
    let kind = kind_of(a);
    if kind != 0 {
        apply_special_policy(b);
    } else {
        b.mark = 0;
        b.weight = b.weight.wrapping_add(0);
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
