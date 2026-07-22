use super::Need;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PolicyMode {
    Plain,
    Alpha,
    Beta,
    Mixed,
}

impl PolicyMode {
    pub fn parse(value: &str) -> Result<Self, String> {
        match value {
            "plain" => Ok(Self::Plain),
            "alpha" => Ok(Self::Alpha),
            "beta" => Ok(Self::Beta),
            "mixed" => Ok(Self::Mixed),
            _ => Err(format!("unknown profile: {value}")),
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct QueryFrame {
    pub need: Need,
    pub mode: PolicyMode,
    pub root: bool,
    pub stable_available: bool,
    pub ordinal: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PolicyFrame {
    pub mode: PolicyMode,
    pub exact: bool,
    pub stable_available: bool,
    pub root: bool,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Wick {
    pub roots: Vec<String>,
    pub salt: usize,
}
