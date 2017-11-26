import math
import matplotlib.pyplot as plt


def rand(seed):
    m = math.pow(2, 31)

    xn = None

    for i in range(0, 1000):
        xn = (16807 * seed) % (math.pow(2, 31) - 1)
        seed = xn

    return xn / m

