import os

# Must be configured before Numba is imported.
# The lab requires testing up to P = 16.
os.environ["NUMBA_NUM_THREADS"] = "16"

import math
import time
import csv

import numpy as np
from numba import njit, prange, set_num_threads


# =========================================================
# CONFIGURATION
# =========================================================

N_RACE = 5_000_000
N_CRITICAL = 1_000_000
N_REDUCTION = 100_000_000

RACE_THREADS = [1, 2, 4, 8]
SCALING_THREADS = [1, 2, 4, 8, 16]

TRIALS = 5


# =========================================================
# SERIAL BASELINE
# =========================================================

@njit
def calc_pi_serial(num_steps):
    step = 1.0 / num_steps
    total = 0.0

    for i in range(num_steps):
        x = (i + 0.5) * step
        total += 4.0 / (1.0 + x * x)

    return total * step


# =========================================================
# TASK 2.1 — NAIVE SHARED UPDATE / RACE CONDITION
# =========================================================

@njit(parallel=True)
def calc_pi_race(num_steps):
    step = 1.0 / num_steps

    # Intentionally shared memory location.
    shared_sum = np.zeros(1, dtype=np.float64)

    for i in prange(num_steps):
        x = (i + 0.5) * step

        # Intentionally unsafe read-modify-write.
        # Multiple threads update the same memory location.
        shared_sum[0] += 4.0 / (1.0 + x * x)

    return shared_sum[0] * step


# =========================================================
# TASK 2.2 — CRITICAL SECTION
# =========================================================

# The critical-section experiment uses Python locking deliberately
# to demonstrate serialization / lock contention.

import threading


def calc_pi_critical(num_steps, num_threads):
    step = 1.0 / num_steps
    shared_sum = [0.0]

    lock = threading.Lock()
    chunk = num_steps // num_threads

    def worker(start, end):
        for i in range(start, end):
            x = (i + 0.5) * step
            term = 4.0 / (1.0 + x * x)

            # Only one thread may update shared_sum at a time.
            with lock:
                shared_sum[0] += term

    threads = []

    for t in range(num_threads):
        start = t * chunk

        if t == num_threads - 1:
            end = num_steps
        else:
            end = start + chunk

        thread = threading.Thread(
            target=worker,
            args=(start, end)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return shared_sum[0] * step


# =========================================================
# TASK 2.3 — PARALLEL REDUCTION
# =========================================================

@njit(parallel=True)
def calc_pi_reduction(num_steps):
    step = 1.0 / num_steps
    total = 0.0

    for i in prange(num_steps):
        x = (i + 0.5) * step

        # Numba recognizes this as a reduction.
        total += 4.0 / (1.0 + x * x)

    return total * step


# =========================================================
# MAIN
# =========================================================

def main():

    # -----------------------------------------------------
    # JIT warm-up
    # -----------------------------------------------------

    set_num_threads(1)

    calc_pi_serial(1000)
    calc_pi_race(1000)
    calc_pi_reduction(1000)

    # =====================================================
    # TASK 2.1
    # Race Condition Quantification
    # =====================================================

    print("\nTASK 2.1 - Race Condition")
    print("-" * 70)

    race_results = []

    for p in RACE_THREADS:

        set_num_threads(p)

        start = time.perf_counter()

        pi_value = calc_pi_race(N_RACE)

        end = time.perf_counter()

        elapsed = end - start
        error = abs(pi_value - math.pi)

        race_results.append([
            p,
            pi_value,
            error,
            elapsed
        ])

        print(
            f"P={p:2d} | "
            f"Pi={pi_value:.12f} | "
            f"Error={error:.6e} | "
            f"Time={elapsed:.4f}s"
        )

    with open("race_results.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Threads",
            "Calculated Pi",
            "Absolute Error",
            "Time (s)"
        ])

        writer.writerows(race_results)

    # =====================================================
    # TASK 2.2
    # Critical Section Overhead
    # =====================================================

    print("\nTASK 2.2 - Critical Section")
    print("-" * 70)

    # Serial baseline
    start = time.perf_counter()

    serial_pi = calc_pi_serial(N_CRITICAL)

    end = time.perf_counter()

    serial_time = end - start

    # Four-thread critical section
    start = time.perf_counter()

    critical_pi = calc_pi_critical(
        N_CRITICAL,
        4
    )

    end = time.perf_counter()

    critical_time = end - start

    overhead = (
        (critical_time - serial_time)
        / serial_time
        * 100
    )

    print(
        f"Serial:   "
        f"Pi={serial_pi:.12f} | "
        f"Time={serial_time:.6f}s"
    )

    print(
        f"Critical: "
        f"Pi={critical_pi:.12f} | "
        f"Time={critical_time:.6f}s"
    )

    print(
        f"Lock contention overhead = "
        f"{overhead:.2f}%"
    )

    with open(
        "critical_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Variant",
            "Calculated Pi",
            "Time (s)",
            "Overhead (%)"
        ])

        writer.writerow([
            "Serial",
            serial_pi,
            serial_time,
            0
        ])

        writer.writerow([
            "Critical Section",
            critical_pi,
            critical_time,
            overhead
        ])

    # =====================================================
    # TASK 2.3
    # Strong Scaling Benchmark
    # =====================================================

    print("\nTASK 2.3 - Strong Scaling")
    print("-" * 70)

    scaling_results = []

    for p in SCALING_THREADS:

        set_num_threads(p)

        trial_times = []

        pi_value = 0.0

        for trial in range(TRIALS):

            start = time.perf_counter()

            pi_value = calc_pi_reduction(
                N_REDUCTION
            )

            end = time.perf_counter()

            trial_times.append(
                end - start
            )

        average = (
            sum(trial_times)
            / TRIALS
        )

        scaling_results.append({
            "threads": p,
            "trials": trial_times,
            "average": average,
            "pi": pi_value
        })

        print(
            f"P={p:2d} | "
            f"Average={average:.4f}s | "
            f"Pi={pi_value:.12f}"
        )

    # =====================================================
    # TASK 2.4
    # Speedup and Efficiency
    # =====================================================

    print("\nTASK 2.4 - Speedup and Efficiency")
    print("-" * 70)

    base_time = scaling_results[0]["average"]

    final_results = []

    for result in scaling_results:

        p = result["threads"]
        average = result["average"]

        speedup = (
            base_time / average
        )

        efficiency = (
            speedup / p
        )

        final_results.append([
            p,
            *result["trials"],
            average,
            result["pi"],
            speedup,
            efficiency
        ])

        print(
            f"P={p:2d} | "
            f"Speedup={speedup:.3f}x | "
            f"Efficiency={efficiency:.3f}"
        )

    with open(
        "scaling_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Threads",
            "Trial 1",
            "Trial 2",
            "Trial 3",
            "Trial 4",
            "Trial 5",
            "Average Time",
            "Calculated Pi",
            "Speedup",
            "Efficiency"
        ])

        writer.writerows(
            final_results
        )

    print("\nResults saved:")
    print("  race_results.csv")
    print("  critical_results.csv")
    print("  scaling_results.csv")


if __name__ == "__main__":
    main()