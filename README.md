All source code, raw benchmark outputs, calculations, and written explanations are included in the attached files.

The experiments were executed on my MacBook Pro with an Apple M1 processor, 8 physical cores (4 Performance and 4 Efficiency cores), 8 logical cores, 8 GB of unified memory, and Python 3.11.9.

In Task 1, performance improved up to 8 workers, reaching a maximum observed speedup of 4.30x. Performance then degraded at 12 and 16 workers because the number of processes exceeded the eight available physical cores.

In Task 2, the measured false-sharing slowdown was only approximately 1.01x. This limited difference is explained by CPython’s Global Interpreter Lock and Python’s object-based list representation, which prevent the supplied program from behaving like a low-level compiled false-sharing benchmark.

In Task 3, the UnsafeCounter produced the correct value of 2,000,000, with zero observed lost updates. This empirical result is also related to CPython’s GIL and runtime scheduling. I reported the actual result rather than fabricating corruption. The lockless thread-local redesign also produced exactly 2,000,000 and completed in 0.0426 seconds, making it 6.42x faster than the LockedCounter and exceeding the required 2.0x speedup.

The `results` files contain the raw measured outputs, the Python files contain the implementations used for testing, and the `answers` files contain the completed tables, calculations, and architectural explanations based on my actual results.
