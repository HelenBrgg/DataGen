import numpy as np
import pandas as pd
import os

from scipy.stats import norm
from ..utils import utils

# TODO unterscheiden, von wo aufgerufen wird und nach filestruktur


def read_seed_data(pfad,  csv_list, file_list=None):
    # Reads files from the 'data' directory
    # Returns a dictionary containing DataFrames from subfiles:
    # text_list = {TS-PL-20: {TS-PL-20_01.csv: [Spannung Strom ...], TS-PL-20_02.csv: [Spannung Strom ...], ...}, TS-PL-21: {TS-PL-21_01.csv: [Spannung Strom ...]}}
    filenames = sorted(os.listdir(pfad))  # Liste der Dateien
    text_list = {}
    subfilenames = []
    for fname in filenames:
        if fname in file_list:
            subfilenames = sorted(os.listdir(pfad + '/' + fname))
            df = {}
            for subfname in subfilenames:
                # exclude files that are not needed for this usecase
                if subfname in csv_list:
                    df_subfile = pd.read_csv(
                        pfad + '/' + fname + '/' + subfname, delimiter=';', skiprows=[1], encoding='latin-1', index_col=False)
                    df_subfile = df_subfile.replace(',', '.', regex=True)
                    # include all known constant data
                    #df_subfile = df_subfile.drop(columns=['Date'])
                    df_subfile = df_subfile.dropna(axis=1).astype(
                        'float')
                    df[subfname] = df_subfile
            text_list[fname] = df
    return text_list


def concat_datafiles(file_list):
    # Concatenates all subfiles in a dataframe and returns the dataframe
    df_concat = pd.DataFrame()
    for file in file_list:
        fileA = file_list[file]
        for subfile in fileA:
            x_position = len(df_concat)
            next_file = fileA[subfile]
            df_concat = pd.concat([df_concat, next_file],
                                  axis=0)  # .reset_index(drop=True)
            df_concat = df_concat  # .reset_index(drop=True)
            # smoothes the cuts
            # TODO test smoothing
            if len(df_concat) > len(fileA[subfile]):
                for column in range(1, len(df_concat.axes[1])):
                    df_concat.iloc[x_position-100:x_position+100, column] = utils.smooth(5,
                                                                                         df_concat.iloc[x_position-100:x_position+100, column])
    index_step = df_concat.iloc[1:2, 0]
    df_concat.iloc[:, 0] = [
        i * index_step for i in list(range(0, len(df_concat)))]
    return df_concat.astype('float')
