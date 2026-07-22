use crate::error::AppResult;
use crate::frame::clear_frame;
use crate::measure;
use crate::model::{
    BatchReport, CoordPoint, Family, Frame, OrientationSummary, TopologySummary,
    ValiditySummary,
};
use crate::pool;
use crate::relay;
use std::collections::BTreeSet;

fn materialize(family: &Family, scale: i32, frame: &Frame) -> Vec<CoordPoint> {
    family
        .points
        .iter()
        .map(|point| CoordPoint {
            id: point.id,
            fast: std::array::from_fn(|axis| frame.fast_value(point.xyz[axis], scale)),
            exact: std::array::from_fn(|axis| frame.exact_value(point.xyz[axis], scale)),
        })
        .collect()
}

fn enumerate(points: &[CoordPoint], frame: &mut Frame) -> Vec<[i32; 4]> {
    let mut cells = Vec::new();
    for a in 0..points.len() - 3 {
        for b in a + 1..points.len() - 2 {
            for c in b + 1..points.len() - 1 {
                for d in c + 1..points.len() {
                    let mut selected = [&points[a], &points[b], &points[c], &points[d]];
                    let sign = measure::orientation(selected, frame);
                    if sign == 0 {
                        continue;
                    }
                    if sign < 0 {
                        selected.swap(0, 1);
                    }
                    let mut occupied = false;
                    for (index, query) in points.iter().enumerate() {
                        if index == a || index == b || index == c || index == d {
                            continue;
                        }
                        if measure::sphere(selected, query, frame) > 0 {
                            occupied = true;
                            break;
                        }
                    }
                    if !occupied {
                        cells.push([
                            selected[0].id,
                            selected[1].id,
                            selected[2].id,
                            selected[3].id,
                        ]);
                    }
                }
            }
        }
    }
    cells
}

fn selected<'a>(row: &[i32; 4], points: &'a [CoordPoint]) -> AppResult<[&'a CoordPoint; 4]> {
    let find = |id: i32| {
        points
            .iter()
            .find(|point| point.id == id)
            .ok_or_else(|| format!("row refers to unknown point identity {id}"))
    };
    Ok([find(row[0])?, find(row[1])?, find(row[2])?, find(row[3])?])
}

fn summarize(
    cells: &[[i32; 4]],
    points: &[CoordPoint],
    frame: &mut Frame,
    fold: relay::FoldStats,
) -> AppResult<(OrientationSummary, ValiditySummary, TopologySummary)> {
    let mut orientation = OrientationSummary {
        positive: 0,
        negative: 0,
        zero: 0,
    };
    let mut validity = ValiditySummary {
        checks: 0,
        violations: fold.overfull,
    };
    if fold.faces != fold.boundary + fold.interior
        || 4 * cells.len() != fold.boundary + 2 * fold.interior
    {
        validity.violations += 1;
    }
    let mut edges = BTreeSet::new();
    for cell in cells {
        let selected = selected(cell, points)?;
        match measure::orientation(selected, frame).signum() {
            1 => orientation.positive += 1,
            -1 => orientation.negative += 1,
            _ => orientation.zero += 1,
        }
        for query in points {
            if cell.contains(&query.id) {
                continue;
            }
            validity.checks += 1;
            if measure::sphere(selected, query, frame) > 0 {
                validity.violations += 1;
            }
        }
        for left in 0..4 {
            for right in left + 1..4 {
                let mut edge = [cell[left], cell[right]];
                edge.sort();
                edges.insert(edge);
            }
        }
    }
    let vertices = points.len();
    let cell_count = cells.len();
    let euler = vertices as isize - edges.len() as isize + fold.faces as isize - cell_count as isize;
    let topology = TopologySummary {
        vertices,
        edges: edges.len(),
        faces: fold.faces,
        cells: cell_count,
        boundary_faces: fold.boundary,
        euler,
    };
    Ok((orientation, validity, topology))
}

pub(crate) fn run(families: &[Family]) -> AppResult<Vec<BatchReport>> {
    let mut frame = Frame::default();
    let mut reports = Vec::new();
    let mut scratch = Vec::<i32>::new();
    for family in families {
        for variant in &family.variants {
            if !pool::shift_is_finite(&variant.shift) {
                return Err(format!("family {} variant {} has a non-finite translation", family.name, variant.name));
            }
            let exponents: Vec<f64> = family
                .points
                .iter()
                .flat_map(|point| {
                    point
                        .xyz
                        .iter()
                        .map(|value| value.exponent.saturating_add(variant.scale) as f64)
                })
                .collect();
            clear_frame(&mut frame, &exponents);
            if frame.invalid {
                return Err(format!("family {} variant {} has an invalid coordinate frame", family.name, variant.name));
            }
            let points = materialize(family, variant.scale, &frame);
            let mut cells = enumerate(&points, &mut frame);
            let fold = relay::fold_complex(&mut cells)?;
            let adjacency = relay::link_faces(&cells);
            let (orientation, validity, topology) = summarize(&cells, &points, &mut frame, fold)?;
            scratch.push(frame.raw_status);
            reports.push(BatchReport {
                family: family.name.clone(),
                variant: variant.name.clone(),
                point_ids: family.points.iter().map(|point| point.id).collect(),
                cells,
                adjacency,
                orientation,
                validity,
                topology,
            });
            pool::clear_slot(&mut scratch);
        }
    }
    reports.sort_by(|left, right| {
        left.family
            .cmp(&right.family)
            .then_with(|| left.variant.cmp(&right.variant))
    });
    Ok(reports)
}
