#include "step_lane.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: lane_main <bravo> <charlie> <out_path>\n");
        return 2;
    }
    return step_lane(argv[1], argv[2], argv[3]) == 0 ? 0 : 1;
}
