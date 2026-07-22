#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Birch {
    pub protocol: u32,
}

impl Birch {
    pub fn baseline() -> Self {
        Self { protocol: 200 }
    }
}

pub fn birch_api() -> Birch {
    Birch::baseline()
}
