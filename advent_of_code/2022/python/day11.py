# !/bin/python3
# https://adventofcode.com/2022/day/11

from copy import deepcopy
from utils import read_input


def parse(monkeys):
    data = []
    for _, items, operation, test, true, false in monkeys:
        operation = operation.split("= ")[1].split()[1:]
        data.append(
            {
                "items": [int(item) for item in items.split(": ")[1].split(", ")],
                "operation": [
                    int(item) if item.isnumeric() else item for item in operation
                ],
                "test": int(test.split(" ")[-1]),
                "true": int(true.split(" ")[-1]),
                "false": int(false.split(" ")[-1]),
            }
        )
    return data


def operation(original, operation, value):
    if value == "old":
        value = original
    if operation == "+":
        return original + value
    return original * value


def keep_away(monkeys, rounds, relief):
    inspected = [0] * len(monkeys)

    mod = 1
    for monkey in monkeys:
        mod *= monkey["test"]

    for _ in range(rounds):
        for i, monkey in enumerate(monkeys):
            inspected[i] += len(monkey["items"])
            for item in monkey["items"]:
                item %= mod
                item = operation(item, *monkey["operation"])
                if relief:
                    item //= 3
                if item % monkey["test"] == 0:
                    monkeys[monkey["true"]]["items"].append(item)
                else:
                    monkeys[monkey["false"]]["items"].append(item)
            monkey["items"] = []

    inspected.sort(reverse=True)
    return inspected[0] * inspected[1]


if __name__ == "__main__":
    monkeys = parse(read_input(delimiter="\n\n", line_delimiter="\n"))

    print("part a:", keep_away(deepcopy(monkeys), 20, True))
    print("part b:", keep_away(deepcopy(monkeys), 10000, False))
