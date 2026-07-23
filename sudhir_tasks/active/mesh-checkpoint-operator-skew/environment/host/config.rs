use crate::error::{AppError, AppResult};
use std::env;
use std::fs;
use std::path::Path;

#[derive(Clone, Debug)]
pub struct Settings {
    pub input: String,
    pub output: String,
    pub half_steps: i32,
    pub full_steps: i32,
    pub dt: f64,
}

pub fn load(path: &Path) -> AppResult<Settings> {
    let text = fs::read_to_string(path).map_err(|e| AppError::msg(format!("conf: {e}")))?;
    let mut input = String::from("/app/data/families.case");
    let mut output = String::from("/app/output/parity_report.json");
    let mut half_steps = 4_i32;
    let mut full_steps = 8_i32;
    let mut dt = 0.05_f64;
    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.split_whitespace();
        let key = parts.next().unwrap_or("");
        let value = parts.next().unwrap_or("");
        match key {
            "input" => input = value.to_string(),
            "output" => output = value.to_string(),
            "half_steps" => {
                half_steps = value.parse().map_err(|_| AppError::msg("half_steps"))?
            }
            "full_steps" => {
                full_steps = value.parse().map_err(|_| AppError::msg("full_steps"))?
            }
            "dt" => dt = value.parse().map_err(|_| AppError::msg("dt"))?,
            _ => {}
        }
    }
    if let Ok(v) = env::var("MESHLAB_INPUT") {
        if !v.is_empty() {
            input = v;
        }
    }
    if let Ok(v) = env::var("MESHLAB_OUTPUT") {
        if !v.is_empty() {
            output = v;
        }
    }
    Ok(Settings {
        input,
        output,
        half_steps,
        full_steps,
        dt,
    })
}
