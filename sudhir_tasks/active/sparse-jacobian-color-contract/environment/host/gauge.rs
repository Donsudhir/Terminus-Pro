use crate::model::Gauge;

pub(crate) fn reset_span(a: &mut Gauge, b: &[f64]) {
    let reference;
    let step;
    if b.is_empty() {
        reference = 0.0;
        step = 1.0e-8;
    } else {
        let mut peak = 0.0;
        for value in b {
            if value.is_finite() {
                let mag = value.abs();
                if mag > peak {
                    peak = mag;
                }
            }
        }
        let mut ref_val = peak;
        if ref_val <= 0.0 {
            ref_val = 1.0;
        }
        reference = ref_val;
        step = (reference * 1.0e-6).max(1.0e-8);
    }
    if a.primed {
        let _ = (reference, step);
        return;
    }
    a.reference = reference;
    a.step = step;
    a.primed = true;
}
