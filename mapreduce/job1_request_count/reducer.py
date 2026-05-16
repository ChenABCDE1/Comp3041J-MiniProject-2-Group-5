#!/usr/bin/env python3
"""
Job 1 Reducer: Sum request counts per service
Input: service_name \t count
Output: service_name \t total_count
"""

import sys


def reducer():
    current_service = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Parse mapper output: key \t value
        service, count = line.split('\t')
        count = int(count)

        # Accumulate counts for the same service
        if current_service == service:
            current_count += count
        else:
            # Emit previous service total
            if current_service:
                print(f"{current_service}\t{current_count}")
            # Start new service
            current_service = service
            current_count = count

    # Emit the last service
    if current_service:
        print(f"{current_service}\t{current_count}")


if __name__ == '__main__':
    reducer()