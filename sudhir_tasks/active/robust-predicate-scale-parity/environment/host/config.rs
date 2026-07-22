use crate::error::{with_path, AppResult};
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

pub(crate) struct RuntimeConfig {
    pub(crate) input: PathBuf,
    pub(crate) output: PathBuf,
}

pub(crate) fn load(path: &Path) -> AppResult<RuntimeConfig> {
    let text = fs::read_to_string(path).map_err(|error| with_path("read", path, error))?;
    let mut values = BTreeMap::new();
    for (index, raw) in text.lines().enumerate() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let Some((key, value)) = line.split_once('=') else {
            return Err(format!("{}:{} malformed setting", path.display(), index + 1));
        };
        values.insert(key.trim().to_string(), value.trim().to_string());
    }
    let default_input = values
        .remove("input")
        .ok_or_else(|| format!("{} missing input setting", path.display()))?;
    let default_output = values
        .remove("output")
        .ok_or_else(|| format!("{} missing output setting", path.display()))?;
    if !values.is_empty() {
        return Err(format!("{} contains unknown settings", path.display()));
    }
    let input = std::env::var_os("GEOMLAB_INPUT")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from(default_input));
    let output = std::env::var_os("GEOMLAB_OUTPUT")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from(default_output));
    Ok(RuntimeConfig { input, output })
}
