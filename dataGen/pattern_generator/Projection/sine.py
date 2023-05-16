import numpy as np


def sine(array, frequency):
    amplitude = array.max() - array.min()
    length = len(array)
    time = np.arange(0, length)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time)
    feature_with_sine = np.add(array, sine_wave)
    return feature_with_sine