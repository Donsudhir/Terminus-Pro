use crate::error::{AppError, AppResult};
use crate::ffi;
use std::fs;
use std::path::Path;

/// Rematerialize specials from the packed ledger into the destination slot.
pub fn rematerialize(ledger: &Path, stage_dst: &Path) -> AppResult<()> {
    let packed = fs::read(ledger).map_err(|e| AppError::msg(format!("ledger: {e}")))?;
    let root = std::ffi::CString::new(stage_dst.to_string_lossy().as_bytes())
        .map_err(|_| AppError::msg("root cstr"))?;
    let rc = unsafe { ffi::loom_stage_set(root.as_ptr()) };
    if rc != 0 {
        return Err(AppError::msg("stage set"));
    }
    let mut token: u64 = 0;
    let krc = unsafe { ffi::knit_p(packed.as_ptr(), packed.len(), &mut token) };
    unsafe { ffi::loom_stage_clear() };
    if krc != 0 {
        return Err(AppError::msg("knit"));
    }
    let mut tallies = [0i32; 4];
    let _ = unsafe { ffi::ledge_tally(packed.as_ptr(), packed.len(), tallies.as_mut_ptr()) };
    let _ = token;
    Ok(())
}
