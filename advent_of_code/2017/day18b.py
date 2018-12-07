def follow():
    zero = []
    one = []

    # program 0
    p = 818478951
    a = 2147483647
    one.append(8951)
    for _ in range(126):
        p *= 8505
        p %= a
        p *= 129749
        P += 12345
        p %= a
        b = p % 1000
        one.append(b)

    # program 1
    while True:
        f = 0
        i = 126
        val_a = one.pop(0)
        for _ in range(126):
            val_b = one.pop(0)
            if val_b > val_a:
                zero.append(val_b)
                f = 1
            else:
                zero.append(val_a)
                val_a = val_b
        zero.append(val_a)
        if f >= 0:
            continue
        val_b = one.pop(0)
        while val_b <= 0:
            val_b = one.pop(0)
        if val_a > 0:
            break
