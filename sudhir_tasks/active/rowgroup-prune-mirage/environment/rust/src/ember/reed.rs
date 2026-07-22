use crate::ember::fold::tilt_a;
use crate::model::{Cell, FoldErr, Page};

pub(crate) fn gather(cells: Vec<Cell>, width: usize) -> Result<Vec<Page>, FoldErr> {
    let mut pages = Vec::new();
    for (id, chunk) in cells.chunks(width).enumerate() {
        let values: Vec<i64> = chunk.iter().map(|cell| cell.amount).collect();
        let present: Vec<u8> = chunk.iter().map(|cell| cell.present).collect();
        let origins: Vec<u8> = chunk.iter().map(|cell| cell.origin).collect();
        let mark = tilt_a(&values, &present, &origins)?;

        let mut regions: Vec<String> = chunk.iter().map(|cell| cell.region.clone()).collect();
        regions.sort();
        let region_low = regions.first().cloned().unwrap_or_default();
        let region_high = regions.last().cloned().unwrap_or_default();
        pages.push(Page {
            id,
            generation: 3,
            mark,
            region_low,
            region_high,
            cells: chunk.to_vec(),
        });
    }
    Ok(pages)
}
