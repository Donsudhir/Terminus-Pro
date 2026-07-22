#include "loam/report.hpp"
#include "loam/store.hpp"

#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <sys/wait.h>
#include <unistd.h>
#include <vector>

namespace {

int run_ingest(const char* input, const char* output) {
    const pid_t child = fork();
    if (child == -1) {
        throw std::runtime_error("fork failed");
    }
    if (child == 0) {
        execl("/app/bin/loam-ingest", "loam-ingest", input, output, nullptr);
        _exit(127);
    }
    int status = 0;
    if (waitpid(child, &status, 0) == -1) {
        throw std::runtime_error("waitpid failed");
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc == 4 && std::string(argv[1]) == "audit") {
            const auto specs = loam::load_cases(argv[2]);
            std::vector<loam::CaseResult> results;
            results.reserve(specs.size());
            for (const auto& spec : specs) {
                results.push_back(loam::run_case(spec));
            }
            loam::write_report(argv[3], results);
            return 0;
        }
        if (argc == 4 && std::string(argv[1]) == "ingest") {
            return run_ingest(argv[2], argv[3]);
        }
        if (argc == 3 && std::string(argv[1]) == "inspect") {
            const auto slabs = loam::load_store(argv[2]);
            for (const auto& slab : slabs) {
                std::cout << slab.id << '|' << static_cast<int>(slab.generation)
                          << '|' << slab.low << '|' << slab.high << '|'
                          << (slab.has_absent ? 1 : 0) << '|' << slab.cells.size()
                          << '\n';
            }
            return 0;
        }
        std::cerr << "usage: loam audit <case-directory> <report-path>\n"
                  << "       loam ingest <csv> <store-directory>\n"
                  << "       loam inspect <store>\n";
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "loam: " << error.what() << '\n';
        return 1;
    }
}
