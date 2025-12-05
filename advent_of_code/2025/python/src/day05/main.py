# !/bin/python3

from src.utils import read_input


def process_input(data):
    ranges = []
    ingredients = []

    for line in data:
        if '-' in line:
            ranges.append([int(x) for x in line.split('-')])
        else:
            ingredients.append(int(line))
    return ranges, ingredients


def merge_ranges(ranges):
    merged = []
    for start, end in ranges:
        handled = False
        for i, (start_merged, end_merged) in enumerate(merged):
            # start is already within a merged range
            if start >= start_merged and start <= end_merged and end >= start_merged and end <= end_merged:
                handled = True
                break
            # start is before a currently merged range, end is after, replace both
            if start <= start_merged and end >= end_merged:
                merged[i][0] = start
                merged[i][1] = end
                handled = True
                break
            # start is before a merged range and end is within merged
            # replace only start
            if start <= start_merged and end >= start_merged and end <= end_merged:
                merged[i][0] = start
                handled = True
                break
            # start is within a merged range and end is after
            # replace only end
            if start >= start_merged and start <= end_merged and end >= end_merged:
                merged[i][1] = end
                handled = True
                break
        if not handled:
            merged.append([start, end])
    return merged


def iterative_merge_ranges(ranges):
    merged = []
    previous_len = len(ranges)
    while len(merged) != previous_len:
        merged = merge_ranges(ranges)
        previous_len = len(ranges)
        ranges = merged
    return merged


def part_a(ranges, ingredients):
    count = 0
    for ingredient in ingredients:
        for start, end in ranges:
            if ingredient >= start and ingredient <= end:
                count += 1
                break
    return count


def part_b(ranges):
    count = 0
    for start, end in ranges:
        count += end - start + 1
    return count


def main():
    ranges, ingredients = process_input(read_input())
    merged = iterative_merge_ranges(ranges)
    print(part_a(merged, ingredients))
    print(part_b(merged))


main()
