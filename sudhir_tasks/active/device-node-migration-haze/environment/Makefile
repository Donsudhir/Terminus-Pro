CC = gcc
AR = ar
RUSTC = rustc

BUILD_DIR ?= build
BIN_DIR ?= bin
CFLAGS = -std=c11 -O2 -Wall -Wextra -Werror
RUSTFLAGS = -C opt-level=2 -C debuginfo=0

LOOM_OBJECTS = $(BUILD_DIR)/loom.o $(BUILD_DIR)/ledge.o
PROBE_OBJECTS = $(BUILD_DIR)/open_probe.o

.PHONY: all clean run

all: $(BIN_DIR)/haze

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BUILD_DIR)/loom.o: loom/loom.c loom/include/loom.h loom/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Iloom/include -c $< -o $@

$(BUILD_DIR)/ledge.o: loom/ledge.c loom/include/loom.h loom/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Iloom/include -c $< -o $@

$(BUILD_DIR)/open_probe.o: probe/open_probe.c probe/include/open_probe.h crate/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Iprobe/include -Icrate/include -c $< -o $@

$(BUILD_DIR)/libhaze.a: $(LOOM_OBJECTS) $(PROBE_OBJECTS)
	$(AR) rcs $@ $^

RUST_SOURCES = $(wildcard crate/*.rs) $(wildcard veil/*.rs) $(wildcard tether/*.rs)

$(BIN_DIR)/haze: crate/main.rs $(RUST_SOURCES) $(BUILD_DIR)/libhaze.a | $(BIN_DIR)
	$(RUSTC) --edition=2021 $(RUSTFLAGS) crate/main.rs \
		-L native=$(BUILD_DIR) -l static=haze \
		-C link-arg=-lm \
		-o $@

run: all
	mkdir -p output
	$(BIN_DIR)/haze

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f output/cutover_report.json
