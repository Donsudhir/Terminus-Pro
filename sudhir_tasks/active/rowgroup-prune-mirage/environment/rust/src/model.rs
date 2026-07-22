pub(crate) const RUNE_VOID: u8 = 0;
pub(crate) const RUNE_FIXED: u8 = 1;

#[derive(Clone, Debug)]
pub(crate) struct Cell {
    pub origin: u8,
    pub present: u8,
    pub amount: i64,
    pub region: String,
}

#[derive(Clone, Debug)]
pub(crate) struct Mark {
    pub low: i64,
    pub high: i64,
    pub has_absent: bool,
}

#[derive(Clone, Debug)]
pub(crate) struct Page {
    pub id: usize,
    pub generation: u8,
    pub mark: Mark,
    pub region_low: String,
    pub region_high: String,
    pub cells: Vec<Cell>,
}

#[derive(Debug)]
pub(crate) enum FoldErr {
    Empty,
    Shape,
}

impl std::fmt::Display for FoldErr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Empty => write!(f, "empty lane set"),
            Self::Shape => write!(f, "lane lengths differ"),
        }
    }
}

impl std::error::Error for FoldErr {}
