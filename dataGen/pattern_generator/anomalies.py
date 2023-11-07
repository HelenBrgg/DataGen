import numpy as np
from scipy.stats import norm


def anomalize(kind, array, position, half_width, height):
    if kind == "square":
        square(array, position, half_width, height)
    elif kind == "bell":
        bell(array, position, half_width, height)


def square(array, position, half_width, height):
    # Create a square wave pattern
    # 'position' specifies the center position of the square wave.
    # 'half_width' determines the half-width of the square wave.
    # 'height' sets the height (amplitude) of the square wave.
    square = np.full(shape=half_width*2, fill_value=height *
                     array.values[position]+array.values[position])
    array[position-half_width:position+half_width] = square
    return array


def bell(array, position, scale, height):
    # 'position' specifies the center position of the bell curve.
    # 'scale' determines the scale of the bell curve.
    # 'height' sets the height of the bell curve.

    # Generate a sequence of data points based on the specified scale
    data = np.arange(scale*8)
    # Calculate the effective height for the bell curve
    height = array.values[position]*height
    # Calculate the normal distribution with the specified parameters
    k = height*scale*np.sqrt(2*np.pi)
    pdf = k*norm.pdf(data, loc=scale*4, scale=scale)

    pdf = pdf + array.values[position]

    array[position-scale*4:position+scale * 4] = pdf
    return array
