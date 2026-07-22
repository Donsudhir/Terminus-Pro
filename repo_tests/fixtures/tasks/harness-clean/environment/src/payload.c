#include <stdio.h>
#include "courier_abi.h"

int thread_slot_value(void);
int errno_slot_value(void);

/* Provided by lane_tag.o from step_lane staging. */
extern const char lane_tag_bytes[];

int main(void) {
    printf("MARKER=%s\n", COURIER_ABI_TOKEN);
    printf("THREAD=%d\n", thread_slot_value());
    printf("ERRNO=%d\n", errno_slot_value());
    printf("LANE_TAG=%s\n", lane_tag_bytes);
    return 0;
}
