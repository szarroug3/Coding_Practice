# !/bin/python3

from src.utils import read_input


def parse_part_a(data):
    problems = []

    for i, line in enumerate(data):
        for j, val in enumerate(line.split()):
            if j == len(problems):
                problems.append({
                    'values': [],
                    'operation': '',
                })
            if val == '+' or val == '*':
                problems[j]['operation'] = val
            else:
                problems[j]['values'].append(int(val))

    return problems


def calculate(problems):
    total = 0
    for problem in problems:
        if problem['operation'] == '+':
            total += sum(problem['values'])
        else:
            mult = 1
            for val in problem['values']:
                mult *= val
            total += mult
    return total


def part_a(data):
    problems = parse_part_a(data)
    return calculate(problems)


def part_b(data):
    rows_len = len(data)
    cols_len = len(data[0])

    # input data has an empty line at the end
    # ignore this line because it breaks our for loops
    if not len(data[rows_len - 1]):
        rows_len -= 1

    problems = []
    problem = {
        'values': [],
        'operation': ''
    }
    # iterage top to bottom then left to right instead of instead of left to right, top to bottom
    for i in range(cols_len):
        curr = ''
        for j in range(rows_len):
            val = data[j][i]
            if val.isdigit():
                curr += val
            elif val != ' ':
                problem['operation'] = val

        if curr:
            problem['values'].append(int(curr))
        else:
            problems.append(problem)

            problem = {
                'values': [],
                'operation': ''
            }
        curr = ''

    problems.append(problem)
    return calculate(problems)


def main():
    data = read_input(ignore_empty=False)
    print('part a:', part_a(data))
    print('part b:', part_b(data))


main()
