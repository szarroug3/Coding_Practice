# !/bin/python3
# http://www.adventofcode.com/2017/day/12

from utils import read_input
from collections import defaultdict


def parse_input(pipes):
    connections = defaultdict(list)
    for pipe in pipes:
        program = pipe[0]
        conns = ' '.join(pipe[2:]).split(', ')
        for conn in conns:
            connections[program].append(conn)
    return connections


def find_connections_to(pipes, program='0', visited=[]):
    visited.append(program)
    for connection in pipes[program]:
        # don't revist a place we've been to
        if connection in visited:
            continue
        visited = find_connections_to(pipes, program=connection, visited=visited)
    return visited


def find_groups(pipes):
    visited = []
    num_groups = 0
    for program in pipes.keys():
        # ignore things that have already been grouped
        if program in visited:
            continue

        group = find_connections_to(pipes, program=program)
        if group:
            visited += group
            num_groups += 1
    return num_groups


PIPES = parse_input(read_input(separator=' '))
print('part a:', len(find_connections_to(PIPES)))
print('part b:', find_groups(PIPES))
