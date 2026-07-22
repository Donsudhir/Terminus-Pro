#include "loam/plan.hpp"

namespace loam {

Gate turn_b(const Slab& a, const Probe& b) {
    if (!b.skipping) {
        return {true, "full"};
    }
    if (b.op == Op::All) {
        return {true, "all"};
    }
    if (b.op == Op::IsNull) {
        return {a.has_absent, a.has_absent ? "possible" : "empty"};
    }
    if (b.op == Op::RegionEqual) {
        const bool read = b.text >= a.region_low && b.text <= a.region_high;
        return {read, read ? "text-hit" : "text-away"};
    }

    const std::int64_t left = b.op == Op::Equal ? b.x : b.x;
    const std::int64_t right = b.op == Op::Equal ? b.x : b.y;
    const bool read = !(right < a.low || left > a.high);
    return {read, read ? "range-hit" : "range-away"};
}

}  // namespace loam
