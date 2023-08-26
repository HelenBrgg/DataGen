import numpy as np
from scipy.stats import norm


def anomalize(kind, array, position, half_width, height):
    if kind == "square":
        square(array, position, half_width, height)
    elif kind == "bell":
        bell(array, position, half_width, height)


def square(array, position, half_width, height):

    square = np.full(shape=half_width*2, fill_value=height *
                     array.values[position]+array.values[position])
    print('square')
    print(square)
    array[position-half_width:position+half_width] = square
    return array


def bell(array, position, scale, height):
    data = np.arange(scale*8)
    height = array.values[position]*height
    k = height*scale*np.sqrt(2*np.pi)
    pdf = k*norm.pdf(data, loc=scale*4, scale=scale)
    print(array.values[position])
    #height = height*array.values[position]
    pdf = pdf + array.values[position]
    print('bell')
    print(array[position-scale*4:position+scale * 4], pdf)
    array[position-scale*4:position+scale * 4] = pdf
    return array
