# Bin Packing to MAX-3-SAT Reduction

## Time Complexity
The reduction runs in **Polynomial Time** in the input bit-length.

Specifically: O(m * n * L + n * m^2) where:
- n = number of items
- m = number of bins  
- L = ceil(log2(C+1)) = number of bits to represent capacity

Since L = O(log C) is bounded by the input bit-length, this is truly polynomial.

**Variable count**: O(n*m + m*n*L) = O(m*n*L)
**Clause count**: O(m*n*L + n*m^2)

## Bounds Calculation
The program automatically calculates the **Theoretical Lower Bound** (`ceil(total_size / capacity)`) and uses this as the default number of bins to check. This represents the minimum possible bins if items were "liquid". Note that due to fragmentation (items are solid), the actual minimum might be higher.

## Usage
**Syntax**:
```bash
python reduced_solution.py <input_file> <capacity> [num_bins]
```

- `input_file`: File containing space-separated item sizes (integers only).
- `capacity`: The bin capacity (integer).
- `num_bins` (Optional): The specific number of bins to check. If omitted, defaults to the calculated lower bound.

**Examples**:

1. **Optimization Check** (Uses calculated lower bound):
   ```bash
   python reduced_solution.py items_only.txt 6
   ```

2. **Decision Check** (Check if it fits in exactly 3 bins):
   ```bash
   python reduced_solution.py items_only.txt 6 3
   ```

## Input Format (Item File)
The input file should contain only the item sizes (space or newline separated).

Example (`items_only.txt`):
```
5 3 6 5 4
```

## Output Format
The program creates a file named `sat_output.txt` containing the MAX-3-SAT instance in standard DIMACS format:
- First line: `<number of variables> <number of clauses>`
- Subsequent lines: `<literal1> <literal2> <literal3>` (integers, negative = negation)

Example output header:
```
235 715
1 2 3
-1 -2 -2
...
```
