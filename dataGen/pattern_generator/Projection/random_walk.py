import numpy as np


# random walk pattern, that randomly chooses steps from -1,0,1
def random_walk(array, amplitude=1.5):
    max_height = array.max()*amplitude
    # Determine the number of steps and create the step set
    step_n = len(array)
    step_set = [-1, 0, 1]

    # Generate random steps based on the step set
    steps = np.random.choice(a=step_set, size=step_n)

    # Calculate factor to achieve max_height
    steps_height = steps.max() - steps.min()
    factor = max_height / steps_height
    steps = steps * factor

    # Calculate the cumulative sum of the steps to create the random walk
    path = steps.cumsum(0)
    # Add the random walk to the input array to create the feature_with_random_walk
    feature_with_random_walk = array + path

    # Ensure non-negativity using np.maximum
    feature_with_random_walk = np.maximum(feature_with_random_walk, 0)

    return feature_with_random_walk
