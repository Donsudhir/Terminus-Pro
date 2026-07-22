#include "loam/exec.hpp"

namespace loam {

Tally sweep_e(const Tally& a, const Tally& b) {
    return {
        a.row_count + b.row_count,
        a.sum_amount + b.sum_amount,
        a.pages_read + b.pages_read,
    };
}

}  // namespace loam
