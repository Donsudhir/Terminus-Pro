pub fn banner_code(kind: i32) -> &'static str {
    match kind {
        0 => "ok",
        1 => "warn",
        2 => "hold",
        _ => "misc",
    }
}

pub fn map_status(code: i32) -> i32 {
    if code == 0 {
        10
    } else if code < 0 {
        20
    } else {
        30
    }
}
