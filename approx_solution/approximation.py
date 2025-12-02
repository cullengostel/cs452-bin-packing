import random
import time
import sys

def anytime_randomized_binpacking(items, bin_capacity, time_limit=1.0, verbose=False):
    start = time.perf_counter()

    best_bins = None
    best_num_bins = float("inf")
    print(f"Lower bound on bins needed: {sum(items) // bin_capacity + (1 if sum(items) % bin_capacity != 0 else 0)}")

    try:
        while time.perf_counter() - start < time_limit:

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

            if len(bins) < best_num_bins:
                best_bins = bins
                best_num_bins = len(bins)

                if verbose:
                    current_time = time.perf_counter() - start
                    print(f"New best solution found: {best_num_bins} bins, remaining space {sum(best_bins)} at {current_time:.3f}s")

    except KeyboardInterrupt:
        # User stopped early
        print("\n*** Early termination detected! ***")

    return best_bins

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python approximation.py <input_file> <capacity> <time_limit> [verbose]")
        return

    filename = sys.argv[1]
    capacity = int(sys.argv[2])
    time_limit = float(sys.argv[3])
    verbose = len(sys.argv) == 5 and sys.argv[4].lower() == "true"

    with open(filename, "r") as f:
        items = [int(x) for x in f.read().split()]

    start_time = time.perf_counter()
    result = anytime_randomized_binpacking(items, capacity, time_limit, verbose)
    end_time = time.perf_counter()

    runtime = end_time - start_time

    if result is not None:
        print("Best solution uses", len(result), "bins.")
        print("Remaining space in the bins:", sum(result))
    else:
        print("No solution found before termination!")

    print(f"Total runtime: {runtime:.3f} seconds")

if __name__ == "__main__":
    main()
