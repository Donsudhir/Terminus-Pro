use std::fmt;

use super::{Need, VaneKind};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Admitted {
    pub key: String,
    pub release: String,
    pub code: u32,
    pub origin: String,
    pub needs: Vec<Need>,
    pub payload: String,
    pub api: String,
    pub priority: u8,
    pub kind: VaneKind,
    pub serial: usize,
}

impl Admitted {
    pub fn identity(&self) -> (String, String, String) {
        (
            self.key.clone(),
            self.release.clone(),
            self.origin.clone(),
        )
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum RejectCode {
    Context,
    Withdrawn,
    Held,
}

impl fmt::Display for RejectCode {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}
