use crate::model::{Shelf, SlotState};

pub(crate) fn make_shelf(groups: i32) -> Shelf {
    let count = groups.max(1) as usize;
    Shelf {
        slots: (0..count)
            .map(|_| SlotState {
                bits: 0,
                bound: false,
            })
            .collect(),
        roster: Vec::new(),
        generation: 0,
    }
}

pub(crate) fn pack_shelf(shelf: &Shelf) -> Vec<i32> {
    let mut out = vec![shelf.generation, shelf.roster.len() as i32];
    out.extend(shelf.roster.iter().copied());
    for slot in &shelf.slots {
        out.push((slot.bits & 0xffff_ffff) as i32);
        out.push(((slot.bits >> 32) & 0xffff_ffff) as i32);
        out.push(if slot.bound { 1 } else { 0 });
    }
    out
}

pub(crate) fn unpack_shelf(data: &[i32], groups: i32) -> Shelf {
    let mut shelf = make_shelf(groups);
    if data.len() < 2 {
        return shelf;
    }
    shelf.generation = data[0];
    let roster_len = data[1].max(0) as usize;
    if data.len() >= 2 + roster_len {
        shelf.roster = data[2..2 + roster_len].to_vec();
    }
    let mut cursor = 2 + roster_len;
    for slot in &mut shelf.slots {
        if cursor + 2 < data.len() {
            let lo = data[cursor] as u32 as u64;
            let hi = data[cursor + 1] as u32 as u64;
            slot.bits = lo | (hi << 32);
            slot.bound = data[cursor + 2] != 0;
            cursor += 3;
        }
    }
    shelf
}
