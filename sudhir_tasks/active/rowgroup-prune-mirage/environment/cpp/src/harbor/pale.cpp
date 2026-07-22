#include "loam/plan.hpp"

namespace loam {

std::string turn_d(const Gate& a, const Probe& b) {
    const char* lane = b.lane == Lane::Batch ? "batch" : "row";
    return std::string(lane) + ":" + (a.read ? "open:" : "closed:") + a.note;
}

}  // namespace loam
