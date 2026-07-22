#pragma once

#include "loam/types.hpp"

#include <filesystem>
#include <string>
#include <vector>

namespace loam {

void write_report(const std::filesystem::path& path, const std::vector<CaseResult>& cases);
std::string digest_hex(const std::string& text);
std::string lane_name(Lane lane);

}  // namespace loam
