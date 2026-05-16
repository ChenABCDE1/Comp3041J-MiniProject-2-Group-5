#!/usr/bin/env python3
"""
Job 1 Mapper: Request Count by Service
Input: CSV lines from cloud service logs
Output: service_name \t 1
"""

import sys


def mapper():
    is_header = True

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Skip CSV header line
        if is_header:
            is_header = False
            continue

        # Parse CSV fields (simple split; dataset has no commas within fields)
        fields = line.split(',')
        if len(fields) >= 10:
            service_name = fields[3]  # 4th column: service_name
            # Emit key-value pair: service_name \t 1
            print(f"{service_name}\t1")


if __name__ == '__main__':
    mapper()