import numpy as np
from scipy.stats import norm


def anomalize():
    if kind == "square":
        square()
    elif kind == "bell":
        bell()


def square():

    return square


def bell(array, position, scale, height):
    data = np.arange(1, 1000, 1)
    pdf = norm.pdf(data, loc=500, scale=scale)
    height = height/pdf.max()
    pdf = pdf*height
    array[position-500:position+500-1] = array[position-500:position+500-1]+pdf
    return array
