# Technical Analysis

Hardware: Apple M1 (MacBookPro17,1), 4 Performance cores and 4 Efficiency cores, 8 physical and 8 logical cores. Reported cache line size: 128 bytes. Workload: N = 13,014,000.

## Q1. False sharing

The eight counters in the naive variant occupy the same 128-byte cache line. Although each thread updates a different counter, writes from different cores can require ownership of that shared line and cause cache-coherence traffic. MESI/MOESI illustrates this general invalidation mechanism; this experiment does not establish which exact protocol the Apple M1 implements.

The naive variant averaged 0.472432 s, compared with 0.403763 s for the OpenMP reduction: a 1.17× time penalty. The naive counter was declared `volatile` to ensure repeated stores. Therefore, the measured difference includes the cost of those stores as well as possible false sharing; it cannot be attributed entirely to cache invalidations.

## Q2. SMT and physical-core limits

This Mac has 8 physical and 8 logical cores, so it has no additional SMT threads. A physical-core-to-SMT comparison is not applicable to this machine.

Measured speedup increased from 3.5704× at 4 threads to 5.2687× at 8 threads, less than a doubling. The eight cores include four Performance and four Efficiency cores with different capabilities. Thread-management costs, resource contention, and workload distribution can also limit scaling. On a CPU with SMT, sibling threads would share execution resources within one physical core, but that case was not measured here.

## Q3. Empirical versus theoretical Amdahl speedup

T_seq = 2.077389 s and T_2 = 1.1097935 s, so S_emp(2) = 1.8719. Solving Amdahl's equation gives:

p = 2 × (1 − 1 / S_emp(2)) = 0.9315.

At 4 threads, the measured speedup was 3.5704× versus the model's 3.3185×. At 8 threads, it was 5.2687× versus 5.4085×. The model is fitted to the two-thread measurement and does not account for heterogeneous Performance/Efficiency cores, synchronization and scheduling overhead, changing CPU frequency, or measurement variation. A negative gap at 4 threads is therefore possible.

## Q4. Scheduling trade-off

Average times at 8 threads were: static 0.391099 s; static(1000) 0.370822 s; dynamic(100) 0.368198 s; dynamic(10000) 0.370483 s; and guided 0.368740 s.

Dynamic(100) had the lowest mean in these runs, but its advantage over dynamic(10000) was only 0.002285 s. The observed run-to-run variation is larger than that difference. Thus, these measurements do not identify a chunk size at which dynamic scheduling overhead clearly outweighed the benefit of load balancing. Smaller chunks may increase scheduling overhead, while larger chunks may leave more work imbalance near the end.