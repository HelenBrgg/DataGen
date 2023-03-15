import tensorflow as tf
from scipy.stats import norm
import numpy as np
import pandas as pd


def calculate_distribution_over_time(duration, distances_over_time, distribution_coefs):
    distribution_matrix = np.zeros(shape=(duration, duration), dtype=float)
    for x in range(0, duration):
        coefs = tf.constant(norm.pdf(
            distances_over_time[x], scale=distribution_coefs[x]), dtype=tf.float32)
        coefs = tf.round(coefs*100)/100
        distribution_matrix[x] = distribution_matrix[x]+coefs
    print(pd.DataFrame(distribution_matrix))
    return distribution_matrix


def calculate_received_coating(substance_coefs, distribution_over_time, duration):
    received_coating = np.zeros(duration)
    for i in range(0, duration):
        spread = substance_coefs[i]*distribution_over_time[i]
        received_coating = spread + received_coating
    return received_coating


def apply_received_coating_on_workpiece(start_of_nozzle, received_coating, length_of_piece, duration_of_measures):
    elevation_profile = np.zeros(length_of_piece)
    if (start_of_nozzle >= 0 and duration_of_measures+start_of_nozzle >= length_of_piece):
        elevation_profile[start_of_nozzle:length_of_piece-1] = tf.slice(
            received_coating, begin=[0], size=[length_of_piece-start_of_nozzle])
    elif start_of_nozzle >= 0 and (duration_of_measures+start_of_nozzle) <= length_of_piece:
        elevation_profile[start_of_nozzle:duration_of_measures +
                          start_of_nozzle] = received_coating
    elif start_of_nozzle <= 0 and (duration_of_measures+start_of_nozzle) <= length_of_piece:
        elevation_profile[0:duration_of_measures+start_of_nozzle] = tf.slice(
            received_coating, begin=[-start_of_nozzle], size=[duration_of_measures+start_of_nozzle])
    elif start_of_nozzle <= 0 and (duration_of_measures+start_of_nozzle) >= length_of_piece:
        elevation_profile[0:length_of_piece] = tf.slice(
            received_coating, begin=[-start_of_nozzle], size=[length_of_piece])
    return elevation_profile
    # tests:
    # elevation_profile = apply_received_coating_on_workpiece(-1,received_coating,10,7)
    # expected:[0.94499, 0.97, 1.395, 1.19, 0.95500004, 1.21, 0., 0., 0., 0.]
    # elevation_profile = apply_received_coating_on_workpiece(-1,received_coating,5,7)
    # expected:[0.94499, 0.97, 1.395, 1.19, 0.95500004]
    # elevation_profile = apply_received_coating_on_workpiece(2,received_coating,10,7)
    # expected:[0., 0., 0.94499, 0.97, 1.395, 1.19, 0.95500004, 1.21, 0., 0.]
    # elevation_profile = apply_received_coating_on_workpiece(2,received_coating,3,7)
    # expected:[0., 0., 0.94499]
