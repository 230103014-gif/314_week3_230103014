import csv
import matplotlib.pyplot as plt


threads = []
speedup = []
efficiency = []

with open("scaling_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        threads.append(int(row["Threads"]))
        speedup.append(float(row["Speedup"]))
        efficiency.append(float(row["Efficiency"]))


# -----------------------------
# Speedup vs Ideal Speedup
# -----------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    speedup,
    marker="o",
    label="Measured Speedup"
)

plt.plot(
    threads,
    threads,
    marker="o",
    linestyle="--",
    label="Ideal Linear Speedup"
)

plt.xlabel("Number of Threads (P)")
plt.ylabel("Speedup S(P)")
plt.title("Parallel Reduction: Measured vs Ideal Speedup")

plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("speedup_graph.png", dpi=200)

plt.close()


# -----------------------------
# Parallel Efficiency
# -----------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    efficiency,
    marker="o"
)

plt.xlabel("Number of Threads (P)")
plt.ylabel("Parallel Efficiency E(P)")
plt.title("Parallel Efficiency")

plt.xticks(threads)
plt.grid(True)
plt.tight_layout()

plt.savefig("efficiency_graph.png", dpi=200)

plt.close()


print("Graphs saved:")
print("  speedup_graph.png")
print("  efficiency_graph.png")