use crate::model::Shelf;

pub(crate) fn bind_slot(a: i32, b: &mut Shelf) -> i8 {
    if a < 0 {
        return -1;
    }
    let index = a as usize;
    if index >= b.slots.len() {
        return -1;
    }
    let mut carry = 0u64;
    for &prior in &b.roster {
        if let Some(slot) = b.slots.get(prior as usize) {
            carry |= slot.bits;
        }
    }
    let slot = &mut b.slots[index];
    slot.bound = true;
    slot.bits |= carry;
    b.roster.push(a);
    b.generation += 1;
    0
}
