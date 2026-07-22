use crate::error::{with_path, AppResult};
use crate::model::{Dyadic, Family, Point, Variant};
use std::collections::BTreeSet;
use std::fs;
use std::path::Path;

fn valid_name(value: &str) -> bool {
    !value.is_empty()
        && value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || byte == b'_' || byte == b'-')
}

fn dyadic(token: &str) -> AppResult<Dyadic> {
    let Some((mantissa, exponent)) = token.rsplit_once('@') else {
        return Err(format!("invalid dyadic value {token}"));
    };
    let mantissa = mantissa
        .parse::<i64>()
        .map_err(|_| format!("invalid dyadic mantissa {token}"))?;
    let exponent = exponent
        .parse::<i32>()
        .map_err(|_| format!("invalid dyadic exponent {token}"))?;
    if mantissa.unsigned_abs() > 1_000_000_000 || !(-900..=900).contains(&exponent) {
        return Err(format!("dyadic value outside supported range {token}"));
    }
    Ok(Dyadic { mantissa, exponent })
}

fn finish(family: Family) -> AppResult<Family> {
    if !(6..=12).contains(&family.points.len()) {
        return Err(format!("family {} has unsupported point cardinality", family.name));
    }
    if family.variants.is_empty() {
        return Err(format!("family {} has no variants", family.name));
    }
    let mut ids = BTreeSet::new();
    for point in &family.points {
        if !ids.insert(point.id) {
            return Err(format!("family {} repeats a point identity", family.name));
        }
    }
    let mut variants = BTreeSet::new();
    for variant in &family.variants {
        if !variants.insert(variant.name.as_str()) {
            return Err(format!("family {} repeats a variant name", family.name));
        }
    }
    let floor = family
        .points
        .iter()
        .flat_map(|point| point.xyz.iter().map(|value| value.exponent))
        .min()
        .ok_or_else(|| format!("family {} has no coordinates", family.name))?;
    for point in &family.points {
        for value in point.xyz {
            let shift = value.exponent - floor;
            if !(0..=30).contains(&shift) {
                return Err(format!("family {} has excessive exponent spread", family.name));
            }
            let aligned = (value.mantissa as i128) << shift;
            if aligned.abs() > 1_000_000 {
                return Err(format!("family {} exceeds the refinement lattice", family.name));
            }
        }
    }
    Ok(family)
}

pub(crate) fn load(path: &Path) -> AppResult<Vec<Family>> {
    let text = fs::read_to_string(path).map_err(|error| with_path("read", path, error))?;
    let mut result = Vec::new();
    let mut current: Option<Family> = None;
    for (line_index, raw) in text.lines().enumerate() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let fields: Vec<&str> = line.split_whitespace().collect();
        let line_number = line_index + 1;
        match fields.first().copied() {
            Some("family") if fields.len() == 2 => {
                if current.is_some() || !valid_name(fields[1]) {
                    return Err(format!("{}:{line_number} invalid family header", path.display()));
                }
                current = Some(Family {
                    name: fields[1].to_string(),
                    points: Vec::new(),
                    variants: Vec::new(),
                });
            }
            Some("point") if fields.len() == 5 => {
                let family = current
                    .as_mut()
                    .ok_or_else(|| format!("{}:{line_number} point outside family", path.display()))?;
                let id = fields[1]
                    .parse::<i32>()
                    .map_err(|_| format!("{}:{line_number} invalid point identity", path.display()))?;
                family.points.push(Point {
                    id,
                    xyz: [dyadic(fields[2])?, dyadic(fields[3])?, dyadic(fields[4])?],
                });
            }
            Some("variant") if fields.len() == 6 => {
                let family = current
                    .as_mut()
                    .ok_or_else(|| format!("{}:{line_number} variant outside family", path.display()))?;
                if !valid_name(fields[1]) {
                    return Err(format!("{}:{line_number} invalid variant name", path.display()));
                }
                let scale = fields[2]
                    .parse::<i32>()
                    .map_err(|_| format!("{}:{line_number} invalid scale exponent", path.display()))?;
                if !(-700..=700).contains(&scale) {
                    return Err(format!("{}:{line_number} scale exponent outside supported range", path.display()));
                }
                family.variants.push(Variant {
                    name: fields[1].to_string(),
                    scale,
                    shift: [dyadic(fields[3])?, dyadic(fields[4])?, dyadic(fields[5])?],
                });
            }
            Some("end") if fields.len() == 1 => {
                let family = current
                    .take()
                    .ok_or_else(|| format!("{}:{line_number} unmatched end", path.display()))?;
                result.push(finish(family)?);
            }
            _ => return Err(format!("{}:{line_number} malformed record", path.display())),
        }
    }
    if current.is_some() {
        return Err(format!("{} has an unterminated family", path.display()));
    }
    if result.is_empty() {
        return Err(format!("{} contains no families", path.display()));
    }
    let mut names = BTreeSet::new();
    for family in &result {
        if !names.insert(family.name.as_str()) {
            return Err(format!("{} repeats a family name", path.display()));
        }
    }
    Ok(result)
}
