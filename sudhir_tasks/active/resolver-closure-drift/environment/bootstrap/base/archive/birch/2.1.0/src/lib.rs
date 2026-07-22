#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RetainedBirch {
    pub protocol: u32,
    pub compatibility: bool,
}

impl RetainedBirch {
    pub fn retained() -> Self {
        Self {
            protocol: 210,
            compatibility: true,
        }
    }
}

pub fn beta_api() -> RetainedBirch {
    RetainedBirch::retained()
}
