use crate::model::{Document, RunRecord};
use std::fs;
use std::path::Path;

pub fn save(path: &Path, runs: &[RunRecord]) -> Result<(), String> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|err| format!("output dir: {err}"))?;
    }
    let document = Document {
        schema_version: 1,
        runs: runs.to_vec(),
    };
    let body = render(&document);
    fs::write(path, body).map_err(|err| format!("output write: {err}"))
}

fn render(document: &Document) -> String {
    let mut parts = Vec::new();
    parts.push(format!("{{\"schema_version\":{}", document.schema_version));
    parts.push(",\"runs\":[".to_string());
    for (index, run) in document.runs.iter().enumerate() {
        if index > 0 {
            parts.push(",".to_string());
        }
        parts.push(render_run(run));
    }
    parts.push("]".to_string());
    let prefix = parts.join("");
    let closed = format!("{prefix}}}");
    let digest = fnv1a(closed.as_bytes());
    format!("{prefix},\"digest\":\"{digest:016x}\"}}\n")
}

fn render_run(run: &RunRecord) -> String {
    format!(
        "{{\"label\":{{\"family\":\"{}\",\"tag\":\"{}\"}},\"ids\":{},\"values\":{},\"indices\":{},\"dims\":{{\"rows\":{},\"cols\":{},\"nnz\":{}}},\"products\":{},\"ledger\":{{\"total\":{},\"groups\":{},\"active\":{}}},\"span_info\":{{\"ref\":{},\"step\":{}}}}}",
        escape(&run.label.family),
        escape(&run.label.tag),
        render_i32_list(&run.ids),
        render_f64_list(&run.values),
        render_i32_list(&run.indices),
        run.dims.rows,
        run.dims.cols,
        run.dims.nnz,
        render_f64_list(&run.products),
        run.ledger.total,
        run.ledger.groups,
        run.ledger.active,
        fmt_f64(run.span_info.reference),
        fmt_f64(run.span_info.step),
    )
}

fn render_i32_list(values: &[i32]) -> String {
    let inner = values
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>()
        .join(",");
    format!("[{inner}]")
}

fn render_f64_list(values: &[f64]) -> String {
    let inner = values
        .iter()
        .map(|value| fmt_f64(*value))
        .collect::<Vec<_>>()
        .join(",");
    format!("[{inner}]")
}

fn fmt_f64(value: f64) -> String {
    if value == 0.0 && value.is_sign_negative() {
        "-0.0".to_string()
    } else if value.fract() == 0.0 && value.abs() < 1.0e15 {
        format!("{:.1}", value)
    } else {
        format!("{:.12e}", value)
    }
}

fn escape(text: &str) -> String {
    text.replace('\\', "\\\\").replace('"', "\\\"")
}

fn fnv1a(payload: &[u8]) -> u64 {
    let mut value = 0xCBF29CE484222325u64;
    for byte in payload {
        value ^= *byte as u64;
        value = value.wrapping_mul(0x100000001B3);
    }
    value
}
