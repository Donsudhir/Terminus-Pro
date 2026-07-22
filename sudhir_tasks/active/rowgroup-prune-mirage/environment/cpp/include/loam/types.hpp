#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace loam {

enum class Origin : std::uint8_t { Retired = 0, Inherited = 1, Current = 2 };

struct Cell {
    std::uint8_t present{};
    Origin origin{Origin::Current};
    std::int64_t amount{};
    std::string region;
};

struct Slab {
    std::size_t id{};
    std::uint8_t generation{};
    std::int64_t low{};
    std::int64_t high{};
    bool has_absent{};
    std::string region_low;
    std::string region_high;
    std::vector<Cell> cells;
    std::vector<std::int64_t> amount_lane;
    std::vector<std::uint8_t> presence_lane;
    std::vector<std::uint8_t> origin_lane;
    std::vector<std::string> region_lane;
};

enum class Op { All, Equal, Range, IsNull, RegionEqual };
enum class Lane { Row, Batch };

struct Probe {
    Op op{Op::All};
    std::int64_t x{};
    std::int64_t y{};
    std::string text;
    Lane lane{Lane::Row};
    bool skipping{};
};

struct Gate {
    bool read{true};
    std::string note;
};

struct Tally {
    std::int64_t row_count{};
    std::int64_t sum_amount{};
    std::int64_t pages_read{};
};

struct CaseSpec {
    std::string case_id;
    std::string store_path;
    Probe probe;
};

struct CaseResult {
    std::string case_id;
    Tally tally;
    std::int64_t pages_total{};
    Lane lane{Lane::Row};
    bool skipping{};
};

}  // namespace loam
