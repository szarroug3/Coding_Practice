# !usr/bin/python3
# https://www.hackerrank.com/challenges/coin-change/problem

from itertools import combinations_with_replacement

def getWays(n, c):
    # Complete this function
    total = 0
    for i in range(1, int(n / min(c)) + 1):
        for com in combinations_with_replacement(c, i):
            if sum(com) == n:
                total += 1
    return total


n, m = input().strip().split(' ')
n, m = [int(n), int(m)]
c = list(map(int, input().strip().split(' ')))
# Print the number of ways of making change for 'n' units using coins having the values given by 'c'
ways = getWays(n, c)
print(ways)
