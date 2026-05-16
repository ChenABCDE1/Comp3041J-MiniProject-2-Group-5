#!/usr/bin/env python3
"""
Job 2 Mapper: Server Error Count by Service
Input: CSV lines from cloud service logs
Output: service_name \t 1 (only for status_code >= 500)
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
            status_code = int(fields[6])  # 7th column

            # Filter: only server errors (5xx status codes)
            if status_code >= 500:
                print(f"{service_name}\t1")


if __name__ == '__main__':
    mapper()