use crate::config;
use crate::engine;
use crate::error::AppResult;
use crate::gauge;
use crate::model::Gauge;
use crate::parse;

pub fn dispatch(arguments: &[String]) -> AppResult<Option<i32>> {
    if arguments.len() >= 2 && arguments[1] == "--inspect-group" {
        if arguments.len() != 4 {
            return Err("inspect-group usage".into());
        }
        let families = parse::load(std::path::Path::new("/app/data/families.resid"))?;
        let family = families
            .iter()
            .find(|item| item.name == "aurora")
            .ok_or("aurora missing")?;
        let col_a: usize = arguments[2].parse().map_err(|_| "col_a")?;
        let col_b: usize = arguments[3].parse().map_err(|_| "col_b")?;
        let grouped = engine::inspect_group(family, col_a, col_b)?;
        println!("{{\"grouped\":{grouped}}}");
        return Ok(Some(0));
    }
    if arguments.len() >= 2 && arguments[1] == "--inspect-span" {
        let settings = config::load(std::path::Path::new("/app/conf/runtime.conf"))?;
        let families = parse::load(std::path::Path::new(&settings.input))?;
        let family = families.first().ok_or("no families")?;
        let tag = family.tags.first().ok_or("no tags")?;
        let mut gauge = crate::model::Gauge {
            reference: 0.0,
            step: settings.step_floor,
            primed: false,
        };
        let record = engine::evaluate_family(family, tag, None, &settings, false, &mut gauge)?;
        println!(
            "{{\"ref\":{},\"step\":{}}}",
            record.span_info.reference, record.span_info.step
        );
        return Ok(Some(0));
    }
    if arguments.len() >= 2 && arguments[1] == "--mode-echo" {
        let settings = config::load(std::path::Path::new("/app/conf/runtime.conf"))?;
        let families = parse::load(std::path::Path::new(&settings.input))?;
        let family = families
            .iter()
            .find(|item| item.name == "aurora")
            .ok_or("aurora missing")?;
        let tag = family
            .tags
            .iter()
            .find(|item| item.name == "base")
            .ok_or("base tag")?;
        let mut gauge = Gauge {
            reference: 0.0,
            step: settings.step_floor,
            primed: false,
        };
        let cold = engine::evaluate_family(family, tag, None, &settings, false, &mut gauge)?;
        let warm = engine::evaluate_family(family, tag, None, &settings, true, &mut gauge)?;
        let same = cold.values == warm.values && cold.indices == warm.indices;
        println!("{{\"same\":{}}}", if same { "true" } else { "false" });
        return Ok(Some(0));
    }
    Ok(None)
}

pub fn map_code(message: &str) -> i32 {
    if message.contains("input") || message.contains("parse") || message.contains("config") {
        2
    } else {
        1
    }
}

pub fn dry_gauge(values: &[f64]) -> Gauge {
    let mut gauge = Gauge {
        reference: 0.0,
        step: 1.0e-8,
        primed: false,
    };
    gauge::reset_span(&mut gauge, values);
    gauge
}
