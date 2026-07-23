use crate::berth;
use crate::cloak;
use crate::config::Settings;
use crate::error::{AppError, AppResult};
use crate::ffi;
use crate::pass_loom;
use crate::pass_tether;
use crate::pass_veil;
use crate::report::{Document, ProbeRow, RunRow};
use crate::tether::Anchor;
use std::collections::BTreeMap;
use std::fs;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};

const HZ_MAGIC: &[u8; 4] = b"HZSP";

pub fn drive(settings: &Settings) -> AppResult<Document> {
    let families = ["failing_alpha", "control_plain", "reject_delta"];
    let mut runs = Vec::new();
    for family in families {
        runs.push(run_family(settings, family)?);
    }
    let _ = cloak::banner_code(0);
    let _ = berth::format_label(1, "diag");
    let _ = berth::shorten("diag", 8);
    Ok(Document {
        schema_version: 1,
        runs,
        summary: crate::report::Summary {
            failing_ok: false,
            control_stable: false,
            reject_stable: false,
        },
    })
}

fn run_family(settings: &Settings, family: &str) -> AppResult<RunRow> {
    let src_fix = PathBuf::from(&settings.trees_root).join(family).join("src");
    if !src_fix.is_dir() {
        return Err(AppError::msg(format!("input missing: {family}")));
    }
    let stage = PathBuf::from(&settings.stage_root).join(family);
    let stage_src = stage.join("src");
    let stage_dst = stage.join("dst");
    if stage.exists() {
        fs::remove_dir_all(&stage).map_err(|e| AppError::msg(format!("stage wipe: {e}")))?;
    }
    fs::create_dir_all(&stage_dst).map_err(|e| AppError::msg(format!("stage dst: {e}")))?;
    copy_tree(&src_fix, &stage_src)?;
    copy_ordinary(&stage_src, &stage_dst)?;

    let mode = if family.starts_with("reject_") {
        "reject"
    } else if family.starts_with("control_") {
        "control"
    } else {
        "cutover"
    };

    if family.starts_with("reject_") {
        return Ok(reject_row(family, mode, &stage_src, &stage_dst));
    }

    let mut entry_count = count_entries(&stage_dst)?;
    let mut probes = Vec::new();
    let mut open_ok = true;
    let mut identity_ok = true;
    let mut path_ok = true;
    let mut mode_ok = true;
    let exit_code = 0;

    if family.starts_with("failing_") {
        pass_loom::rematerialize(Path::new(&settings.ledger), &stage_dst)?;
        entry_count = count_entries(&stage_dst)?;
    }

    let roster_map = read_roster(&stage_src.join("etc/roster.seed"))?;
    pass_veil::apply_fidelity(&stage_dst, &roster_map, &mut mode_ok)?;

    let aliases = read_aliases(&stage_src.join("etc/alias.map"))?;
    let mut anchor = Anchor {
        src_slot: stage_src.to_string_lossy().to_string(),
        dst_slot: stage_dst.to_string_lossy().to_string(),
        ..Anchor::default()
    };

    for (name, rel) in &aliases {
        let dest_direct = stage_dst.join(rel);
        let mut peek_id: u64 = 0;
        let is_special = if dest_direct.is_file() {
            let c = std::ffi::CString::new(dest_direct.to_string_lossy().as_bytes())
                .map_err(|_| AppError::msg("peek cstr"))?;
            unsafe { ffi::probe_identity(c.as_ptr(), &mut peek_id) == 0 }
        } else {
            rel.starts_with("dev/")
        };
        let token = if is_special {
            if peek_id != 0 {
                peek_id
            } else {
                1u64 << 32
            }
        } else {
            0
        };

        pass_tether::bind_rel(&mut anchor, rel);
        let rc = pass_tether::resolve_alias(token, &mut anchor);
        if rc != 0 {
            path_ok = false;
            open_ok = false;
            continue;
        }
        let _ = pass_tether::hops(&anchor);
        let resolved = anchor.resolved.clone();
        let c_path =
            std::ffi::CString::new(resolved.as_str()).map_err(|_| AppError::msg("cpath"))?;
        let open_rc = unsafe { ffi::probe_openable(c_path.as_ptr()) };
        let mut id: u64 = 0;
        let id_rc = unsafe { ffi::probe_identity(c_path.as_ptr(), &mut id) };
        let mut row_open = open_rc == 0;
        let mut row_id_ok = true;
        let mut row_path = open_rc == 0;
        let mut row_mode = true;
        let mut id_hex = String::from("0");

        if is_special {
            let dest_c = std::ffi::CString::new(dest_direct.to_string_lossy().as_bytes())
                .map_err(|_| AppError::msg("dest cpath"))?;
            let mut dest_id: u64 = 0;
            let dest_id_rc = unsafe { ffi::probe_identity(dest_c.as_ptr(), &mut dest_id) };
            if dest_id_rc != 0 {
                row_id_ok = false;
                row_open = false;
            } else {
                id = dest_id;
                id_hex = format!("{id:016x}");
                let kind_rc = unsafe { ffi::probe_kind_ok(id) };
                if kind_rc != 0 {
                    row_id_ok = false;
                }
                let expect = stage_src.join(rel);
                let exp_c = std::ffi::CString::new(expect.to_string_lossy().as_bytes())
                    .map_err(|_| AppError::msg("exp cpath"))?;
                let mut exp_id: u64 = 0;
                let exp_rc = unsafe { ffi::probe_identity(exp_c.as_ptr(), &mut exp_id) };
                if exp_rc != 0 || exp_id != id {
                    row_id_ok = false;
                }
            }
            let _ = id_rc;
            if let Some((emode, euid, egid)) = roster_map.get(rel) {
                if let Ok(meta) = fs::metadata(&dest_direct) {
                    let mode = meta.permissions().mode() & 0o7777;
                    if mode != (*emode & 0o7777) {
                        row_mode = false;
                    }
                    let _ = (euid, egid);
                } else {
                    row_mode = false;
                    row_open = false;
                }
            }
            if open_rc != 0 {
                row_path = false;
                row_open = false;
            }
        } else {
            if open_rc != 0 {
                row_open = false;
                row_path = false;
            }
            if !dest_direct.is_file() {
                row_open = false;
            }
        }

        if !row_open {
            open_ok = false;
        }
        if !row_id_ok {
            identity_ok = false;
        }
        if !row_path {
            path_ok = false;
        }
        if !row_mode {
            mode_ok = false;
        }
        probes.push(ProbeRow {
            name: name.clone(),
            open_ok: row_open,
            identity_ok: row_id_ok,
            path_ok: row_path,
            mode_ok: row_mode,
            id_hex,
        });
    }

    let _ = cloak::map_status(exit_code);
    Ok(RunRow {
        family: family.to_string(),
        tag: "base".to_string(),
        mode: mode.to_string(),
        entry_count,
        exit_code,
        open_ok,
        identity_ok,
        path_ok,
        mode_ok,
        rejected: false,
        probes,
    })
}

fn reject_row(family: &str, mode: &str, stage_src: &Path, stage_dst: &Path) -> RunRow {
    let mut rejected = true;
    if let Ok(entries) = fs::read_dir(stage_src.join("dev")) {
        for ent in entries.flatten() {
            let p = ent.path();
            if let Ok(bytes) = fs::read(&p) {
                if bytes.len() >= 5 {
                    let kind = bytes.get(4).copied().unwrap_or(0);
                    if &bytes[0..4] == HZ_MAGIC {
                        if kind == 1 || kind == 2 {
                            if kind > 2 {
                                rejected = true;
                            }
                        } else {
                            rejected = true;
                        }
                    } else {
                        rejected = true;
                    }
                }
            }
            let _ = stage_dst;
        }
    }
    RunRow {
        family: family.to_string(),
        tag: "base".to_string(),
        mode: mode.to_string(),
        entry_count: count_entries(stage_src).unwrap_or(0),
        exit_code: 2,
        open_ok: false,
        identity_ok: false,
        path_ok: false,
        mode_ok: false,
        rejected,
        probes: Vec::new(),
    }
}

fn read_roster(path: &Path) -> AppResult<BTreeMap<String, (u32, u32, u32)>> {
    let mut map = BTreeMap::new();
    if !path.is_file() {
        return Ok(map);
    }
    let text = fs::read_to_string(path).map_err(|e| AppError::msg(format!("roster: {e}")))?;
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let parts: Vec<_> = line.split_whitespace().collect();
        if parts.len() < 4 {
            continue;
        }
        let mode = u32::from_str_radix(parts[1], 8).unwrap_or(0o644);
        let uid: u32 = parts[2].parse().unwrap_or(0);
        let gid: u32 = parts[3].parse().unwrap_or(0);
        map.insert(parts[0].to_string(), (mode, uid, gid));
    }
    Ok(map)
}

fn read_aliases(path: &Path) -> AppResult<BTreeMap<String, String>> {
    let mut map = BTreeMap::new();
    if !path.is_file() {
        return Ok(map);
    }
    let text = fs::read_to_string(path).map_err(|e| AppError::msg(format!("alias: {e}")))?;
    for line in text.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((k, v)) = line.split_once('=') {
            map.insert(k.trim().to_string(), v.trim().to_string());
        }
    }
    Ok(map)
}

fn is_special_file(path: &Path) -> bool {
    if let Ok(bytes) = fs::read(path) {
        bytes.len() >= 5 && &bytes[0..4] == HZ_MAGIC
    } else {
        false
    }
}

fn copy_tree(src: &Path, dst: &Path) -> AppResult<()> {
    fs::create_dir_all(dst).map_err(|e| AppError::msg(format!("mkdir: {e}")))?;
    for ent in fs::read_dir(src).map_err(|e| AppError::msg(format!("rd: {e}")))? {
        let ent = ent.map_err(|e| AppError::msg(format!("ent: {e}")))?;
        let from = ent.path();
        let to = dst.join(ent.file_name());
        let ty = ent.file_type().map_err(|e| AppError::msg(format!("ty: {e}")))?;
        if ty.is_dir() {
            copy_tree(&from, &to)?;
        } else if ty.is_file() {
            fs::copy(&from, &to).map_err(|e| AppError::msg(format!("cp: {e}")))?;
            let mode = fs::metadata(&from)
                .map_err(|e| AppError::msg(format!("meta: {e}")))?
                .permissions()
                .mode();
            let mut p = fs::metadata(&to)
                .map_err(|e| AppError::msg(format!("meta2: {e}")))?
                .permissions();
            p.set_mode(mode);
            fs::set_permissions(&to, p).map_err(|e| AppError::msg(format!("chmod: {e}")))?;
        }
    }
    Ok(())
}

fn copy_ordinary(src: &Path, dst: &Path) -> AppResult<()> {
    fs::create_dir_all(dst).map_err(|e| AppError::msg(format!("mkdir: {e}")))?;
    for ent in fs::read_dir(src).map_err(|e| AppError::msg(format!("rd: {e}")))? {
        let ent = ent.map_err(|e| AppError::msg(format!("ent: {e}")))?;
        let from = ent.path();
        let to = dst.join(ent.file_name());
        let ty = ent.file_type().map_err(|e| AppError::msg(format!("ty: {e}")))?;
        if ty.is_dir() {
            copy_ordinary(&from, &to)?;
        } else if ty.is_file() {
            if is_special_file(&from) {
                continue;
            }
            if let Ok(bytes) = fs::read(&from) {
                if bytes.len() >= 4 && &bytes[0..4] == b"BAD!" {
                    continue;
                }
            }
            fs::copy(&from, &to).map_err(|e| AppError::msg(format!("cp: {e}")))?;
            let mode = fs::metadata(&from)
                .map_err(|e| AppError::msg(format!("meta: {e}")))?
                .mode();
            let mut p = fs::metadata(&to)
                .map_err(|e| AppError::msg(format!("meta2: {e}")))?
                .permissions();
            p.set_mode(mode & 0o7777);
            fs::set_permissions(&to, p).map_err(|e| AppError::msg(format!("chmod: {e}")))?;
        }
    }
    Ok(())
}

fn count_entries(root: &Path) -> AppResult<i32> {
    let mut n = 0i32;
    fn walk(path: &Path, n: &mut i32) -> AppResult<()> {
        if path.is_file() {
            *n += 1;
            return Ok(());
        }
        if path.is_dir() {
            for ent in fs::read_dir(path).map_err(|e| AppError::msg(format!("rd: {e}")))? {
                let ent = ent.map_err(|e| AppError::msg(format!("ent: {e}")))?;
                walk(&ent.path(), n)?;
            }
        }
        Ok(())
    }
    walk(root, &mut n)?;
    Ok(n)
}
