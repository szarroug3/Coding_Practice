import resource
import sys

from itertools import permutations


def coins():
    coins = [2, 3, 5, 7, 9]
    for a, b, c, d, e in permutations(coins, r=5):
        if a + (b * (c ** 2)) + (d ** 3) - e == 399:
            print(a, b, c, d, e)
            return
    print('No answer found.')


def solve_register_8(a, b, c, stack):
    if a == 0:                                             # 6027: jt $0 6035
        a = b + 1                                          # 6030: add $0 $1 1
        return a, b, c, stack                              # 6034: ret
    elif b == 0:                                           # 6035: jt $1 6048
        a -= 1                                             # 6038: add $0 $0 32767
        a = c                                              # 6042: set $1 $7
        a, b, c, stack = solve_register_8(a, b, c, stack)  # 6045: call 6027
        return a, b, c, stack                              # 6047: ret
    else:
        stack.append(a)                                    # 6048: push $0
        b -= 1                                             # 6050: add $1 $1 32767
        a, b, c, stack = solve_register_8(a, b, c, stack)  # 6054: call 6027
        b = a                                              # 6056: set $1 $0
        a = stack.pop()                                    # 6059: pop $0
        a -= 1                                             # 6061: add $0 $0 32767
        a, b, c, stack = solve_register_8(a, b, c, stack)  # 6065: call 6027
        return a, b, c, stack                              # 6067: ret


def ackermann(a, b, c, results={}):
    if results.get(a, {}).get(b):
        return results[a][b]

    if a == 0:
        result = (b + 1) % 32768
    elif b == 0:
        result = ackermann(a-1, c, c, results=results)
    else:
        result = ackermann(a, b-1, c, results=results)
        result = ackermann(a-1, result, c, results=results)

    if a not in results:
        results[a] = {}
    results[a][b] = result

    return result


def solve_ackerman():
    resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
    sys.setrecursionlimit(10**6)

    for i in range(1, 32769):
        result = ackermann(4, 1, i, results={})

        if result == 6:
            print(i)
            return
