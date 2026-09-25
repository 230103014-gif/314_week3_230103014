from concurrent.futures import ThreadPoolExecutor
import threading
import time
import csv


THREAD_COUNTS = [1, 2, 4, 8, 16, 32, 64]
TRIALS = 5


def benchmark_team(num_threads: int) -> float:
    """
    Measure the wall-clock time required to create,
    run, synchronize, and join a team of threads.
    """

    barrier = threading.Barrier(num_threads + 1)

    def worker():
        barrier.wait()

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker)
            for _ in range(num_threads)
        ]

        barrier.wait()

        for future in futures:
            future.result()

    end = time.perf_counter()

    return end - start


def main():
    results = []

    print("Thread Oversubscription Benchmark")
    print("-" * 55)

    for p in THREAD_COUNTS:
        trial_times = []

        for trial in range(TRIALS):
            elapsed = benchmark_team(p)
            trial_times.append(elapsed)

        average = sum(trial_times) / TRIALS

        results.append((p, *trial_times, average))

        print(
            f"P = {p:2d} | "
            f"Average time = {average:.6f} seconds"
        )

    with open("timing_results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Threads",
            "Trial 1",
            "Trial 2",
            "Trial 3",
            "Trial 4",
            "Trial 5",
            "Average"
        ])

        writer.writerows(results)

    print("\nResults saved to timing_results.csv")


if __name__ == "__main__":
    main()