#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <omp.h>

#define N 13014000ULL
#define MOD 1000000007ULL

static uint32_t collatz_steps(uint64_t n) {
    uint32_t steps = 0;
    while (n > 1) {
        if (n % 2 == 0) n /= 2;
        else n = 3 * n + 1;
        steps++;
    }
    return steps;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s static|static1000|dynamic100|dynamic10000|guided\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "static") == 0)
        omp_set_schedule(omp_sched_static, 0);
    else if (strcmp(argv[1], "static1000") == 0)
        omp_set_schedule(omp_sched_static, 1000);
    else if (strcmp(argv[1], "dynamic100") == 0)
        omp_set_schedule(omp_sched_dynamic, 100);
    else if (strcmp(argv[1], "dynamic10000") == 0)
        omp_set_schedule(omp_sched_dynamic, 10000);
    else if (strcmp(argv[1], "guided") == 0)
        omp_set_schedule(omp_sched_guided, 0);
    else {
        fprintf(stderr, "Unknown schedule: %s\n", argv[1]);
        return 1;
    }

    omp_set_dynamic(0);
    omp_set_num_threads(8);

    uint32_t max_steps = 0;
    uint64_t sum = 0;
    double start = omp_get_wtime();

    #pragma omp parallel for schedule(runtime) \
        reduction(max:max_steps) reduction(+:sum)
    for (uint64_t i = 1; i <= N; i++) {
        uint32_t steps = collatz_steps(i);
        if (steps > max_steps) max_steps = steps;
        sum += steps;
    }

    double elapsed = omp_get_wtime() - start;

    printf("Schedule: %s\n", argv[1]);
    printf("Maximum steps: %" PRIu32 "\n", max_steps);
    printf("Checksum: %" PRIu64 "\n", sum % MOD);
    printf("Time: %.6f seconds\n", elapsed);
    return 0;
}