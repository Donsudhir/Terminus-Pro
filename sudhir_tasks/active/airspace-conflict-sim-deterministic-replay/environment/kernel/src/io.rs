use crate::types::{Request, Response};
use std::io::{self, Read};

pub fn read_request() -> Result<Request, String> {
    let mut buf = String::new();
    io::stdin()
        .read_to_string(&mut buf)
        .map_err(|e| format!("stdin read failed: {e}"))?;
    serde_json::from_str(&buf).map_err(|e| format!("json decode failed: {e}"))
}

pub fn encode_response(accepted: Vec<String>) -> Result<String, String> {
    serde_json::to_string(&Response { accepted }).map_err(|e| format!("json encode failed: {e}"))
}
