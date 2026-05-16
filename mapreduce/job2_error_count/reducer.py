#!/usr/bin/env python3
"""
Job 2 Reducer: Sum server error counts per service
Identical logic to Job 1 reducer (reusable component)
"""

import sys


def reducer():
    current_service = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        service, count = line.split('\t')
        count = int(count)

        if current_service == service:
            current_count += count
        else:
            if current_service:
                print(f"{current_service}\t{current_count}")
            current_service = service
            current_count = count

    if current_service:
        print(f"{current_service}\t{current_count}")


if __name__ == '__main__':
    reducer()