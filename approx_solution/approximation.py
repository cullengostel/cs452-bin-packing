import random
import time

def anytime_randomized_binpacking(items, bin_capacity, time_limit=1.0):
    start = time.perf_counter()
    best_bins = None
    best_num_bins = float("inf")

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

    return best_bins
