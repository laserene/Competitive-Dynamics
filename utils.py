import random


def sign(x):
    try:
        return 1 if x >= 0 else -1
    except:
        return 1


def get_random_competitor(n_nodes):
    return random.randint(0, n_nodes - 1)

