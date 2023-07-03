import tensorflow as tf
import yaml
import math
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


def extend_data(Smat_in, extend_data):
    output_path = extend_data['path_output']
    for series in extend_data['series_list']:
        Smat = Smat_in.copy()
        for standardization in series['standardizing']:
            if standardization['desired_mean'] != None:
                Smat.iloc[:, standardization['column']] = be.standardize_and_normalize(
                    Smat.iloc[:, standardization['column']], standardization['desired_mean'])
        if series['baseediting']['stretching']['factor'] != None:
            print(Smat)
            print(type(Smat))
            Smat = be.stretch(
                series['baseediting']['stretching']['factor'], Smat, 'linear')
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
                print('anomaly')
                Smat.iloc[:, anomaly['column']] = Smat.iloc[:, anomaly['column']].replace(anomalies.anomalize(
                    anomaly['type'], Smat.iloc[:, anomaly['column']], anomaly['position'], anomaly['half_width'], Smat.iloc[:, anomaly['column']].max()*anomaly['height_factor']))
        Smat.to_csv(output_path + '/' +
                    series['name']+'.csv', sep=';', encoding='utf-8')


def generate(output_path, series_name, generation_data):
    Data = pd.read_csv(
        output_path + '/' + series_name, delimiter=';', encoding='latin-1', index_col=0)

    Smat = tf.constant([Data[column] for column in Data], dtype=tf.float32)
    # length of the piece
   # length = len(Smat[1]) + generation_data['length']
    # duration of the spraying process
    duration = len(Smat[1]) + generation_data['duration']
    # position of the nozzle at time 1 (nozzle starts moving)
    # r1 = generation_data['start_position']

    # which features influence the mass in the end? (speed and temperature maybe)
    substance_vals = tf.constant([generation_data['substance_vals']])
    substance_coefs = substance_vals @ Smat
    print('substance_coefs:')
    print(substance_coefs)
    substance_coefs_check = pd.DataFrame(substance_coefs)
    print(substance_coefs_check.isnull().sum())
    # print(substance_coefs.isnull().sum())
    # which features influene the distribution (higher voltage leads to wider spread)

    distribution_vals = tf.constant([generation_data['distribution_vals']])
    distribution_coefs = tf.reshape(distribution_vals @ Smat, shape=(-1, 1))
    print('distribution_coefs:')
    print(distribution_coefs)
    distribution_coefs_check = pd.DataFrame(distribution_coefs)
    print(distribution_coefs_check.isnull().sum())
    # distances = generation_data['distances']
    a_list = list(range(1, 10001))
    b_list = a_list[::-1]
    c_list = a_list = list(range(0, 10001))
    distances = b_list+c_list
    # distances = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2,
    #             1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # eg:
    # [[0.   0.05 0.24 0.4  0.24 0.05 0.  ]
    # [0.   0.025 0.075 0.8  0.075 0.025 0. ]
    # [0.   0.   0.   0.05 0.24 0.4  0.24]]
    distribution_over_time = ep.calculate_distribution_over_time(
        duration, distances, distribution_coefs)
    print('distribution_over_time:')
    print(distribution_over_time)
    print(distribution_over_time[:1020, 1020])
    distribution_over_time_check = pd.DataFrame(distribution_over_time)
    print(distribution_over_time_check.isnull().sum())
    substance_coefs_unpacked = tf.unstack(tf.reshape(substance_coefs, [-1]))
    received_coating = ep.calculate_received_coating(
        substance_coefs_unpacked, distribution_over_time, duration)
    print('received_coating:')
    print(received_coating)
    print(received_coating[10])
    received_coating_check = pd.DataFrame(received_coating)
    print(received_coating_check.isnull().sum())
   # elevation_profile = ep.apply_received_coating_on_workpiece(
    # r1, received_coating, length, duration)
    if(Data.columns.str.contains("Robotergeschwindigkeit").any()):
        speed_of_robot = Data.iloc[::, 7]
        if (speed_of_robot.max() == 50 and speed_of_robot.min() == 50):
            elevation_profile = received_coating/2
            elevation_profile = be.stretch(
                2, elevation_profile, 'pad', 'forward')
        if (speed_of_robot.max() == 75 and speed_of_robot.min() == 75):
            elevation_profile = received_coating/3
            elevation_profile = be.stretch(
                3, elevation_profile, 'pad', 'forward')
        if (speed_of_robot.max() == 100 and speed_of_robot.min() == 100):
            elevation_profile = received_coating/4
            elevation_profile = be.stretch(
                4, elevation_profile, 'pad', 'forward')
        else:
            elevation_profile = received_coating
    else:
        elevation_profile = received_coating
    print('elevation_profile:')
    print(elevation_profile)

    Data['elevation_profile'] = elevation_profile
    print(Data)
    Data.to_csv(
        generation_data['output_path']+'/'+'profile_' + series_name)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        data = config['data']
        mode = data['mode']
       # Smat = read_in(mode, data)
        extention_data = config['extend']
        #extend_data(Smat, extention_data)
        for series in extention_data['series_list']:
            generate(extention_data['path_output'],
                     series['name']+'.csv', series['generate'])
