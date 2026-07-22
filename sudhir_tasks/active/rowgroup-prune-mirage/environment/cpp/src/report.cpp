#include "loam/report.hpp"

#include <fstream>
#include <sstream>
#include <stdexcept>

namespace loam {
namespace {

std::string escape_json(const std::string& value) {
    std::string out;
    for (const char ch : value) {
        if (ch == '"' || ch == '\\') {
            out.push_back('\\');
        }
        out.push_back(ch);
    }
    return out;
}

std::string cases_json(const std::vector<CaseResult>& cases) {
    std::ostringstream out;
    out << '[';
    for (std::size_t i = 0; i < cases.size(); ++i) {
        if (i != 0) out << ',';
        const auto& item = cases[i];
        out << "{\"case_id\":\"" << escape_json(item.case_id)
            << "\",\"row_count\":" << item.tally.row_count
            << ",\"sum_amount\":" << item.tally.sum_amount
            << ",\"pages_total\":" << item.pages_total
            << ",\"pages_read\":" << item.tally.pages_read
            << ",\"path\":\"" << lane_name(item.lane)
            << "\",\"skipping\":" << (item.skipping ? "true" : "false")
            << '}';
    }
    out << ']';
    return out.str();
}

}  // namespace

std::string lane_name(const Lane lane) {
    return lane == Lane::Batch ? "batch" : "row";
}

void write_report(const std::filesystem::path& path, const std::vector<CaseResult>& cases) {
    if (path.has_parent_path()) {
        std::filesystem::create_directories(path.parent_path());
    }
    const std::string body = cases_json(cases);
    const std::string digest = digest_hex(body);
    std::ofstream output(path, std::ios::binary | std::ios::trunc);
    if (!output) {
        throw std::runtime_error("cannot write report: " + path.string());
    }
    output << "{\"status\":\"complete\",\"cases\":" << body
           << ",\"digest\":\"" << digest << "\"}\n";
}

}  // namespace loam
