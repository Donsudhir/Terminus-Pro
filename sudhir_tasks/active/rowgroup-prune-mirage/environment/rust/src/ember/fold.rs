use crate::model::{FoldErr, Mark};

pub(crate) fn tilt_a(a: &[i64], b: &[u8], c: &[u8]) -> Result<Mark, FoldErr> {
    if a.is_empty() {
        return Err(FoldErr::Empty);
    }
    if a.len() != b.len() || a.len() != c.len() {
        return Err(FoldErr::Shape);
    }

    let mut low = a[0];
    let mut high = a[0];
    let mut has_absent = false;
    for (value, present) in a.iter().zip(b.iter()) {
        low = low.min(*value);
        high = high.max(*value);
        has_absent |= *present == 0;
    }

    Ok(Mark {
        low,
        high,
        has_absent,
    })
}
