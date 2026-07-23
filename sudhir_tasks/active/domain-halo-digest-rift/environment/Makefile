CC = gcc
AR = ar
RUSTC = rustc

BUILD_DIR ?= build
BIN_DIR ?= bin
CFLAGS = -std=c11 -O2 -fno-fast-math -ffp-contract=off -Wall -Wextra -Werror
RUSTFLAGS = -C opt-level=2 -C debuginfo=0

NATIVE_OBJECTS = $(BUILD_DIR)/ledge.o $(BUILD_DIR)/brim.o $(BUILD_DIR)/ember.o

.PHONY: all clean run

all: $(BIN_DIR)/partlab

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BUILD_DIR)/ledge.o: native/ledge.c native/include/ledge.h native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/brim.o: native/brim.c native/include/ledge.h native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/ember.o: native/ember.c native/include/ledge.h native/include/common.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) -Inative/include -c $< -o $@

$(BUILD_DIR)/libnative.a: $(NATIVE_OBJECTS)
	$(AR) rcs $@ $^

HOST_SOURCES = $(wildcard host/*.rs)

$(BIN_DIR)/partlab: host/main.rs $(HOST_SOURCES) $(BUILD_DIR)/libnative.a | $(BIN_DIR)
	$(RUSTC) --edition=2021 $(RUSTFLAGS) host/main.rs \
		-L native=$(BUILD_DIR) -l static=native \
		-C link-arg=-lm \
		-o $@

run: all
	mkdir -p output
	$(BIN_DIR)/partlab

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f output/parity_report.json
