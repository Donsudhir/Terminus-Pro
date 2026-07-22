use std::os::raw::{c_double, c_int};

extern "C" {
    pub fn mix_cols(a: *const c_int, b: *const c_int, n: c_int, c: *mut c_int) -> c_int;
    pub fn ledge_stats(a: *const c_int, b: *const c_int, n: c_int, c: *mut c_int) -> c_int;
    pub fn ember_apply(
        base: *const c_double,
        work: *mut c_double,
        n: c_int,
        groups: *const c_int,
        target: c_int,
        seed_bits: u64,
        step: c_double,
    ) -> c_int;
    pub fn ember_diff(
        plus: *const c_double,
        minus: *const c_double,
        out: *mut c_double,
        m: c_int,
        inv_step: c_double,
    ) -> c_int;
    pub fn quill_tint(r: *mut c_double, m: c_int) -> c_int;
    pub fn quill_companion(n: c_int, out: *mut c_double) -> c_int;
    pub fn quill_pack(
        groups: *const c_int,
        n: c_int,
        group_id: c_int,
        diff: *const c_double,
        m: c_int,
        row_map: *const c_int,
        row_count: c_int,
        buf: *mut c_double,
        count: *mut c_int,
    ) -> c_int;
    pub fn ridge_eval(
        coeff: *const c_double,
        rows: c_int,
        cols: c_int,
        nnz: c_int,
        row_ptr: *const c_int,
        col_idx: *const c_int,
        x: *const c_double,
        r: *mut c_double,
    ) -> c_int;
    pub fn ridge_companion(
        coeff: *const c_double,
        rows: c_int,
        cols: c_int,
        nnz: c_int,
        row_ptr: *const c_int,
        col_idx: *const c_int,
        v: *const c_double,
        out: *mut c_double,
    ) -> c_int;
    pub fn merge_slots(a: *mut c_double, b: c_int, c: *mut c_int) -> c_int;
    pub fn tally_marks(a: *const c_double, b: c_int, c: *mut c_int) -> c_int;
}
