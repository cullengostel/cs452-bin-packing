#!/bin/bash

# Run tests on all cases
# The huge_test_case.txt is expected to take 60+ minutes

mkdir -p outputs

for f in *.txt; do
    name=$(basename "$f" .txt)
    output_file="outputs/${name}_output.txt"

    if [[ "$f" == "z_huge_test_case.txt" ]]; then
        # This test case will run for more than 60 minutes
        echo "Running $f (WARNING: 60+ mins expected)..."
        python ../reduction.py "$f" 130
    else
        echo "Running $f..."
        python ../reduction.py "$f" 20
    fi

    # Move the output to the outputs folder
    if [ -f "sat_output.txt" ]; then
        mv "sat_output.txt" "$output_file"
    fi
done
