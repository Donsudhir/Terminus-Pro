use std::collections::BTreeMap;
use std::fmt;

#[derive(Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct LockRow {
    pub key: String,
    pub release: String,
    pub origin: String,
    pub payload: String,
    pub api: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Trellis {
    pub rows: Vec<LockRow>,
    pub parents: BTreeMap<String, Vec<String>>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum GraphError {
    Empty,
    Duplicate,
    MissingEdge,
    ExtraNode,
}

impl fmt::Display for GraphError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}
