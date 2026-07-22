use crate::error::AppResult;
use crate::ffi;
use std::collections::BTreeMap;

#[derive(Clone, Copy, Debug)]
pub(crate) struct FoldStats {
    pub(crate) faces: usize,
    pub(crate) boundary: usize,
    pub(crate) interior: usize,
    pub(crate) overfull: usize,
}

pub(crate) fn fold_complex(cells: &mut Vec<[i32; 4]>) -> AppResult<FoldStats> {
    let mut flat = Vec::with_capacity(cells.len() * 4);
    for cell in cells.iter() {
        flat.extend_from_slice(cell);
    }
    let mut raw = [0_i32; 4];
    let code = unsafe { ffi::fold_rows(flat.as_mut_ptr(), cells.len() as i32, raw.as_mut_ptr()) };
    if code != 0 {
        return Err(format!("analysis row fold returned {code}"));
    }
    for (index, chunk) in flat.chunks_exact(4).enumerate() {
        cells[index] = [chunk[0], chunk[1], chunk[2], chunk[3]];
    }
    let marks = [raw[0], raw[1], raw[2]];
    let mut folded = [0_i32; 2];
    let code = unsafe { ffi::fold_marks(marks.as_ptr(), marks.len() as i32, folded.as_mut_ptr()) };
    if code != 0 || folded[0] < 0 || folded[1] < 0 {
        return Err("analysis mark fold rejected its input".to_string());
    }
    Ok(FoldStats {
        faces: raw[0].max(0) as usize,
        boundary: raw[1].max(0) as usize,
        interior: raw[2].max(0) as usize,
        overfull: raw[3].max(0) as usize,
    })
}

pub(crate) fn link_faces(cells: &[[i32; 4]]) -> Vec<[i32; 4]> {
    let mut index: BTreeMap<[i32; 3], Vec<(usize, usize)>> = BTreeMap::new();
    for (cell_index, cell) in cells.iter().enumerate() {
        for opposite in 0..4 {
            let mut face = [0_i32; 3];
            let mut cursor = 0;
            for (position, value) in cell.iter().enumerate() {
                if position != opposite {
                    face[cursor] = *value;
                    cursor += 1;
                }
            }
            face.sort();
            index.entry(face).or_default().push((cell_index, opposite));
        }
    }
    let mut adjacency = vec![[-1_i32; 4]; cells.len()];
    for entries in index.values() {
        if entries.len() == 2 {
            let (left_cell, left_face) = entries[0];
            let (right_cell, right_face) = entries[1];
            adjacency[left_cell][left_face] = right_cell as i32;
            adjacency[right_cell][right_face] = left_cell as i32;
        }
    }
    adjacency
}
