use crate::types::Candidate;

pub fn rank(c: &Candidate) -> (i32, i32, i32, &str) {
    // Higher is better on first two fields, then lower ready tick, then lexical ID.
    let score = c.priority * 10 + c.age;
    let urgency = c.age;
    (score, urgency, -c.ready_tick, &c.flight_id)
}
