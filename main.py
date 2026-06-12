"""
Algorithm Consultants Report - Logistics Company Jamaica
Algorithms: Quick Sort + Binary Search
Datasets: GSA IOLP Leases + Logistics Shipment Records (100,000)
"""

import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# ── Load Datasets ─────────────────────────────────────────────

def load_dataset():
    """Load GSA IOLP Leases dataset."""
    return pd.read_excel("2026-6-5-iolp-leases.xlsx")

def load_logistics():
    """Load Logistics shipment dataset (100,000 records)."""
    return pd.read_excel("Logistics-dataset.xlsx")

def get_sqft_list(df):
    return df['Building Rentable Square Feet'].dropna().astype(int).tolist()

def get_lease_numbers(df):
    return df['Lease Number'].dropna().tolist()

def get_shipment_weights(log_df):
    """Return shipment weights — used as the sort/search values."""
    return log_df['Weight_in_gms'].dropna().astype(int).tolist()

def get_shipment_ids(log_df):
    return log_df['ID'].dropna().astype(int).tolist()

# ── Quick Sort ────────────────────────────────────────────────

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left  = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x >  pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

# ── Binary Search ─────────────────────────────────────────────

def binary_search(arr, target):
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

# ── Timing ────────────────────────────────────────────────────

def measure_sort_time(data):
    start = time.perf_counter()
    quick_sort(data)
    return time.perf_counter() - start

def measure_search_time(sorted_data, target, runs=500):
    start = time.perf_counter()
    for _ in range(runs):
        binary_search(sorted_data, target)
    return (time.perf_counter() - start) / runs

# ── Plotting ──────────────────────────────────────────────────

def plot_results(sizes, sort_times, search_times, lease_df, log_df):
    sort_ms   = [t * 1000    for t in sort_times]
    search_us = [t * 1000000 for t in search_times]
    labels    = [f"{s:,}"    for s in sizes]

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.patch.set_facecolor("#0f172a")
    fig.suptitle("Logistics Company Jamaica — Algorithm Performance\n"
                 "Datasets: GSA IOLP Leases + Shipment Records (100,000)",
                 color="#e2e8f0", fontsize=13, fontweight="bold")

    def style(ax, xgrid=False):
        ax.set_facecolor("#1e293b")
        ax.tick_params(colors="#e2e8f0", labelsize=8)
        ax.yaxis.grid(True, color="#334155", linestyle="--")
        if xgrid:
            ax.xaxis.grid(True, color="#334155", linestyle="--")
        ax.yaxis.grid(xgrid, color="#334155", linestyle="--")
        for sp in ax.spines.values():
            sp.set_edgecolor("#334155")

    def label(ax, title, xlabel, ylabel):
        ax.set_title(title, color="#e2e8f0", fontweight="bold", pad=8)
        ax.set_xlabel(xlabel, color="#e2e8f0", fontsize=9)
        ax.set_ylabel(ylabel, color="#e2e8f0", fontsize=9)

    # Row 1: Algorithm timing charts

    # Quick Sort bar
    ax = axes[0][0]; style(ax)
    bars = ax.bar(labels, sort_ms, color="#38bdf8", width=0.5)
    for b, v in zip(bars, sort_ms):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()*1.02, f"{v:.2f}",
                ha="center", va="bottom", color="#e2e8f0", fontsize=8)
    label(ax, "Quick Sort — Time (ms)", "Records", "ms")

    # Binary Search bar
    ax = axes[0][1]; style(ax)
    bars = ax.bar(labels, search_us, color="#f472b6", width=0.5)
    for b, v in zip(bars, search_us):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()*1.02, f"{v:.4f}",
                ha="center", va="bottom", color="#e2e8f0", fontsize=8)
    label(ax, "Binary Search — Time (µs)", "Records", "µs")

    # Growth comparison
    ax = axes[0][2]; style(ax)
    ax.plot(labels, [v/sort_ms[0]   for v in sort_ms],   color="#38bdf8", marker="o", lw=2, label="Quick Sort")
    ax.plot(labels, [v/search_us[0] for v in search_us], color="#f472b6", marker="s", lw=2, label="Binary Search")
    ax.legend(facecolor="#1e293b", labelcolor="#e2e8f0", edgecolor="#334155", fontsize=8)
    label(ax, "Growth Comparison (×)", "Records", "Relative time")

    # Row 2: Dataset insight charts

    # Shipment mode breakdown (Logistics dataset)
    ax = axes[1][0]; style(ax)
    mode_counts = log_df['Mode_of_Shipment'].value_counts()
    ax.bar(mode_counts.index, mode_counts.values, color="#a78bfa", width=0.5)
    label(ax, "Shipments by Mode", "Mode", "Count")

    # Weight distribution (Logistics dataset)
    ax = axes[1][1]; style(ax)
    weights = log_df['Weight_in_gms'].dropna()
    ax.hist(weights, bins=50, color="#38bdf8", edgecolor="#0f172a")
    label(ax, "Shipment Weight Distribution (g)", "Weight (g)", "Count")

    # On-time delivery rate by warehouse (Logistics dataset)
    ax = axes[1][2]; style(ax, xgrid=True)
    on_time = log_df.groupby('Warehouse_block')['Reached.on.Time_Y.N'].mean() * 100
    ax.barh(on_time.index, on_time.values, color="#f472b6")
    label(ax, "On-Time Delivery % by Warehouse", "% On Time", "Warehouse")

    plt.tight_layout()
    plt.savefig("runtime_graphs.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print("\n  [✓] Graph saved as runtime_graphs.png")
    plt.show()

# ── Main Demo ─────────────────────────────────────────────────

def run_demo():
    print("=" * 65)
    print("  ALGORITHM CONSULTANTS — LOGISTICS COMPANY JAMAICA")
    print("=" * 65)

    # Load both datasets
    lease_df = load_dataset()
    log_df   = load_logistics()
    weights  = get_shipment_weights(log_df)

    print(f"\n  Lease records loaded   : {len(lease_df):,}")
    print(f"  Shipment records loaded: {len(log_df):,}")

    # Small sample demo using shipment weights
    sample        = weights[:10]
    sorted_sample = quick_sort(sample)
    print(f"\n[ STEP 1 ] Sample shipment weights (g), unsorted: {sample}")
    print(f"[ STEP 2 ] After Quick Sort:                       {sorted_sample}")

    target = sorted_sample[5]
    print(f"\n[ STEP 3 ] Binary Search for {target:,}g → index {binary_search(sorted_sample, target)}")
    print(f"[ STEP 4 ] Binary Search for 9,999,999g  → {binary_search(sorted_sample, 9999999)}")

    # Timing across 1,000 / 10,000 / 100,000 (full assignment range)
    sizes = [1_000, 10_000, 100_000]
    sort_times, search_times = [], []

    print(f"\n{'=' * 65}")
    print("  TIMING — Shipment Weight Sort & Search")
    print(f"{'=' * 65}")

    for size in sizes:
        subset        = random.sample(weights, size)
        st            = measure_sort_time(subset)
        sorted_subset = quick_sort(subset)
        se            = measure_search_time(sorted_subset, sorted_subset[size // 2])
        sort_times.append(st)
        search_times.append(se)
        print(f"  {size:>7,} records | Sort: {st*1000:>8.3f} ms | Search: {se*1000000:.4f} µs")

    # Summary table
    print("\n" + tabulate(
        [[f"{s:,}", f"{st*1000:.3f} ms", f"{se*1000000:.4f} µs"]
         for s, st, se in zip(sizes, sort_times, search_times)],
        headers=["Dataset Size", "Quick Sort", "Binary Search"],
        tablefmt="fancy_grid"
    ))

    # Full 100k dataset insight
    sorted_all = quick_sort(weights)
    median     = sorted_all[len(sorted_all) // 2]
    print(f"\n  Full shipment dataset ({len(sorted_all):,} records):")
    print(f"  Lightest: {sorted_all[0]:,}g | Heaviest: {sorted_all[-1]:,}g")
    print(f"  Median weight: {median:,}g → index {binary_search(sorted_all, median):,}")

    plot_results(sizes, sort_times, search_times, lease_df, log_df)


if __name__ == "__main__":
    run_demo()