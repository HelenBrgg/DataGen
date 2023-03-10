import tensorflow as tf

import elevation_profile.elevation_profile as elevation_profile


def main(sys_args: List[str]) -> None:

    Smat = tf.constant([[1, 2, 3, 1, 2, 3, 1], [1, 0, 1, 0, 1, 0, 1]
                       [0.1, 0.3, 0.4, 0.5, 0.6, 0.1, 0.3]], dtype=tf.float32)

    length = 3
    duration = 7
    r1 = -3

    substance_vals = tf.constant([[1, .0.02]])
    substance_coefs = substance_vals @ Smat

    distribution_vals = tf.constant([[.5, 0]])
    distribution_coefs = tf.reshape(distribution_vals @ Smat, shape=(-1, 1))

    p_vec = tf.reshape(tf.range(0, duration), shape=(-1, 1))

    r_vec = tf.reshape(tf.range(0, duration), shape=(1, -1))

    distances_over_time = tf.math.abs(p_vec - r_vec)

    distribution_over_time = elevation_profile.calculate_distribution_over_time(
        duration, distances_over_time, distribution_coefs)

    substance_coefs_unpacked = tf.unstack(tf.reshape(substance_coefs, [-1]))

    received_coating = elevation_profile.calculate_received_coating(
        substance_coefs_unpacked, distribution_over_time)

    elevation_profile = elevation_profile.apply_received_coating_on_workpiece(
        r1, received_coating, length, duration)

    print(elevation_profile)
