# !/bin/python3
# http://www.adventofcode.com/2017/day/10

from utils import read_input


def get_reversed_subsection(nums, start, end):
    if end > start:
        return nums[start:end][::-1]
    return (nums[start:] + nums[:end])[::-1]


def get_hash(lengths, num_loops=1):
    nums = [x for x in range(256)]
    len_nums = len(nums)
    i = 0
    skip_size = 0

    for loop in range(num_loops):
        for l in lengths:
            # get end positon
            end = (i + l) % len_nums
            reverse = get_reversed_subsection(nums, i, end)
            for offset in range(l):
                nums[(i + offset) % len_nums] = reverse[offset]

            # increment current position and skip size
            i = (i + l + skip_size) % len_nums
            skip_size += 1
    return nums


def get_ascii(input_string):
    result = []
    for string in input_string:
        result.append(int(ord(string)))
    return result + [17, 31, 73, 47, 23]


def xor(numbers):
    result = 0
    for num in numbers:
        result ^= num
    return result


def get_knot_hash(lengths):
    nums = get_hash(lengths, num_loops=64)

    knot_hash = ''
    for i in range(0, 256, 16):
        knot_hash += hex(xor(nums[i:i + 16]))[2:].zfill(2)

    return knot_hash


LENGTHS = read_input()

try:
    HASH = get_hash([int(L.strip()) for L in LENGTHS.split(',')])
    print('part a:', HASH[0] * HASH[1])
except:
    pass


print('part b:', get_knot_hash(get_ascii(LENGTHS)))
