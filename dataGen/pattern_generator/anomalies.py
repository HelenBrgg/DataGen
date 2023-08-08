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
    print('square')
    print(square)
    array_with_square[position-half_width:position+half_width] = square
    return array_with_square


def bell(array, position, scale, height):
    data = np.arange(scale*8)
    pdf = norm.pdf(data, loc=scale*4, scale=scale)
    height = height/pdf.max()
    pdf = pdf*height
    print('bell')
    print(array[position-scale*4:position+scale * 4], pdf)
    array[position-scale*4:position+scale * 4] = pdf
    return array
