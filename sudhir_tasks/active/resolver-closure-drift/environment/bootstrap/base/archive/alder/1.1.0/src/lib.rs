#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Alder {
    pub generation: u32,
    pub stable: bool,
}

impl Alder {
    pub fn current() -> Self {
        Self {
            generation: 120,
            stable: true,
        }
    }
}

pub fn alder_api() -> Alder {
    Alder::current()
}
