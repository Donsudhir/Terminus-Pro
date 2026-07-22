mod config;
mod engine;
mod error;
mod ffi;
mod gauge;
mod locker;
mod meter;
mod model;
mod parse;
mod partition;
mod report;
mod roster;
mod router;
mod unpack;
mod vault;

use crate::error::AppResult;
use std::path::Path;

fn execute() -> AppResult<()> {
    let settings = config::load(Path::new("/app/conf/runtime.conf"))?;
    let families = parse::load(Path::new(&settings.input))?;
    let runs = engine::run(&families, &settings)?;
    report::save(Path::new(&settings.output), &runs)
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
