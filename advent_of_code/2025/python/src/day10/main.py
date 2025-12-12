# !/bin/python3

from z3 import Bool
from z3 import Int
from z3 import Optimize
from src.utils import read_input


def process_input(data):
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    manual = []

    for line in data:
        config_end_index = line.index(']')
        goal = [True if val ==
                '#' else False for val in line[1:config_end_index]]

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
            opt.add(light == goal)

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
            opt.add((sum(light_buttons[i]) % 2 == 1) == goal)

        opt.minimize(sum(buttons))

        if opt.check():
            model = opt.model()
            sum_expr = sum(model[button] for button in buttons)
            total += model.evaluate(sum_expr).as_long()
    return total


def part_a(manual):
    presses = 0
    for config in manual:
        goal = config['goal']
        buttons = config['buttons']
    return 0


def part_b_z3(manual):
    total = 0
    for config in manual:
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
            total += model.evaluate(sum_expr).as_long()
    return total


def part_b(manual):
    return 0


def main():
    manual = process_input(read_input())
    print(part_a_z3(manual))
    print(part_b_z3(manual))


main()
