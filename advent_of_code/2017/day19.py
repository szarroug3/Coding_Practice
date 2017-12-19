# !/bin/python3
# http://www.adventofcode.com/2017/day/19

from utils import read_input


def get_next_vertical(diagram, i, j, direction):
    """
    Get next i, j, and direction based on current i, j and location
    """
    offset = -1 if direction == 'up' else 1
    if diagram[i][j] != '+':
        k = i + offset
        num_steps = 1
        while k >= 0 and k < len(diagram):
            # if we hit an empty spot, we're done
            if diagram[k][j] == ' ':
                return None
            if diagram[k][j] != '-':
                return k, j, direction, num_steps
            k += offset
            num_steps += 1
        return None

    # if we're here, that means our current position is on top of a +
    # we need to figure out whether to go left or right
    # try left first
    k = j - 1
    num_steps = 1
    while k >= 0:
        # we hit a space, this direction is a no-go
        if diagram[i][k] == ' ':
            break
        # we found what we're looking for
        if diagram[i][k] != '|':
            return i, k, 'left', num_steps
        # we hit a crossroad, move on
        k -= 1
        num_steps += 1

    # if we're here, we didn't find a suitable path goint left
    # try going right
    k = j + 1
    num_steps = 1
    while k < len(diagram[i]):
        # we hit a space, this direction is a no-go
        if diagram[i][k] == ' ':
            break
        # we found what we're looking for
        if diagram[i][k] != '|':
            return i, k, 'right', num_steps
        # we hit a crossroad, move on
        k += 1
        num_steps += 1


def get_next_horizontal(diagram, i, j, direction):
    """
    Get next i, j, and direction based on current i, j and location
    """
    offset = -1 if direction == 'left' else 1
    if diagram[i][j] != '+':
        k = j + offset
        num_steps = 1
        while k >= 0 and k < len(diagram[i]):
            # if we hit an empty spot, we're done
            if diagram[i][k] == ' ':
                return None
            if diagram[i][k] != '|':
                return i, k, direction, num_steps
            k += offset
            num_steps += 1
        return None

    # if we're here, that means our current position is on top of a +
    # we need to figure out whether to go up or down
    # try up first
    k = i - 1
    num_steps = 1
    while k >= 0:
        # we hit a space, this direction is a no-go
        if diagram[k][j] == ' ':
            break
        # we found what we're looking for
        if diagram[k][j] != '-':
            return k, j, 'up', num_steps
        # we hit a crossroad, move on
        k -= 1
        num_steps += 1

    # if we're here, we didn't find a suitable path goint up
    # try going down
    k = i + 1
    num_steps = 1
    while k < len(diagram):
        # we hit a space, this direction is a no-go
        if diagram[k][j] == ' ':
            break
        # we found what we're looking for
        if diagram[k][j] != '-':
            return k, j, 'down', num_steps
        # we hit a crossroad, move on
        k += 1
        num_steps += 1


def follow_map(diagram):
    i = 0
    j = diagram[0].index('|')
    direction = 'down'
    string = ''
    num_steps = 1

    while True:
        if diagram[i][j].isalpha():
            string += diagram[i][j]
        if direction == 'up' or direction == 'down':
            next_info = get_next_vertical(diagram, i, j, direction)
            if not next_info:
                return string, num_steps
            i, j, direction, new_steps = next_info
            num_steps += new_steps
            continue
        next_info = get_next_horizontal(diagram, i, j, direction)
        if not next_info:
            return string, num_steps
        i, j, direction, new_steps = next_info
        num_steps += new_steps


if __name__ == '__main__':
    DIAGRAM = [list(x) for x in read_input(ignore_empty=False)]
    STRING, NUM_STEPS = follow_map(DIAGRAM)
    print('part a:', STRING)
    print('part b:', NUM_STEPS)
