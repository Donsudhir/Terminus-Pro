CXX = g++
FC = gfortran
AR = ar
RUSTC = rustc

BUILD_DIR ?= build
BIN_DIR ?= bin
CXXFLAGS = -std=c++17 -O2 -fno-fast-math -ffp-contract=off -Wall -Wextra -Werror
FFLAGS = -O2 -Wall -Wextra -Werror
RUSTFLAGS = -C opt-level=2 -C debuginfo=0

NATIVE_OBJECTS = $(BUILD_DIR)/span.o $(BUILD_DIR)/ledge.o $(BUILD_DIR)/ember.o
PACK_OBJECTS = $(BUILD_DIR)/fold.o $(BUILD_DIR)/tally.o
KERNEL_OBJECTS = $(BUILD_DIR)/ridge.o

.PHONY: all clean run

all: $(BIN_DIR)/meshlab

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BUILD_DIR)/span.o: native/span.cpp native/include/span.h native/include/common.h | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/ledge.o: native/ledge.cpp native/include/span.h native/include/common.h | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/ember.o: native/ember.cpp native/include/common.h | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/fold.o: pack/fold.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/tally.o: pack/tally.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/ridge.o: kernels/ridge.f90 kernels/ridge.h | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/libnative.a: $(NATIVE_OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libpack.a: $(PACK_OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libridge.a: $(KERNEL_OBJECTS)
	$(AR) rcs $@ $^

HOST_SOURCES = $(wildcard host/*.rs)

$(BIN_DIR)/meshlab: host/main.rs $(HOST_SOURCES) $(BUILD_DIR)/libnative.a $(BUILD_DIR)/libpack.a $(BUILD_DIR)/libridge.a | $(BIN_DIR)
	$(RUSTC) --edition=2021 $(RUSTFLAGS) host/main.rs \
		-L native=$(BUILD_DIR) -l static=native -l static=pack -l static=ridge \
		-C link-arg=-lstdc++ -C link-arg=-lgfortran -C link-arg=-lquadmath -C link-arg=-lm \
		-o $@

run: all
	mkdir -p output
	$(BIN_DIR)/meshlab

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f output/parity_report.json
