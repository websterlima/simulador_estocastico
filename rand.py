import math
import matplotlib.pyplot as plt


def rand(seed):
    m = math.pow(2, 31)

    xn = None

    for i in range(0, 1000):
        xn = (16807 * seed) % (math.pow(2, 31) - 1)
        seed = xn

    return xn / m

def mult_rand(n, seed):
    m = math.pow(2, 31)

    xn = None

    rands = []

    for i in range(0, n):
        xn = (16807 * seed) % (math.pow(2, 31) - 1)
        seed = xn

        rands.append(xn / m)

    return rands