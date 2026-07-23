use crate::error::{AppError, AppResult};

#[derive(Clone, Debug)]
pub struct Settings {
    pub trees_root: String,
    pub ledger: String,
    pub output: String,
    pub stage_root: String,
}

pub fn load(path: &std::path::Path) -> AppResult<Settings> {
    let text = std::fs::read_to_string(path).map_err(|e| AppError::msg(format!("conf: {e}")))?;
    let mut trees_root = String::from("/app/fixtures/trees");
    let mut ledger = String::from("/app/ledger/packed.bin");
    let mut output = String::from("/app/output/cutover_report.json");
    let mut stage_root = String::from("/app/var/stage");
    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.splitn(2, char::is_whitespace);
        let key = parts.next().unwrap_or("");
        let val = parts.next().unwrap_or("").trim();
        match key {
            "trees_root" => trees_root = val.to_string(),
            "ledger" => ledger = val.to_string(),
            "output" => output = val.to_string(),
            "stage_root" => stage_root = val.to_string(),
            _ => {}
        }
    }
    if let Ok(v) = std::env::var("HAZE_TREES") {
        if !v.is_empty() {
            trees_root = v;
        }
    }
    if let Ok(v) = std::env::var("HAZE_OUTPUT") {
        if !v.is_empty() {
            output = v;
        }
    }
    if let Ok(v) = std::env::var("HAZE_LEDGER") {
        if !v.is_empty() {
            ledger = v;
        }
    }
    Ok(Settings {
        trees_root,
        ledger,
        output,
        stage_root,
    })
}
