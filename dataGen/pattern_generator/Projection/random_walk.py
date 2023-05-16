import numpy as np


def random_walk(array):
    step_n = len(array)
    step_set = [-1, 0, 1]
    # Simulate steps in 1D
    steps = np.random.choice(a=step_set, size=step_n)
    factor = steps.max()/(array.max()-array.min())
    steps = steps*factor
    path = steps.cumsum(0)
    feature_with_random_walk = np.add(array, path)
    return feature_with_random_walk
