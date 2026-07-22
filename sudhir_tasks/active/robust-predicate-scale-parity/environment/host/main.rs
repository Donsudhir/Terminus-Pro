mod config;
mod engine;
mod error;
mod ffi;
mod fnv;
mod frame;
mod measure;
mod model;
mod parse;
mod plate;
mod pool;
mod relay;
mod router;
mod write;

use crate::error::AppResult;
use std::path::Path;

fn execute() -> AppResult<()> {
    let settings = config::load(Path::new("/app/config/runtime.conf"))?;
    let families = parse::load(&settings.input)?;
    let reports = engine::run(&families)?;
    write::save(&settings.output, &reports)
}

fn main() {
    let arguments: Vec<String> = std::env::args().collect();
    match router::dispatch(&arguments) {
        Ok(Some(code)) => std::process::exit(code),
        Ok(None) => {}
        Err(message) => std::process::exit(router::map_code(&message)),
    }
    if let Err(message) = execute() {
        std::process::exit(router::map_code(&message));
    }
}
