#!/usr/bin/env python3
"""
Task 4: Validation of MapReduce and Ray Outputs
Provides concrete verification by manual counting against program outputs.
"""

import csv
import os
import sys
from collections import defaultdict


def load_data():
    """Load dataset with absolute path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, 'data', 'Comp3041J MiniProject 2 Dataset.csv')

    if not os.path.exists(data_path):
        print(f"ERROR: Dataset not found: {data_path}")
        sys.exit(1)

    return data_path


def manual_count_all(data_path):
    """
    Manually count all metrics from raw CSV for cross-validation.
    This serves as ground truth to verify MapReduce and Ray outputs.
    """
    # Initialize counters
    request_count = defaultdict(int)  # Job 1
    error_count = defaultdict(int)  # Job 2
    slow_endpoints = defaultdict(int)  # Job 3
    ray_stats = defaultdict(lambda: {  # Ray stats
        'total': 0, 'slow': 0, 'errors': 0, 'timeouts': 0
    })

    print("=" * 70)
    print("Task 4: Manual Validation - Counting from Raw CSV")
    print("=" * 70)
    print(f"\nProcessing: {data_path}")

    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            service = row['service_name']
            endpoint = row['endpoint']
            status = int(row['status_code'])
            rt = int(row['response_time_ms'])
            error_type = row.get('error_type', '').strip()

            # Job 1: Total requests per service
            request_count[service] += 1

            # Job 2: Server errors (status >= 500)
            if status >= 500:
                error_count[service] += 1

            # Job 3: Slow endpoints (response_time > 800)
            if rt > 800:
                key = f"{service},{endpoint}"
                slow_endpoints[key] += 1

            # Ray: Comprehensive stats per service
            ray_stats[service]['total'] += 1
            if rt > 800:
                ray_stats[service]['slow'] += 1
            if status >= 500:
                ray_stats[service]['errors'] += 1
            if error_type == 'Timeout':
                ray_stats[service]['timeouts'] += 1

    return {
        'request_count': dict(request_count),
        'error_count': dict(error_count),
        'slow_endpoints': dict(slow_endpoints),
        'ray_stats': dict(ray_stats)
    }


def validate_job1(manual_results, mapreduce_dir):
    """Validate Job 1 (Request Count) against manual count."""
    print("\n" + "=" * 70)
    print("Validation 1: Job 1 - Request Count by Service")
    print("=" * 70)

    manual = manual_results['request_count']

    # Load MapReduce output
    output_file = os.path.join(mapreduce_dir, 'outputs', 'request_count.txt')

    if not os.path.exists(output_file):
        print(f"WARNING: MapReduce output not found: {output_file}")
        return False

    mr_results = {}
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                mr_results[parts[0]] = int(parts[1])

    # Compare
    print(f"{'Service':<<20s} {'Manual':>8s} {'MapReduce':>10s} {'Match':>6s}")
    print("-" * 50)

    all_match = True
    for service in sorted(manual.keys()):
        manual_val = manual[service]
        mr_val = mr_results.get(service, 0)
        match = "✓" if manual_val == mr_val else "✗"
        if manual_val != mr_val:
            all_match = False

        print(f"{service:<20s} {manual_val:>8d} {mr_val:>10d} {match:>6s}")

    print(f"\nResult: {'PASS' if all_match else 'FAIL'}")
    return all_match


def validate_job2(manual_results, mapreduce_dir):
    """Validate Job 2 (Error Count) against manual count."""
    print("\n" + "=" * 70)
    print("Validation 2: Job 2 - Server Error Count by Service")
    print("=" * 70)

    manual = manual_results['error_count']
    output_file = os.path.join(mapreduce_dir, 'outputs', 'error_count.txt')

    if not os.path.exists(output_file):
        print(f"WARNING: MapReduce output not found: {output_file}")
        return False

    mr_results = {}
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                mr_results[parts[0]] = int(parts[1])

    print(f"{'Service':<<20s} {'Manual':>8s} {'MapReduce':>10s} {'Match':>6s}")
    print("-" * 50)

    all_match = True
    for service in sorted(manual.keys()):
        manual_val = manual[service]
        mr_val = mr_results.get(service, 0)
        match = "✓" if manual_val == mr_val else "✗"
        if manual_val != mr_val:
            all_match = False

        print(f"{service:<20s} {manual_val:>8d} {mr_val:>10d} {match:>6s}")

    print(f"\nResult: {'PASS' if all_match else 'FAIL'}")
    return all_match


def validate_job3(manual_results, mapreduce_dir):
    """Validate Job 3 (Top 10 Slow Endpoints) against manual count."""
    print("\n" + "=" * 70)
    print("Validation 3: Job 3 - Top 10 Slow Endpoints")
    print("=" * 70)

    manual = manual_results['slow_endpoints']

    # Get manual top 10
    manual_top10 = sorted(manual.items(), key=lambda x: -x[1])[:10]

    # Load MapReduce top 10
    output_file = os.path.join(mapreduce_dir, 'outputs', 'top10_slow_endpoints.txt')

    if not os.path.exists(output_file):
        print(f"WARNING: MapReduce output not found: {output_file}")
        return False

    mr_top10 = []
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                mr_top10.append((parts[0], int(parts[1])))

    print(f"{'Rank':>4s} {'Endpoint':<<45s} {'Manual':>6s} {'MR':>6s} {'Match':>6s}")
    print("-" * 70)

    all_match = True
    for i, ((man_endpoint, man_count), (mr_endpoint, mr_count)) in enumerate(
            zip(manual_top10, mr_top10), 1
    ):
        endpoint_match = man_endpoint == mr_endpoint
        count_match = man_count == mr_count
        match = "✓" if (endpoint_match and count_match) else "✗"
        if not (endpoint_match and count_match):
            all_match = False

        print(f"{i:>4d} {mr_endpoint:<45s} {man_count:>6d} {mr_count:>6d} {match:>6s}")

    print(f"\nResult: {'PASS' if all_match else 'FAIL'}")
    return all_match


def validate_ray_degraded(manual_results, ray_dir):
    """
    Validate Ray degraded service detection.
    Manually recalculate conditions and compare with Ray output.
    """
    print("\n" + "=" * 70)
    print("Validation 4: Ray - Degraded Service Detection")
    print("=" * 70)

    manual = manual_results['ray_stats']

    # Manually calculate degraded services
    manual_degraded = []
    for service, stats in sorted(manual.items()):
        total = stats['total']
        if total == 0:
            continue

        slow_rate = stats['slow'] / total
        error_rate = stats['errors'] / total
        timeout_count = stats['timeouts']

        reasons = []
        if slow_rate > 0.20:
            reasons.append("high slow request rate")
        if error_rate > 0.10:
            reasons.append("high server error rate")
        if timeout_count >= 5:
            reasons.append("repeated timeout errors")

        if reasons:
            manual_degraded.append((service, "; ".join(reasons)))

    # Load Ray output
    output_file = os.path.join(ray_dir, 'outputs', 'degraded_services.txt')

    if not os.path.exists(output_file):
        print(f"WARNING: Ray output not found: {output_file}")
        return False

    ray_degraded = []
    with open(output_file, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', 1)  # Split only on first comma
            if len(parts) == 2:
                ray_degraded.append((parts[0], parts[1]))

    # Compare
    print("Manual Degraded Services:")
    for service, reason in manual_degraded:
        print(f"  {service}: {reason}")

    print("\nRay Degraded Services:")
    for service, reason in ray_degraded:
        print(f"  {service}: {reason}")

    # Check match
    manual_set = set(manual_degraded)
    ray_set = set(ray_degraded)

    if manual_set == ray_set:
        print(f"\nResult: PASS - All degraded services match")
        return True
    else:
        print(f"\nResult: FAIL - Mismatch detected")
        print(f"  Only in manual: {manual_set - ray_set}")
        print(f"  Only in Ray: {ray_set - manual_set}")
        return False


def main():
    print("=" * 70)
    print("Task 4: Validation of All Outputs")
    print("=" * 70)

    # Load data
    data_path = load_data()
    manual_results = manual_count_all(data_path)

    # Build paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    mapreduce_dir = os.path.join(project_root, 'mapreduce')
    ray_dir = os.path.join(project_root, 'ray_detection')

    # Run validations
    results = []
    results.append(("Job 1: Request Count", validate_job1(manual_results, mapreduce_dir)))
    results.append(("Job 2: Error Count", validate_job2(manual_results, mapreduce_dir)))
    results.append(("Job 3: Top 10 Slow", validate_job3(manual_results, mapreduce_dir)))
    results.append(("Ray: Degraded Services", validate_ray_degraded(manual_results, ray_dir)))

    # Summary
    print("\n" + "=" * 70)
    print("Validation Summary")
    print("=" * 70)
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name:<30s} {status}")

    all_passed = all(r[1] for r in results)
    print(f"\nOverall: {'ALL VALIDATIONS PASSED' if all_passed else 'SOME VALIDATIONS FAILED'}")
    print("=" * 70)

    # Guidance for report
    print("\nFor Group Report Section V:")
    print("  Describe one concrete validation example, such as:")
    print("  - Manual count vs program output comparison")
    print("  - A checked degraded service and why it was classified as degraded")
    print("  - This script demonstrates all four validation types")


if __name__ == '__main__':
    main()