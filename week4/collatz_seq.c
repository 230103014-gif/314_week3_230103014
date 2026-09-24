#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <omp.h>

#define N 13014000ULL
#define MOD 1000000007ULL

static uint32_t collatz_steps(uint64_t n) {
    uint32_t steps = 0;

    while (n > 1) {
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = 3 * n + 1;
        }
        steps++;
    }

    return steps;
}

int main(void) {
    uint32_t max_steps = 0;
    uint64_t sum = 0;

    double start = omp_get_wtime();

    for (uint64_t i = 1; i <= N; i++) {
        uint32_t steps = collatz_steps(i);

        if (steps > max_steps) {
            max_steps = steps;
        }
        sum = (sum + steps) % MOD;
    }

    double elapsed = omp_get_wtime() - start;

    printf("N: %" PRIu64 "\n", (uint64_t)N);
    printf("Maximum steps: %" PRIu32 "\n", max_steps);
    printf("Checksum: %" PRIu64 "\n", sum);
    printf("Time: %.6f seconds\n", elapsed);

    return 0;
}