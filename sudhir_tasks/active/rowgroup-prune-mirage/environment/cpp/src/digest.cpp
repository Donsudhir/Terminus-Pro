#include "loam/report.hpp"

#include <cstdint>
#include <iomanip>
#include <sstream>

namespace loam {

std::string digest_hex(const std::string& text) {
    std::uint64_t value = 1469598103934665603ULL;
    for (const unsigned char byte : text) {
        value ^= byte;
        value *= 1099511628211ULL;
    }
    std::ostringstream out;
    out << std::hex << std::setfill('0') << std::setw(16) << value;
    return out.str();
}

}  // namespace loam
