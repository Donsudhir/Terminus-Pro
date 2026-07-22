/* Source for vendor slot archives — seeded into bravo/charlie at image build. */
static __thread int slot;

int thread_slot_value(void) {
    slot = 7;
    return slot;
}
