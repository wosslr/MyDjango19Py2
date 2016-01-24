def fib(m):
    n, a, b = 0, 0, 1
    y = float(0)
    result = []
    while n < m:
        # yield a
        a, b = b, a + b
        y = a / b
        result.append(y)
        n += 1
    return result