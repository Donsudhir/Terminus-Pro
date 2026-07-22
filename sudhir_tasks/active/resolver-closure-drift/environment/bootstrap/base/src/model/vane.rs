use std::fmt;

use super::Need;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub enum VaneKind {
    Normal,
    Alpha,
    Beta,
    HeldPin,
    HeldLane,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Vane {
    pub key: String,
    pub release: String,
    pub code: u32,
    pub origin: String,
    pub kind: VaneKind,
    pub withdrawn: bool,
    pub needs: Vec<Need>,
    pub payload: String,
    pub api: String,
    pub serial: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ClassError {
    Outside,
    Contradictory,
    Empty,
}

impl fmt::Display for ClassError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}
