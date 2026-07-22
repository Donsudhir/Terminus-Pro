use std::fs;
use std::path::Path;
use std::process::Command;

use crate::model::Trellis;
use crate::store::payload::locate;

pub fn compile(
    trellis: &Trellis,
    archive_root: &Path,
    apis: &[String],
) -> Result<(), String> {
    let root = std::env::temp_dir().join(format!("forge-payload-{}", std::process::id()));
    if root.exists() {
        fs::remove_dir_all(&root)
            .map_err(|error| format!("cannot clear {}: {error}", root.display()))?;
    }
    fs::create_dir_all(root.join("src"))
        .map_err(|error| format!("cannot create {}: {error}", root.display()))?;

    let mut manifest = String::from(
        "[package]\nname = \"payload-check\"\nversion = \"0.0.0\"\nedition = \"2021\"\n\n[dependencies]\n",
    );
    for row in &trellis.rows {
        let path = locate(archive_root, &row.payload)?;
        manifest.push_str(&format!(
            "{} = {{ path = {:?} }}\n",
            row.key,
            path.as_os_str()
        ));
    }
    fs::write(root.join("Cargo.toml"), manifest)
        .map_err(|error| format!("cannot write build manifest: {error}"))?;

    let mut main_rs = String::from("fn main() {\n");
    for item in apis {
        let (crate_name, symbol) = item
            .split_once(':')
            .ok_or_else(|| format!("invalid api request: {item}"))?;
        main_rs.push_str(&format!("    let _ = {crate_name}::{symbol}();\n"));
    }
    main_rs.push_str("}\n");
    fs::write(root.join("src/main.rs"), main_rs)
        .map_err(|error| format!("cannot write build source: {error}"))?;

    let lock = Command::new("cargo")
        .args(["generate-lockfile", "--offline"])
        .current_dir(&root)
        .output()
        .map_err(|error| format!("cannot start cargo: {error}"))?;
    if !lock.status.success() {
        return Err(String::from_utf8_lossy(&lock.stderr).into_owned());
    }
    let built = Command::new("cargo")
        .args(["build", "--offline", "--locked"])
        .current_dir(&root)
        .output()
        .map_err(|error| format!("cannot start cargo: {error}"))?;
    let report = format!(
        "{{\"members\":{},\"success\":{}}}\n",
        trellis.rows.len(),
        built.status.success()
    );
    fs::write("/app/output/build-report.json", report)
        .map_err(|error| format!("cannot write build report: {error}"))?;
    if !built.status.success() {
        return Err(String::from_utf8_lossy(&built.stderr).into_owned());
    }
    fs::remove_dir_all(&root)
        .map_err(|error| format!("cannot remove {}: {error}", root.display()))?;
    Ok(())
}
