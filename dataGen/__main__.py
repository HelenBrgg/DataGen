import tensorflow as tf
import yaml
import pandas as pd
from .seeddata_reader import seeddata_reader as sr
from .base_editor import base_editor as be
from .pattern_generator.projection import sine, random_walk
from .pattern_generator import anomalies

from .elevation_profile_generator import elevation_profile as ep

# Read-in data or create dummy data


def read_in(mode, data):
    if mode == "dummy_data":
        Smat = pd.DataFrame(data['dummy'])
        print(Smat)
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
            if standardization['desired_mean'] != None:
                Smat.iloc[:, standardization['column']] = be.standardize(
                    Smat.iloc[:, standardization['column']], standardization['desired_mean'])
        if series['baseediting']['stretching']['factor'] != None:
            print(Smat)
            print(type(Smat))
            Smat = be.stretch(
                series['baseediting']['stretching']['factor'], Smat)
            print(Smat)
        if series['baseediting']['noising']['factor'] != None:
            Smat = be.noise(
                series['baseediting']['noising']['factor'], Smat)
        if series['baseediting']['concatenating']['times'] != None:
            Smat = be.concatenate(
                series['baseediting']['concatenating']['times'], series['baseediting']['concatenating']['smooth_number'], series['baseediting']['concatenating']['smooth_factor'], Smat)
        if series['baseediting']['smoothing']['factor'] != None:
            Smat = be.smooth(
                series['baseediting']['smoothing']['factor'], Smat)
        for projection in series['projections']:
            if projection['type'] == 'sine':
                Smat.iloc[:, projection['column']] = sine.sine(
                    Smat.iloc[:, projection['column']], projection['frequency'], projection['amplitude'])
            if projection['type'] == 'random_walk':
                Smat.iloc[:, projection['column']] = random_walk.random_walk(
                    Smat.iloc[:, projection['column']], projection['factor'])
        for anomaly in series['anomalies']:
            if anomaly['type'] != None:
                Smat.iloc[:, anomaly['column']] = Smat.iloc[:, anomaly['column']].replace(anomalies.anomalize(
                    anomaly['type'], Smat.iloc[:, anomaly['column']], anomaly['position'], anomaly['half_width'], anomaly['height_factor']))
        Smat.to_csv(output_path + '/' +
                    series['name']+'.csv', sep=';', encoding='utf-8')


def generate(output_path, series_name, generation_data):
    Smat = pd.read_csv(
        output_path + '/' + series_name, delimiter=';', encoding='latin-1', index_col=0)

    Smat = tf.constant([Smat[column] for column in Smat], dtype=tf.float32)
    print(Smat)
    length = len(Smat[1]) + generation_data['length']
    duration = len(Smat[1]) + generation_data['duration']
    print(duration)
    # position of the nozzle at time 1 (nozzle starts moving)
    r1 = generation_data['start_position']

    substance_vals = tf.constant([generation_data['substance_vals']])
    substance_coefs = substance_vals @ Smat
    print('substance_coefs:')
    print(substance_coefs)

    distribution_vals = tf.constant([generation_data['distribution_vals']])
    distribution_coefs = tf.reshape(distribution_vals @ Smat, shape=(-1, 1))

    distances = generation_data['distances']
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
       # for series in extention_data['series_list']:
        #    generate(extention_data['path_output'],
        #            series['name']+'.csv', series['generate'])
