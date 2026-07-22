#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AlphaAlder {
    pub channel: &'static str,
    pub generation: u32,
}

impl AlphaAlder {
    pub fn preview() -> Self {
        Self {
            channel: "alpha",
            generation: 110,
        }
    }
}

pub fn alpha_api() -> AlphaAlder {
    AlphaAlder::preview()
}
