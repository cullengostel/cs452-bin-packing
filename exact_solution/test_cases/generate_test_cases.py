# generate_test_cases.py
import os
import random

NUM_CASES = 60       # number of test cases to generate
N_MIN = 8            # minimum number of items
N_MAX = 20           # maximum number of items
ITEM_MAX = 100       # maximum item size
OUT_DIR = "."        # write .txt files in the current folder
SEED = 42            # random seed for reproducibility

random.seed(SEED)

for i in range(NUM_CASES):
    n = random.randint(N_MIN, N_MAX)
    # mix of small and large items
    if random.random() < 0.6:
        items = [random.randint(1, ITEM_MAX) for _ in range(n)]
    else:
        items = [random.randint(ITEM_MAX // 2, ITEM_MAX) for _ in range(max(1, n // 4))]
        items += [random.randint(1, ITEM_MAX // 2) for _ in range(n - len(items))]
        random.shuffle(items)

    case_name = f"case_{i+1:03d}.txt"
    with open(os.path.join(OUT_DIR, case_name), "w") as f:
        f.write(" ".join(map(str, items)) + "\n")

print(f"Generated {NUM_CASES} test cases in '{OUT_DIR}/'")
