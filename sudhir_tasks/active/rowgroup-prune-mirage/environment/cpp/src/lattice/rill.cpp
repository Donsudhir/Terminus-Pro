#include "loam/exec.hpp"

#include <cstddef>
#include <vector>

namespace loam {

Tally sweep_c(const Slab& a, const Probe& b, const Gate& c) {
    Tally tally;
    if (!c.read) {
        return tally;
    }
    tally.pages_read = 1;

    const std::size_t count = a.amount_lane.size();
    std::vector<unsigned char> admit(count, 0);
    for (std::size_t i = 0; i < count; ++i) {
        admit[i] = a.presence_lane[i] != 0 ? 1 : 0;
    }

    if (b.op == Op::IsNull) {
        for (std::size_t i = 0; i < count; ++i) {
            if (admit[i] == 0) {
                ++tally.row_count;
            }
        }
        return tally;
    }

    for (std::size_t i = 0; i < count; ++i) {
        if (admit[i] == 0) {
            continue;
        }
        bool keep = false;
        switch (b.op) {
            case Op::All:
                keep = true;
                break;
            case Op::Equal:
                keep = a.amount_lane[i] == b.x;
                break;
            case Op::Range:
                keep = a.amount_lane[i] >= b.x && a.amount_lane[i] <= b.y;
                break;
            case Op::IsNull:
                keep = false;
                break;
            case Op::RegionEqual:
                keep = a.region_lane[i] == b.text;
                break;
        }
        if (keep) {
            ++tally.row_count;
            tally.sum_amount += a.amount_lane[i];
        }
    }
    return tally;
}

}  // namespace loam
