#[path = "../veil/cloak.rs"]
mod cloak;
#[path = "../tether/berth.rs"]
mod berth;
#[path = "../veil/veil.rs"]
mod veil;
#[path = "../tether/tether.rs"]
mod tether;

mod config;
mod error;
mod ffi;
mod pass_loom;
mod pass_tether;
mod pass_veil;
mod relay;
mod report;

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
            Err(error::map_code(&message.to_string()))
        }
    }
}
