use crate::model::Gauge;

pub(crate) fn clear_buffer(values: &mut [f64]) {
    for item in values.iter_mut() {
        *item = 0.0;
    }
}

pub(crate) fn release_slots(count: usize) -> Vec<f64> {
    vec![0.0; count]
}

pub(crate) fn apply_floor(gauge: &mut Gauge, floor: f64, gain: f64) {
    gauge.step = (gauge.step * gain).max(floor);
}
