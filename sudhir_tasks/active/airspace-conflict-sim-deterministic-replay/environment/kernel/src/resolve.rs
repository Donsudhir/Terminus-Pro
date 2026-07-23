use crate::ranker::rank;
use crate::types::Candidate;

pub fn resolve(mut candidates: Vec<Candidate>, capacity: usize) -> Vec<String> {
    candidates.sort_by(|a, b| {
        let ka = rank(a);
        let kb = rank(b);
        kb.cmp(&ka)
    });

    candidates
        .into_iter()
        .take(capacity)
        .map(|c| c.flight_id)
        .collect()
}
