import random
import time
import sys
from multiprocessing import Pool, cpu_count, current_process

def single_trial(items, bin_capacity, verbose=False):
    shuffled = items[:]
    random.shuffle(shuffled)

    bins = []
    for item in shuffled:
        best_idx = -1
        min_space = bin_capacity + 1

        for i, space in enumerate(bins):
            if space >= item and (space - item) < min_space:
                best_idx = i
                min_space = space - item

        if best_idx == -1:
            bins.append(bin_capacity - item)
        else:
            bins[best_idx] -= item

    return bins


def anytime_randomized_parallel(items, bin_capacity, max_time, processes, verbose=False):
    print(f"Lower bound on bins needed: {sum(items) // bin_capacity + (1 if sum(items) % bin_capacity != 0 else 0)}")
    print(f"Total Items: {len(items)}")
    print(f"Using {processes} parallel processes")

    start = time.perf_counter()
    best_bins = None
    best_count = float("inf")

    pool = Pool(processes=processes)

    pending = [
        pool.apply_async(single_trial, (items, bin_capacity, verbose))
        for _ in range(processes)
    ]

    try:
        while time.perf_counter() - start < max_time:
            for i in range(processes):
                if pending[i].ready():
                    bins = pending[i].get()

                    if len(bins) < best_count:
                        best_count = len(bins)
                        best_bins = bins
                        if verbose:
                            print(f"[{time.perf_counter() - start:.3f}s] New best: {best_count} bins")

                    pending[i] = pool.apply_async(single_trial, (items, bin_capacity, verbose))

    except KeyboardInterrupt:
        print("\nUser interrupted execution early.")
        pool.terminate()
        pool.join()
        return best_bins

    pool.terminate()
    pool.join()
    return best_bins


def main():
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print("Usage:")
        print("  python approximation.py <input_file> <capacity> <time_limit> <processes> [verbose]")
        return

    filename = sys.argv[1]
    capacity = int(sys.argv[2])
    time_limit = float(sys.argv[3])
    processes = int(sys.argv[4])

    if processes < 1:
        print("Error: processes must be >= 1")
        return

    processes = min(processes, cpu_count())

    verbose = len(sys.argv) == 6 and sys.argv[5].lower() == "true"

    with open(filename, "r") as f:
        items = [int(x) for x in f.read().split()]

    start_time = time.perf_counter()
    result = anytime_randomized_parallel(items, capacity, time_limit, processes, verbose)
    end_time = time.perf_counter()

    if result is not None:
        print("\nBest solution uses", len(result), "bins")
        print("Remaining space in the bins:", sum(result))
    else:
        print("No solution found")

    print(f"Total runtime: {end_time - start_time:.3f} seconds")


if __name__ == "__main__":
    main()
