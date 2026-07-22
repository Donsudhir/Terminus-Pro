#[derive(Clone, Debug)]
pub struct SampleRow {
    pub label: String,
    pub value: i32,
}

#[derive(Clone, Debug)]
pub struct DisplayFrame {
    pub low: i32,
    pub high: i32,
}

#[derive(Clone, Debug)]
pub struct Fane {
    pub label: String,
    pub value: i32,
}

#[derive(Clone, Debug)]
pub enum SampleError {
    Outside,
}

pub fn cast_fane(a: &SampleRow, b: &DisplayFrame) -> Result<Fane, SampleError> {
    if a.value < b.low || a.value >= b.high {
        return Err(SampleError::Outside);
    }
    Ok(Fane {
        label: a.label.clone(),
        value: a.value,
    })
}
