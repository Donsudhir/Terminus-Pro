#[derive(Clone, Copy, Debug)]
pub(crate) struct Dyadic {
    pub(crate) mantissa: i64,
    pub(crate) exponent: i32,
}

#[derive(Clone, Debug)]
pub(crate) struct Point {
    pub(crate) id: i32,
    pub(crate) xyz: [Dyadic; 3],
}

#[derive(Clone, Debug)]
pub(crate) struct Variant {
    pub(crate) name: String,
    pub(crate) scale: i32,
    pub(crate) shift: [Dyadic; 3],
}

#[derive(Clone, Debug)]
pub(crate) struct Family {
    pub(crate) name: String,
    pub(crate) points: Vec<Point>,
    pub(crate) variants: Vec<Variant>,
}

#[derive(Clone, Debug)]
pub(crate) struct CoordPoint {
    pub(crate) id: i32,
    pub(crate) fast: [f64; 3],
    pub(crate) exact: [i64; 3],
}

#[derive(Clone, Debug)]
pub(crate) struct Frame {
    pub(crate) floor: i32,
    pub(crate) gain: i32,
    pub(crate) armed: bool,
    pub(crate) needs_refine: bool,
    pub(crate) invalid: bool,
    pub(crate) raw_status: i32,
    pub(crate) refined: u64,
}

impl Default for Frame {
    fn default() -> Self {
        Self {
            floor: 0,
            gain: 0,
            armed: false,
            needs_refine: false,
            invalid: false,
            raw_status: 0,
            refined: 0,
        }
    }
}

impl Frame {
    pub(crate) fn fast_value(&self, value: Dyadic, scale: i32) -> f64 {
        let exponent = value.exponent.saturating_add(scale).saturating_add(self.gain);
        (value.mantissa as f64) * 2.0_f64.powi(exponent)
    }

    pub(crate) fn exact_value(&self, value: Dyadic, scale: i32) -> i64 {
        let exponent = value.exponent.saturating_add(scale);
        let shift = exponent.saturating_sub(self.floor);
        if shift < 0 {
            let right = shift.unsigned_abs();
            if right >= 63 {
                return 0;
            }
            return value.mantissa >> right;
        }
        let left = shift as u32;
        if left >= 63 {
            return 0;
        }
        value.mantissa.checked_shl(left).unwrap_or(0)
    }
}

#[derive(Clone, Debug)]
pub(crate) struct OrientationSummary {
    pub(crate) positive: usize,
    pub(crate) negative: usize,
    pub(crate) zero: usize,
}

#[derive(Clone, Debug)]
pub(crate) struct ValiditySummary {
    pub(crate) checks: usize,
    pub(crate) violations: usize,
}

#[derive(Clone, Debug)]
pub(crate) struct TopologySummary {
    pub(crate) vertices: usize,
    pub(crate) edges: usize,
    pub(crate) faces: usize,
    pub(crate) cells: usize,
    pub(crate) boundary_faces: usize,
    pub(crate) euler: isize,
}

#[derive(Clone, Debug)]
pub(crate) struct BatchReport {
    pub(crate) family: String,
    pub(crate) variant: String,
    pub(crate) point_ids: Vec<i32>,
    pub(crate) cells: Vec<[i32; 4]>,
    pub(crate) adjacency: Vec<[i32; 4]>,
    pub(crate) orientation: OrientationSummary,
    pub(crate) validity: ValiditySummary,
    pub(crate) topology: TopologySummary,
}

#[derive(Clone, Copy, Debug)]
pub(crate) struct ProbeRow {
    pub(crate) raw: i32,
    pub(crate) mapped: i8,
    pub(crate) final_sign: i8,
    pub(crate) refine: bool,
}
