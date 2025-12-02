# exact_bin_packing.py
import sys
import time

class ExactBinPacking:
    def __init__(self, capacity):
        self.capacity = capacity
        self.best_bins = None
        self.best_k = float('inf')

    def solve(self, items, time_limit=None):
        start_time = time.time()
        n = len(items)
        self.best_bins = None
        self.best_k = float('inf')

        def backtrack(index, bins):
            nonlocal start_time

            if time_limit and (time.time() - start_time) > time_limit:
                raise TimeoutError("Time limit exceeded")

            if index == n:
                if len(bins) < self.best_k:
                    self.best_k = len(bins)
                    self.best_bins = [b[:] for b in bins]
                return

            x = items[index]

            # Try placing in existing bins
            for i in range(len(bins)):
                if sum(bins[i]) + x <= self.capacity:
                    bins[i].append(x)
                    backtrack(index + 1, bins)
                    bins[i].pop()

            # Try placing in a new bin
            bins.append([x])
            backtrack(index + 1, bins)
            bins.pop()

        try:
            backtrack(0, [])
        except TimeoutError:
            pass

        return self.best_k, self.best_bins, time.time() - start_time

# ------------------------------
# Command-line usage
# ------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exact_bin_packing.py <test_case.txt> <capacity> [time_limit_seconds]")
        sys.exit(1)

    test_case_file = sys.argv[1]
    capacity = int(sys.argv[2])
    time_limit = float(sys.argv[3]) if len(sys.argv) > 3 else None

    # Read items
    with open(test_case_file) as f:
        items = list(map(int, f.readline().split()))

    solver = ExactBinPacking(capacity)
    k, bins, t = solver.solve(items, time_limit=time_limit)

    print(f"Test case: {test_case_file}")
    print(f"Items: {items}")
    print(f"Capacity: {capacity}")
    print(f"Optimal bins: {k}")
    print(f"Bin assignment: {bins}")
    print(f"Time: {t:.3f}s")
