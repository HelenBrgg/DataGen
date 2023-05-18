import numpy as np
from scipy.stats import norm


def anomalize(kind, array, position, half_width, height):
    if kind == "square":
        square(array, position, half_width, height)
    elif kind == "bell":
        bell(array, position, half_width, height)


def square(array, position, half_width, height):
    array_with_square = array
    square = np.full(shape=half_width*2, fill_value=height)
    print(array_with_square)
    array_with_square[position-half_width:position+half_width] = square
    print(array_with_square[position-half_width:position+half_width])
    print(array_with_square)
    return array_with_square


def bell(array, position, scale, height):
    data = np.arange(1, 1000, 1)
    pdf = norm.pdf(data, loc=500, scale=scale)
    height = height/pdf.max()
    pdf = pdf*height
    array[position-500:position+500-1] = array[position-500:position+500-1]+pdf
    return array
