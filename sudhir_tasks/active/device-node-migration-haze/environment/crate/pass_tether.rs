use crate::tether::{self, Anchor};

/// Resolve one alias under the active anchor context.
pub fn resolve_alias(token: u64, anchor: &mut Anchor) -> i8 {
    tether::moor_r(token, anchor)
}

pub fn bind_rel(anchor: &mut Anchor, rel: &str) {
    tether::set_rel(anchor, rel);
}

pub fn hops(anchor: &Anchor) -> u32 {
    tether::peek_hops(anchor)
}
