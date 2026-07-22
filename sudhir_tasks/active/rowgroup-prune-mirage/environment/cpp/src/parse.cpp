#include "loam/store.hpp"

#include <algorithm>
#include <fstream>
#include <stdexcept>
#include <string>

namespace loam {
namespace {

std::vector<std::string> split(const std::string& line) {
    std::vector<std::string> fields;
    std::size_t start = 0;
    while (true) {
        const auto end = line.find('|', start);
        fields.push_back(line.substr(start, end - start));
        if (end == std::string::npos) {
            break;
        }
        start = end + 1;
    }
    return fields;
}

Op parse_op(const std::string& value) {
    if (value == "all") return Op::All;
    if (value == "eq") return Op::Equal;
    if (value == "range") return Op::Range;
    if (value == "isnull") return Op::IsNull;
    if (value == "region_eq") return Op::RegionEqual;
    throw std::runtime_error("unknown operation: " + value);
}

Lane parse_lane(const std::string& value) {
    if (value == "row") return Lane::Row;
    if (value == "batch") return Lane::Batch;
    throw std::runtime_error("unknown path: " + value);
}

}  // namespace

std::vector<CaseSpec> load_cases(const std::filesystem::path& directory) {
    std::vector<std::filesystem::path> paths;
    for (const auto& entry : std::filesystem::directory_iterator(directory)) {
        if (entry.is_regular_file() && entry.path().extension() == ".case") {
            paths.push_back(entry.path());
        }
    }
    std::sort(paths.begin(), paths.end());

    std::vector<CaseSpec> cases;
    for (const auto& path : paths) {
        std::ifstream input(path);
        if (!input) {
            throw std::runtime_error("cannot open case file: " + path.string());
        }
        std::string line;
        while (std::getline(input, line)) {
            if (line.empty() || line[0] == '#') {
                continue;
            }
            const auto fields = split(line);
            if (fields.size() != 8) {
                throw std::runtime_error("bad case row in " + path.string());
            }
            Probe probe;
            probe.op = parse_op(fields[2]);
            if (probe.op == Op::RegionEqual) {
                probe.text = fields[3];
            } else {
                probe.x = std::stoll(fields[3]);
                probe.y = std::stoll(fields[4]);
            }
            probe.lane = parse_lane(fields[5]);
            probe.skipping = fields[6] == "1";
            cases.push_back({fields[0], fields[1], std::move(probe)});
        }
    }
    return cases;
}

}  // namespace loam
