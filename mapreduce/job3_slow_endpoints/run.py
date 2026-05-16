#!/usr/bin/env python3
"""
Job 3 Execution Script: Top 10 Slow Endpoints
"""

import subprocess
import sys
import os
import time


def run_local_pipeline(input_file, output_file, top10_file):
    """Execute Job 3 MapReduce pipeline and extract Top 10."""
    print("=" * 60)
    print("Job 3: Top 10 Slow Endpoints")
    print("=" * 60)

    start_time = time.time()

    # Mapper
    print("\n[1/3] Running Mapper (filtering response_time > 800ms)...")
    with open(input_file, 'r') as f:
        mapper_result = subprocess.run(
            [sys.executable, 'mapper.py'],
            stdin=f,
            capture_output=True,
            text=True
        )

    if mapper_result.returncode != 0:
        print(f"Mapper error: {mapper_result.stderr}")
        return

    # Sort
    print("[2/3] Sorting...")
    sorted_lines = sorted(mapper_result.stdout.strip().split('\n'))

    # Reducer
    print("[3/3] Running Reducer...")
    reducer_input = '\n'.join(sorted_lines)
    reducer_result = subprocess.run(
        [sys.executable, 'reducer.py'],
        input=reducer_input,
        capture_output=True,
        text=True
    )

    if reducer_result.returncode != 0:
        print(f"Reducer error: {reducer_result.stderr}")
        return

    # Save full output
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(reducer_result.stdout)

    # Extract Top 10
    lines = reducer_result.stdout.strip().split('\n')
    # Sort by count (second column, tab-separated) descending
    sorted_by_count = sorted(
        lines,
        key=lambda x: int(x.split('\t')[1]) if '\t' in x else 0,
        reverse=True
    )
    top10 = sorted_by_count[:10]

    with open(top10_file, 'w') as f:
        f.write('\n'.join(top10) + '\n')

    elapsed = time.time() - start_time

    print(f"\n{'=' * 60}")
    print("Job 3 Completed Successfully")
    print(f"{'=' * 60}")
    print(f"Full output:  {output_file}")
    print(f"Top 10 file:  {top10_file}")
    print(f"Runtime:      {elapsed:.3f} seconds")
    print(f"\nTop 10 Slow Endpoints:")
    print("-" * 60)
    for line in top10:
        endpoint, count = line.split('\t')
        print(f"  {endpoint:45s} {count:>6s}")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    INPUT_FILE = '../../data/cloud_service_logs.csv'
    OUTPUT_FILE = '../outputs/slow_endpoints_full.txt'
    TOP10_FILE = '../outputs/top10_slow_endpoints.txt'

    run_local_pipeline(INPUT_FILE, OUTPUT_FILE, TOP10_FILE)