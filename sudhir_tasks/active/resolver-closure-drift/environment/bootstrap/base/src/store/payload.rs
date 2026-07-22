use std::path::{Path, PathBuf};

pub fn locate(root: &Path, relative: &str) -> Result<PathBuf, String> {
    if relative.starts_with('/') || relative.contains("..") {
        return Err("invalid payload path".to_string());
    }
    let path = root.join(relative);
    if !path.join("Cargo.toml").is_file() || !path.join("src/lib.rs").is_file() {
        return Err(format!("payload is incomplete: {}", path.display()));
    }
    Ok(path)
}
