use crate::error::{AppError, AppResult};
use crate::ffi;
use crate::veil::{self, Roster};
use std::collections::BTreeMap;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::Path;

/// Apply roster fidelity onto destination entries.
pub fn apply_fidelity(
    stage_dst: &Path,
    roster: &BTreeMap<String, (u32, u32, u32)>,
    mode_ok: &mut bool,
) -> AppResult<()> {
    for (rel, (emode, euid, egid)) in roster {
        let dest = stage_dst.join(rel);
        if !dest.exists() {
            continue;
        }
        let mut id: u64 = 0;
        let is_special = if dest.is_file() {
            let c = std::ffi::CString::new(dest.to_string_lossy().as_bytes())
                .map_err(|_| AppError::msg("fid cstr"))?;
            let rc = unsafe { ffi::probe_identity(c.as_ptr(), &mut id) };
            rc == 0
        } else {
            false
        };
        let mut row = Roster::default();
        veil::load_seed(&mut row, *emode, *euid, *egid);
        let token = if is_special { id } else { 0 };
        let rc = veil::hinge_q(token, &mut row);
        if rc != 0 {
            *mode_ok = false;
            continue;
        }
        let mut perms = fs::metadata(&dest)
            .map_err(|e| AppError::msg(format!("meta: {e}")))?
            .permissions();
        perms.set_mode(row.mode);
        fs::set_permissions(&dest, perms).map_err(|e| AppError::msg(format!("chmod: {e}")))?;
        let _ = (row.uid, row.gid, row.mark, veil::peek_weight(&row));
        if is_special && row.mode != (*emode & 0o7777) {
            *mode_ok = false;
        }
    }
    Ok(())
}
