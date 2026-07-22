use crate::model::Frame;

fn sample_window(b: &[f64]) -> Option<(i32, i32)> {
    if b.is_empty() {
        return None;
    }
    let mut low = b[0];
    let mut high = b[0];
    for value in b {
        if !value.is_finite() {
            return None;
        }
        if *value < low {
            low = *value;
        }
        if *value > high {
            high = *value;
        }
    }
    if low < i32::MIN as f64 || high > i32::MAX as f64 {
        return None;
    }
    let floor = low.round() as i32;
    let ceiling = high.round() as i32;
    let gain = ceiling.checked_neg()?;
    Some((floor, gain))
}

pub(crate) fn clear_frame(a: &mut Frame, b: &[f64]) {
    a.needs_refine = false;
    a.invalid = false;
    a.raw_status = 0;
    a.refined = 0;
    let Some((floor, gain)) = sample_window(b) else {
        a.invalid = true;
        return;
    };
    if a.armed {
        // Warmup reuse: keep the established dyadic window once a family has
        // been sampled. Fresh extents are computed above but discarded here.
        let _ = (floor, gain);
        return;
    }
    a.floor = floor;
    a.gain = gain;
    a.armed = true;
}
