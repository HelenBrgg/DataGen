import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt


def smooth(factor, array):
    smoothed_ts = pd.Series(gaussian_filter1d(array.values, sigma=factor))
    """ x_vals = np.arange(len(array))
    smoothed_vals = np.zeros(x_vals.shape)
    print('1')
    for x_position in x_vals:
        print(x_position)
        array = array.astype(float)
        if array.var() != 0:
            kernel = np.exp(-(x_vals - x_position) ** 2 /
                            (2 * array.var()*factor ** 2))
        else:
            kernel = np.exp(-(x_vals - x_position) ** 2 /
                            (2 * factor ** 2))
        kernel = kernel / sum(kernel)
        smoothed_vals[x_position] = sum(array * kernel)"""
    return smoothed_ts
