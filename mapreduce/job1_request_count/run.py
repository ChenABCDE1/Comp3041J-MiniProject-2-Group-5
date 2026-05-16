#!/usr/bin/env python3
"""
Job 1 Execution Script (Windows-compatible)
Runs mapper and reducer locally for testing and development.
For Hadoop cluster deployment, use Hadoop Streaming commands.
"""

import subprocess
import sys
import os
import time


def run_local_pipeline(input_file, output_file):
    """
    Execute MapReduce pipeline locally using stdin/stdout piping.
    Simulates Hadoop Streaming behavior for testing.
    """
    print("=" * 60)
    print("Job 1: Request Count by Service")
    print("=" * 60)

    start_time = time.time()

    # Step 1: Run mapper
    print("\n[1/3] Running Mapper...")
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

    # Step 2: Sort (simulates Hadoop shuffle phase)
    print("[2/3] Sorting (Shuffle phase simulation)...")
    sorted_lines = sorted(mapper_result.stdout.strip().split('\n'))

    # Step 3: Run reducer
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

    # Save output
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(reducer_result.stdout)

    elapsed = time.time() - start_time

    print(f"\n{'=' * 60}")
    print("Job 1 Completed Successfully")
    print(f"{'=' * 60}")
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print(f"Runtime:     {elapsed:.3f} seconds")
    print(f"\nOutput preview:")
    print(reducer_result.stdout[:500])
    print(f"{'=' * 60}")


if __name__ == '__main__':
    # Configuration
    INPUT_FILE = '../../data/cloud_service_logs.csv'
    OUTPUT_FILE = '../outputs/request_count.txt'

    run_local_pipeline(INPUT_FILE, OUTPUT_FILE)