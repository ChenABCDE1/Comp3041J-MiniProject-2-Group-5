#!/usr/bin/env python3
"""
Job 1 Execution Script (Windows-compatible)
Runs mapper and reducer locally for testing.
"""

import subprocess
import sys
import os
import time


def run_local_pipeline():
    """
    Execute MapReduce pipeline locally.
    Uses absolute paths to avoid working directory issues.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build absolute paths
    mapper_path = os.path.join(script_dir, 'mapper.py')
    reducer_path = os.path.join(script_dir, 'reducer.py')

    # Data file path (go up two levels to project root, then into data/)
    project_root = os.path.dirname(os.path.dirname(script_dir))
    input_file = os.path.join(project_root, 'data', 'Comp3041J MiniProject 2 Dataset.csv')

    # Output path
    outputs_dir = os.path.join(os.path.dirname(script_dir), 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    output_file = os.path.join(outputs_dir, 'request_count.txt')

    print("=" * 60)
    print("Job 1: Request Count by Service")
    print("=" * 60)
    print(f"Script directory: {script_dir}")
    print(f"Input file:       {input_file}")
    print(f"Output file:      {output_file}")

    # Verify files exist
    if not os.path.exists(input_file):
        print(f"\nERROR: Input file not found: {input_file}")
        print("Please ensure the dataset is in the data/ folder.")
        return

    if not os.path.exists(mapper_path):
        print(f"\nERROR: Mapper not found: {mapper_path}")
        return

    start_time = time.time()

    # Step 1: Run mapper
    print("\n[1/3] Running Mapper...")
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

    # Step 2: Sort (simulates Hadoop shuffle)
    print("[2/3] Sorting (Shuffle phase)...")
    mapper_lines = mapper_result.stdout.strip().split('\n')
    # Filter empty lines and sort
    sorted_lines = sorted([line for line in mapper_lines if line.strip()])

    # Step 3: Run reducer
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

    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reducer_result.stdout)

    elapsed = time.time() - start_time

    print(f"\n{'=' * 60}")
    print("Job 1 Completed Successfully")
    print(f"{'=' * 60}")
    print(f"Runtime:     {elapsed:.3f} seconds")
    print(f"Output lines: {len(reducer_result.stdout.strip().split(chr(10)))}")
    print(f"\nOutput preview:")
    print(reducer_result.stdout[:800])
    print(f"{'=' * 60}")


if __name__ == '__main__':
    run_local_pipeline()