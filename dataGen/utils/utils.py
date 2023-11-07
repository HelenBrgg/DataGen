import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d


def smooth(factor, array):
    smoothed_ts = pd.Series(gaussian_filter1d(array.values, sigma=factor))
    return smoothed_ts
