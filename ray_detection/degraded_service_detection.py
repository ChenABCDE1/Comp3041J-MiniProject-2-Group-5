#!/usr/bin/env python3
"""
Task 3: Ray Degraded Service Detection
Uses Ray remote tasks for parallel processing of log data chunks.
Detects degraded services based on three conditions:
  1. Slow request rate > 20%
  2. Server error rate > 10%
  3. Timeout errors >= 5
"""

import ray
import os
import sys
import time
from typing import List, Dict, Tuple

# Initialize Ray (local mode with 4 CPUs)
ray.init(ignore_reinit_error=True, num_cpus=4)


@ray.remote
def process_log_chunk(chunk_data: str) -> Dict[str, Dict]:
    """
    Ray remote task: Process a data chunk and return service statistics.

    Args:
        chunk_data: String containing CSV lines (with header)

    Returns:
        Dictionary: {service_name: {'total_requests': n, 'slow_requests': n,
                                    'server_errors': n, 'timeout_errors': n}}
    """
    stats = {}
    lines = chunk_data.strip().split('\n')

    # Skip header line
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        fields = line.split(',')
        if len(fields) < 10:
            continue

        service = fields[3]
        try:
            status_code = int(fields[6])
            response_time = int(fields[7])
        except (ValueError, IndexError):
            continue

        error_type = fields[9].strip() if len(fields) > 9 else ""

        # Initialize service stats if not exists
        if service not in stats:
            stats[service] = {
                'total_requests': 0,
                'slow_requests': 0,
                'server_errors': 0,
                'timeout_errors': 0
            }

        stats[service]['total_requests'] += 1

        if response_time > 800:
            stats[service]['slow_requests'] += 1

        if status_code >= 500:
            stats[service]['server_errors'] += 1

        if error_type == 'Timeout':
            stats[service]['timeout_errors'] += 1

    return stats


def merge_partial_results(partial_results: List[Dict]) -> Dict:
    """
    Merge statistics from multiple Ray task outputs.

    Args:
        partial_results: List of dictionaries from each remote task

    Returns:
        Combined statistics for all services
    """
    final_stats = {}

    for partial in partial_results:
        for service, counts in partial.items():
            if service not in final_stats:
                final_stats[service] = {
                    'total_requests': 0,
                    'slow_requests': 0,
                    'server_errors': 0,
                    'timeout_errors': 0
                }
            for key in counts:
                final_stats[service][key] += counts[key]

    return final_stats


def detect_degraded_services(stats: Dict) -> List[Tuple[str, str]]:
    """
    Detect degraded services based on three conditions.

    Args:
        stats: Combined service statistics

    Returns:
        List of (service_name, reason) tuples
    """
    degraded = []

    for service, counts in sorted(stats.items()):
        total = counts['total_requests']
        if total == 0:
            continue

        slow_rate = counts['slow_requests'] / total
        error_rate = counts['server_errors'] / total
        timeout_count = counts['timeout_errors']

        reasons = []

        if slow_rate > 0.20:
            reasons.append("high slow request rate")
        if error_rate > 0.10:
            reasons.append("high server error rate")
        if timeout_count >= 5:
            reasons.append("repeated timeout errors")

        if reasons:
            degraded.append((service, "; ".join(reasons)))

    return degraded


def load_and_split_data(filepath: str, num_chunks: int = 4) -> List[str]:
    """
    Split CSV file into chunks for parallel processing.

    Args:
        filepath: Path to CSV file
        num_chunks: Number of parallel chunks (default 4 for 4 CPUs)

    Returns:
        List of chunk strings, each with header
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = lines[0]
    data_lines = lines[1:]
    chunk_size = len(data_lines) // num_chunks + 1

    chunks = []
    for i in range(0, len(data_lines), chunk_size):
        chunk = header + ''.join(data_lines[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def display_statistics(stats: Dict):
    """Display detailed statistics for each service."""
    print("\n" + "=" * 70)
    print("Detailed Service Statistics")
    print("=" * 70)
    print(f"{'Service':<<20s} {'Total':>8s} {'Slow':>6s} {'Err%':>6s} {'T/O':>4s}")
    print("-" * 70)

    for service in sorted(stats.keys()):
        s = stats[service]
        total = s['total_requests']
        slow_pct = s['slow_requests'] / total * 100
        err_pct = s['server_errors'] / total * 100

        print(f"{service:<20s} {total:>8d} {s['slow_requests']:>6d} "
              f"{err_pct:>6.1f}% {s['timeout_errors']:>4d}")


def main():
    print("=" * 70)
    print("Task 3: Ray Degraded Service Detection")
    print("=" * 70)

    # Build absolute path to dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'data', 'Comp3041J MiniProject 2 Dataset.csv')

    print(f"\nDataset: {data_path}")

    if not os.path.exists(data_path):
        print(f"ERROR: Dataset not found: {data_path}")
        ray.shutdown()
        return

    # Step 1: Load and split data
    print("\n[1/4] Loading and splitting data...")
    chunks = load_and_split_data(data_path, num_chunks=4)
    print(f"       Split into {len(chunks)} chunks for parallel processing")

    # Step 2: Submit Ray remote tasks
    print(f"\n[2/4] Submitting {len(chunks)} Ray remote tasks...")
    start_time = time.time()
    futures = [process_log_chunk.remote(chunk) for chunk in chunks]
    partial_results = ray.get(futures)
    print("       All remote tasks completed")

    # Step 3: Merge partial results
    print("\n[3/4] Merging partial results...")
    final_stats = merge_partial_results(partial_results)

    # Display statistics
    display_statistics(final_stats)

    # Step 4: Detect degraded services
    print("\n[4/4] Detecting degraded services...")
    degraded = detect_degraded_services(final_stats)

    elapsed = time.time() - start_time

    # Display results
    print("\n" + "=" * 70)
    print("DEGRADED SERVICE DETECTION RESULTS")
    print("=" * 70)
    print("service_name,reason")
    print("-" * 70)

    for service, reason in degraded:
        print(f"{service},{reason}")

    # Save output
    outputs_dir = os.path.join(script_dir, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    output_file = os.path.join(outputs_dir, 'degraded_services.txt')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("service_name,reason\n")
        for service, reason in degraded:
            f.write(f"{service},{reason}\n")

    # Runtime summary
    print(f"\n{'=' * 70}")
    print("Execution Summary (for Group Report Section VI)")
    print(f"{'=' * 70}")
    print(f"Ray Task Runtime:           {elapsed:.3f} seconds")
    print(f"Number of Data Chunks:        {len(chunks)}")
    print(f"Number of Services Analyzed:  {len(final_stats)}")
    print(f"Degraded Services Found:      {len(degraded)}")
    print(f"Execution Environment:        Local Windows Machine, 4 CPUs")
    print(f"Ray Version:                  {ray.__version__}")
    print(f"{'=' * 70}")
    print(f"\nOutput saved to: {output_file}")

    ray.shutdown()


if __name__ == '__main__':
    main()