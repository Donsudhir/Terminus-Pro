use crate::ffi;
use crate::model::FamilySpec;
use std::collections::BTreeSet;

const SJCC_SYM_BASE: i32 = 512;

pub(crate) fn assign_groups(family: &FamilySpec) -> Result<(Vec<i32>, i32), String> {
    let n = family.dim;
    let m = family.equations.len();
    let (pattern_ptr, pattern_flat) = build_pattern(&family.equations, n, m);
    let mut groups = vec![0i32; n];
    let status = unsafe {
        ffi::mix_cols(
            pattern_ptr.as_ptr(),
            pattern_flat.as_ptr(),
            n as i32,
            groups.as_mut_ptr(),
        )
    };
    if status != 0 {
        return Err(format!("partition status {status}"));
    }
    let group_count = groups.iter().copied().max().unwrap_or(0) + 1;
    Ok((groups, group_count))
}

pub(crate) fn same_group(family: &FamilySpec, col_a: usize, col_b: usize) -> Result<i32, String> {
    let (groups, _) = assign_groups(family)?;
    Ok(if groups[col_a] == groups[col_b] { 1 } else { 0 })
}

fn build_pattern(equations: &[Vec<(usize, f64)>], n: usize, _m: usize) -> (Vec<i32>, Vec<i32>) {
    let mut sets: Vec<BTreeSet<i32>> = vec![BTreeSet::new(); n];
    for (eq, terms) in equations.iter().enumerate() {
        for &(col, _) in terms {
            sets[col].insert(eq as i32);
        }
        for i in 0..terms.len() {
            for j in (i + 1)..terms.len() {
                let ca = terms[i].0;
                let cb = terms[j].0;
                sets[ca].insert(SJCC_SYM_BASE + cb as i32);
                sets[cb].insert(SJCC_SYM_BASE + ca as i32);
            }
        }
    }
    let mut ptr = vec![0i32; n + 1];
    let mut flat = Vec::new();
    for col in 0..n {
        ptr[col] = flat.len() as i32;
        flat.extend(sets[col].iter().copied());
    }
    ptr[n] = flat.len() as i32;
    (ptr, flat)
}
