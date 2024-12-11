# !/bin/python3

from src.utils import read_input


def process_input(data):
    equations = []
    for line in data:
        result, values = line.split(': ')
        equations.append({
            'result': int(result),
            'values': [int(val) for val in values.split(' ')]
        })
    return equations


def trinary(value):
  if value == 0:
    return "0"

  result = ""
  while value > 0:
    value, remainder = divmod(value, 3)
    result = str(remainder) + result

  return result


def possible(result, values, base=2):
    num_of_operations = len(values) - 1
    max_value = base ** num_of_operations

    for i in range(max_value):
        if base == 2:
            converted = bin(i)[2:]
        else:
            converted = trinary(i)

        converted = converted.zfill(num_of_operations)
        total = values[0]

        for i, operation in enumerate(converted):
            if operation == '0':
                total += values[i + 1]
            elif operation == '1':
                total *= values[i + 1]
            else:
                total = int(f'{total}{values[i + 1]}')

        if total == result:
            return True

    return False

def part_a(equations):
    total = 0
    for test in equations:
        if possible(test['result'], test['values']):
            total += test['result']
    return total


def part_b(equations):
    total = 0
    for test in equations:
        if possible(test['result'], test['values'], base=3):
            total += test['result']
    return total


def main():
    data = read_input()
    equations = process_input(data)
    print(part_a(equations))
    print(part_b(equations))


main()
