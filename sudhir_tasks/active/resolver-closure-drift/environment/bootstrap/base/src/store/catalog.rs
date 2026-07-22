use std::fs;
use std::path::Path;

use crate::model::{Need, RawRecord};

#[derive(Clone, Debug)]
pub struct Catalog {
    rows: Vec<RawRecord>,
}

impl Catalog {
    pub fn load(path: &Path) -> Result<Self, String> {
        let text = fs::read_to_string(path)
            .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
        let mut rows = Vec::new();
        for line in text.lines().map(str::trim) {
            if !line.starts_with('{') {
                continue;
            }
            let key = string_field(line, "name")?;
            let needs_text = string_field(line, "needs")?;
            let needs = if needs_text.is_empty() {
                Vec::new()
            } else {
                needs_text
                    .split(';')
                    .map(Need::parse)
                    .collect::<Result<Vec<Need>, String>>()?
            };
            rows.push(RawRecord {
                key,
                release: string_field(line, "version")?,
                code: int_field(line, "code")?,
                origin: string_field(line, "source")?,
                preview: bool_field(line, "preview")?,
                withdrawn: bool_field(line, "withdrawn")?,
                needs,
                payload: string_field(line, "payload")?,
                api: string_field(line, "api")?,
                serial: rows.len(),
            });
        }
        if rows.is_empty() {
            return Err("catalog contains no records".to_string());
        }
        Ok(Self { rows })
    }

    pub fn for_key(&self, key: &str) -> Vec<RawRecord> {
        self.rows
            .iter()
            .filter(|row| row.key == key)
            .cloned()
            .collect()
    }
}

fn string_field(text: &str, key: &str) -> Result<String, String> {
    let marker = format!("\"{key}\":\"");
    let start = text
        .find(&marker)
        .map(|position| position + marker.len())
        .ok_or_else(|| format!("missing string field: {key}"))?;
    let end = text[start..]
        .find('"')
        .map(|offset| start + offset)
        .ok_or_else(|| format!("unterminated string field: {key}"))?;
    Ok(text[start..end].to_string())
}

fn int_field(text: &str, key: &str) -> Result<u32, String> {
    let marker = format!("\"{key}\":");
    let start = text
        .find(&marker)
        .map(|position| position + marker.len())
        .ok_or_else(|| format!("missing integer field: {key}"))?;
    let end = text[start..]
        .find([',', '}'])
        .map(|offset| start + offset)
        .ok_or_else(|| format!("unterminated integer field: {key}"))?;
    text[start..end]
        .parse::<u32>()
        .map_err(|_| format!("invalid integer field: {key}"))
}

fn bool_field(text: &str, key: &str) -> Result<bool, String> {
    let marker = format!("\"{key}\":");
    let start = text
        .find(&marker)
        .map(|position| position + marker.len())
        .ok_or_else(|| format!("missing boolean field: {key}"))?;
    Ok(text[start..].starts_with("true"))
}
