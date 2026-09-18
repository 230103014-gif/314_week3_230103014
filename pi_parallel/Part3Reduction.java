import java.util.concurrent.ThreadLocalRandom;

public class Part3Reduction {

    static final long TOTAL_POINTS = 100_000_000L;

    public static double runBenchmark(int numThreads) throws InterruptedException {

        long pointsPerThread = TOTAL_POINTS / numThreads;

        long[] localHits = new long[numThreads];
        Thread[] threads = new Thread[numThreads];

        long startTime = System.nanoTime();

        for (int i = 0; i < numThreads; i++) {

            final int threadIndex = i;

            threads[i] = new Thread(() -> {

                long hits = 0;

                for (long j = 0; j < pointsPerThread; j++) {

                    double x = ThreadLocalRandom.current().nextDouble();
                    double y = ThreadLocalRandom.current().nextDouble();

                    if (x * x + y * y <= 1.0) {
                        hits++;
                    }
                }

                localHits[threadIndex] = hits;
            });

            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        long totalHits = 0;

        for (long hits : localHits) {
            totalHits += hits;
        }

        long endTime = System.nanoTime();

        double pi = 4.0 * totalHits / TOTAL_POINTS;
        double runtimeMs = (endTime - startTime) / 1_000_000.0;

        System.out.println(
                numThreads + " threads"
                + " | Hits: " + totalHits
                + " | PI: " + pi
                + " | Runtime: " + runtimeMs + " ms"
        );

        return runtimeMs;
    }

    public static void main(String[] args) throws InterruptedException {

        int[] threadCounts = {1, 2, 4, 8, 16, 32};

        double[] runtimes = new double[threadCounts.length];

        System.out.println("=== OPENMP-STYLE REDUCTION ===");

        for (int i = 0; i < threadCounts.length; i++) {
            runtimes[i] = runBenchmark(threadCounts[i]);
        }

        double baseline = runtimes[0];

        System.out.println();
        System.out.println("Threads | Runtime(ms) | Speedup | Efficiency");
        System.out.println("--------------------------------------------");

        for (int i = 0; i < threadCounts.length; i++) {

            int threads = threadCounts[i];
            double runtime = runtimes[i];

            double speedup = baseline / runtime;
            double efficiency = (speedup / threads) * 100.0;

            System.out.printf(
                    "%7d | %11.3f | %7.2fx | %9.2f%%%n",
                    threads,
                    runtime,
                    speedup,
                    efficiency
            );
        }
    }
}