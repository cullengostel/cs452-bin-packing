#!/bin/bash
PROGRAM="../exact_bin_packing.py"  # parent folder
CAPACITY=100
TIME_LIMIT=3600.0

echo "Running all test cases..."

# Loop over each .txt file in this folder
for f in ./*.txt; do
    [ -e "$f" ] || continue  # skip if no files
    echo "--------------------------------------------"
    echo "Running test case: $f"
    echo "Command: python $PROGRAM $f $CAPACITY $TIME_LIMIT"

    start=$(date +%s)
    python "$PROGRAM" "$f" $CAPACITY $TIME_LIMIT
    end=$(date +%s)

    runtime=$((end - start))
    echo "Runtime: ${runtime}s"

    if [ "$runtime" -gt 3600 ]; then
        echo "# WARNING: This test case exceeds 60 minutes runtime"
    fi
done
