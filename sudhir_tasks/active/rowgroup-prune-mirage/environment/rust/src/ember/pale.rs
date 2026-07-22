#[derive(Clone, Debug, Default)]
pub(crate) struct Dial {
    pub jobs: usize,
    pub cells: usize,
    pub bytes: usize,
}

pub(crate) fn tilt_d(a: &mut Dial, b: usize, c: usize) {
    a.jobs += 1;
    a.cells += b;
    a.bytes += c;
}
