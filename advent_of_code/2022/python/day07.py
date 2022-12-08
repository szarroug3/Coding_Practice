# !/bin/python3
# https://adventofcode.com/2022/day/7

from utils import read_input


def cd(commands, index, filesystem, cwd):
    subdir = commands[index][5:]
    if subdir == '..':
        cwd = cwd[:-1]
    else:
        cwd_path = '/'.join(cwd)
        fullpath = cwd_path + '/' + subdir if cwd_path else subdir
        if cwd_path in filesystem:
            filesystem[cwd_path]['subdirs'].append(fullpath)
        filesystem[fullpath] = {'files': {}, 'subdirs': []}
        cwd.append(subdir)
    return index+1, cwd


def ls(commands, index, filesystem, cwd):
    index += 1
    while index < len(commands) and not commands[index].startswith('$'):
        cmd = commands[index]
        if not cmd.startswith('dir'):
            data = cmd.split(' ')
            cwd_path = '/'.join(cwd)
            filesystem[cwd_path]['files'][data[1]] = int(data[0])

        index += 1

    return index, cwd


def get_size(filesystem, directory):
    if 'size' in filesystem[directory]:
        return filesystem[directory]['size']

    size = sum(filesystem[directory]['files'].values())
    for subdir in filesystem[directory]['subdirs']:
        size += get_size(filesystem, subdir)
    filesystem[directory]['size'] = size
    return size


def get_filesystem(commands):
    functions = {'cd': cd, 'ls': ls}
    filesystem = {}
    cwd = []

    i = 0
    while i < len(commands):
        func = functions[commands[i][2:4]]
        i, cwd = func(commands, i, filesystem, cwd)

    for subdir in filesystem:
        get_size(filesystem, subdir)

    return filesystem


def part_a(filesystem):
    total = 0
    for subdir in filesystem.values():
        if subdir['size'] <= 100000:
            total += subdir['size']
    return total


def part_b(filesystem):
    total = 70000000
    unused = total - filesystem['/']['size']
    needed = 30000000 - unused

    minimum = total
    for subdir in filesystem.values():
        if subdir['size'] < minimum and subdir['size'] > needed:
            minimum = subdir['size']

    return minimum


if __name__ == '__main__':
    filesystem = get_filesystem(read_input())

    print('part a:', part_a(filesystem))
    print('part b:', part_b(filesystem))
