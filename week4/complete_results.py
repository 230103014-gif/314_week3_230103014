import csv
from pathlib import Path

path = Path("results.csv")

with path.open(newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    columns = list(reader.fieldnames)

def measured_time(row):
    return (float(row["run2_s"]) + float(row["run3_s"])) / 2

baseline = next(r for r in rows if r["experiment"] == "baseline")
two_threads = next(
    r for r in rows if r["experiment"] == "scaling" and r["threads"] == "2"
)
reduction = next(
    r for r in rows if r["experiment"] == "false_sharing"
    and r["setting"] == "reduction"
)

t_seq = measured_time(baseline)
p = 2 * (1 - measured_time(two_threads) / t_seq)

extra = [
    "empirical_speedup", "theoretical_speedup", "reality_gap",
    "throughput_iter_s", "time_ratio_vs_reduction"
]
columns += [name for name in extra if name not in columns]

for row in rows:
    for name in extra:
        row[name] = ""

    t = measured_time(row)

    if row["experiment"] == "scaling":
        k = int(row["threads"])
        empirical = t_seq / t
        theoretical = 1 / ((1 - p) + p / k)
        row["empirical_speedup"] = f"{empirical:.4f}"
        row["theoretical_speedup"] = f"{theoretical:.4f}"
        row["reality_gap"] = f"{theoretical - empirical:.4f}"

    if row["experiment"] == "false_sharing":
        row["throughput_iter_s"] = f"{13014000 / t:.0f}"
        row["time_ratio_vs_reduction"] = (
            f"{t / measured_time(reduction):.4f}"
        )

with path.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print("Added calculated columns to results.csv")