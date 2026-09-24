# Parallel Computing Laboratory

This repository contains my practical work for the Advanced Parallel Programming & Architecture laboratory sessions.

It includes three sets of experiments:

- the original Python benchmarking laboratory;
- the Java parallel π approximation laboratory;
- the C/OpenMP Collatz practicum.

All benchmark results shown here are based on actual executions on my machine.

## Hardware

The experiments were executed on my MacBook Pro with an Apple M1 processor, 8 physical cores (4 Performance and 4 Efficiency cores), 8 logical cores, and 8 GB of unified memory.

The Python laboratory used Python 3.11.9. The Java laboratory used OpenJDK 21.0.5. The C/OpenMP practicum used Apple Clang with Homebrew `libomp`. The system reported a 128-byte cache line.

## Repository Structure

The root directory contains the original Python laboratory:

```text
parallel_lab/
├── task1_amdahl.py
├── task1_results.txt
├── task1_answers.txt
├── task2_falsesharing.py
├── task2_results.txt
├── task2_answers.txt
├── task3_sync.py
├── task3_results.txt
├── task3_answers.txt
├── task3_lockless.py
├── task3_lockless_results.txt
├── pi_parallel/
└── week4/
```

The Java laboratory is in `pi_parallel/`:

```text
pi_parallel/
├── Part1PhantomBug.java
├── part1_results.txt
├── Part2Synchronization.java
├── part2_results.txt
├── Part3Reduction.java
└── part3_results.txt
```

The C/OpenMP practicum is in `week4/`:

```text
week4/
├── collatz_seq.c
├── collatz.c
├── false_sharing.c
├── scheduling.c
├── hw_info.txt
├── results.csv
├── speedup_plot.png
├── analysis.md
├── analysis.pdf
├── amdahl_notes.txt
├── plot_speedup.py
└── make_analysis_pdf.py
```

Only source files, measurements, analysis, and generated deliverables are listed above. Locally compiled programs and the submission archive are not required in the Git repository.

## Python Laboratory

The `.py` files contain the implementations. The matching `results` files contain actual benchmark outputs, measured runtimes, and calculations. The `answers` files contain written explanations based on the observed results.

- **Task 1 — Amdahl and scaling:** Performance improved up to 8 workers, reaching a maximum observed speedup of 4.30×. It then degraded at 12 and 16 workers, beyond the machine's 8 physical cores.
- **Task 2 — false sharing:** The measured slowdown was approximately 1.01×. CPython's Global Interpreter Lock and object-based list representation limit what this Python experiment can demonstrate about low-level cache-line contention.
- **Task 3 — synchronization:** The `UnsafeCounter` produced the correct value of 2,000,000, with no observed lost updates. The lockless thread-local version also produced 2,000,000 and completed in 0.0426 seconds, 6.42× faster than the locked version. The recorded answer reports this observed behavior rather than assuming corruption occurred.

## Java Parallel π Laboratory

The three Java files investigate an incorrect parallel estimate, synchronization overhead, and reduction. Their matching `.txt` files contain the actual outputs, runtimes, comparisons, and explanations.

In Part 2, the synchronized version took 2238.82 ms versus 282.18 ms for the single-threaded version in the recorded run, a slowdown of approximately 7.93×.

For example, to run Part 2:

```bash
cd pi_parallel
javac Part2Synchronization.java
java Part2Synchronization
```

## Week 4: C/OpenMP Collatz Practicum

The workload is **N = 13,014,000**, calculated from the last four digits of my student ID (3014). The programs calculate the Collatz stopping time for every integer from 1 through N.

- `collatz_seq.c` establishes the sequential baseline.
- `collatz.c` measures OpenMP scaling with 1, 2, 4, and 8 threads.
- `false_sharing.c` compares per-thread counters in one cache line with an OpenMP reduction.
- `scheduling.c` compares static, dynamic, and guided loop scheduling.
- `results.csv` stores the raw timing runs and averages.
- `speedup_plot.png` compares measured speedup, the Amdahl prediction, and ideal linear speedup.
- `hw_info.txt` contains the hardware output captured on the test machine.
- `analysis.pdf` contains answers to the four technical questions. `analysis.md` is its editable source.

The sequential baseline averaged **2.077389 seconds**. The 8-thread version averaged **0.394290 seconds**, giving a measured speedup of **5.2687×**. The parallel fraction fitted from the 2-thread result was **p ≈ 0.9315**. Every scaling run produced a maximum stopping time of **688** and a checksum of **55,862,372**.

The false-sharing experiment counted **10,481,895** numbers requiring more than 100 steps. The naive variant averaged **0.472432 seconds**, compared with **0.403763 seconds** for reduction. The scheduling variants produced similar times. The interpretation and limitations are discussed in `analysis.pdf`.

### Building on this Mac

From the `week4` directory, Apple Clang can compile the OpenMP program using Homebrew `libomp`:

```bash
gcc -O2 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include collatz.c -L/opt/homebrew/opt/libomp/lib -Wl,-rpath,/opt/homebrew/opt/libomp/lib -lomp -o collatz
./collatz 8
```

The scripts `plot_speedup.py` and `make_analysis_pdf.py` regenerate the graph and PDF from the saved data and analysis. Benchmark times can vary between runs and machines.
