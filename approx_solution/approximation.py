import random
import time
import sys

def anytime_randomized_binpacking(items, bin_capacity, time_limit=1.0, rng=None):
    start = time.perf_counter()
    if rng is None:
        rng = random.Random()
    random.seed()

    best_bins = None
    best_num_bins = float("inf")

    while time.perf_counter() - start < time_limit:

        shuffled = items[:]
        rng.shuffle(shuffled)

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

    return best_bins

def main():
    if len(sys.argv) != 4:
        print("Usage: python approximation.py <input_file> <capacity> <time_limit>")
        return

    filename = sys.argv[1]
    capacity = int(sys.argv[2])
    time_limit = float(sys.argv[3])

    with open(filename, "r") as f:
        items = [int(x) for x in f.read().split()]

    result = anytime_randomized_binpacking(items, capacity, time_limit)

    print("Best solution uses", len(result), "bins.")
    # print("Remaining space per bin:", result)

if __name__ == "__main__":
    main()
