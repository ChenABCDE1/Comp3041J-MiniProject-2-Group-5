#!/usr/bin/env python3
"""
Job 3 Mapper: Identify slow endpoint requests
Input: CSV lines from cloud service logs
Output: service_name,endpoint \t 1 (only for response_time_ms > 800)
"""

import sys


def mapper():
    is_header = True

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Skip CSV header
        if is_header:
            is_header = False
            continue

        fields = line.split(',')
        if len(fields) >= 10:
            service_name = fields[3]  # 4th column
            endpoint = fields[4]  # 5th column
            response_time = int(fields[7])  # 8th column

            # Filter: only slow requests (> 800ms)
            if response_time > 800:
                composite_key = f"{service_name},{endpoint}"
                print(f"{composite_key}\t1")


if __name__ == '__main__':
    mapper()