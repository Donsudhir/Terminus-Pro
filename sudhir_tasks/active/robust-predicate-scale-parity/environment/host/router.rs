use crate::error::AppResult;
use crate::measure;
use crate::model::Frame;
use crate::plate::map_state;

pub(crate) fn map_code(message: &str) -> i32 {
    eprintln!("geometry lab: {message}");
    2
}

pub(crate) fn dispatch(arguments: &[String]) -> AppResult<Option<i32>> {
    if arguments.len() == 1 {
        return Ok(None);
    }
    match arguments[1].as_str() {
        "--inspect-status" => {
            if arguments.len() != 3 {
                return Err("--inspect-status requires one integer".to_string());
            }
            let raw = arguments[2]
                .parse::<i32>()
                .map_err(|_| "invalid state value".to_string())?;
            let mut frame = Frame::default();
            let mapped = map_state(raw, &mut frame);
            println!(
                "{{\"raw\":{},\"mapped\":{},\"refine\":{}}}",
                frame.raw_status,
                mapped,
                if frame.needs_refine { "true" } else { "false" }
            );
            Ok(Some(0))
        }
        "--inspect-series" => {
            if arguments.len() < 4 {
                return Err("--inspect-series requires an exact sign and terms".to_string());
            }
            let exact = arguments[2]
                .parse::<i32>()
                .map_err(|_| "invalid exact sign".to_string())?;
            if ![-1, 0, 1].contains(&exact) {
                return Err("exact sign outside supported range".to_string());
            }
            let terms: Result<Vec<f64>, _> = arguments[3..]
                .iter()
                .map(|value| value.parse::<f64>())
                .collect();
            let terms = terms.map_err(|_| "invalid series term".to_string())?;
            let mut frame = Frame::default();
            let row = measure::inspect_series(&terms, exact, &mut frame);
            println!(
                "{{\"raw\":{},\"mapped\":{},\"final\":{},\"refine\":{}}}",
                row.raw,
                row.mapped,
                row.final_sign,
                if row.refine { "true" } else { "false" }
            );
            Ok(Some(0))
        }
        _ => Err("unknown command argument".to_string()),
    }
}
