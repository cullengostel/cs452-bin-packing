Bin Packing to MAX-3-SAT Reduction
==================================

Algorithm Description
---------------------
This program reduces the Bin Packing Problem (fitting n items into m bins of capacity C) to the 3-SAT problem (satisfiability of boolean formulas).

The reduction works as follows:
1.  Variables: For each item i (0..n-1) and bin j (0..m-1), we create a boolean variable x_{i,j} which is true if item i is placed in bin j.
2.  Placement Constraints:
    *   Each item must be in at least one bin: (x_{i,0} v x_{i,1} v ... v x_{i,m-1}).
    *   Each item must be in at most one bin: For every pair of bins j1, j2, (-x_{i,j1} v -x_{i,j2}).
3.  Capacity Constraints:
    *   For each bin j, we construct a digital logic circuit (using AND/OR/XOR gates) to sum the sizes of items placed in that bin.
    *   We use a tree of binary adders to compute the sum.
    *   We compare the sum to the Capacity C using a digital comparator.
    *   The logic gates are converted to CNF clauses using the Tseitin transformation.

Running Time Analysis (Big-O)
-----------------------------
Let:
*   n = Number of items
*   m = Number of bins (typically approx Sum_Items / Capacity)
*   L = Number of bits required to represent the Capacity C (log2(C))

The complexity is determined by the number of clauses generated:
*   Time Complexity: O(n * m^2 + n * m * L)

Breakdown:
1.  Uniqueness Constraints: There are n items. Each item has constraints for every pair of bins.
    *   Clauses: n * m * (m-1) / 2  =>  O(n * m^2)
2.  Capacity Constraints: There are m bins. For each bin, we build an adder circuit for n items of L bits.
    *   Adder Circuit Size: O(n * L) gates per bin.
    *   Clauses: O(m * n * L)

In the worst case where m is close to n (e.g., small capacity), the complexity is O(n^3).

Clause Bounds
-------------
Let K be a small constant representing clauses per logic gate (~10).

*   Lower Bound: n (each item in >= 1 bin)
*   Upper Bound: n*m^2 + K*m*n*L

Usage Example
-------------
To run the reduction on a sample input file:

    python reduced_solution.py <input> <capacity> <num_bins>

Where:
*   <input> is the path to a file containing the space separated integer sizes.
*   <capacity> is an integer representing the capacity of the bins.
*   <num_bins> is the number of bins to work with. If blank, it will automatically use the calculated lower bound.

Example:
    python reduced_solution.py ./test_cases/case_0_10.txt 20 100

The program will output the generated 3-SAT instance to sat_output.txt in DIMACS format.