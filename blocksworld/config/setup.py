import numpy as np


# Goal state: numbers 1 in a 4x4 array.
# 0 represents the agent.


def generate_puzzle():
    return np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [2, 3, 4, 0]
    ])


def goal_state():
    return np.array([
        [1, 1, 1, 1],
        [1, 2, 1, 1],
        [1, 3, 1, 1],
        [1, 4, 1, 0]
    ])