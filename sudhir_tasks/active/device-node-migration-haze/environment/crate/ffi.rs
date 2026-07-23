use std::os::raw::{c_char, c_int};

extern "C" {
    pub fn loom_stage_set(slot: *const c_char) -> c_int;
    pub fn loom_stage_clear();
    pub fn knit_p(a: *const u8, b: usize, c: *mut u64) -> c_int;
    pub fn ledge_tally(a: *const u8, b: usize, c: *mut c_int) -> c_int;
    pub fn probe_identity(path: *const c_char, out_id: *mut u64) -> c_int;
    pub fn probe_openable(path: *const c_char) -> c_int;
    pub fn probe_kind_ok(id: u64) -> c_int;
}
