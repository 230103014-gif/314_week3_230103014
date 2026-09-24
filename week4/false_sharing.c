#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <omp.h>

#define N 13014000ULL
#define THREADS 8

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
    if (argc != 2 ||
        (strcmp(argv[1], "naive") != 0 &&
         strcmp(argv[1], "reduction") != 0)) {
        fprintf(stderr, "Usage: %s naive|reduction\n", argv[0]);
        return 1;
    }

    omp_set_dynamic(0);
    omp_set_num_threads(THREADS);

    uint32_t max_steps = 0;
    uint64_t total_hits = 0;
    double start = omp_get_wtime();

    if (strcmp(argv[1], "naive") == 0) {
        // All eight counters fit within one 128-byte cache line.
        _Alignas(128) volatile uint64_t hit_count[THREADS] = {0};

        #pragma omp parallel for schedule(static) reduction(max:max_steps)
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t steps = collatz_steps(i);
            if (steps > max_steps) max_steps = steps;
            if (steps > 100) hit_count[omp_get_thread_num()]++;
        }

        for (int t = 0; t < THREADS; t++) {
            total_hits += hit_count[t];
        }
    } else {
        #pragma omp parallel for schedule(static) \
            reduction(max:max_steps) reduction(+:total_hits)
        for (uint64_t i = 1; i <= N; i++) {
            uint32_t steps = collatz_steps(i);
            if (steps > max_steps) max_steps = steps;
            if (steps > 100) total_hits++;
        }
    }

    double elapsed = omp_get_wtime() - start;

    printf("Variant: %s\n", argv[1]);
    printf("Threads: %d\n", THREADS);
    printf("Maximum steps: %" PRIu32 "\n", max_steps);
    printf("Hits (>100 steps): %" PRIu64 "\n", total_hits);
    printf("Time: %.6f seconds\n", elapsed);
    return 0;
}