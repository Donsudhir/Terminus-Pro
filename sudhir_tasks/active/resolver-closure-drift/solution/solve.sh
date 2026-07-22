#!/usr/bin/env bash
set -euo pipefail

cat > /app/bootstrap/base/src/aero/veil.rs <<'EOF'
use crate::model::{
    ClassError, PolicyMode, QueryFrame, RawRecord, Vane, VaneKind,
};

pub(crate) fn cast_vane(a: &RawRecord, b: &QueryFrame) -> Result<Vane, ClassError> {
    if a.key.is_empty()
        || a.release.is_empty()
        || a.origin.is_empty()
        || a.payload.is_empty()
        || a.api.is_empty()
    {
        return Err(ClassError::Empty);
    }
    if b.need.low >= b.need.high || !b.need.accepts(a) {
        return Err(ClassError::Outside);
    }
    if a.withdrawn && b.stable_available && b.need.exact.is_none() {
        return Err(ClassError::Contradictory);
    }
    let kind = match (a.preview, a.withdrawn, b.mode) {
        (true, false, PolicyMode::Alpha | PolicyMode::Mixed)
            if b.need.preview =>
        {
            VaneKind::Alpha
        }
        (false, true, PolicyMode::Beta | PolicyMode::Mixed)
            if b.need.exact == Some(a.code) =>
        {
            VaneKind::Beta
        }
        (false, false, _) => VaneKind::Normal,
        _ => return Err(ClassError::Contradictory),
    };
    let mut needs = a.needs.clone();
    needs.sort_by(|left, right| {
        left.key
            .cmp(&right.key)
            .then_with(|| left.low.cmp(&right.low))
            .then_with(|| left.high.cmp(&right.high))
            .then_with(|| left.exact.cmp(&right.exact))
    });
    if needs
        .iter()
        .any(|need| need.key.is_empty() || need.low >= need.high)
    {
        return Err(ClassError::Contradictory);
    }
    needs.dedup();
    Ok(Vane {
        key: a.key.clone(),
        release: a.release.clone(),
        code: a.code,
        origin: a.origin.clone(),
        kind,
        withdrawn: a.withdrawn,
        needs,
        payload: a.payload.clone(),
        api: a.api.clone(),
        serial: a.serial,
    })
}
EOF

cat > /app/bootstrap/base/src/cairn/sill.rs <<'EOF'
use crate::model::{
    Admitted, PolicyFrame, PolicyMode, RejectCode, Vane, VaneKind,
};

pub(crate) fn turn_sill(a: Vane, b: &PolicyFrame) -> Result<Admitted, RejectCode> {
    let priority = match (a.kind, b.mode) {
        (VaneKind::Alpha, PolicyMode::Alpha | PolicyMode::Mixed)
            if !a.withdrawn =>
        {
            0
        }
        (VaneKind::Beta, PolicyMode::Beta | PolicyMode::Mixed)
            if a.withdrawn && b.exact =>
        {
            0
        }
        (VaneKind::HeldLane, PolicyMode::Beta | PolicyMode::Mixed)
            if a.withdrawn && b.exact =>
        {
            0
        }
        (VaneKind::Normal, _) if !a.withdrawn => {
            if b.stable_available {
                10
            } else if b.root {
                20
            } else {
                30
            }
        }
        (VaneKind::HeldPin, _) | (VaneKind::HeldLane, _) => {
            return Err(RejectCode::Held);
        }
        (VaneKind::Alpha, _) | (VaneKind::Beta, _) => {
            return Err(RejectCode::Context);
        }
        (VaneKind::Normal, _) => return Err(RejectCode::Withdrawn),
    };
    if matches!(a.kind, VaneKind::Beta | VaneKind::HeldLane)
        && (!b.exact || !a.withdrawn)
    {
        return Err(RejectCode::Context);
    }
    Ok(Admitted {
        key: a.key,
        release: a.release,
        code: a.code,
        origin: a.origin,
        needs: a.needs,
        payload: a.payload,
        api: a.api,
        priority,
        kind: a.kind,
        serial: a.serial,
    })
}
EOF

cat > /app/bootstrap/base/src/quill/quay.rs <<'EOF'
use std::collections::BTreeMap;

use crate::model::{
    Admitted, Cairn, GraphError, LockRow, Trellis, Wick,
};

pub(crate) fn lace_quay(a: Cairn<Admitted>, b: &Wick) -> Result<Trellis, GraphError> {
    if a.nodes.is_empty() || b.roots.is_empty() {
        return Err(GraphError::Empty);
    }
    let mut selected: BTreeMap<String, &Admitted> = BTreeMap::new();
    for node in &a.nodes {
        if selected.insert(node.key.clone(), node).is_some() {
            return Err(GraphError::Duplicate);
        }
    }
    let mut parents: BTreeMap<String, Vec<String>> = BTreeMap::new();
    let mut children: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for (left, right) in &a.edges {
        if !selected.contains_key(left) || !selected.contains_key(right) {
            return Err(GraphError::MissingEdge);
        }
        parents.entry(right.clone()).or_default().push(left.clone());
        children.entry(left.clone()).or_default().push(right.clone());
    }
    for node in &a.nodes {
        for need in &node.needs {
            let child = selected
                .get(&need.key)
                .ok_or(GraphError::MissingEdge)?;
            if child.code < need.low
                || child.code >= need.high
                || need.exact.is_some_and(|value| value != child.code)
                || !a.edges.contains(&(node.key.clone(), need.key.clone()))
            {
                return Err(GraphError::MissingEdge);
            }
        }
    }
    let mut seen = std::collections::BTreeSet::new();
    let mut queue: std::collections::VecDeque<String> =
        b.roots.iter().cloned().collect();
    while let Some(key) = queue.pop_front() {
        if !seen.insert(key.clone()) {
            continue;
        }
        if let Some(next) = children.get(&key) {
            for child in next {
                queue.push_back(child.clone());
            }
        }
    }
    if seen.len() != selected.len() {
        return Err(GraphError::ExtraNode);
    }
    for values in parents.values_mut() {
        values.sort();
        values.dedup();
    }
    let selected_len = selected.len();
    drop(selected);
    let mut rows: Vec<LockRow> = a
        .nodes
        .into_iter()
        .map(|node| LockRow {
            key: node.key,
            release: node.release,
            origin: node.origin,
            payload: node.payload,
            api: node.api,
        })
        .collect();
    rows.sort();
    rows.dedup();
    if rows.len() != selected_len {
        return Err(GraphError::Duplicate);
    }
    Ok(Trellis { rows, parents })
}
EOF
