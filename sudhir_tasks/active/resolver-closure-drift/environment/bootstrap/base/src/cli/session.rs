use std::fs;
use std::path::{Path, PathBuf};

use crate::build::workspace::compile;
use crate::graph::walk::resolve;
use crate::model::{Need, PolicyMode, Wick};
use crate::quill::quay::lace_quay;
use crate::store::catalog::Catalog;
use crate::trace;
use crate::wire::lock::write;

pub struct Project {
    pub title: String,
    pub profile: PolicyMode,
    pub catalog: PathBuf,
    pub roots: Vec<Need>,
    pub apis: Vec<String>,
    pub seed: usize,
}

impl Project {
    pub fn load(path: &Path) -> Result<Self, String> {
        let text = fs::read_to_string(path)
            .map_err(|error| format!("cannot read {}: {error}", path.display()))?;
        Ok(Self {
            title: scalar(&text, "title")?,
            profile: PolicyMode::parse(&scalar(&text, "profile")?)?,
            catalog: PathBuf::from(scalar(&text, "catalog")?),
            roots: list(&text, "roots")?
                .iter()
                .map(|value| Need::parse(value))
                .collect::<Result<Vec<Need>, String>>()?,
            apis: list(&text, "apis")?,
            seed: scalar(&text, "seed")?
                .parse::<usize>()
                .map_err(|_| "invalid seed".to_string())?,
        })
    }
}

pub fn entry() -> Result<(), String> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 || args[1] != "solve" {
        return Err("usage: forge solve PROJECT".to_string());
    }
    let project = Project::load(Path::new(&args[2]))?;
    let catalog = Catalog::load(&project.catalog)?;
    let cairn = resolve(&catalog, &project.roots, project.profile, project.seed)?;
    let wick = Wick {
        roots: project.roots.iter().map(|need| need.key.clone()).collect(),
        salt: project.seed,
    };
    let trellis = lace_quay(cairn, &wick).map_err(|error| error.to_string())?;
    write(Path::new("/app/output/workspace.lock"), &trellis)?;
    let archive_root = project
        .catalog
        .parent()
        .ok_or_else(|| "catalog path has no parent".to_string())?;
    compile(&trellis, archive_root, &project.apis)?;
    trace::emit(&project.title, trellis.rows.len())?;
    Ok(())
}

fn scalar(text: &str, key: &str) -> Result<String, String> {
    let prefix = format!("{key} = ");
    text.lines()
        .map(str::trim)
        .find_map(|line| line.strip_prefix(&prefix))
        .map(|value| value.trim_matches('"').to_string())
        .ok_or_else(|| format!("missing field: {key}"))
}

fn list(text: &str, key: &str) -> Result<Vec<String>, String> {
    let value = scalar(text, key)?;
    let inner = value
        .strip_prefix('[')
        .and_then(|row| row.strip_suffix(']'))
        .ok_or_else(|| format!("invalid list: {key}"))?;
    Ok(inner
        .split(',')
        .map(str::trim)
        .filter(|row| !row.is_empty())
        .map(|row| row.trim_matches('"').to_string())
        .collect())
}
