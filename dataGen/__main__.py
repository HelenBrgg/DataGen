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
    # reads in data and concats all datafiles
    if mode == "dummy_data":
        Smat = pd.DataFrame(data['dummy'])
    elif mode == "seed_data":
        datapath = data['datapath']
        csvs = data['csvs']
        files = data['files']
        text_list = sr.read_seed_data(datapath, csvs, files)
        Smat = sr.concat_datafiles(text_list)
    return Smat


def extend_data(Smat_in, extend_data):
    # extends data, e.g. smooth, concatenate, adding anomalies and patterns
    output_path = extend_data['path_output']
    for series in extend_data['series_list']:
        Smat = Smat_in.copy()
        for scale in series['standardizing']:
            if scale['column'] != None:
                if scale['desired_mean'] != None:
                    Smat.iloc[:, scale['column']] = be.scale(
                        Smat.iloc[:, scale['column']], scale['min_val'], scale['max_val'], scale['desired_mean'])
                else:
                    Smat.iloc[:, scale['column']] = be.scale(
                        Smat.iloc[:, scale['column']], scale['min_val'], scale['max_val'])

        if series['baseediting']['stretching']['factor'] != None:
            print('stretching', Smat.dtypes)
            Smat = be.stretch(
                series['baseediting']['stretching']['factor'], Smat, series['baseediting']['stretching']['method'])
            print('after stretching', Smat.dtypes)
        if series['baseediting']['noising']['factor'] != None:
            print('noise', Smat.dtypes)
            Smat = be.noise(
                series['baseediting']['noising']['factor'], Smat)
            print('after noise', Smat.dtypes)
        if series['baseediting']['concatenating']['times'] != None:
            print('concatenate', Smat.dtypes)
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
                    Smat.iloc[:, projection['column'],  projection['amplitude']])
        for anomaly in series['anomalies']:
            if anomaly['type'] != None:
                print('anomaly')
                Smat.iloc[:, anomaly['column']] = Smat.iloc[:, anomaly['column']].replace(anomalies.anomalize(
                    anomaly['type'], Smat.iloc[:, anomaly['column']], anomaly['position'], anomaly['half_width'], anomaly['height_factor']))
        Smat.to_csv(output_path + '/' +
                    series['name']+'.csv', sep=';', encoding='utf-8')


def generate(output_path, series_name, generation_data):
    Data = pd.read_csv(
        output_path + '/' + series_name, delimiter=';', encoding='latin-1', index_col=[0])

    Smat = tf.constant([Data[column] for column in Data], dtype=tf.float32)

    ####for exponential relation####
    # Transpose to make columns as rows#
    # columns = tf.unstack(Smat_old)#

    # Apply transformations to the desired columns#
    #columns[1] = columns[1]**1.3#
    #columns[2] = columns[2]**2#
    #columns[3] = columns[3]**0.4#

    # Re-assemble and transpose back to get the modified Smat#
    #Smat = tf.stack(columns)#
    #Smat_np = Smat.numpy()#
    #Smat_old_np = Smat_old.numpy()#
    ################################

    duration = len(Smat[1]) + generation_data['duration']

    # which features influence the mass in the end? (speed and temperature maybe)
    substance_vals = tf.constant([generation_data['substance_vals']])
    substance_coefs = substance_vals @ Smat
    print('substance_coefs:')
    print(substance_coefs)

    # which features influence the distribution (higher voltage leads to wider spread)

    distribution_vals = tf.constant([generation_data['distribution_vals']])
    distribution_coefs = tf.reshape(distribution_vals @ Smat, shape=(-1, 1))

    half_width = generation_data['conesize']
    a_list = list(range(1, half_width + 1))
    b_list = a_list[::-1]
    c_list = a_list = list(range(0, half_width + 1))
    distances = b_list+c_list

    # eg:
    # [[0.   0.05 0.24 0.4  0.24 0.05 0.  ]
    # [0.   0.025 0.075 0.8  0.075 0.025 0. ]
    # [0.   0.   0.   0.05 0.24 0.4  0.24]]

    substance_coefs_unpacked = tf.unstack(tf.reshape(substance_coefs, [-1]))

    elevation_profile2 = ep.calculate_received_coating1(
        substance_coefs_unpacked, duration, distances, distribution_coefs)

    Data['elevation_profile2'] = elevation_profile2

    Data.to_csv(
        generation_data['output_path']+'/'+'profile_' + series_name)
    Data_subsampled = be.stretch(
        generation_data['final_subsampling'], Data, 'linear')
    Data_subsampled.to_csv(
        generation_data['output_path_subsampled']+'/'+'profile_' + series_name)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        #read in config
        config = yaml.safe_load(f)
        data = config['data']
        mode = data['mode']
        extention_data = config['extend']
        # read in seed data
        Smat = read_in(mode, data)
        # transform and clean data, add baseediting, add anomalies and patterns

        extend_data(Smat, extention_data)
        # extended data gets saved as csv in outputpath
        for series in extention_data['series_list']:
            generate(extention_data['path_output'],
                     series['name']+'.csv', series['generate'])
