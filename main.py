"""
Algorithm Consultants Report
Logistics Company - Jamaica
Algorithms: Quick Sort + Binary Search
Dataset: GSA IOLP Leases (7,395 records)
"""

import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from tabulate import tabulate

# ─────────────────────────────────────────────
# LOAD REAL DATASET
# ─────────────────────────────────────────────

DATASET_PATH = "2026-6-5-iolp-leases.xlsx"

def load_dataset():
    """Load the GSA IOLP Leases dataset."""
    df = pd.read_excel(DATASET_PATH)
    return df

def get_sqft_list(df):
    """Return a clean list of Building Rentable Square Feet (integers)."""
    return df['Building Rentable Square Feet'].dropna().astype(int).tolist()

def get_lease_numbers(df):
    """Return list of lease number strings."""
    return df['Lease Number'].dropna().tolist()

# ─────────────────────────────────────────────
# QUICK SORT
# ─────────────────────────────────────────────

def quick_sort(arr):
    """
    Quick Sort using last element as pivot.
    Best/Avg: O(n log n)  |  Worst: O(n²)  |  Space: O(log n)
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left  = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x >  pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


# ─────────────────────────────────────────────
# BINARY SEARCH
# ─────────────────────────────────────────────

def binary_search(arr, target):
    """
    Iterative Binary Search on a SORTED array.
    Best: O(1)  |  Avg/Worst: O(log n)  |  Space: O(1)
    Returns index of target, or -1 if not found.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# ─────────────────────────────────────────────
# TIMING
# ─────────────────────────────────────────────

def measure_sort_time(data_subset):
    start = time.perf_counter()
    quick_sort(data_subset)
    return time.perf_counter() - start

def measure_search_time(sorted_data, target, runs=500):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        binary_search(sorted_data, target)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


# ─────────────────────────────────────────────
# MAIN DEMO
# ─────────────────────────────────────────────

def run_demo():
    print("=" * 65)
    print("  ALGORITHM CONSULTANTS — LOGISTICS COMPANY JAMAICA")
    print("  Dataset: GSA IOLP Federal Leases")
    print("=" * 65)

    # ── Load dataset ────────────────────────────────────────────
    print("\n[ LOADING DATASET ]")
    df = load_dataset()
    all_sqft = get_sqft_list(df)
    print(f"  Total records loaded : {len(df):,}")
    print(f"  Numeric values (sqft): {len(all_sqft):,}")

    # ── Small sample demo ───────────────────────────────────────
    sample = all_sqft[:10]
    print(f"\n[ STEP 1 ] Sample Building Sq Ft (first 10 records, unsorted):")
    print(f"  {sample}")

    sorted_sample = quick_sort(sample)
    print(f"\n[ STEP 2 ] After Quick Sort:")
    print(f"  {sorted_sample}")

    target = sorted_sample[5]
    idx = binary_search(sorted_sample, target)
    print(f"\n[ STEP 3 ] Binary Search for {target:,} sq ft:")
    print(f"  → Found at index {idx}")

    missing = 999999
    idx2 = binary_search(sorted_sample, missing)
    print(f"\n[ STEP 4 ] Binary Search for {missing:,} sq ft:")
    print(f"  → {'Found at index ' + str(idx2) if idx2 != -1 else 'Not found (-1)'}")

    # ── Timing across 3 dataset sizes ───────────────────────────
    sizes = [100, 1_000, min(10_000, len(all_sqft))]
    print("\n" + "=" * 65)
    print("  EXECUTION TIME MEASUREMENTS (from real lease dataset)")
    print("=" * 65)

    sort_times   = []
    search_times = []

    for size in sizes:
        subset = random.sample(all_sqft, size)
        st = measure_sort_time(subset)
        sort_times.append(st)

        sorted_subset = quick_sort(subset)
        search_target = sorted_subset[size // 2]
        se = measure_search_time(sorted_subset, search_target)
        search_times.append(se)

        print(f"\n  Dataset size : {size:,} records")
        print(f"  Quick Sort   : {st * 1000:.4f} ms")
        print(f"  Binary Search: {se * 1_000_000:.4f} µs")

    # ── Summary table ───────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  SUMMARY TABLE")
    print("=" * 65)
    table_data = [
        [f"{s:,}", f"{st*1000:.4f} ms", f"{se*1_000_000:.4f} µs"]
        for s, st, se in zip(sizes, sort_times, search_times)
    ]
    print(tabulate(table_data,
                   headers=["Dataset Size", "Quick Sort Time", "Binary Search Time"],
                   tablefmt="fancy_grid"))

    # ── Full dataset sort demo ───────────────────────────────────
    print("\n" + "=" * 65)
    print("  FULL DATASET SORT (all records)")
    print("=" * 65)
    start = time.perf_counter()
    sorted_all = quick_sort(all_sqft)
    full_time = time.perf_counter() - start
    print(f"  Sorted {len(sorted_all):,} records in {full_time*1000:.2f} ms")
    print(f"  Smallest building: {sorted_all[0]:,} sq ft")
    print(f"  Largest building : {sorted_all[-1]:,} sq ft")
    search_val = sorted_all[len(sorted_all)//2]
    full_idx = binary_search(sorted_all, search_val)
    print(f"  Binary search for median ({search_val:,} sq ft) → index {full_idx:,}")

    # ── Plots ───────────────────────────────────────────────────
    plot_results(sizes, sort_times, search_times, df)


# ─────────────────────────────────────────────
# PLOTTING
# ─────────────────────────────────────────────

def plot_results(sizes, sort_times, search_times, df):
    fig = plt.figure(figsize=(16, 11))
    fig.patch.set_facecolor("#0f172a")
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

    ACCENT  = "#38bdf8"
    ACCENT2 = "#f472b6"
    ACCENT3 = "#a78bfa"
    BG      = "#1e293b"
    TEXT    = "#e2e8f0"
    GRID    = "#334155"

    lkw = dict(color=TEXT, fontsize=9)
    tkw = dict(color=TEXT, fontsize=11, fontweight="bold", pad=8)

    sort_ms   = [t * 1_000       for t in sort_times]
    search_us = [t * 1_000_000   for t in search_times]
    size_labels = [f"{s:,}" for s in sizes]

    def style(ax):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT, labelsize=8)
        ax.yaxis.grid(True, color=GRID, linestyle="--", zorder=0)
        for sp in ax.spines.values(): sp.set_edgecolor(GRID)

    # Plot 1 — Quick Sort bar
    ax1 = fig.add_subplot(gs[0, 0])
    style(ax1)
    bars = ax1.bar(size_labels, sort_ms, color=ACCENT, width=0.5, zorder=3)
    for b, v in zip(bars, sort_ms):
        ax1.text(b.get_x()+b.get_width()/2, b.get_height()+max(sort_ms)*0.03,
                 f"{v:.3f}", ha="center", va="bottom", color=TEXT, fontsize=8)
    ax1.set_title("Quick Sort — Time (ms)", **tkw)
    ax1.set_xlabel("Records", **lkw); ax1.set_ylabel("ms", **lkw)

    # Plot 2 — Binary Search bar
    ax2 = fig.add_subplot(gs[0, 1])
    style(ax2)
    bars2 = ax2.bar(size_labels, search_us, color=ACCENT2, width=0.5, zorder=3)
    for b, v in zip(bars2, search_us):
        ax2.text(b.get_x()+b.get_width()/2, b.get_height()+max(search_us)*0.03,
                 f"{v:.4f}", ha="center", va="bottom", color=TEXT, fontsize=8)
    ax2.set_title("Binary Search — Time (µs)", **tkw)
    ax2.set_xlabel("Records", **lkw); ax2.set_ylabel("µs", **lkw)

    # Plot 3 — Growth comparison (normalised)
    ax3 = fig.add_subplot(gs[0, 2])
    style(ax3)
    x = list(range(len(sizes)))
    sn = [v/sort_ms[0]   for v in sort_ms]
    bn = [v/search_us[0] for v in search_us]
    ax3.plot(x, sn, color=ACCENT,  marker="o", lw=2.5, ms=8, label="Quick Sort",    zorder=3)
    ax3.plot(x, bn, color=ACCENT2, marker="s", lw=2.5, ms=8, label="Binary Search", zorder=3)
    ax3.set_xticks(x); ax3.set_xticklabels(size_labels)
    ax3.set_title("Growth Comparison (×)", **tkw)
    ax3.set_xlabel("Records", **lkw); ax3.set_ylabel("Relative time", **lkw)
    ax3.legend(facecolor=BG, labelcolor=TEXT, edgecolor=GRID, fontsize=8)

    # Plot 4 — Top 15 states by number of leases
    ax4 = fig.add_subplot(gs[1, 0:2])
    style(ax4)
    state_counts = df['State'].value_counts().head(15)
    ax4.barh(state_counts.index[::-1], state_counts.values[::-1],
             color=ACCENT3, zorder=3)
    ax4.set_title("Top 15 States by Number of Leases", **tkw)
    ax4.set_xlabel("Number of Leases", **lkw)
    ax4.xaxis.grid(True, color=GRID, linestyle="--", zorder=0)
    ax4.yaxis.grid(False)

    # Plot 5 — Distribution of building sizes
    ax5 = fig.add_subplot(gs[1, 2])
    style(ax5)
    sqft = df['Building Rentable Square Feet'].dropna()
    sqft_clipped = sqft[sqft < sqft.quantile(0.95)]   # remove extreme outliers for viz
    ax5.hist(sqft_clipped, bins=40, color=ACCENT, edgecolor=BG, zorder=3)
    ax5.set_title("Building Size Distribution\n(sq ft, 95th pct)", **tkw)
    ax5.set_xlabel("Sq Ft", **lkw); ax5.set_ylabel("Count", **lkw)

    fig.suptitle("Logistics Company Jamaica — Algorithm Performance Report\n"
                 "Dataset: GSA IOLP Federal Leases (7,395 records)",
                 color=TEXT, fontsize=13, fontweight="bold", y=1.01)

    plt.savefig("runtime_graphs.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print("\n  [✓] Graph saved as runtime_graphs.png")
    plt.show()


# ─────────────────────────────────────────────
if __name__ == "__main__":
    run_demo()