import numpy as np


def random_walk(array):
    max_height = array.max()*1.5
    step_n = len(array)
    step_set = [-1, 0, 1]
    steps = np.random.choice(a=step_set, size=step_n)

    # Calculate factor to achieve max_height
    steps_height = steps.max() - steps.min()
    factor = max_height / steps_height
    steps = steps * factor

    path = steps.cumsum(0)
    feature_with_random_walk = array + path

    # Ensure non-negativity using np.maximum
    feature_with_random_walk = np.maximum(feature_with_random_walk, 0)

    return feature_with_random_walk
