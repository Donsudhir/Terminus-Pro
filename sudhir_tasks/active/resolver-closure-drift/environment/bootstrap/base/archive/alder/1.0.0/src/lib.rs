#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Alder {
    pub generation: u32,
}

impl Alder {
    pub fn stable() -> Self {
        Self { generation: 100 }
    }
}

pub fn alder_api() -> Alder {
    Alder::stable()
}
