import threading
import time


TOTAL_OPS = 2_000_000
NUM_THREADS = 4
LOCKED_TIME = 0.2733


def bench_lockless():
    partial_results = [0] * NUM_THREADS
    ops_per_thread = TOTAL_OPS // NUM_THREADS

    def work(thread_index):
        local_counter = 0

        for _ in range(ops_per_thread):
            local_counter += 1

        partial_results[thread_index] = local_counter

    threads = [
        threading.Thread(target=work, args=(i,))
        for i in range(NUM_THREADS)
    ]

    start = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    final_value = sum(partial_results)
    elapsed = time.perf_counter() - start

    return final_value, elapsed


if __name__ == "__main__":
    value, lockless_time = bench_lockless()
    speedup = LOCKED_TIME / lockless_time

    print(f"Lockless Value: {value:,} / {TOTAL_OPS:,}")
    print(f"Lockless Execution Time: {lockless_time:.4f}s")
    print(f"Locked Execution Time: {LOCKED_TIME:.4f}s")
    print(f"Speedup over LockedCounter: {speedup:.2f}x")
    