# !/bin/python3
# https://adventofcode.com/2018/day/9

from collections import defaultdict, deque
from utils import read_input


def play(num_players, num_marbles):
    marbles = deque([0])
    curr_player = 0
    players = defaultdict(int)

    for i in range(1, num_marbles+1):
        if i % 23 == 0:
            marbles.rotate(7)
            players[curr_player] += i + marbles.popleft()
            curr_player = (curr_player + 1) % num_players
        else:
            marbles.rotate(-2)
            marbles.insert(0, i)

    return max(players.values())


if __name__ == '__main__':
    data = read_input(separator=' ')
    num_players, num_marbles = int(data[0]), int(data[6])
    print('part a:', play(num_players, num_marbles))
    print('part b:', play(num_players, num_marbles*100))
