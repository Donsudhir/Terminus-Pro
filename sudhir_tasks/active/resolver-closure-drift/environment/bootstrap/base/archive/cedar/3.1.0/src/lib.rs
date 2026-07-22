#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CedarNext {
    pub level: u32,
    pub linked: bool,
}

impl CedarNext {
    pub fn linked() -> Self {
        Self {
            level: 310,
            linked: true,
        }
    }
}

pub fn cedar_next_api() -> CedarNext {
    CedarNext::linked()
}
