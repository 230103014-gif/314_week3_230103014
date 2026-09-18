# Parallel Computing Laboratory

This repository contains my practical work for the Advanced Parallel Programming & Architecture laboratory sessions.

The repository currently includes two sets of experiments:

- the original Python benchmarking laboratory;
- the Java parallel π approximation laboratory.

All results shown in this repository are based on actual executions on my machine.

## Hardware

The experiments were executed on my MacBook Pro with an Apple M1 processor, 8 physical cores (4 Performance cores and 4 Efficiency cores), 8 logical cores, and 8 GB of unified memory.

The Python laboratory used Python 3.11.9.

The Java laboratory was executed using OpenJDK 21.0.5.

---

## Repository Structure

The root directory contains the Python laboratory files:

```text
parallel_lab/
│
├── task1_amdahl.py
├── task1_results.txt
├── task1_answers.txt
│
├── task2_falsesharing.py
├── task2_results.txt
├── task2_answers.txt
│
├── task3_sync.py
├── task3_results.txt
├── task3_answers.txt
│
├── task3_lockless.py
├── task3_lockless_results.txt
│
└── pi_parallel/

The pi_parallel folder contains the newer Java laboratory:

pi_parallel/
│
├── Part1PhantomBug.java
├── part1_results.txt
│
├── Part2Synchronization.java
├── part2_results.txt
│
├── Part3Reduction.java
└── part3_results.txt

The .java files contain the implementations used for the experiments.

The .txt files contain the actual benchmark outputs, measured runtimes, calculated speedups and efficiencies, and written explanations based on the observed results.
