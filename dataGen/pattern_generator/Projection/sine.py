import numpy as np


def sine(array, frequency, amplitude=None):
    if amplitude is not None:
        amplitude = amplitude
    else:
        # Calculate amplitude as 30% of the range of values in the input array
        amplitude = (array.max() - array.min()) * 0.3

    length = len(array)
    # Create a time vector based on the length
    time = np.arange(0, length)

    # Generate a sine wave with the specified frequency and calculated amplitude
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time)
    feature_with_sine = np.add(array, sine_wave)

    return feature_with_sine
