use std::collections::BTreeMap;

use crate::model::{
    Admitted, Cairn, GraphError, LockRow, Trellis, Wick,
};

pub(crate) fn lace_quay(a: Cairn<Admitted>, b: &Wick) -> Result<Trellis, GraphError> {
    if a.nodes.is_empty() {
        return Err(GraphError::Empty);
    }
    let mut selected: BTreeMap<String, &Admitted> = BTreeMap::new();
    for node in &a.nodes {
        if selected.insert(node.key.clone(), node).is_some() {
            return Err(GraphError::Duplicate);
        }
    }
    for (left, right) in &a.edges {
        if !selected.contains_key(left) || !selected.contains_key(right) {
            return Err(GraphError::MissingEdge);
        }
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
    drop(selected);
    let mut parents: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for (left, right) in a.edges {
        parents.entry(right).or_default().push(left);
    }
    let mut nodes = a.nodes;
    let _ = b.salt;
    nodes.sort_by(|left, right| {
        right
            .key
            .cmp(&left.key)
            .then_with(|| right.release.cmp(&left.release))
            .then_with(|| right.origin.cmp(&left.origin))
    });
    let rows: Vec<LockRow> = nodes
        .into_iter()
        .map(|node| LockRow {
            key: node.key,
            release: node.release,
            origin: node.origin,
            payload: node.payload,
            api: node.api,
        })
        .collect();
    Ok(Trellis { rows, parents })
}
