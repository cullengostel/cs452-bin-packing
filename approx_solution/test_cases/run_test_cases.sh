#!/bin/bash
# Run all test cases for the Anytime Bin Packing project
# ------------------------------------------------------
# REQUIRED BY SPEC:
# Label which test case (if any) runs more than 60 minutes.

#!/bin/bash

PROGRAM="approximation.py"
CAPACITY=100
TIME_LIMIT=1.0

echo "Running all test cases..."

for f in test_cases/*.txt
do
    echo "--------------------------------------------"
    echo "Running test case: $f"
    echo "Command: python $PROGRAM $f $CAPACITY $TIME_LIMIT"
    python $PROGRAM "$f" $CAPACITY $TIME_LIMIT

done
