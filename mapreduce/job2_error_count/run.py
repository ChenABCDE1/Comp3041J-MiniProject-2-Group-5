#!/usr/bin/env python3
"""
Job 2 Execution Script: Server Error Count by Service
"""

import subprocess
import sys
import os
import time


def run_local_pipeline(input_file, output_file):
    """Execute Job 2 MapReduce pipeline locally."""
    print("=" * 60)
    print("Job 2: Server Error Count by Service")
    print("=" * 60)

    start_time = time.time()

    # Mapper
    print("\n[1/3] Running Mapper (filtering status_code >= 500)...")
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

    # Save
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(reducer_result.stdout)

    elapsed = time.time() - start_time

    print(f"\n{'=' * 60}")
    print("Job 2 Completed Successfully")
    print(f"{'=' * 60}")
    print(f"Runtime: {elapsed:.3f} seconds")
    print(f"\nOutput preview:")
    print(reducer_result.stdout[:500])


if __name__ == '__main__':
    INPUT_FILE = '../../data/cloud_service_logs.csv'
    OUTPUT_FILE = '../outputs/error_count.txt'

    run_local_pipeline(INPUT_FILE, OUTPUT_FILE)