# !/bin/python3

from src.utils import read_input


def process_input(data):
    graph = {}

    for line in data:
        end_of_input = line.index(':')
        node = line[:end_of_input]
        outputs = line[end_of_input+2:].split(' ')
        graph[node] = outputs

    return graph


def traverse(graph, node, cache={'out': 1}):
    cache[node] = 0
    for edge in graph.get(node, []):
        if edge in cache:
            cache[node] += cache[edge]
        else:
            cache = traverse(graph, edge, cache)
            cache[node] += cache[edge]

    return cache


def part_a(graph):
    cache = traverse(graph, 'you')
    return cache['you']


def part_b(graph):
    paths = [
        ['svr', 'fft'],
        ['fft', 'dac'],
        ['fft', 'out'],
        ['svr', 'dac'],
        ['dac', 'fft'],
        ['dac', 'out'],
    ]
    caches = {
        f'{start}_{end}': traverse(graph, start, cache={'out': 0, end: 1})[start] for start, end in paths
    }
    return (caches['svr_fft'] * caches['fft_dac'] * caches['dac_out']) + \
        (caches['svr_dac'] * caches['dac_fft'] * caches['fft_out'])


def main():
    graph = process_input(read_input())
    print('part a:', part_a(graph))
    print('part b:', part_b(graph))


main()
