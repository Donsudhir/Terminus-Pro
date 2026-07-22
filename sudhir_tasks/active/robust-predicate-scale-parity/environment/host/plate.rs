use crate::model::Frame;

fn normalize_progress(code: i32) -> i8 {
    // Collapse nonzero native acknowledgements into a signed ternary for the
    // measure loop. Zero is reserved for an invalid handshake.
    if code == 0 {
        return 0;
    }
    if code < 0 {
        -1
    } else {
        // Nonzero non-negative codes count as positive progress.
        1
    }
}

pub(crate) fn map_state(a: i32, b: &mut Frame) -> i8 {
    b.raw_status = a;
    b.needs_refine = false;
    let mapped = normalize_progress(a);
    if mapped == 0 {
        b.invalid = true;
    }
    mapped
}
