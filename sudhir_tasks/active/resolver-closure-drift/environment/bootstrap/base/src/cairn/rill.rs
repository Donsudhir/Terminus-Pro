use crate::aero::pale::Fane;

#[derive(Clone, Debug)]
pub struct AdvisoryFrame {
    pub ceiling: i32,
}

#[derive(Clone, Debug)]
pub struct Shown {
    pub label: String,
    pub value: i32,
}

#[derive(Clone, Debug)]
pub enum DropCode {
    Above,
}

pub fn turn_rill(a: Fane, b: &AdvisoryFrame) -> Result<Shown, DropCode> {
    if a.value > b.ceiling {
        return Err(DropCode::Above);
    }
    Ok(Shown {
        label: a.label,
        value: a.value,
    })
}
