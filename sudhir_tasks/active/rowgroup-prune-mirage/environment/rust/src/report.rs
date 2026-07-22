use crate::ember::pale::Dial;

pub(crate) fn line(a: &Dial) -> String {
    format!("jobs={} cells={} bytes={}", a.jobs, a.cells, a.bytes)
}
