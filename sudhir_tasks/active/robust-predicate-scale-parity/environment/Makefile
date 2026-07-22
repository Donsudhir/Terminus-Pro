CC = gcc
FC = gfortran
AR = ar
RUSTC = rustc

BUILD_DIR ?= build
BIN_DIR ?= bin
CFLAGS = -std=c11 -O2 -fno-fast-math -ffp-contract=off -Wall -Wextra -Werror
FFLAGS = -O2 -Wall -Wextra -Werror
RUSTFLAGS = -C opt-level=2 -C debuginfo=0

NATIVE_OBJECTS = $(BUILD_DIR)/series.o $(BUILD_DIR)/refine.o $(BUILD_DIR)/window.o
ANALYSIS_OBJECTS = $(BUILD_DIR)/pack.o $(BUILD_DIR)/stats.o

.PHONY: all clean run

all: $(BIN_DIR)/geomlab

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BUILD_DIR)/series.o: native/series.c native/include/series.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/refine.o: native/refine.c native/include/refine.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/window.o: native/window.c native/include/window.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/pack.o: analysis/pack.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/stats.o: analysis/stats.f90 | $(BUILD_DIR)
	$(FC) $(FFLAGS) -c $< -o $@

$(BUILD_DIR)/libnative.a: $(NATIVE_OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libanalysis.a: $(ANALYSIS_OBJECTS)
	$(AR) rcs $@ $^

$(BIN_DIR)/geomlab: host/main.rs $(BUILD_DIR)/libnative.a $(BUILD_DIR)/libanalysis.a | $(BIN_DIR)
	$(RUSTC) --edition=2021 $(RUSTFLAGS) host/main.rs \
		-L native=$(BUILD_DIR) -l static=native -l static=analysis \
		-C link-arg=-lgfortran -C link-arg=-lquadmath -C link-arg=-lm \
		-o $@

run: all
	mkdir -p output
	$(BIN_DIR)/geomlab

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f output/geometry_report.json
