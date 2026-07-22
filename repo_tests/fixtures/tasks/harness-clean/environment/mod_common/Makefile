CC = gcc
CFLAGS = -O2 -Wall -Wextra -I.
BIN = /app/bin

all: $(BIN)/knit_main $(BIN)/lane_main $(BIN)/seal_main

$(BIN):
	mkdir -p $(BIN)

$(BIN)/knit_main: ../mod_a/op_knit.c ../mod_a/knit_main.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ ../mod_a/op_knit.c ../mod_a/knit_main.c

$(BIN)/lane_main: ../mod_b/step_lane.c ../mod_b/lane_main.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ ../mod_b/step_lane.c ../mod_b/lane_main.c

$(BIN)/seal_main: ../mod_c/seal_phase.c ../mod_c/seal_main.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ ../mod_c/seal_phase.c ../mod_c/seal_main.c

.PHONY: all clean
clean:
	rm -f $(BIN)/knit_main $(BIN)/lane_main $(BIN)/seal_main
