Exact Bin Packing Solver
========================

Description:
-------------
This program implements an exact solver for the Bin Packing Problem using 
a backtracking approach. Given a set of items with integer sizes and a 
bin capacity, it finds the minimum number of bins required to pack all items 
without exceeding the bin capacity.

Time Complexity (O running time):
---------------------------------
- Let n = number of items, C = bin capacity.
- In the worst case, the algorithm explores every possible assignment of items 
  to bins. Each item can be placed either in an existing bin or a new bin.
- The total number of recursive calls is bounded by O(n!), because the solver 
  tries every permutation of item assignments to bins.
- Space complexity is O(n * k), where k is the number of bins in the current 
  best solution (worst case k = n).

Usage:
------
Command-line syntax:
    python exact_bin_packing.py <test_case.txt> <capacity> [time_limit_seconds]

Parameters:
    <test_case.txt>        Text file containing a single line of integers 
                           representing item sizes separated by spaces.
    <capacity>             Integer value specifying the capacity of each bin.
    [time_limit_seconds]   Optional: maximum allowed runtime in seconds.

Example:
--------
Suppose you have a test case file named "sample_input.txt" with contents:
    20 50 30 70 10 40

To solve this problem with a bin capacity of 100 and a time limit of 3600 seconds:
    python exact_bin_packing.py sample_input.txt 100 3600.0

Expected output:
    Test case: sample_input.txt
    Items: [20, 50, 30, 70, 10, 40]
    Capacity: 100
    Optimal bins: <minimum number of bins>
    Bin assignment: <list of bins with assigned items>
    Time: <runtime in seconds>

Batch Execution:
----------------
You can use the provided shell script `run_test_cases.sh` to run all test case 
files in a folder:

    ./run_test_cases.sh

This script will:
    - Iterate over all .txt files in the current folder
    - Call the solver with a specified capacity and time limit
    - Display runtime for each test case
    - Warn if any test case exceeds the 1-hour runtime threshold