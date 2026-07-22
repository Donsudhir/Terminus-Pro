#!/bin/bash
set -euo pipefail

cat > /app/rust/src/ember/fold.rs <<'RS'
use crate::model::{FoldErr, Mark, RUNE_FIXED, RUNE_VOID};

pub(crate) fn tilt_a(a: &[i64], b: &[u8], c: &[u8]) -> Result<Mark, FoldErr> {
    if a.is_empty() {
        return Err(FoldErr::Empty);
    }
    if a.len() != b.len() || a.len() != c.len() {
        return Err(FoldErr::Shape);
    }

    let mut low: Option<i64> = None;
    let mut high: Option<i64> = None;
    let mut has_absent = false;

    for index in 0..a.len() {
        let live = if c[index] == RUNE_VOID {
            false
        } else if c[index] == RUNE_FIXED {
            true
        } else {
            b[index] != u8::default()
        };

        if !live {
            has_absent = true;
            continue;
        }

        low = Some(match low {
            Some(previous) => previous.min(a[index]),
            None => a[index],
        });
        high = Some(match high {
            Some(previous) => previous.max(a[index]),
            None => a[index],
        });
    }

    Ok(Mark {
        low: low.unwrap_or_default(),
        high: high.unwrap_or_default(),
        has_absent,
    })
}
RS

cat > /app/cpp/src/harbor/veil.cpp <<'CPP'
#include "loam/plan.hpp"

namespace loam {

Gate turn_b(const Slab& a, const Probe& b) {
    if (!b.skipping) {
        return {true, "full"};
    }
    if (b.op == Op::All) {
        return {true, "all"};
    }
    if (a.generation < 3) {
        return {true, "legacy-open"};
    }
    if (b.op == Op::IsNull) {
        return {a.has_absent, a.has_absent ? "possible" : "empty"};
    }
    if (b.op == Op::RegionEqual) {
        if (a.region_low.empty() || a.region_high.empty() || a.region_low > a.region_high) {
            return {true, "unknown-text"};
        }
        const bool read = b.text >= a.region_low && b.text <= a.region_high;
        return {read, read ? "text-hit" : "text-away"};
    }
    if (a.low > a.high) {
        return {true, "unknown-range"};
    }

    std::int64_t left = b.x;
    std::int64_t right = b.op == Op::Range ? b.y : b.x;
    if (left > right) {
        const std::int64_t swap = left;
        left = right;
        right = swap;
    }
    const bool read = !(right < a.low || left > a.high);
    return {read, read ? "range-hit" : "range-away"};
}

}  // namespace loam
CPP

cat > /app/cpp/src/lattice/rill.cpp <<'CPP'
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
        const auto lane = static_cast<Origin>(a.origin_lane[i]);
        if (lane == Origin::Retired) {
            admit[i] = 0;
        } else if (lane == Origin::Inherited) {
            admit[i] = 1;
        } else {
            admit[i] = a.presence_lane[i] != 0 ? 1 : 0;
        }
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
CPP

/app/tools/build-all
/app/tools/reset-lab
/app/bin/loam audit /app/data/cases /app/output/audit.json
