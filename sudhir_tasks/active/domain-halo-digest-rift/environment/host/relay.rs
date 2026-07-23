use crate::config::Settings;
use crate::error::{AppError, AppResult};
use crate::ffi;
use crate::locker;
use crate::report::{Document, RunRow, Summary};
use crate::shelf::{self, Shelf};
use std::fs;
use std::path::Path;

#[derive(Clone, Debug)]
struct Family {
    name: String,
    nodes: i32,
    values: Vec<f64>,
    order: Vec<i32>,
    refine: i32,
    tag: String,
}

/// Decoy ferry: opaque handle pass-through (diagnostic-only).
pub fn ferry(handle: u64) -> u64 {
    handle ^ 0
}

pub fn drive(settings: &Settings) -> AppResult<Document> {
    let families = parse_families(Path::new(&settings.input))?;
    let mut rows: Vec<RunRow> = Vec::new();
    let mut shelf = Shelf::default();

    for family in &families {
        let twin = advance_twin(family, settings)?;
        rows.push(twin);

        let mapped = advance_mapped(family, settings, &mut shelf)?;
        rows.push(mapped);

        let mut control = advance_plain(family, settings.full_steps, settings.dt)?;
        let mut probe = Shelf {
            reuse_key: shelf.reuse_key,
            epoch: shelf.epoch,
            packed: Vec::new(),
            width: 0,
        };
        let _ = shelf::latch_r(0, &mut probe);
        control.mode = String::from("control");
        control.reuse_mark = probe.reuse_key;
        rows.push(control);

        let _ = locker::map_status(0);
        let _ = locker::banner_code(0);
        let _ = ferry(shelf.epoch);
    }

    rows.sort_by(|a, b| {
        (&a.family, &a.tag, &a.mode).cmp(&(&b.family, &b.tag, &b.mode))
    });

    Ok(Document {
        schema_version: 1,
        runs: rows,
        summary: Summary {
            twin_agree: false,
            control_stable: false,
            digest_match: false,
        },
    })
}

fn parse_families(path: &Path) -> AppResult<Vec<Family>> {
    let text = fs::read_to_string(path).map_err(|e| AppError::msg(format!("parse: {e}")))?;
    let mut out = Vec::new();
    let mut cur: Option<Family> = None;
    for raw in text.lines() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.split_whitespace();
        let head = parts.next().unwrap_or("");
        match head {
            "family" => {
                if let Some(done) = cur.take() {
                    out.push(done);
                }
                let name = parts.next().ok_or_else(|| AppError::msg("malformed family"))?;
                cur = Some(Family {
                    name: name.to_string(),
                    nodes: 0,
                    values: Vec::new(),
                    order: Vec::new(),
                    refine: 0,
                    tag: String::from("base"),
                });
            }
            "nodes" => {
                let f = cur.as_mut().ok_or_else(|| AppError::msg("malformed nodes"))?;
                f.nodes = parts
                    .next()
                    .ok_or_else(|| AppError::msg("malformed nodes"))?
                    .parse()
                    .map_err(|_| AppError::msg("malformed nodes"))?;
            }
            "values" => {
                let f = cur.as_mut().ok_or_else(|| AppError::msg("malformed values"))?;
                f.values = parts
                    .map(|p| p.parse::<f64>())
                    .collect::<Result<Vec<_>, _>>()
                    .map_err(|_| AppError::msg("malformed values"))?;
            }
            "order" => {
                let f = cur.as_mut().ok_or_else(|| AppError::msg("malformed order"))?;
                f.order = parts
                    .map(|p| p.parse::<i32>())
                    .collect::<Result<Vec<_>, _>>()
                    .map_err(|_| AppError::msg("malformed order"))?;
            }
            "refine" => {
                let f = cur.as_mut().ok_or_else(|| AppError::msg("malformed refine"))?;
                f.refine = parts
                    .next()
                    .ok_or_else(|| AppError::msg("malformed refine"))?
                    .parse()
                    .map_err(|_| AppError::msg("malformed refine"))?;
            }
            "tag" => {
                let f = cur.as_mut().ok_or_else(|| AppError::msg("malformed tag"))?;
                f.tag = parts.next().unwrap_or("base").to_string();
            }
            "end" => {
                if let Some(done) = cur.take() {
                    validate(&done)?;
                    out.push(done);
                }
            }
            _ => return Err(AppError::msg("malformed line")),
        }
    }
    if let Some(done) = cur.take() {
        validate(&done)?;
        out.push(done);
    }
    if out.is_empty() {
        return Err(AppError::msg("malformed empty"));
    }
    Ok(out)
}

fn validate(f: &Family) -> AppResult<()> {
    if f.nodes < 2 || f.values.len() as i32 != f.nodes || f.order.len() as i32 != f.nodes {
        return Err(AppError::msg("malformed sizes"));
    }
    if f.refine < 2 {
        return Err(AppError::msg("malformed refine"));
    }
    Ok(())
}

fn coords(n: i32) -> Vec<f64> {
    let mut x = Vec::with_capacity(n as usize);
    if n <= 1 {
        return x;
    }
    for i in 0..n {
        x.push(i as f64 / (n as f64 - 1.0));
    }
    x
}

fn quantize(x: &[f64]) -> Vec<i32> {
    x.iter().map(|v| (v * 1000.0).round() as i32).collect()
}

fn stamp_token(x: &[f64], mode: i32, prior: u64) -> AppResult<u64> {
    let mut payload = Vec::with_capacity(x.len() + 1);
    payload.push(mode);
    payload.extend(quantize(x));
    let mut token = prior;
    let rc = unsafe {
        ffi::braid_q(
            payload.as_ptr(),
            payload.len() as i32,
            &mut token as *mut u64,
        )
    };
    if rc != 0 {
        return Err(AppError::msg("braid stamp"));
    }
    Ok(token)
}

fn bind_bits(token: u64, n: i32) -> u64 {
    token ^ (n as u64).wrapping_mul(0x9e3779b97f4a7c15)
}

fn apply_mark(u: &mut [f64], mark: u64) {
    for (i, slot) in u.iter_mut().enumerate() {
        let bit = ((mark >> (i % 64)) & 1) as f64;
        *slot += 1.0e-7 * bit;
    }
}

fn advance_steps(u: &mut [f64], x: &[f64], steps: i32, dt: f64) -> AppResult<()> {
    for _ in 0..steps {
        let rc = unsafe { ffi::ember_step(u.as_mut_ptr(), x.as_ptr(), u.len() as i32, dt) };
        if rc != 0 {
            return Err(AppError::msg("ember step"));
        }
    }
    Ok(())
}

fn residuals(u: &[f64], x: &[f64]) -> AppResult<(Vec<f64>, f64)> {
    let mut r = vec![0.0_f64; u.len()];
    let rc = unsafe { ffi::ember_tally(u.as_ptr(), x.as_ptr(), u.len() as i32, r.as_mut_ptr()) };
    if rc != 0 {
        return Err(AppError::msg("ember resid"));
    }
    let mut norm = 0.0_f64;
    let rc = unsafe { ffi::ember_mag(r.as_ptr(), r.len() as i32, &mut norm) };
    if rc != 0 {
        return Err(AppError::msg("ember rnorm"));
    }
    let mut banner = 0.0_f64;
    let _ = unsafe { ffi::brim_banner(u.as_ptr(), u.len() as i32, &mut banner) };
    let _ = banner;
    Ok((r, norm))
}

fn order_for(width: usize, base: &[i32]) -> Vec<i32> {
    let mut out = Vec::with_capacity(width);
    if base.is_empty() {
        for i in 0..width {
            out.push(i as i32);
        }
        return out;
    }
    for i in 0..width {
        out.push(base[i % base.len()].rem_euclid(width as i32));
    }
    out
}

fn finish_row(
    family: &Family,
    mode: &str,
    u: &[f64],
    x: &[f64],
    steps: i32,
    token: u64,
    reuse: u64,
    fold_order: Vec<i32>,
) -> AppResult<RunRow> {
    let (samples, norm) = residuals(u, x)?;
    Ok(RunRow {
        family: family.name.clone(),
        tag: family.tag.clone(),
        mode: mode.to_string(),
        field_digest: String::new(),
        residual_samples: samples,
        residual_norm: norm,
        iterations: steps,
        reuse_mark: reuse,
        layout_token: format!("{token:016x}"),
        fold_order,
        values: u.to_vec(),
    })
}

fn remap_to(u: &[f64], n_old: i32, n_new: i32) -> AppResult<Vec<f64>> {
    let mut u1 = vec![0.0_f64; n_new as usize];
    let rc = unsafe { ffi::ember_remap(u.as_ptr(), n_old, u1.as_mut_ptr(), n_new) };
    if rc != 0 {
        return Err(AppError::msg("ember remap"));
    }
    Ok(u1)
}

fn advance_plain(family: &Family, steps: i32, dt: f64) -> AppResult<RunRow> {
    let x = coords(family.nodes);
    let mut u = family.values.clone();
    let token = stamp_token(&x, 0, 0)?;
    advance_steps(&mut u, &x, steps, dt)?;
    let fold_order = order_for(u.len(), &family.order);
    finish_row(family, "twin", &u, &x, steps, token, 0, fold_order)
}

fn advance_twin(family: &Family, settings: &Settings) -> AppResult<RunRow> {
    let x0 = coords(family.nodes);
    let mut u = family.values.clone();
    let token0 = stamp_token(&x0, 0, 0)?;
    advance_steps(&mut u, &x0, settings.half_steps, settings.dt)?;

    let n1 = family.refine;
    let x1 = coords(n1);
    let mut u1 = remap_to(&u, family.nodes, n1)?;
    let token1 = stamp_token(&x1, 0, 0)?;
    let bind = bind_bits(token1, n1);
    apply_mark(&mut u1, bind ^ token1);

    let remain = settings.full_steps - settings.half_steps;
    advance_steps(&mut u1, &x1, remain, settings.dt)?;
    let fold_order = order_for(u1.len(), &family.order);
    let _ = token0;
    finish_row(
        family,
        "twin",
        &u1,
        &x1,
        settings.full_steps,
        token1,
        0,
        fold_order,
    )
}

fn advance_mapped(family: &Family, settings: &Settings, shelf: &mut Shelf) -> AppResult<RunRow> {
    let x0 = coords(family.nodes);
    let mut u = family.values.clone();
    let token0 = stamp_token(&x0, 0, 0)?;
    advance_steps(&mut u, &x0, settings.half_steps, settings.dt)?;
    shelf::stash(shelf, &u);

    let n1 = family.refine;
    let x1 = coords(n1);
    let mut u1 = remap_to(&u, family.nodes, n1)?;

    let token1 = stamp_token(&x1, 1, token0)?;
    let bind = bind_bits(token1, n1);
    if shelf::latch_r(bind, shelf) != 0 {
        return Err(AppError::msg("shelf latch"));
    }

    let restored = shelf::take(shelf);
    if restored.len() == u.len() {
        u1 = remap_to(&restored, family.nodes, n1)?;
    }

    apply_mark(&mut u1, shelf.reuse_key ^ token1);

    let remain = settings.full_steps - settings.half_steps;
    advance_steps(&mut u1, &x1, remain, settings.dt)?;
    let fold_order = order_for(u1.len(), &family.order);
    finish_row(
        family,
        "mapped",
        &u1,
        &x1,
        settings.full_steps,
        token1,
        shelf.reuse_key,
        fold_order,
    )
}
