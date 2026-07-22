use std::fs;

use crate::aero::pale::{cast_fane, DisplayFrame, SampleRow};
use crate::cairn::rill::{turn_rill, AdvisoryFrame};
use crate::quill::bay::{lace_bay, Batch, Gauge};

pub fn emit(label: &str, count: usize) -> Result<(), String> {
    let sample = SampleRow {
        label: label.to_string(),
        value: count as i32,
    };
    let fane = cast_fane(
        &sample,
        &DisplayFrame {
            low: 0,
            high: i32::MAX,
        },
    )
    .map_err(|error| format!("{error:?}"))?;
    let shown = turn_rill(
        fane,
        &AdvisoryFrame {
            ceiling: i32::MAX,
        },
    )
    .map_err(|error| format!("{error:?}"))?;
    let tally = lace_bay(
        Batch { rows: vec![shown] },
        &Gauge {
            label: "compile".to_string(),
        },
    )
    .map_err(|error| format!("{error:?}"))?;
    fs::write(
        "/app/output/resolve.log",
        format!("{} {} {}\n", tally.label, tally.total, label),
    )
    .map_err(|error| format!("cannot write trace: {error}"))
}
