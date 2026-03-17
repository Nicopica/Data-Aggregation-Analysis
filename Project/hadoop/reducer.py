#!/usr/bin/env python3
import sys

def main():
    min_value = float('inf')
    max_value = float('-inf')
    total_sum = 0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            key, value_str = line.split('\t', 1)
            value = float(value_str)

            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value
            
            total_sum += value
            count += 1
            
        except ValueError:
            continue
            
    if count > 0:
        average = total_sum / count
        print("Min: {}\tMax: {}\tAverage: {}".format(min_value, max_value, average))
    else:
        print("No data processed.")

if __name__ == "__main__":
    main()
