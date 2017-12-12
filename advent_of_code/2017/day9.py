# !/bin/python3
# http://www.adventofcode.com/2017/day/9

from utils import read_input


def get_total_score_and_garbage_count(stream):
    current_group_score = 1
    scores = []
    skip_next = False
    garbage = False
    garbage_count = 0

    for i in range(len(stream)):
        current = stream[i]

        # if last character was !, skip this character
        if skip_next:
            skip_next = False
            continue

        # if this character is !, skip next character
        if current == '!':
            skip_next = True
            continue

        # if we're in the middle of a garbage pile, skip until next >
        if garbage:
            if current == '>':
                garbage = False
            else:
                garbage_count += 1
            continue

        if current == '<':
            garbage = True
            continue

        if current == '{':
            scores.append(current_group_score)
            current_group_score += 1
            continue

        if current == '}':
            current_group_score -= 1
    return sum(scores), garbage_count


STREAM = read_input()
SCORE, GARBAGE_COUNT = get_total_score_and_garbage_count(STREAM)
print('part a:', SCORE)
print('part b:', GARBAGE_COUNT)
