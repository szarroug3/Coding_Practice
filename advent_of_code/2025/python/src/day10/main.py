# !/bin/python3

from copy import copy
from z3 import Bool
from z3 import Int
from z3 import Optimize
from src.utils import read_input


def process_input(data):
    manual = []

    for line in data:
        config_end_index = line.index(']')
        goal = list(line[1:config_end_index])

        joltage_start_index = line.index('{')
        joltage_end_index = line.index('}')
        joltages = [int(val) for val in line[joltage_start_index +
                                             1:joltage_end_index].split(',')]

        buttons_start_index = config_end_index + 2
        buttons_end_index = joltage_start_index - 2
        buttons_config = line[buttons_start_index +
                              1:buttons_end_index].split(') (')
        buttons = []
        for button_config in buttons_config:
            buttons.append([int(val) for val in button_config.split(',')])

        manual.append({
            'goal': goal,
            'joltages': joltages,
            'buttons': buttons
        })
    return manual


def get_minimum_presses_for_lights(buttons, goal, get_all_possibilities=False):
    min_presses = None
    result = [] if get_all_possibilities else None

    # it only makes sense to push each button
    # a maximum of one time. use binary
    # to get all possible configs
    all_lights_on = int('1'*len(buttons), 2)
    for i in range(1, all_lights_on + 1):
        binary = bin(i)[2:].rjust(len(buttons), '0')

        # if the number of 1s in this config
        # is more than the current min, don't
        # bother trying it
        press_count = binary.count('1')
        if not get_all_possibilities and min_presses and press_count >= min_presses:
            continue

        lights = ['.'] * len(goal)
        buttons_to_press = [bool(int(val)) for val in binary]
        for i, press in enumerate(buttons_to_press):
            if not press:
                continue

            for light in buttons[i]:
                lights[light] = '.' if lights[light] == '#' else '#'

        if lights == goal:
            min_presses = press_count
            if get_all_possibilities:
                result.append(binary)
            else:
                result = binary
    return result, min_presses


def part_a(manual):
    total = 0
    for config in manual:
        buttons = config['buttons']
        goal = config['goal']
        _, min_presses = get_minimum_presses_for_lights(buttons, goal)
        total += min_presses
    return total


def part_a_z3(manual):
    total = 0
    for config in manual:
        opt = Optimize()

        lights = []
        light_buttons = {}
        for i, goal in enumerate(config['goal']):
            light = Bool(f'light_{i}')
            lights.append(light)
            light_buttons[i] = []
            opt.add(light == (goal == '#'))

        buttons = []
        for i, button in enumerate(config['buttons']):
            button = Int(f'button_{i}')
            buttons.append(button)
            opt.add(button >= 0)

        for i, button in enumerate(config['buttons']):
            for light in button:
                if light not in light_buttons:
                    light_buttons[light] = []
                light_buttons[light].append(buttons[i])

        for i, goal in enumerate(config['goal']):
            opt.add((sum(light_buttons[i]) % 2 == 1) == (goal == '#'))

        opt.minimize(sum(buttons))

        if opt.check():
            model = opt.model()
            sum_expr = sum(model[button] for button in buttons)
            total += model.evaluate(sum_expr).as_long()
    return total


def get_parity(remaining):
    basic = ['.' if val % 2 == 0 else '#' for val in remaining]
    offset = 1
    while '#' not in basic:
        offset *= 2
        remaining = [val / 2 for val in remaining]
        basic = ['.' if val % 2 == 0 else '#' for val in remaining]
    return basic, offset


def get_allowed_buttons(remaining, buttons):
    allowed_counters = []
    for i, left in enumerate(remaining):
        if left >= 1:
            allowed_counters.append(i)

    allowed_buttons = []
    for button in buttons:
        acceptable = True
        for counter in button:
            if counter not in allowed_counters:
                acceptable = False
                break
        if acceptable:
            allowed_buttons.append(button)

    return allowed_buttons


def try_possibility(remaining, possibility, buttons, offset, visited):
    distance = possibility.count('1') * offset
    for i, press in enumerate(possibility):
        if press == '0':
            continue

        stringified = ','.join(str(val) for val in buttons[i])
        if stringified not in visited:
            visited[stringified] = 0
        visited[stringified] += offset
        for button in buttons[i]:
            if remaining[button] < offset:
                return False, None, None, visited
            remaining[button] -= offset
    return True, remaining, distance, visited


def print_visited(visited):
    things = [0] * 12
    for buttons, count in visited.items():
        for counter in buttons.split(','):
            things[int(counter)] += count
    print(things)
    return things[5] == 0 and things[9] == 0
    # for i, count in enumerate(things):
    # print(f'button_{i} = {count}')


def print_button_presses(visited, buttons):
    print('printing buttons', buttons)
    things = []
    for button in buttons:
        stringified = ','.join([str(val) for val in button])
        if stringified in visited:
            things.append(visited[stringified])
        else:
            things.append(0)
    print('button presses', things)


def get_presses(remaining, buttons, goals, original_buttons, distance=0, parities={}, visited={}):
    print('-'*10)
    stringified = ','.join([str(left) for left in remaining])
    print('remaining', remaining)
    print('buttons', buttons)
    show = print_button_presses(visited, original_buttons)
    # print_visited(visited)

    values = set(remaining)
    if len(values) == 1 and 0 in values:
        return True, remaining, distance, parities, visited

    if stringified in parities:
        basic, offset = parities[stringified]
    else:
        basic, offset = get_parity(remaining)
        parities[stringified] = (basic, offset)

    allowed_buttons = get_allowed_buttons(remaining, buttons)
    if not allowed_buttons:
        if show:
            print('PANIC1')
        print('no buttons')
        return False, None, None, parities, visited

    possibilities, _ = get_minimum_presses_for_lights(
        allowed_buttons, basic, get_all_possibilities=True)
    print('possibilities', possibilities)

    counts = []
    for possibility in sorted(possibilities, key=lambda p: p.count('1'), reverse=True):
        print('trying possibility', possibility)
        possible, left, presses, curr_visited = try_possibility(
            copy(remaining), possibility, allowed_buttons, offset, copy(visited))
        if not possible:
            print('ignoring')
            continue

        acceptable, modified_remaining, modified_count, parities, curr_visited = get_presses(
            left, allowed_buttons, goals, original_buttons, distance + presses, parities, curr_visited)

        if acceptable:
            counts.append(
                [modified_count, modified_remaining, curr_visited])

    if counts:
        distance, remaining, visited = sorted(
            counts, key=lambda c: c[0])[0]
        return True, remaining, distance, parities, visited

    print('no possibilities worked')
    if show:
        print('PANIC2')
    show = print_button_presses(visited, original_buttons)
    if show:
        print('PANIC3')
    return False, None, None, parities, visited


def part_b(manual, results):
    total = 0
    parities = {}
    # [1,3,4,5,6,8], [0,1,5,6,8,9], [8,9], [1,2,3,4,6,7], [1,2,3,4,5,6,7,8], [4], [5,6,9], [0,2,3,4,5,6,7],
    # [0,2,3,4,5,7,8,9], [0,1,3,4,7,9], [0,2,4,5], [1,2,3,5,7,9]]
    # button_0 = 12
    # button_1 = 17
    # button_2 = 5
    # button_3 = 23
    # button_4 = 15
    # button_5 = 0
    # button_6 = 10
    # button_7 = 2
    # button_8 = 17
    # button_9 = 0
    # button_10 = 6
    # button_11 = 10
    indices = [105, 120, 128, 131, 137, 166]
    for i, config in enumerate(manual[105:106]):
        print(config['buttons'])
        # if i not in indices:
        # continue
        print('processing', i)
        goals = config['joltages']
        buttons = config['buttons']
        good, _, count, parities, _ = get_presses(
            goals, buttons, goals, copy(buttons), parities=parities)
        if not good:
            print('bad')
        elif count != results[105]:
            print('mismatch', results[105], count)
        if count:
            print('good')
            total += count
        # print(i, count)
    return total


def part_b_z3(manual):
    total = 0
    results = []
    for index, config in enumerate(manual):
        opt = Optimize()

        counters = []
        counter_buttons = {}
        for i, goal in enumerate(config['joltages']):
            counter = Int(f'counter_{i}')
            counters.append(counter)
            counter_buttons[i] = []
            opt.add(counter == goal)

        buttons = []
        for i, button in enumerate(config['buttons']):
            button = Int(f'button_{i}')
            buttons.append(button)
            opt.add(button >= 0)

        for i, button in enumerate(config['buttons']):
            for counter in button:
                if counter not in counter_buttons:
                    counter_buttons[counter] = []
                counter_buttons[counter].append(buttons[i])

        for i, goal in enumerate(config['joltages']):
            opt.add(sum(counter_buttons[i]) == goal)

        opt.minimize(sum(buttons))

        if opt.check():
            model = opt.model()
            sum_expr = sum([model[button] for button in buttons])
            # if index == 105:
            # print(model)
            count = model.evaluate(sum_expr).as_long()
            total += count
            # print(index, count)
            results.append(count)
    return total, results


def main():
    manual = process_input(read_input())
    results = part_b_z3(manual)[1]
    print('part a (z3):', part_a_z3(manual))
    print('part b (z3):', part_b_z3(manual))
    print('part a:', part_a(manual))
    print('part b:', part_b(manual, results))


main()
