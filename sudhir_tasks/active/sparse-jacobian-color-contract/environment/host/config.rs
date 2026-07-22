use std::path::Path;

#[derive(Clone, Debug)]
pub struct Settings {
    pub input: String,
    pub output: String,
    pub step_floor: f64,
    pub step_gain: f64,
}

pub fn load(path: &Path) -> crate::error::AppResult<Settings> {
    let text = std::fs::read_to_string(path).map_err(|err| format!("config read: {err}"))?;
    let mut input = String::from("/app/data/families.resid");
    let mut output = String::from("/app/output/sensitivity_report.json");
    let mut step_floor = 1.0e-8;
    let mut step_gain = 0.5;
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.split_whitespace();
        let key = parts.next().unwrap_or("");
        match key {
            "input" => {
                if let Some(value) = parts.next() {
                    input = value.to_string();
                }
            }
            "output" => {
                if let Some(value) = parts.next() {
                    output = value.to_string();
                }
            }
            "step_floor" => {
                if let Some(value) = parts.next() {
                    step_floor = value
                        .parse()
                        .map_err(|_| "config step_floor".to_string())?;
                }
            }
            "step_gain" => {
                if let Some(value) = parts.next() {
                    step_gain = value.parse().map_err(|_| "config step_gain".to_string())?;
                }
            }
            _ => {}
        }
    }
    if let Ok(value) = std::env::var("SENSLAB_INPUT") {
        input = value;
    }
    if let Ok(value) = std::env::var("SENSLAB_OUTPUT") {
        output = value;
    }
    Ok(Settings {
        input,
        output,
        step_floor,
        step_gain,
    })
}
