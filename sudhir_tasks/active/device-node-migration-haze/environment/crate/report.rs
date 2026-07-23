use crate::error::{AppError, AppResult};
use std::fs;
use std::path::Path;

#[derive(Clone, Debug)]
pub struct ProbeRow {
    pub name: String,
    pub open_ok: bool,
    pub identity_ok: bool,
    pub path_ok: bool,
    pub mode_ok: bool,
    pub id_hex: String,
}

#[derive(Clone, Debug)]
pub struct RunRow {
    pub family: String,
    pub tag: String,
    pub mode: String,
    pub entry_count: i32,
    pub exit_code: i32,
    pub open_ok: bool,
    pub identity_ok: bool,
    pub path_ok: bool,
    pub mode_ok: bool,
    pub rejected: bool,
    pub probes: Vec<ProbeRow>,
}

#[derive(Clone, Debug)]
pub struct Summary {
    pub failing_ok: bool,
    pub control_stable: bool,
    pub reject_stable: bool,
}

#[derive(Clone, Debug)]
pub struct Document {
    pub schema_version: i32,
    pub runs: Vec<RunRow>,
    pub summary: Summary,
}

pub fn save(path: &Path, document: &Document) -> AppResult<()> {
    let mut filled = document.clone();
    filled.summary = build_summary(&filled.runs);
    filled.runs.sort_by(|a, b| {
        (&a.family, &a.tag, &a.mode).cmp(&(&b.family, &b.tag, &b.mode))
    });
    let body = render_without_digest(&filled);
    let digest = fnv1a64(body.as_bytes());
    let mut out = body;
    if out.ends_with('}') {
        out.pop();
    }
    out.push_str(&format!(",\"digest\":\"{digest:016x}\"}}\n"));
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|e| AppError::msg(format!("out dir: {e}")))?;
    }
    fs::write(path, out).map_err(|e| AppError::msg(format!("write: {e}")))?;
    Ok(())
}

fn build_summary(runs: &[RunRow]) -> Summary {
    let mut failing_ok = true;
    let mut control_stable = true;
    let mut reject_stable = true;
    let mut saw_failing = false;
    let mut saw_control = false;
    let mut saw_reject = false;

    for row in runs {
        if row.family.starts_with("failing_")
            || (row.mode == "cutover" && row.family.contains("failing"))
        {
            saw_failing = true;
            if row.rejected || !row.open_ok || !row.identity_ok || !row.path_ok || !row.mode_ok {
                failing_ok = false;
            }
        }
        if row.family.starts_with("control_") || row.mode == "control" {
            saw_control = true;
            if row.rejected || row.exit_code != 0 || !row.open_ok {
                control_stable = false;
            }
        }
        if row.family.starts_with("reject_") || row.mode == "reject" {
            saw_reject = true;
            if !row.rejected {
                reject_stable = false;
            }
        }
    }
    if !saw_failing {
        failing_ok = false;
    }
    if !saw_control {
        control_stable = false;
    }
    if !saw_reject {
        reject_stable = false;
    }
    Summary {
        failing_ok,
        control_stable,
        reject_stable,
    }
}

fn esc(s: &str) -> String {
    let mut out = String::from("\"");
    for ch in s.chars() {
        match ch {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            _ => out.push(ch),
        }
    }
    out.push('"');
    out
}

fn render_without_digest(doc: &Document) -> String {
    let mut parts: Vec<String> = Vec::new();
    parts.push(format!("{{\"schema_version\":{}", doc.schema_version));
    parts.push(",\"runs\":[".to_string());
    for (i, row) in doc.runs.iter().enumerate() {
        if i > 0 {
            parts.push(",".to_string());
        }
        parts.push("{".to_string());
        parts.push(format!("\"family\":{},", esc(&row.family)));
        parts.push(format!("\"tag\":{},", esc(&row.tag)));
        parts.push(format!("\"mode\":{},", esc(&row.mode)));
        parts.push(format!("\"entry_count\":{},", row.entry_count));
        parts.push(format!("\"exit_code\":{},", row.exit_code));
        parts.push(format!("\"open_ok\":{},", row.open_ok));
        parts.push(format!("\"identity_ok\":{},", row.identity_ok));
        parts.push(format!("\"path_ok\":{},", row.path_ok));
        parts.push(format!("\"mode_ok\":{},", row.mode_ok));
        parts.push(format!("\"rejected\":{},", row.rejected));
        parts.push("\"probes\":[".to_string());
        for (j, p) in row.probes.iter().enumerate() {
            if j > 0 {
                parts.push(",".to_string());
            }
            parts.push(format!(
                "{{\"name\":{},\"open_ok\":{},\"identity_ok\":{},\"path_ok\":{},\"mode_ok\":{},\"id_hex\":{}}}",
                esc(&p.name),
                p.open_ok,
                p.identity_ok,
                p.path_ok,
                p.mode_ok,
                esc(&p.id_hex)
            ));
        }
        parts.push("]}".to_string());
    }
    parts.push("],\"summary\":{".to_string());
    parts.push(format!("\"failing_ok\":{},", doc.summary.failing_ok));
    parts.push(format!("\"control_stable\":{},", doc.summary.control_stable));
    parts.push(format!("\"reject_stable\":{}", doc.summary.reject_stable));
    parts.push("}}".to_string());
    parts.concat()
}

fn fnv1a64(data: &[u8]) -> u64 {
    let mut h: u64 = 0xCBF29CE484222325;
    for b in data {
        h ^= *b as u64;
        h = h.wrapping_mul(0x100000001B3);
    }
    h
}
