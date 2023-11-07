import tensorflow as tf
from scipy.stats import norm
import numpy as np


def calculate_received_coating1(substance_coefs, duration, distances, distribution_coefs):
    received_coating = np.zeros(duration)
    spread_length = int(len(distances))
    half_spread_length = int(len(distances)/2)
    scale_factors = np.array(distribution_coefs)*5

    for i in range(0, duration):
        # distribution for each time step, the distribution changes according to some parameter, sometimes narrower, sometimes wider
        coefs = tf.constant(
            norm.pdf(distances, scale=scale_factors[i]*2), dtype=tf.float32)
        # coefs = tf.round(coefs*100)/100
        # the actuall mass that is distributed through the cone
        spread = substance_coefs[i]*coefs
        if(i <= half_spread_length):
            received_coating[0:i+half_spread_length +
                             1] += spread[half_spread_length-i:]
        elif(i+half_spread_length >= duration):
            received_coating[i-half_spread_length:] += spread[:
                                                              spread_length-((i+half_spread_length)-duration+1)]
        else:
            received_coating[i-half_spread_length:i+half_spread_length +
                             1] += spread
    return received_coating
