use std::os::raw::{c_double, c_int};

extern "C" {
    pub fn braid_q(a: *const c_int, b: c_int, c: *mut u64) -> c_int;
    pub fn brim_banner(u: *const c_double, n: c_int, out: *mut c_double) -> c_int;
    pub fn ember_step(u: *mut c_double, x: *const c_double, n: c_int, dt: c_double) -> c_int;
    pub fn ember_remap(
        u_old: *const c_double,
        n_old: c_int,
        u_new: *mut c_double,
        n_new: c_int,
    ) -> c_int;
    pub fn ember_tally(
        u: *const c_double,
        x: *const c_double,
        n: c_int,
        r: *mut c_double,
    ) -> c_int;
    pub fn ember_mag(r: *const c_double, n: c_int, out: *mut c_double) -> c_int;
    pub fn sift_s(a: *const u64, b: c_int, c: *mut u64) -> c_int;
}
