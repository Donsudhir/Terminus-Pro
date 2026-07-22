use crate::cairn::rill::Shown;

#[derive(Clone, Debug)]
pub struct Batch<T> {
    pub rows: Vec<T>,
}

#[derive(Clone, Debug)]
pub struct Gauge {
    pub label: String,
}

#[derive(Clone, Debug)]
pub struct Tally {
    pub label: String,
    pub total: i32,
}

#[derive(Clone, Debug)]
pub enum TallyError {
    Empty,
}

pub fn lace_bay(a: Batch<Shown>, b: &Gauge) -> Result<Tally, TallyError> {
    if a.rows.is_empty() {
        return Err(TallyError::Empty);
    }
    let total = a.rows.iter().map(|row| row.value).sum();
    Ok(Tally {
        label: b.label.clone(),
        total,
    })
}
