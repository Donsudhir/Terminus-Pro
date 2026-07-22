pub(crate) fn map_banner(code: i32) -> &'static str {
    match code {
        0 => "ready",
        1 => "running",
        2 => "paused",
        _ => "unknown",
    }
}

pub(crate) fn compose_status(code: i32, detail: i32) -> String {
    format!("{}:{}", map_banner(code), detail)
}
