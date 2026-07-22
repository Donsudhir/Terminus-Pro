use crate::ffi;
use crate::model::{CoordPoint, Frame, ProbeRow};
use crate::plate::map_state;

fn resolve(terms: &[f64], exact: i32, frame: &mut Frame) -> ProbeRow {
    let magnitudes: Vec<f64> = terms.iter().map(|value| value.abs()).collect();
    let mut estimate = 0.0_f64;
    let mut low = 0.0_f64;
    let mut high = 0.0_f64;
    unsafe {
        let _ = ffi::eval_frame(
            terms.as_ptr(),
            terms.len() as i32,
            &mut low,
            &mut high,
        );
    }
    let raw = unsafe {
        ffi::eval_band(
            terms.as_ptr(),
            magnitudes.as_ptr(),
            terms.len() as i32,
            &mut estimate,
        )
    };
    let mapped = map_state(raw, frame);
    let final_sign = if mapped == 0 && frame.needs_refine {
        frame.refined = frame.refined.saturating_add(1);
        exact.signum() as i8
    } else {
        mapped
    };
    ProbeRow {
        raw,
        mapped,
        final_sign,
        refine: frame.needs_refine,
    }
}

pub(crate) fn inspect_series(terms: &[f64], exact: i32, frame: &mut Frame) -> ProbeRow {
    resolve(terms, exact, frame)
}

pub(crate) fn orientation(points: [&CoordPoint; 4], frame: &mut Frame) -> i32 {
    let ax = points[0].fast[0] - points[3].fast[0];
    let ay = points[0].fast[1] - points[3].fast[1];
    let az = points[0].fast[2] - points[3].fast[2];
    let bx = points[1].fast[0] - points[3].fast[0];
    let by = points[1].fast[1] - points[3].fast[1];
    let bz = points[1].fast[2] - points[3].fast[2];
    let cx = points[2].fast[0] - points[3].fast[0];
    let cy = points[2].fast[1] - points[3].fast[1];
    let cz = points[2].fast[2] - points[3].fast[2];
    let terms = [
        ax * by * cz,
        -ax * bz * cy,
        -ay * bx * cz,
        ay * bz * cx,
        az * bx * cy,
        -az * by * cx,
    ];
    let mut exact_values = [0_i64; 12];
    for (index, point) in points.iter().enumerate() {
        exact_values[index * 3..index * 3 + 3].copy_from_slice(&point.exact);
    }
    let exact = unsafe { ffi::refine_orient3d(exact_values.as_ptr()) };
    resolve(&terms, exact, frame).final_sign as i32
}

pub(crate) fn sphere(points: [&CoordPoint; 4], query: &CoordPoint, frame: &mut Frame) -> i32 {
    let mut matrix = [[0.0_f64; 4]; 4];
    for row in 0..4 {
        let x = points[row].fast[0] - query.fast[0];
        let y = points[row].fast[1] - query.fast[1];
        let z = points[row].fast[2] - query.fast[2];
        matrix[row] = [x, y, z, x * x + y * y + z * z];
    }
    let mut terms = Vec::with_capacity(24);
    for a in 0..4 {
        for b in 0..4 {
            if b == a {
                continue;
            }
            for c in 0..4 {
                if c == a || c == b {
                    continue;
                }
                for d in 0..4 {
                    if d == a || d == b || d == c {
                        continue;
                    }
                    let permutation = [a, b, c, d];
                    let mut inversions = 0;
                    for left in 0..4 {
                        for right in left + 1..4 {
                            if permutation[left] > permutation[right] {
                                inversions += 1;
                            }
                        }
                    }
                    let value = matrix[0][a] * matrix[1][b] * matrix[2][c] * matrix[3][d];
                    terms.push(if inversions % 2 == 0 { value } else { -value });
                }
            }
        }
    }
    let mut exact_values = [0_i64; 15];
    for (index, point) in points.iter().enumerate() {
        exact_values[index * 3..index * 3 + 3].copy_from_slice(&point.exact);
    }
    exact_values[12..15].copy_from_slice(&query.exact);
    let exact = unsafe { ffi::refine_insphere(exact_values.as_ptr()) };
    resolve(&terms, exact, frame).final_sign as i32
}
