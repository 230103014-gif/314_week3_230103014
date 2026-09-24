/*
 * Collatz OpenMP scaling experiment
 * Student ID suffix: 3014
 * Workload: N = 13,014,000
 *
 * Compile on this macOS system:
 * gcc -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include collatz.c -L/opt/homebrew/opt/libomp/lib -Wl,-rpath,/opt/homebrew/opt/libomp/lib -lomp -o collatz
 *
 * Run: ./collatz 1
 *      ./collatz 2
 *      ./collatz 4
 *      ./collatz 8
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
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
        fprintf(stderr, "Usage: %s <threads>\n", argv[0]);
        return 1;
    }

    int threads = atoi(argv[1]);
    if (threads < 1 || threads > 8) {
        fprintf(stderr, "Choose 1 to 8 threads.\n");
        return 1;
    }

    omp_set_dynamic(0);
    omp_set_num_threads(threads);

    uint32_t max_steps = 0;
    uint64_t sum = 0;
    double start = omp_get_wtime();

    #pragma omp parallel for schedule(static) reduction(max:max_steps) reduction(+:sum)
    for (uint64_t i = 1; i <= N; i++) {
        uint32_t steps = collatz_steps(i);
        if (steps > max_steps) max_steps = steps;
        sum += steps;
    }

    double elapsed = omp_get_wtime() - start;

    printf("Threads: %d\n", threads);
    printf("Maximum steps: %" PRIu32 "\n", max_steps);
    printf("Checksum: %" PRIu64 "\n", sum % MOD);
    printf("Time: %.6f seconds\n", elapsed);

    return 0;
}