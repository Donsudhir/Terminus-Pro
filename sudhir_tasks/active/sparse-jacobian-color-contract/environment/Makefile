CC = gcc
FC = gfortran
AR = ar
RUSTC = rustc

BUILD_DIR ?= build
BIN_DIR ?= bin
CFLAGS = -std=c11 -O2 -fno-fast-math -ffp-contract=off -Wall -Wextra -Werror
FFLAGS = -O2 -Wall -Wextra -Werror
RUSTFLAGS = -C opt-level=2 -C debuginfo=0

NATIVE_OBJECTS = $(BUILD_DIR)/lane.o $(BUILD_DIR)/ledge.o $(BUILD_DIR)/ember.o $(BUILD_DIR)/quill.o
ANALYSIS_OBJECTS = $(BUILD_DIR)/knit.o $(BUILD_DIR)/tally.o
KERNEL_OBJECTS = $(BUILD_DIR)/ridge.o

.PHONY: all clean run

all: $(BIN_DIR)/senslab

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BUILD_DIR)/lane.o: native/lane.c native/include/lane.h native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/ledge.o: native/ledge.c native/include/lane.h native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/ember.o: native/ember.c native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/quill.o: native/quill.c native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/knit.o: analysis/knit.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/tally.o: analysis/tally.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/ridge.o: kernels/ridge.f90 kernels/ridge.h | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/libnative.a: $(NATIVE_OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libanalysis.a: $(ANALYSIS_OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libridge.a: $(KERNEL_OBJECTS)
	$(AR) rcs $@ $^

HOST_SOURCES = $(wildcard host/*.rs)

$(BIN_DIR)/senslab: host/main.rs $(HOST_SOURCES) $(BUILD_DIR)/libnative.a $(BUILD_DIR)/libanalysis.a $(BUILD_DIR)/libridge.a | $(BIN_DIR)
	$(RUSTC) --edition=2021 $(RUSTFLAGS) host/main.rs \
		-L native=$(BUILD_DIR) -l static=native -l static=analysis -l static=ridge \
		-C link-arg=-lgfortran -C link-arg=-lquadmath -C link-arg=-lm \
		-o $@

run: all
	mkdir -p output
	$(BIN_DIR)/senslab

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f output/sensitivity_report.json
