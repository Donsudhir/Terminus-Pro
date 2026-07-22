mod codec;
mod ember;
mod model;
mod report;

use ember::pale::{tilt_d, Dial};
use std::path::{Path, PathBuf};

fn main() {
    if let Err(error) = run() {
        eprintln!("loam-ingest: {error}");
        std::process::exit(1);
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        return Err("usage: loam-ingest <csv> <store>".into());
    }
    let cells = codec::read_csv(Path::new(&args[1]))?;
    let pages = ember::reed::gather(cells, 4)?;
    let directory = PathBuf::from(&args[2]);
    std::fs::create_dir_all(&directory)?;
    let target = directory.join("data.store");
    codec::write_pages(&target, &pages)?;

    let size = std::fs::metadata(&target)?.len() as usize;
    let mut dial = Dial::default();
    let cell_count = pages.iter().map(|page| page.cells.len()).sum();
    tilt_d(&mut dial, cell_count, size);
    eprintln!("{}", report::line(&dial));
    Ok(())
}
