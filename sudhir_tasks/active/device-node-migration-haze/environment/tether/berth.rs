pub fn format_label(slot: u32, rel: &str) -> String {
    format!("slot{slot}:{rel}")
}

pub fn shorten(rel: &str, max: usize) -> String {
    if rel.len() <= max {
        rel.to_string()
    } else {
        format!("{}…", &rel[..max.saturating_sub(1)])
    }
}
