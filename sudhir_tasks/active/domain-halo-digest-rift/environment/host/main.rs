mod config;
mod error;
mod ffi;
mod locker;
mod relay;
mod report;
mod shelf;

use crate::error::AppResult;
use std::path::Path;

fn execute() -> AppResult<()> {
    let settings = config::load(Path::new("/app/conf/runtime.conf"))?;
    let document = relay::drive(&settings)?;
    report::save(Path::new(&settings.output), &document)
}

fn main() {
    if let Err(code) = run() {
        std::process::exit(code);
    }
}

fn run() -> Result<(), i32> {
    match execute() {
        Ok(()) => Ok(()),
        Err(message) => {
            eprintln!("{message}");
            Err(error::map_code(&message))
        }
    }
}
