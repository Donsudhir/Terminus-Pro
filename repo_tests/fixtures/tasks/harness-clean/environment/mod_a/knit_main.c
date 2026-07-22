#include "op_knit.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: knit_main <alpha> <bravo> <out_dir>\n");
        return 2;
    }
    return op_knit(argv[1], argv[2], argv[3]) == 0 ? 0 : 1;
}
