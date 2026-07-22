#include "loam/exec.hpp"

namespace loam {
namespace {

bool is_live(const Cell& cell) {
    if (cell.origin == Origin::Retired) {
        return false;
    }
    if (cell.origin == Origin::Inherited) {
        return true;
    }
    return cell.present != 0;
}

bool matches(const Cell& cell, const Probe& probe) {
    switch (probe.op) {
        case Op::All:
            return true;
        case Op::Equal:
            return cell.amount == probe.x;
        case Op::Range:
            return cell.amount >= probe.x && cell.amount <= probe.y;
        case Op::IsNull:
            return false;
        case Op::RegionEqual:
            return cell.region == probe.text;
    }
    return false;
}

}  // namespace

Tally walk_row(const Slab& a, const Probe& b, const Gate& c) {
    Tally tally;
    if (!c.read) {
        return tally;
    }
    tally.pages_read = 1;
    for (const auto& cell : a.cells) {
        const bool live = is_live(cell);
        if (b.op == Op::IsNull) {
            if (!live) {
                ++tally.row_count;
            }
            continue;
        }
        if (live && matches(cell, b)) {
            ++tally.row_count;
            tally.sum_amount += cell.amount;
        }
    }
    return tally;
}

}  // namespace loam
