README — Anytime Randomized Bin Packing Algorithm
=================================================

1. Description
--------------
This project implements an anytime randomized algorithm for the classic
Bin Packing problem. Given a list of item sizes and a bin capacity, the
algorithm repeatedly generates randomized packings and keeps the best
solution found until a time limit expires.

2. Running Time Analysis
------------------------
Let:
  n = number of items
  B = number of bins created in a trial (worst case B = n)

In each iteration of the anytime loop:

  • We shuffle the items: O(n)
  • For each item, we scan all current bins to find the best fit:
        Worst-case: sum over all items of O(B) = O(n²)
  • Therefore one iteration costs:  O(n + n²) = O(n²)

If the time limit is T seconds and each iteration takes τ seconds,
the number of iterations performed is approximately k = T / τ.

Total running time:  O(k · n²)

Since τ increases with n, the relationship is approximately:

     Total time = O((T / n²) · n²) = O(T)

However, the **number of iterations** completed within the time limit
decreases quadratically as n increases.

3. Example Command Line
-----------------------
Assuming your main program is named:

    anytime_binpacking.py
and your test input file is:

    tests/sample1.txt

You can run the program as:

    python3 anytime_binpacking.py tests/sample1.txt 100 1.0

Which means:
    - Input file = tests/sample1.txt
    - Bin capacity = 100
    - Time limit = 1.0 seconds

4. Contents
-----------
• anytime_binpacking.py    — Main program
• test_driver.py           — Driver used for quick testing
• presentation.pdf         — Project presentation (included in submission)
• test_cases/              — Folder containing all test cases
• test_cases/run_test_cases.sh — Runs program on all test files
     - While running, the script prints which test cases exceed 60 minutes
       (none should, but the script contains the required markers).

5. Notes
--------
All code is written in Python and requires Python 3.8 or later.
