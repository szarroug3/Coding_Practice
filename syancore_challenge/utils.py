from itertools import permutations


def coins():
    coins = [2, 3, 5, 7, 9]
    for a, b, c, d, e in permutations(coins, r=5):
        if a + (b * (c ** 2)) + (d ** 3) - e == 399:
            print(a, b, c, d, e)
            return
    print('No answer found.')


coins()
