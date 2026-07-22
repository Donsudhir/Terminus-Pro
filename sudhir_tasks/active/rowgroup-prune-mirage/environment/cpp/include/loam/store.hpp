#pragma once

#include "loam/types.hpp"

#include <filesystem>
#include <vector>

namespace loam {

std::vector<Slab> load_store(const std::filesystem::path& path);
std::vector<CaseSpec> load_cases(const std::filesystem::path& directory);
CaseResult run_case(const CaseSpec& spec);

}  // namespace loam
