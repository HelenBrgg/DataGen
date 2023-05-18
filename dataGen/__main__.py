import tensorflow as tf
import numpy as np
import pandas as pd
from utils import utils
from seeddata_reader import seeddata_reader as sr
from base_editor import base_editor as be
from pattern_generator.projection import sine, random_walk
from pattern_generator import anomalies

from elevation_profile_generator import elevation_profile as ep


def read_in(data=None):
    if data is None:
        # read-in Data or create dummy data
        Dummy_Smat = pd.DataFrame([[1, 1, 1, 1, 4, 1, 4, 1, 2, 1], [2, 2, 1, 8, 2, 2, 2, 3, 1, 1],
                                   [1, 8, 1, 1, 5, 1, 3, 1, 1, 1], [1, 3, 1, 5, 4, 8, 2, 1, 3, 1], ])
        Smat = Dummy_Smat
    else:
        # still need to adjust how to decide which data to take, so far in the data_reader module... not good
        text_list = sr.dateien_lesen(data)
        df = sr.concat_datafiles(text_list['TS-PL-20'])  # test smoothing
        # check if float is not already set elsewhere
        Seeddata_Smat = df.astype(
            {'Spannung_PL (2)': 'float', 'Strom_PL (3)': 'float', 'Drahtvorschub': 'float'})
        Smat = Seeddata_Smat
    return Smat


def extend_data(df):
    # TODO test stretching
    df_small = be.stretching(0.5, df)

    df_big = be.stretching(1.5, df)
    # TODO test concatenating
    df_concatenated = be.concatenate(5, df)
    # TODO test noising
    df_noisy = be.noising(0.01, df_big)
    df_small.to_csv("output_data/out_before.csv", encoding='utf-8')
    # smooth because too much noise is left after shrinking
    # create new function that does smoothing for whole dataframe
    for column in df_small:
        df_small[column] = utils.smooth(0.1, df_small[column])
    # create file structure for output data
    df_small.to_csv("output_data/out.csv", encoding='utf-8')
    # TODO test sine
    df_sine = sine.sine(df_big["Spannung_PL (2)"], 0.00001)
    # TODO test random walk
    df_random_walk = random_walk.random_walk(df_big["Spannung_PL (2)"])
    print(df_small['Spannung_PL (2)'])
    # TODO test anomalies
    df_small['Spannung_PL (2)'] = anomalies.anomalize(
        "bell", df_small['Spannung_PL (2)'], 20000, 100, df_small['Spannung_PL (2)'].max()*2)
    df_small['Spannung_PL (2)'] = anomalies.anomalize(
        "square", df_small['Spannung_PL (2)'], 20000, 100,  df_small['Spannung_PL (2)'].max()*2)
    return df_small


def generate(Smat):
    length = len(Smat[1]) - 3
    duration = len(Smat[1])
    print(duration)
    r1 = -3  # position of the nozzle at time 1 (nozzle starts moving)

    substance_vals = tf.constant([[1, .0, .5]])
    substance_coefs = substance_vals @ Smat
    print('substance_coefs:')
    print(substance_coefs)

    distribution_vals = tf.constant([[0, 0.5, 0]])
    distribution_coefs = tf.reshape(distribution_vals @ Smat, shape=(-1, 1))

    distances = [4, 3, 2, 1, 0, 1, 2, 3, 4]

    distribution_over_time = ep.calculate_distribution_over_time(
        duration, distances, distribution_coefs)
    print(distribution_over_time)
    substance_coefs_unpacked = tf.unstack(tf.reshape(substance_coefs, [-1]))

    received_coating = ep.calculate_received_coating(
        substance_coefs_unpacked, distribution_over_time, duration)
    print(received_coating)
    elevation_profile = ep.apply_received_coating_on_workpiece(
        r1, received_coating, length, duration)

    print('elevation_profile:')
    print(elevation_profile)


if __name__ == "__main__":
    Smat = read_in("data")
    df_small = extend_data(Smat)
    print(df_small)
#    generate()
