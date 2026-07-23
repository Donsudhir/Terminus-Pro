#[derive(Clone, Debug, Default)]
pub struct Shelf {
    pub reuse_key: u64,
    pub epoch: u64,
    pub packed: Vec<f64>,
    pub width: i32,
}

pub(crate) fn latch_r(a: u64, b: &mut Shelf) -> i8 {
    if b.width < 0 {
        return -1;
    }
    b.reuse_key |= a;
    b.epoch = b.epoch.wrapping_add(1);
    0
}

pub fn stash(b: &mut Shelf, values: &[f64]) {
    b.packed = values.to_vec();
    b.width = values.len() as i32;
}

pub fn take(b: &Shelf) -> Vec<f64> {
    b.packed.clone()
}
