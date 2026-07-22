use crate::model::Dyadic;

pub(crate) fn clear_slot<T>(values: &mut Vec<T>) {
    values.clear();
    if values.capacity() > 4096 {
        values.shrink_to(1024);
    }
}

pub(crate) fn shift_is_finite(values: &[Dyadic; 3]) -> bool {
    values.iter().all(|value| {
        let scaled = (value.mantissa as f64) * 2.0_f64.powi(value.exponent);
        scaled.is_finite()
    })
}
