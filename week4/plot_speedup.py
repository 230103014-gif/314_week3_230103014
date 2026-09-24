import csv
import matplotlib.pyplot as plt

with open("results.csv", newline="") as file:
    rows = list(csv.DictReader(file))

def average(row):
    return (float(row["run2_s"]) + float(row["run3_s"])) / 2

baseline = next(row for row in rows if row["experiment"] == "baseline")
scaling = sorted(
    (row for row in rows if row["experiment"] == "scaling"),
    key=lambda row: int(row["threads"]),
)

t_seq = average(baseline)
threads = [int(row["threads"]) for row in scaling]
empirical = [t_seq / average(row) for row in scaling]

p = 2 * (1 - average(scaling[1]) / t_seq)
theoretical = [1 / ((1 - p) + p / k) for k in threads]
ideal = threads

plt.figure(figsize=(8, 5))
plt.plot(threads, empirical, "o-", linewidth=2, label="Measured speedup")
plt.plot(threads, theoretical, "s--", linewidth=2, label="Amdahl prediction")
plt.plot(threads, ideal, ":", linewidth=2, label="Linear ideal")
plt.xticks(threads)
plt.xlabel("Number of threads")
plt.ylabel("Speedup vs sequential baseline")
plt.title("Collatz speedup on MacBookPro17,1")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("speedup_plot.png", dpi=300)
print("Saved speedup_plot.png")