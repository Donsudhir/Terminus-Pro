use crate::error::{with_path, AppResult};
use crate::fnv::fnv1a;
use crate::model::BatchReport;
use std::fmt::Write as _;
use std::fs;
use std::path::Path;

fn quoted(target: &mut String, value: &str) {
    target.push('"');
    for character in value.chars() {
        match character {
            '"' => target.push_str("\\\""),
            '\\' => target.push_str("\\\\"),
            '\n' => target.push_str("\\n"),
            '\r' => target.push_str("\\r"),
            '\t' => target.push_str("\\t"),
            value if value.is_control() => {
                let _ = write!(target, "\\u{:04x}", value as u32);
            }
            value => target.push(value),
        }
    }
    target.push('"');
}

fn integer_row<const N: usize>(target: &mut String, row: &[i32; N]) {
    target.push('[');
    for (index, value) in row.iter().enumerate() {
        if index > 0 {
            target.push(',');
        }
        let _ = write!(target, "{value}");
    }
    target.push(']');
}

fn batch_json(target: &mut String, report: &BatchReport) {
    target.push_str("{\"identity\":{\"family\":");
    quoted(target, &report.family);
    target.push_str(",\"variant\":");
    quoted(target, &report.variant);
    target.push_str(",\"point_ids\":[");
    for (index, value) in report.point_ids.iter().enumerate() {
        if index > 0 {
            target.push(',');
        }
        let _ = write!(target, "{value}");
    }
    target.push_str("]},\"cells\":[");
    for (index, row) in report.cells.iter().enumerate() {
        if index > 0 {
            target.push(',');
        }
        integer_row(target, row);
    }
    target.push_str("],\"adjacency\":[");
    for (index, row) in report.adjacency.iter().enumerate() {
        if index > 0 {
            target.push(',');
        }
        integer_row(target, row);
    }
    let _ = write!(
        target,
        "],\"orientation\":{{\"positive\":{},\"negative\":{},\"zero\":{}}},\"validity\":{{\"checks\":{},\"violations\":{}}},\"topology\":{{\"vertices\":{},\"edges\":{},\"faces\":{},\"cells\":{},\"boundary_faces\":{},\"euler\":{}}}}}",
        report.orientation.positive,
        report.orientation.negative,
        report.orientation.zero,
        report.validity.checks,
        report.validity.violations,
        report.topology.vertices,
        report.topology.edges,
        report.topology.faces,
        report.topology.cells,
        report.topology.boundary_faces,
        report.topology.euler,
    );
}

pub(crate) fn save(path: &Path, reports: &[BatchReport]) -> AppResult<()> {
    let mut payload = String::from("{\"schema_version\":1,\"batches\":[");
    for (index, report) in reports.iter().enumerate() {
        if index > 0 {
            payload.push(',');
        }
        batch_json(&mut payload, report);
    }
    payload.push_str("]}");
    let digest = fnv1a(payload.as_bytes());
    let mut complete = payload;
    complete.pop();
    let _ = writeln!(complete, ",\"digest\":\"{digest:016x}\"}}");
    let parent = path
        .parent()
        .ok_or_else(|| format!("{} has no parent directory", path.display()))?;
    fs::create_dir_all(parent).map_err(|error| with_path("create", parent, error))?;
    let temporary = path.with_extension("json.tmp");
    fs::write(&temporary, complete.as_bytes()).map_err(|error| with_path("write", &temporary, error))?;
    fs::rename(&temporary, path).map_err(|error| with_path("rename", path, error))?;
    Ok(())
}
