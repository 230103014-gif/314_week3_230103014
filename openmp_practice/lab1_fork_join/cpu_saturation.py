from concurrent.futures import ThreadPoolExecutor
from numba import njit
import math
import time
import os


WORK_PER_THREAD = 1_000_000_000


@njit(nogil=True)
def heavy_work(iterations):
    total = 0.0

    for i in range(1, iterations + 1):
        total += math.sqrt(i)

    return total


def worker(thread_id):
    start = time.perf_counter()

    result = heavy_work(WORK_PER_THREAD)

    end = time.perf_counter()

    print(
        f"Thread {thread_id:2d} finished "
        f"in {end - start:.3f} seconds"
    )

    return result


def run_cpu_test(num_threads):
    print()
    print(f"Running CPU saturation test with {num_threads} threads")
    print(f"Work per thread: {WORK_PER_THREAD:,} square roots")
    print("-" * 60)

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker, tid)
            for tid in range(num_threads)
        ]

        for future in futures:
            future.result()

    end = time.perf_counter()

    print("-" * 60)
    print(f"Total wall-clock time: {end - start:.3f} seconds")


if __name__ == "__main__":

    # Compile before benchmark so JIT compilation is not included.
    print("Warming up Numba...")
    heavy_work(1000)

    print(f"Logical CPUs reported by Python: {os.cpu_count()}")

    threads = int(
        input("Enter number of threads for CPU test: ")
    )

    run_cpu_test(threads)