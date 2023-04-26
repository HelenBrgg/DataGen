import tensorflow as tf
import numpy as np
import pandas as pd
from seeddata_reader import seeddata_reader as sr
from base_editor import base_editor as be

from elevation_profile_generator import elevation_profile as ep

# read-in Data or create dummy data
Dummy_Smat = pd.DataFrame([[1, 1, 1, 1, 4, 1, 4, 1, 2, 1], [2, 2, 1, 8, 2, 2, 2, 3, 1, 1],
                          [1, 8, 1, 1, 5, 1, 3, 1, 1, 1], [1, 3, 1, 5, 4, 8, 2, 1, 3, 1], ])
print(type(int))
text_list = sr.dateien_lesen("data")
df = sr.concat_datafiles(text_list['TS-PL-20'])  # Dummy_Smat
Seeddata_Smat = df.astype(
    {'Spannung_PL (2)': 'float', 'Strom_PL (3)': 'float', 'Drahtvorschub': 'float'})
print("df")
print(Seeddata_Smat)
df_small = be.stretching(0.5, Seeddata_Smat)
df_big = be.stretching(1.5, Seeddata_Smat)
df_concatenated = be.concatenate(5, Seeddata_Smat)
print("df_small")
print(df_small)
print("df_big")
print(df_big)
print


def main():
    # create elevation profile
    Smat = Seeddata_Smat

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


# if __name__ == "__main__":
 #   main()
