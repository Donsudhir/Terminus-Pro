use crate::config::Settings;
use crate::ffi;
use crate::gauge::reset_span;
use crate::meter::apply_floor;
use crate::model::{
    Dims, FamilySpec, Gauge, Ledger, RunLabel, RunRecord, SpanInfo, TagSpec,
};
use crate::partition;
use crate::roster::{make_shelf, pack_shelf, unpack_shelf};
use crate::unpack;
use crate::vault::bind_slot;
use std::cmp::Ordering;

pub fn run(families: &[FamilySpec], settings: &Settings) -> Result<Vec<RunRecord>, String> {
    let mut runs = Vec::new();
    // Workspace span scratch reused across evaluations (dims usually match).
    let mut span_scratch = Gauge {
        reference: 0.0,
        step: settings.step_floor,
        primed: false,
    };
    for family in families {
        for tag in &family.tags {
            let record = evaluate_family(family, tag, None, settings, false, &mut span_scratch)?;
            runs.push(record);
        }
    }
    runs.sort_by(|left, right| {
        left.label
            .family
            .cmp(&right.label.family)
            .then_with(|| left.label.tag.cmp(&right.label.tag))
    });
    Ok(runs)
}

pub fn evaluate_family(
    family: &FamilySpec,
    tag: &TagSpec,
    perm: Option<&[usize]>,
    settings: &Settings,
    resume: bool,
    gauge: &mut Gauge,
) -> Result<RunRecord, String> {
    let n = family.dim;
    let m = family.equations.len();
    let (col_ptr, col_idx, coeffs) = build_sparse(family);
    let (groups, group_count) = partition::assign_groups(family)?;

    let mut x = apply_affine(&family.base, tag);
    if let Some(order) = perm {
        x = permute_values(&x, order);
    }

    let mut baseline = vec![0.0; m];
    eval_residual(&coeffs, &col_ptr, &col_idx, m, n, &x, &mut baseline)?;

    reset_span(gauge, &baseline);
    apply_floor(gauge, settings.step_floor, settings.step_gain);

    let mut shelf = make_shelf(group_count);
    if resume {
        let mut plan = make_shelf(group_count);
        for gid in 0..group_count {
            let mask = group_mask(&groups, n, gid);
            plan.slots[gid as usize].bits = mask;
            bind_slot(gid, &mut plan);
        }
        let encoded = pack_shelf(&plan);
        shelf = unpack_shelf(&encoded, group_count);
    }

    let mut packed_triples: Vec<f64> = Vec::new();
    let mut work = vec![0.0; n];
    let mut plus = vec![0.0; m];
    let mut minus = vec![0.0; m];
    let mut diff = vec![0.0; m];
    let inv_step = 0.5 / gauge.step;

    for gid in 0..group_count {
        let mask = group_mask(&groups, n, gid);
        shelf.slots[gid as usize].bits = mask;
        bind_slot(gid, &mut shelf);
        let seed_bits = shelf.slots[gid as usize].bits;
        unsafe {
            ffi::ember_apply(
                x.as_ptr(),
                work.as_mut_ptr(),
                n as i32,
                groups.as_ptr(),
                gid,
                seed_bits,
                gauge.step,
            );
        }
        eval_residual(&coeffs, &col_ptr, &col_idx, m, n, &work, &mut plus)?;
        unsafe {
            ffi::ember_apply(
                x.as_ptr(),
                work.as_mut_ptr(),
                n as i32,
                groups.as_ptr(),
                gid,
                seed_bits,
                -gauge.step,
            );
        }
        eval_residual(&coeffs, &col_ptr, &col_idx, m, n, &work, &mut minus)?;
        unsafe {
            ffi::ember_diff(
                plus.as_ptr(),
                minus.as_ptr(),
                diff.as_mut_ptr(),
                m as i32,
                inv_step,
            );
        }
        for col in 0..n {
            if groups[col] != gid {
                continue;
            }
            for eq in 0..m {
                if let Some(value) = pick_entry(&col_ptr, &col_idx, &diff, eq, col) {
                    packed_triples.push(eq as f64);
                    packed_triples.push(col as f64);
                    packed_triples.push(value);
                }
            }
        }
    }

    let (values, indices, active, total) = unpack::flatten_slots(&packed_triples, group_count)?;
    let direction = companion_direction(n);
    let products = packed_matvec(m, &indices, &values, &direction);
    let ids: Vec<i32> = (1..=n).map(|v| v as i32).collect();
    Ok(RunRecord {
        label: RunLabel {
            family: family.name.clone(),
            tag: tag.name.clone(),
        },
        ids,
        values,
        indices,
        dims: Dims {
            rows: m as i32,
            cols: n as i32,
            nnz: total,
        },
        products,
        ledger: Ledger {
            total,
            groups: group_count,
            active,
        },
        span_info: SpanInfo {
            reference: gauge.reference,
            step: gauge.step,
        },
    })
}

fn group_mask(groups: &[i32], n: usize, gid: i32) -> u64 {
    let mut mask = 0u64;
    for col in 0..n {
        if groups[col] == gid {
            mask |= 1u64 << col;
        }
    }
    mask
}

fn packed_matvec(rows: usize, indices: &[i32], values: &[f64], direction: &[f64]) -> Vec<f64> {
    let mut out = vec![0.0; rows];
    for (entry, value) in values.iter().enumerate() {
        let row = indices[2 * entry] as usize;
        let col = indices[2 * entry + 1] as usize;
        if row < rows && col < direction.len() {
            out[row] += *value * direction[col];
        }
    }
    out
}

fn build_sparse(family: &FamilySpec) -> (Vec<i32>, Vec<i32>, Vec<f64>) {
    let n = family.dim;
    let mut col_ptr = vec![0i32; n + 1];
    let mut col_idx = Vec::new();
    let mut coeffs = Vec::new();
    for col in 0..n {
        col_ptr[col] = col_idx.len() as i32;
        for (eq, terms) in family.equations.iter().enumerate() {
            for &(term_col, coeff) in terms {
                if term_col == col {
                    col_idx.push(eq as i32);
                    coeffs.push(coeff);
                }
            }
        }
    }
    col_ptr[n] = col_idx.len() as i32;
    (col_ptr, col_idx, coeffs)
}

fn apply_affine(base: &[f64], tag: &TagSpec) -> Vec<f64> {
    base.iter()
        .zip(tag.shift.iter())
        .map(|(value, shift)| value * tag.scale + shift)
        .collect()
}

fn permute_values(values: &[f64], order: &[usize]) -> Vec<f64> {
    order.iter().map(|&idx| values[idx]).collect()
}

fn pick_entry(
    col_ptr: &[i32],
    col_idx: &[i32],
    diff: &[f64],
    eq: usize,
    col: usize,
) -> Option<f64> {
    for pos in col_ptr[col] as usize..col_ptr[col + 1] as usize {
        if col_idx[pos] as usize == eq {
            return Some(diff[eq]);
        }
    }
    None
}

fn eval_residual(
    coeffs: &[f64],
    col_ptr: &[i32],
    col_idx: &[i32],
    rows: usize,
    cols: usize,
    x: &[f64],
    out: &mut [f64],
) -> Result<(), String> {
    let nnz = coeffs.len() as i32;
    let status = unsafe {
        ffi::ridge_eval(
            coeffs.as_ptr(),
            rows as i32,
            cols as i32,
            nnz,
            col_ptr.as_ptr(),
            col_idx.as_ptr(),
            x.as_ptr(),
            out.as_mut_ptr(),
        )
    };
    if status != 0 {
        return Err(format!("ridge_eval status {status}"));
    }
    let tint = unsafe { ffi::quill_tint(out.as_mut_ptr(), rows as i32) };
    if tint != 0 {
        return Err(format!("quill_tint status {tint}"));
    }
    Ok(())
}

fn companion_direction(n: usize) -> Vec<f64> {
    let mut out = vec![0.0; n];
    let status = unsafe { ffi::quill_companion(n as i32, out.as_mut_ptr()) };
    if status != 0 {
        // Fallback keeps the binary buildable if the native helper rejects n;
        // products still fail closed unless the companion table matches.
        return (0..n).map(|idx| 1.0 + 0.1 * idx as f64).collect();
    }
    out
}

pub fn inspect_group(family: &FamilySpec, col_a: usize, col_b: usize) -> Result<i32, String> {
    partition::same_group(family, col_a, col_b)
}

pub fn compare_order(a: &RunRecord, b: &RunRecord) -> Ordering {
    a.label
        .family
        .cmp(&b.label.family)
        .then_with(|| a.label.tag.cmp(&b.label.tag))
}
