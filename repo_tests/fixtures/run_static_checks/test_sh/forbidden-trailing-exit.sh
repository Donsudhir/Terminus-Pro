#!/bin/bash

mkdir -p /logs/verifier
python -m pytest /tests/test_outputs.py -rA
RC=$?
if [ "$RC" -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi
exit "$RC"
