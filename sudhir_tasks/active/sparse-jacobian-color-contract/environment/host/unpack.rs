use crate::ffi;

pub(crate) fn flatten_slots(
    packed_triples: &[f64],
    group_count: i32,
) -> Result<(Vec<f64>, Vec<i32>, i32, i32), String> {
    let nnz = (packed_triples.len() / 3) as i32;
    let mut merge_buf = vec![0.0; 1 + 3 * nnz as usize];
    merge_buf[0] = nnz as f64;
    for (index, value) in packed_triples.iter().enumerate() {
        merge_buf[1 + index] = *value;
    }
    let mut merge_out = vec![0i32; 3 + 2 * nnz as usize];
    let merge_status =
        unsafe { ffi::merge_slots(merge_buf.as_mut_ptr(), group_count, merge_out.as_mut_ptr()) };
    if merge_status != 0 {
        return Err(format!("flatten status {merge_status}"));
    }

    let mut values = Vec::new();
    let mut indices = Vec::new();
    for entry in 0..nnz as usize {
        let row = merge_out[3 + 2 * entry];
        let col = merge_out[3 + 2 * entry + 1];
        let value = merge_buf[1 + 3 * entry + 2];
        indices.push(row);
        indices.push(col);
        values.push(value);
    }
    Ok((values, indices, merge_out[0], merge_out[1]))
}
