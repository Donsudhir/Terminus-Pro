use crate::error::{AppError, AppResult};
use crate::ffi;
use std::fs;
use std::path::Path;

#[derive(Clone, Debug)]
pub struct RunRow {
    pub family: String,
    pub tag: String,
    pub mode: String,
    pub field_digest: String,
    pub residual_samples: Vec<f64>,
    pub residual_norm: f64,
    pub iterations: i32,
    pub reuse_mark: u64,
    pub layout_token: String,
    pub fold_order: Vec<i32>,
    pub values: Vec<f64>,
}

#[derive(Clone, Debug)]
pub struct Summary {
    pub twin_agree: bool,
    pub control_stable: bool,
    pub digest_match: bool,
}

#[derive(Clone, Debug)]
pub struct Document {
    pub schema_version: i32,
    pub runs: Vec<RunRow>,
    pub summary: Summary,
}

pub fn save(path: &Path, document: &Document) -> AppResult<()> {
    let mut filled = document.clone();
    for row in &mut filled.runs {
        row.field_digest = fold_digest(&row.values, &row.fold_order)?;
    }
    filled.summary = build_summary(&filled.runs);
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

fn fold_digest(values: &[f64], order: &[i32]) -> AppResult<String> {
    let n = values.len() as i32;
    if n <= 0 || order.len() != values.len() {
        return Err(AppError::msg("fold width"));
    }
    let mut buf: Vec<u64> = Vec::with_capacity(values.len() * 2);
    for &idx in order {
        buf.push(idx as u64);
    }
    for &v in values {
        buf.push(v.to_bits());
    }
    let mut out = 0_u64;
    let rc = unsafe { ffi::sift_s(buf.as_ptr(), n, &mut out as *mut u64) };
    if rc != 0 {
        return Err(AppError::msg("fold sift"));
    }
    Ok(format!("{out:016x}"))
}

fn build_summary(runs: &[RunRow]) -> Summary {
    let mut twin_agree = true;
    let mut digest_match = true;
    let mut families: Vec<(String, String)> = Vec::new();
    for row in runs {
        let key = (row.family.clone(), row.tag.clone());
        if !families.contains(&key) {
            families.push(key);
        }
    }
    for (family, tag) in &families {
        let twin = runs.iter().find(|r| {
            r.family == *family && r.tag == *tag && r.mode == "twin"
        });
        let mapped = runs.iter().find(|r| {
            r.family == *family && r.tag == *tag && r.mode == "mapped"
        });
        match (twin, mapped) {
            (Some(t), Some(m)) => {
                if t.field_digest != m.field_digest {
                    twin_agree = false;
                }
            }
            _ => twin_agree = false,
        }
    }
    for row in runs {
        if independent_fold(&row.values, &row.fold_order) != row.field_digest {
            digest_match = false;
        }
    }
    let control_stable = runs
        .iter()
        .filter(|r| r.mode == "control")
        .all(|r| r.reuse_mark == 0);
    Summary {
        twin_agree,
        control_stable,
        digest_match,
    }
}

fn independent_fold(values: &[f64], order: &[i32]) -> String {
    let mut h: u64 = 0xCBF29CE484222325;
    for &idx in order {
        let sample = values[idx as usize];
        let bytes = sample.to_le_bytes();
        for b in bytes {
            h ^= b as u64;
            h = h.wrapping_mul(0x100000001B3);
        }
    }
    format!("{h:016x}")
}

fn render_without_digest(doc: &Document) -> String {
    let mut s = String::from("{\"schema_version\":");
    s.push_str(&doc.schema_version.to_string());
    s.push_str(",\"runs\":[");
    for (i, row) in doc.runs.iter().enumerate() {
        if i > 0 {
            s.push(',');
        }
        s.push_str(&render_row(row));
    }
    s.push_str("],\"summary\":{");
    s.push_str("\"twin_agree\":");
    s.push_str(if doc.summary.twin_agree { "true" } else { "false" });
    s.push_str(",\"control_stable\":");
    s.push_str(if doc.summary.control_stable {
        "true"
    } else {
        "false"
    });
    s.push_str(",\"digest_match\":");
    s.push_str(if doc.summary.digest_match {
        "true"
    } else {
        "false"
    });
    s.push_str("}}");
    s
}

fn render_row(row: &RunRow) -> String {
    let mut s = String::from("{");
    s.push_str(&format!("\"family\":{},", json_str(&row.family)));
    s.push_str(&format!("\"tag\":{},", json_str(&row.tag)));
    s.push_str(&format!("\"mode\":{},", json_str(&row.mode)));
    s.push_str(&format!("\"field_digest\":{},", json_str(&row.field_digest)));
    s.push_str("\"samples\":[");
    for (i, v) in row.values.iter().enumerate() {
        if i > 0 {
            s.push(',');
        }
        s.push_str(&format!("{v:.17}"));
    }
    s.push_str("],\"residual_samples\":[");
    for (i, v) in row.residual_samples.iter().enumerate() {
        if i > 0 {
            s.push(',');
        }
        s.push_str(&format!("{v:.17}"));
    }
    s.push_str(&format!("],\"residual_norm\":{:.17},", row.residual_norm));
    s.push_str(&format!("\"iterations\":{},", row.iterations));
    s.push_str(&format!("\"reuse_mark\":{},", row.reuse_mark));
    s.push_str(&format!(
        "\"layout_token\":{},",
        json_str(&row.layout_token)
    ));
    s.push_str("\"fold_order\":[");
    for (i, v) in row.fold_order.iter().enumerate() {
        if i > 0 {
            s.push(',');
        }
        s.push_str(&v.to_string());
    }
    s.push_str("]}");
    s
}

fn json_str(v: &str) -> String {
    format!("\"{}\"", v.replace('\\', "\\\\").replace('"', "\\\""))
}

fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut h: u64 = 0xCBF29CE484222325;
    for &b in bytes {
        h ^= b as u64;
        h = h.wrapping_mul(0x100000001B3);
    }
    h
}
