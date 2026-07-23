use crate::model::{
    Admitted, PolicyFrame, PolicyMode, RejectCode, Vane, VaneKind,
};

pub(crate) fn turn_sill(a: Vane, b: &PolicyFrame) -> Result<Admitted, RejectCode> {
    let priority = match a.kind {
        VaneKind::Alpha
            if matches!(b.mode, PolicyMode::Alpha | PolicyMode::Mixed)
                && !a.withdrawn =>
        {
            0
        }
        VaneKind::Beta
            if matches!(b.mode, PolicyMode::Beta | PolicyMode::Mixed)
                && a.withdrawn
                && b.exact =>
        {
            0
        }
        VaneKind::Normal if !a.withdrawn => {
            if b.stable_available {
                10
            } else if b.root {
                20
            } else {
                30
            }
        }
        VaneKind::HeldPin | VaneKind::HeldLane => {
            return Err(RejectCode::Context);
        }
        VaneKind::Alpha | VaneKind::Beta => {
            return Err(RejectCode::Context);
        }
        VaneKind::Normal => return Err(RejectCode::Withdrawn),
    };
    Ok(Admitted {
        key: a.key,
        release: a.release,
        code: a.code,
        origin: a.origin,
        needs: a.needs,
        payload: a.payload,
        api: a.api,
        priority,
        kind: a.kind,
        serial: a.serial,
    })
}
