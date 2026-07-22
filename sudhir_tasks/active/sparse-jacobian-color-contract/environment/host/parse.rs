use crate::model::{FamilySpec, TagSpec};
use std::fs;
use std::path::Path;

pub fn load(path: &Path) -> Result<Vec<FamilySpec>, String> {
    let text = fs::read_to_string(path).map_err(|err| format!("input read: {err}"))?;
    let mut families = Vec::new();
    let mut current: Option<FamilySpec> = None;

    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.split_whitespace();
        let head = parts.next().unwrap_or("");
        match head {
            "family" => {
                if let Some(family) = current.take() {
                    families.push(family);
                }
                let name = parts.next().ok_or("family name")?.to_string();
                current = Some(FamilySpec {
                    name,
                    dim: 0,
                    equations: Vec::new(),
                    base: Vec::new(),
                    tags: Vec::new(),
                    permutations: Vec::new(),
                });
            }
            "dim" => {
                let family = current.as_mut().ok_or("dim outside family")?;
                family.dim = parts
                    .next()
                    .ok_or("dim value")?
                    .parse()
                    .map_err(|_| "dim parse")?;
            }
            "eq" => {
                let family = current.as_mut().ok_or("eq outside family")?;
                let count: usize = parts.next().ok_or("eq count")?.parse().map_err(|_| "eq parse")?;
                family.equations.clear();
                for _ in 0..count {
                    family.equations.push(Vec::new());
                }
            }
            "term" => {
                let family = current.as_mut().ok_or("term outside family")?;
                let eq: usize = parts.next().ok_or("term eq")?.parse().map_err(|_| "term eq")?;
                let col: usize = parts.next().ok_or("term col")?.parse().map_err(|_| "term col")?;
                let coeff: f64 = parts
                    .next()
                    .ok_or("term coeff")?
                    .parse()
                    .map_err(|_| "term coeff")?;
                if eq == 0 || eq > family.equations.len() {
                    return Err("term eq range".into());
                }
                if col == 0 || col > family.dim {
                    return Err("term col range".into());
                }
                family.equations[eq - 1].push((col - 1, coeff));
            }
            "base" => {
                let family = current.as_mut().ok_or("base outside family")?;
                family.base.clear();
                for token in parts {
                    family.base.push(token.parse().map_err(|_| "base parse")?);
                }
                if family.base.len() != family.dim {
                    return Err("base length".into());
                }
            }
            "tag" => {
                let family = current.as_mut().ok_or("tag outside family")?;
                let name = parts.next().ok_or("tag name")?.to_string();
                let scale: f64 = parts.next().ok_or("tag scale")?.parse().map_err(|_| "tag scale")?;
                let mut shift = Vec::new();
                for token in parts {
                    shift.push(token.parse().map_err(|_| "tag shift")?);
                }
                if shift.len() != family.dim {
                    return Err("tag shift length".into());
                }
                family.tags.push(TagSpec { name, scale, shift });
            }
            "perm" => {
                let family = current.as_mut().ok_or("perm outside family")?;
                let name = parts.next().ok_or("perm name")?.to_string();
                let mut order = Vec::new();
                for token in parts {
                    let idx: usize = token.parse().map_err(|_| "perm idx")?;
                    if idx == 0 || idx > family.dim {
                        return Err("perm range".into());
                    }
                    order.push(idx - 1);
                }
                if order.len() != family.dim {
                    return Err("perm length".into());
                }
                family.permutations.push((name, order));
            }
            "end" => {
                let family = current.take().ok_or("end without family")?;
                if family.equations.is_empty() || family.tags.is_empty() {
                    return Err("incomplete family".into());
                }
                families.push(family);
            }
            _ => return Err(format!("unknown record: {head}")),
        }
    }
    if current.is_some() {
        return Err("unclosed family".into());
    }
    if families.is_empty() {
        return Err("no families".into());
    }
    Ok(families)
}
