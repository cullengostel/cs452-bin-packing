#!/bin/bash
# Run all test cases for the Anytime Bin Packing project
# ------------------------------------------------------
# REQUIRED BY SPEC:
# Label which test case (if any) runs more than 60 minutes.

PROGRAM="approximation.py"
CAPACITY=100
TIME_LIMIT=1.0

echo "Running all test cases..."

for f in test_cases/*.txt
do
    echo "--------------------------------------------"
    echo "Running test case: $f"
    echo "Command: python $PROGRAM $f $CAPACITY $TIME_LIMIT"

    start=$(date +%s)
    python $PROGRAM "$f" $CAPACITY $TIME_LIMIT
    end=$(date +%s)

    runtime=$((end - start))

    echo "Runtime: ${runtime}s"

    # REQUIRED COMMENT:
    if [ "$runtime" -gt 3600 ]; then
        echo "# WARNING: This test case exceeds 60 minutes runtime"
        echo "# (Required note for project spec)"
    fi
done
