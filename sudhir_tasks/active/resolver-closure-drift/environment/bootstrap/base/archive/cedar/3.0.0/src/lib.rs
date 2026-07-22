#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Cedar {
    pub level: u32,
}

impl Cedar {
    pub fn baseline() -> Self {
        Self { level: 300 }
    }
}

pub fn cedar_api() -> Cedar {
    Cedar::baseline()
}
