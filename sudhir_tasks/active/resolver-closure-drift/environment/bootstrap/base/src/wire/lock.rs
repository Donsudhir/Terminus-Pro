use std::fs;
use std::path::Path;

use crate::model::Trellis;

pub fn write(path: &Path, trellis: &Trellis) -> Result<(), String> {
    let mut body = String::new();
    for row in &trellis.rows {
        for value in [&row.key, &row.release, &row.origin] {
            if value.is_empty() || value.bytes().any(|byte| byte.is_ascii_whitespace()) {
                return Err("invalid lock value".to_string());
            }
        }
        body.push_str(&row.key);
        body.push(' ');
        body.push_str(&row.release);
        body.push(' ');
        body.push_str(&row.origin);
        body.push('\n');
    }
    let parent = path
        .parent()
        .ok_or_else(|| "lock path has no parent".to_string())?;
    fs::create_dir_all(parent)
        .map_err(|error| format!("cannot create {}: {error}", parent.display()))?;
    let temporary = path.with_extension("lock.next");
    fs::write(&temporary, body.as_bytes())
        .map_err(|error| format!("cannot write {}: {error}", temporary.display()))?;
    fs::rename(&temporary, path)
        .map_err(|error| format!("cannot replace {}: {error}", path.display()))
}
