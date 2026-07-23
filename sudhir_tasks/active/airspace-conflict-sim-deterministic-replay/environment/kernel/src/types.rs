use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct Candidate {
    pub flight_id: String,
    pub priority: i32,
    pub age: i32,
    pub ready_tick: i32,
}

#[derive(Debug, Deserialize)]
pub struct Request {
    pub capacity: usize,
    pub candidates: Vec<Candidate>,
}

#[derive(Debug, Serialize)]
pub struct Response {
    pub accepted: Vec<String>,
}
