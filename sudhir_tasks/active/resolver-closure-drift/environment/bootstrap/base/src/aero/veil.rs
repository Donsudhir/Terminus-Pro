use crate::model::{
    ClassError, PolicyMode, QueryFrame, RawRecord, Vane, VaneKind,
};

pub(crate) fn cast_vane(a: &RawRecord, b: &QueryFrame) -> Result<Vane, ClassError> {
    if a.key.is_empty()
        || a.release.is_empty()
        || a.origin.is_empty()
        || a.payload.is_empty()
        || a.api.is_empty()
    {
        return Err(ClassError::Empty);
    }
    if b.need.low >= b.need.high || !b.need.accepts(a) {
        return Err(ClassError::Outside);
    }
    let kind = if a.preview && b.need.preview {
        VaneKind::HeldPin
    } else if a.withdrawn
        && b.need.exact.is_some()
        && matches!(b.mode, PolicyMode::Beta | PolicyMode::Mixed)
    {
        VaneKind::HeldLane
    } else {
        VaneKind::Normal
    };
    let mut needs = a.needs.clone();
    needs.sort_by(|left, right| {
        left.key
            .cmp(&right.key)
            .then_with(|| left.low.cmp(&right.low))
            .then_with(|| left.high.cmp(&right.high))
            .then_with(|| left.exact.cmp(&right.exact))
    });
    Ok(Vane {
        key: a.key.clone(),
        release: a.release.clone(),
        code: a.code,
        origin: a.origin.clone(),
        kind,
        withdrawn: a.withdrawn,
        needs,
        payload: a.payload.clone(),
        api: a.api.clone(),
        serial: b.ordinal,
    })
}
