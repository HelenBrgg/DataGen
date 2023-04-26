import numpy as np


def smooth(array):
    x_vals = np.arange(len(array))
    smoothed_vals = np.zeros(x_vals.shape)
    for x_position in x_vals:
        array = array.astype(float)
        kernel = np.exp(-(x_vals - x_position) ** 2 / (2 * 5 ** 2))
        kernel = kernel / sum(kernel)
        smoothed_vals[x_position] = sum(array * kernel)
    return smoothed_vals
