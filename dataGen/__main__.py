import tensorflow as tf
import numpy as np
from seeddata_reader import seeddata_reader as sr

from elevation_profile import elevation_profile as ep

Dummy_Smat = tf.constant([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype=tf.float32)
text_list = sr.dateien_lesen("data")
df = text_list['TS-PL-20']['TS-PL-20_01.csv']
df.index = np.array([i.replace(",", ".") for i in df.index])
Seeddata_Smat = tf.constant([df['Spannung_PL (2)'].values.astype(float), df['Strom_PL (3)'].values.astype(
    float), df['Drahtvorschub'].values.astype(float)], dtype=tf.float32)


def main():
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

    p_vec = tf.reshape(tf.range(0, duration), shape=(-1, 1))

    r_vec = tf.reshape(tf.range(0, duration), shape=(1, -1))

    #distances_over_time = tf.math.abs(p_vec - r_vec)
    #print('distances over time:')
    # print(distances_over_time)

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
    main()
