#!/usr/bin/env python3
"""
Execute all three MapReduce jobs sequentially.
Records runtime for comparison analysis in the Group Report.
"""

import subprocess
import sys
import os
import time


def run_job(script_path, job_name):
    """Run a single job and return its runtime."""
    print(f"\n{'#' * 70}")
    print(f"# {job_name:^66s} #")
    print(f"{'#' * 70}")

    start = time.time()
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    elapsed = time.time() - start

    print(result.stdout)
    if result.stderr:
        print(f"Warnings/Errors:\n{result.stderr}")

    return elapsed


def main():
    # Get mapreduce directory
    mapreduce_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("MapReduce Baseline Analytics - All Jobs")
    print("=" * 70)
    print(f"Working directory: {mapreduce_dir}")

    total_start = time.time()

    # Job 1
    job1_path = os.path.join(mapreduce_dir, 'job1_request_count', 'run.py')
    t1 = run_job(job1_path, 'Job 1: Request Count')

    # Job 2
    job2_path = os.path.join(mapreduce_dir, 'job2_error_count', 'run.py')
    t2 = run_job(job2_path, 'Job 2: Error Count')

    # Job 3
    job3_path = os.path.join(mapreduce_dir, 'job3_slow_endpoints', 'run.py')
    t3 = run_job(job3_path, 'Job 3: Slow Endpoints')

    total_elapsed = time.time() - total_start

    print(f"\n{'=' * 70}")
    print("Execution Summary (for Group Report Section VI)")
    print(f"{'=' * 70}")
    print(f"Job 1 (Request Count):      {t1:.3f} seconds")
    print(f"Job 2 (Error Count):          {t2:.3f} seconds")
    print(f"Job 3 (Slow Endpoints):       {t3:.3f} seconds")
    print(f"Total Runtime:                {total_elapsed:.3f} seconds")
    print(f"Execution Environment:        Local Windows Machine")
    print(f"Python Version:               {sys.version.split()[0]}")
    print(f"{'=' * 70}")
    print("\nAll outputs saved to: mapreduce/outputs/")
    print("  - request_count.txt")
    print("  - error_count.txt")
    print("  - top10_slow_endpoints.txt")


if __name__ == '__main__':
    main()