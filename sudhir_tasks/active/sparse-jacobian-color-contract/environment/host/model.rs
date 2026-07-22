#[derive(Clone, Debug)]
pub struct TagSpec {
    pub name: String,
    pub scale: f64,
    pub shift: Vec<f64>,
}

#[derive(Clone, Debug)]
pub struct FamilySpec {
    pub name: String,
    pub dim: usize,
    pub equations: Vec<Vec<(usize, f64)>>,
    pub base: Vec<f64>,
    pub tags: Vec<TagSpec>,
    pub permutations: Vec<(String, Vec<usize>)>,
}

#[derive(Clone, Debug)]
pub struct RunLabel {
    pub family: String,
    pub tag: String,
}

#[derive(Clone, Debug)]
pub struct RunRecord {
    pub label: RunLabel,
    pub ids: Vec<i32>,
    pub values: Vec<f64>,
    pub indices: Vec<i32>,
    pub dims: Dims,
    pub products: Vec<f64>,
    pub ledger: Ledger,
    pub span_info: SpanInfo,
}

#[derive(Clone, Debug)]
pub struct Dims {
    pub rows: i32,
    pub cols: i32,
    pub nnz: i32,
}

#[derive(Clone, Debug)]
pub struct Ledger {
    pub total: i32,
    pub groups: i32,
    pub active: i32,
}

#[derive(Clone, Debug)]
pub struct SpanInfo {
    pub reference: f64,
    pub step: f64,
}

#[derive(Clone, Debug)]
pub struct Shelf {
    pub slots: Vec<SlotState>,
    pub roster: Vec<i32>,
    pub generation: i32,
}

#[derive(Clone, Debug)]
pub struct SlotState {
    pub bits: u64,
    pub bound: bool,
}

#[derive(Clone, Debug)]
pub struct Gauge {
    pub reference: f64,
    pub step: f64,
    pub primed: bool,
}

#[derive(Clone, Debug)]
pub struct Document {
    pub schema_version: i32,
    pub runs: Vec<RunRecord>,
}
