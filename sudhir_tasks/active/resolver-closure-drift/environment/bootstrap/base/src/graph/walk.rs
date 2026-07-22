use std::collections::{BTreeMap, VecDeque};

use crate::aero::veil::cast_vane;
use crate::cairn::sill::turn_sill;
use crate::model::{
    Admitted, Cairn, Need, PolicyFrame, PolicyMode, QueryFrame,
};
use crate::store::catalog::Catalog;

pub fn resolve(
    catalog: &Catalog,
    roots: &[Need],
    mode: PolicyMode,
    salt: usize,
) -> Result<Cairn<Admitted>, String> {
    let mut ordered_roots = roots.to_vec();
    if salt % 2 == 1 {
        ordered_roots.reverse();
    }
    let mut queue: VecDeque<(Need, String, bool)> = ordered_roots
        .into_iter()
        .map(|need| (need, "root".to_string(), true))
        .collect();
    let mut constraints: BTreeMap<String, Vec<Need>> = BTreeMap::new();
    let mut chosen: Vec<Admitted> = Vec::new();
    let mut edges = Vec::new();
    let mut turns = 0usize;

    while let Some((need, from, root)) = queue.pop_front() {
        turns += 1;
        if turns > 256 {
            return Err("graph walk did not converge".to_string());
        }
        if from != "root" {
            edges.push((from, need.key.clone()));
        }
        let known = constraints.entry(need.key.clone()).or_default();
        if !known.contains(&need) {
            known.push(need.clone());
        }
        let effective = meet(known)?;
        let candidates = catalog.for_key(&effective.key);
        let stable_available = candidates
            .iter()
            .any(|row| effective.accepts(row) && !row.preview && !row.withdrawn);
        let mut admitted = Vec::new();
        for (ordinal, raw) in candidates.iter().enumerate() {
            let query = QueryFrame {
                need: effective.clone(),
                mode,
                root,
                stable_available,
                ordinal: ordinal + raw.serial,
            };
            if let Ok(vane) = cast_vane(raw, &query) {
                let policy = PolicyFrame {
                    mode,
                    exact: effective.exact.is_some(),
                    stable_available,
                    root,
                };
                if let Ok(row) = turn_sill(vane, &policy) {
                    admitted.push(row);
                }
            }
        }
        admitted.sort_by(|left, right| {
            left.priority
                .cmp(&right.priority)
                .then_with(|| right.code.cmp(&left.code))
                .then_with(|| left.serial.cmp(&right.serial))
        });
        let next = admitted
            .into_iter()
            .next()
            .ok_or_else(|| format!("resolution stalled for {}", effective.key))?;
        if let Some(position) = chosen.iter().position(|row| row.key == next.key) {
            if chosen[position].identity() == next.identity() {
                continue;
            }
            chosen[position] = next.clone();
        } else {
            chosen.push(next.clone());
        }
        for child in &next.needs {
            queue.push_back((child.clone(), next.key.clone(), false));
        }
    }
    Ok(Cairn::new(chosen, edges))
}

fn meet(rows: &[Need]) -> Result<Need, String> {
    let first = rows
        .first()
        .ok_or_else(|| "empty constraint group".to_string())?;
    let low = rows.iter().map(|row| row.low).max().unwrap_or(first.low);
    let high = rows.iter().map(|row| row.high).min().unwrap_or(first.high);
    let exact = rows.iter().find_map(|row| row.exact);
    if low >= high || exact.is_some_and(|value| value < low || value >= high) {
        return Err(format!("incompatible constraints for {}", first.key));
    }
    Ok(Need {
        key: first.key.clone(),
        low,
        high,
        preview: rows.iter().any(|row| row.preview),
        exact,
    })
}
