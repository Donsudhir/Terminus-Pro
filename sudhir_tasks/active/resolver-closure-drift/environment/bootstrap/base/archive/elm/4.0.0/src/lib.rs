#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Elm {
    pub protocol: u32,
}

impl Elm {
    pub fn leaf() -> Self {
        Self { protocol: 400 }
    }
}

pub fn elm_api() -> Elm {
    Elm::leaf()
}
