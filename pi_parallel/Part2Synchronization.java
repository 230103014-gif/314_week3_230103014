import java.util.concurrent.ThreadLocalRandom;

public class Part2Synchronization {

    static long totalHits = 0;

    static final long TOTAL_POINTS = 50_000_000L;
    static final int NUM_THREADS = 4;

    public static synchronized void incrementHits() {
        totalHits++;
    }

    public static void runSynchronizedVersion() throws InterruptedException {

        totalHits = 0;

        long pointsPerThread = TOTAL_POINTS / NUM_THREADS;

        Thread[] threads = new Thread[NUM_THREADS];

        long startTime = System.nanoTime();

        for (int i = 0; i < NUM_THREADS; i++) {

            threads[i] = new Thread(() -> {

                for (long j = 0; j < pointsPerThread; j++) {

                    double x = ThreadLocalRandom.current().nextDouble();
                    double y = ThreadLocalRandom.current().nextDouble();

                    if (x * x + y * y <= 1.0) {
                        incrementHits();
                    }
                }
            });

            threads[i].start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        long endTime = System.nanoTime();

        double pi = 4.0 * totalHits / TOTAL_POINTS;
        double runtimeMs = (endTime - startTime) / 1_000_000.0;

        System.out.println("=== SYNCHRONIZED VERSION ===");
        System.out.println("Total hits: " + totalHits);
        System.out.println("Estimated PI: " + pi);
        System.out.println("Runtime: " + runtimeMs + " ms");
    }


    public static void runSingleThreadVersion() {

        long hits = 0;

        long startTime = System.nanoTime();

        for (long i = 0; i < TOTAL_POINTS; i++) {

            double x = ThreadLocalRandom.current().nextDouble();
            double y = ThreadLocalRandom.current().nextDouble();

            if (x * x + y * y <= 1.0) {
                hits++;
            }
        }

        long endTime = System.nanoTime();

        double pi = 4.0 * hits / TOTAL_POINTS;
        double runtimeMs = (endTime - startTime) / 1_000_000.0;

        System.out.println();
        System.out.println("=== SINGLE-THREADED VERSION ===");
        System.out.println("Total hits: " + hits);
        System.out.println("Estimated PI: " + pi);
        System.out.println("Runtime: " + runtimeMs + " ms");
    }


    public static void main(String[] args) throws InterruptedException {

        runSynchronizedVersion();
        runSingleThreadVersion();
    }
}