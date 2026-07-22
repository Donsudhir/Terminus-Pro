use std::ffi::{c_double, c_int};

unsafe extern "C" {
    pub(crate) fn eval_band(a: *const c_double, b: *const c_double, n: i32, c: *mut c_double) -> c_int;
    pub(crate) fn eval_frame(a: *const c_double, b: i32, c: *mut c_double, d: *mut c_double) -> c_int;
    pub(crate) fn refine_orient3d(a: *const i64) -> c_int;
    pub(crate) fn refine_insphere(a: *const i64) -> c_int;
    pub(crate) fn fold_rows(a: *mut c_int, b: c_int, c: *mut c_int) -> c_int;
    pub(crate) fn fold_marks(a: *const c_int, b: c_int, c: *mut c_int) -> c_int;
}
