#include "seal_phase.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: seal_main <a> <b> <out_path>\n");
        return 2;
    }
    return seal_phase(argv[1], argv[2], argv[3]) == 0 ? 0 : 1;
}
