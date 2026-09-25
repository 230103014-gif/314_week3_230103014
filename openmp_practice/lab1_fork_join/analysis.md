# Lab 1: Fork-Join Model, Team Creation, and Thread Scoping

## Task 1.1 — Verification of Non-Determinism

The starter program was executed 10 consecutive times without modifying the source code. The complete stdout output was saved in `outputs_10_runs.txt`.

The logical thread ranks did not execute in sequential order. In the observed runs, the typical output order was:

0 → 3 → 1 → 2

This occurs because submitted tasks are scheduled by the operating system and the Python thread pool rather than being executed according to their logical rank.

The experiment also showed that a logical task ID is not the same as a native operating-system thread ID. In several runs, the same native OS thread executed more than one logical task because `ThreadPoolExecutor` reuses worker threads.

The fact that several runs produced the same ordering does not make execution deterministic. Thread scheduling does not guarantee this ordering, and it may change depending on system load, timing, and scheduler decisions.


## Task 1.2 — Thread Oversubscription Sweep

The thread-team creation and join time was benchmarked for:

P = {1, 2, 4, 8, 16, 32, 64}

Each configuration was measured over five trials and the average wall-clock time was calculated.

| Threads (P) | Average Time (s) |
|------------:|-----------------:|
| 1  | 0.000083 |
| 2  | 0.000118 |
| 4  | 0.000186 |
| 8  | 0.000346 |
| 16 | 0.000723 |
| 32 | 0.001530 |
| 64 | 0.002972 |

The results show that thread-team management overhead increases as the number of threads increases.

The benchmark contains almost no useful computational work, so increasing the thread count does not provide a speedup. Instead, additional threads introduce scheduling, synchronization, and thread-management overhead.

The increase becomes especially visible at 16, 32, and 64 threads. This illustrates the cost associated with creating and coordinating a large software thread team.