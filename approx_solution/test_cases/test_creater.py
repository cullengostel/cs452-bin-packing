import random


for i in range(50):
    filename = f"test_cases/approximate_case_{i+1}.txt"
    num_items = random.randint(750, 5000)
    items = [random.randint(0, 100) for _ in range(num_items)]
    with open(filename, "w") as f:
        f.write(" ".join(map(str, items)) + "\n")

# print(f"Lower bound on bins needed: {sum(items) // 100 + (1 if sum(items) % 100 != 0 else 0)}")
# print(f"Test case saved to {filename}")
