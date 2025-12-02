# test_binpacking.py
import time
import random
from approximation import anytime_randomized_binpacking


def generate_test_case(n_items, bin_capacity, min_size=1):
    """Generate a random test case."""
    return [random.randint(min_size, bin_capacity) for _ in range(n_items)]


def run_anytime_experiments(test_cases, bin_capacity, time_limits, repeats=5):
    """
    Run the anytime stochastic algorithm on multiple test cases.

    test_cases: list of item lists
    time_limits: list of floats, time limit per test case in seconds
    repeats: number of stochastic runs per test case
    """
    for idx, items in enumerate(test_cases):
        time_limit = time_limits[idx]
        print("=" * 70)
        print(f"TEST CASE {idx + 1}")
        print(f"Items: {len(items)}, Bin capacity: {bin_capacity}")
        print(f"Time limit for this test: {time_limit} seconds")
        print(f"Repeats per test: {repeats}")

        bin_counts = []
        run_times = []

        for r in range(repeats):
            start = time.perf_counter()
            rng = random.Random(1000 + r)

            bins = anytime_randomized_binpacking(
                items,
                bin_capacity,
                time_limit=time_limit,
                rng=rng
            )

            end = time.perf_counter()
            bin_counts.append(len(bins))
            run_times.append(end - start)

            print(f"  Run {r+1}: bins={len(bins)}, time={end-start:.4f}s")

        print("\n--- SUMMARY ---")
        print(f"Best solution:   {min(bin_counts)} bins")
        print(f"Worst solution:  {max(bin_counts)} bins")
        print(f"Average bins:    {sum(bin_counts)/len(bin_counts):.2f}")
        print(f"Avg runtime:     {sum(run_times)/len(run_times):.4f} sec\n")


if __name__ == "__main__":
    random.seed(420)
    BIN_CAPACITY = 100
    item_amount = 10000
    test_case = generate_test_case(item_amount, BIN_CAPACITY)
    test_cases = [
        test_case,
        test_case,
        test_case,
        test_case
    ]

    time_limits = [
        1,
        5,
        10,
        30
    ]

    run_anytime_experiments(test_cases, BIN_CAPACITY, time_limits, repeats=5)
