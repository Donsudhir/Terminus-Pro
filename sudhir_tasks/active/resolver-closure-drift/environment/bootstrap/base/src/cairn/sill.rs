use crate::model::{
    Admitted, PolicyFrame, PolicyMode, RejectCode, Vane, VaneKind,
};

pub(crate) fn turn_sill(a: Vane, b: &PolicyFrame) -> Result<Admitted, RejectCode> {
    let priority = match a.kind {
        VaneKind::HeldPin if matches!(b.mode, PolicyMode::Alpha) => 0,
        VaneKind::HeldLane
            if matches!(b.mode, PolicyMode::Beta) && b.exact =>
        {
            0
        }
        VaneKind::Alpha
            if matches!(b.mode, PolicyMode::Alpha | PolicyMode::Mixed) =>
        {
            0
        }
        VaneKind::Normal if !a.withdrawn => {
            if b.stable_available {
                10
            } else {
                20
            }
        }
        VaneKind::Beta => return Err(RejectCode::Held),
        VaneKind::HeldPin | VaneKind::HeldLane => {
            return Err(RejectCode::Context);
        }
        VaneKind::Alpha | VaneKind::Normal => {
            return Err(RejectCode::Withdrawn);
        }
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
