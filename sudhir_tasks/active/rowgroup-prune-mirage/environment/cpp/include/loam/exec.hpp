#pragma once

#include "loam/types.hpp"

namespace loam {

Tally walk_row(const Slab& a, const Probe& b, const Gate& c);
Tally sweep_c(const Slab& a, const Probe& b, const Gate& c);
Tally sweep_e(const Tally& a, const Tally& b);

}  // namespace loam
