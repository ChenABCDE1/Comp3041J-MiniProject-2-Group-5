#!/usr/bin/env python3
"""
Job 2 Execution Script: Server Error Count by Service
"""

import subprocess
import sys
import os
import time


def run_local_pipeline():
    """Execute Job 2 MapReduce pipeline locally."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    mapper_path = os.path.join(script_dir, 'mapper.py')
    reducer_path = os.path.join(script_dir, 'reducer.py')

    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'data', 'Comp3041J MiniProject 2 Dataset.csv')

    outputs_dir = os.path.join(os.path.dirname(script_dir), 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    output_file = os.path.join(outputs_dir, 'error_count.txt')

    print("=" * 60)
    print("Job 2: Server Error Count by Service")
    print("=" * 60)
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")

    if not os.path.exists(input_file):
        print(f"\nERROR: Input file not found: {input_file}")
        return

    start_time = time.time()

    # Mapper
    print("\n[1/3] Running Mapper (filtering status_code >= 500)...")
    with open(input_file, 'r', encoding='utf-8') as f:
        mapper_result = subprocess.run(
            [sys.executable, mapper_path],
            stdin=f,
            capture_output=True,
            text=True
        )

    if mapper_result.returncode != 0:
        print(f"Mapper error: {mapper_result.stderr}")
        return

    # Sort
    print("[2/3] Sorting...")
    sorted_lines = sorted([line for line in mapper_result.stdout.strip().split('\n') if line.strip()])

    # Reducer
    print("[3/3] Running Reducer...")
    reducer_input = '\n'.join(sorted_lines)
    reducer_result = subprocess.run(
        [sys.executable, reducer_path],
        input=reducer_input,
        capture_output=True,
        text=True
    )

    if reducer_result.returncode != 0:
        print(f"Reducer error: {reducer_result.stderr}")
        return

    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reducer_result.stdout)

    elapsed = time.time() - start_time

    print(f"\n{'=' * 60}")
    print("Job 2 Completed Successfully")
    print(f"{'=' * 60}")
    print(f"Runtime: {elapsed:.3f} seconds")
    print(f"\nOutput preview:")
    print(reducer_result.stdout[:800])


if __name__ == '__main__':
    run_local_pipeline()