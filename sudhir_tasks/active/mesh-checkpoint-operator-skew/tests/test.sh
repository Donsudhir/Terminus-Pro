#!/bin/bash

# Verifier dependencies (including pytest-json-ctrf and transitive pins) are
# installed in the Dockerfile from the hash-locked verifier-requirements.txt —
# no network installs here.
#
# CM-007: run pytest from /tests with confcutdir + PYTHONSAFEPATH so a root
# agent cannot plant /app/pytest.py or /conftest.py and force reward=1.

mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
    echo 0 > /logs/verifier/reward.txt
    exit 1
fi

cd /tests && PYTHONSAFEPATH=1 python -m pytest -o cache_dir=/tmp/pytest_cache \
  --confcutdir=/tests \
  --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA

if [ $? -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi
