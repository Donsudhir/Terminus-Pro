#!/bin/bash

mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt
if [ "$PWD" = "/" ]; then
    echo 0 > /logs/verifier/reward.txt
    exit 1
fi

cd /tests && PYTHONSAFEPATH=1 python -m pytest --confcutdir=/tests \
    --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
status="$?"
if [ "${status}" -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
else
    echo "0" > /logs/verifier/reward.txt
fi
