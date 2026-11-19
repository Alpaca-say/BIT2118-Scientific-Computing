#!/usr/bin/env bash
# Re-runs every program from the code/ folder and refreshes outputs/ and figures/
set -e
cd "$(dirname "$0")/code"
export MPLBACKEND=Agg
mkdir -p ../outputs ../figures
for f in Task_*.py; do
  echo "Running $f"
  python3 "$f" > "../outputs/${f%.py}_output.txt" 2>&1
done
echo "Done. See ../outputs and ../figures"
