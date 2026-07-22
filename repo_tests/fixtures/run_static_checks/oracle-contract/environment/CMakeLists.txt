cmake_minimum_required(VERSION 3.20)
project(contract_fixture C)

# TB_TIMELINE_MODE selects the timeline behavior used by the shipped runner.
# TB_REEXEC_MODE selects the second execution behavior.
set(TB_TIMELINE_MODE 1 CACHE STRING "timeline mode")
set(TB_REEXEC_MODE 1 CACHE STRING "re-execution mode")
add_executable(netplay_matrix main.c)
