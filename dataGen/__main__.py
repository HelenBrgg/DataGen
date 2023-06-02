import tensorflow as tf
import yaml
import numpy as np
import pandas as pd
from utils import utils
from seeddata_reader import seeddata_reader as sr
from base_editor import base_editor as be
from pattern_generator.projection import sine, random_walk
from pattern_generator import anomalies

from elevation_profile_generator import elevation_profile as ep

# Read-in data or create dummy data


def read_in(mode, data):
    if mode == "dummy_data":
        Smat = pd.DataFrame([data['dummy']])
    elif mode == "seed_data":
        datapath = data['datapath']
        csvs = data['csvs']
        files = data['files']
        text_list = sr.dateien_lesen(datapath, csvs, files)
        Smat = sr.concat_datafiles(text_list)
    return Smat


def extend_data(Smat, extend_data):
    output_path = extend_data['path_output']
    for series in extend_data['series_list']:
        for standardization in series['standardizing']:
            Smat[standardization['column']] = be.standardize(
                Smat[standardization['column']], standardization['desired_mean'])
        if series['baseediting']['stretching']['factor'] != None:
            Smat = be.stretch(
                series['baseediting']['stretching']['factor'], Smat)
        if series['baseediting']['noising']['factor'] != None:
            Smat = be.noise(
                series['baseediting']['noising']['factor'], Smat)
        if series['baseediting']['concatenating']['times'] != None:
            Smat = be.concatenate(
                series['baseediting']['concatenating']['times'], Smat)
        if series['baseediting']['smoothing']['factor'] != None:
            Smat = be.smooth(
                series['baseediting']['smoothing']['factor'], Smat)
        for projection in series['projections']:
            if projection['type'] == sine:
                Smat[projection['column']] = sine.sine(
                    Smat[projection['column']], projection['frequency'])
            if projection['type'] == random_walk:
                Smat[projection['column']] = random_walk.random_walk(
                    Smat[projection['column']], projection['factor'])
        for anomaly in series['anomalies']:
            Smat.iloc[:, anomaly['column']] = Smat.iloc[:, anomaly['column']].replace(anomalies.anomalize(
                anomaly['type'], Smat.iloc[:, anomaly['column']], anomaly['position'], anomaly['half_width'], anomaly['height_factor']))
    Smat.to_csv(output_path + '/' +
                series['name']+'.csv', sep=';', encoding='utf-8')
    """# TODO test stretching
    df_small = be.stretching(0.5, df)
    df_big = be.stretching(1.5, df)
    # TODO test concatenating
    df_concatenated = be.concatenate(5, df)
    # TODO test noising
    df_noisy = be.noising(0.01, df_big)

    # smooth because too much noise is left after shrinking
    # create new function that does smoothing for whole dataframe
    for column in df_small:
        df_small[column] = utils.smooth(0.1, df_small[column])
    # create file structure for output data
    # TODO test sine
    df_sine = sine.sine(df_big["Spannung_PL (2)"], 0.00001)
    # TODO test random walk
    df_random_walk = random_walk.random_walk(df_big["Spannung_PL (2)"])
    # TODO test anomalies
    print()
    df_small.iloc[:, 1] = df_small.iloc[:, 1].replace(anomalies.anomalize(
        "bell", df_small.iloc[:, 1], 20000, 100, df_small.iloc[:, 1].max()*2))
    df_small.iloc[:, 2] = df_small.iloc[:, 2].replace(anomalies.anomalize(
        "square", df_small.iloc[:, 2], 20000, 100,  df_small.iloc[:, 2].max()*2))
    df_small.to_csv("output_data/out_small.csv", encoding='utf-8')
    df_big.to_csv("output_data/out_big.csv", encoding='utf-8')
    df_concatenated.to_csv(
        "output_data/out_concatenated.csv", encoding='utf-8')
    df_noisy.to_csv("output_data/out_noisy.csv", encoding='utf-8')
    df_sine.to_csv("output_data/out_sine.csv", encoding='utf-8')
    df_random_walk.to_csv("output_data/out_random_walk.csv", encoding='utf-8')
    return df_small"""


def generate(file, csv_list, file_list=None):
    Smat = sr.dateien_lesen(file, csv_list, file_list)
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

    distances = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2,
                 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 19]

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
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        data = config['data']
        mode = data['mode']
        Smat = read_in(mode, data)
        extention_data = config['extend']
        extend_data(Smat, extention_data)

        # generate()

        # all parameters in the extend function itself... not so nice

        # extend_data(Smat)
        # generate("output_data", ['out_big.csv'])
