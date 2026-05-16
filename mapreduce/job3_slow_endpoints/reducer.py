#!/usr/bin/env python3
"""
Job 3 Reducer: Sum slow request counts per endpoint
Identical aggregation logic to Jobs 1 and 2
"""

import sys


def reducer():
    current_endpoint = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        endpoint, count = line.split('\t')
        count = int(count)

        if current_endpoint == endpoint:
            current_count += count
        else:
            if current_endpoint:
                print(f"{current_endpoint}\t{current_count}")
            current_endpoint = endpoint
            current_count = count

    if current_endpoint:
        print(f"{current_endpoint}\t{current_count}")


if __name__ == '__main__':
    reducer()