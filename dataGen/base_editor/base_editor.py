import pandas as pd
import numpy as np
from utils import utils


def stretch(factor, dataframe):
    print(dataframe)
    if factor < 1:
        steps = round(1/(1-factor))
        df_stretched = dataframe.drop(index=dataframe.index[::steps])
        df_stretched = df_stretched.reset_index(drop=True)
    else:
        new_length = int(len(dataframe) * factor)

        # create a new index with evenly spaced values
        new_index = np.linspace(dataframe.index.min(),
                                dataframe.index.max(), new_length)
        for x in range(0, len(new_index)):
            if int(new_index[x]) > int(new_index[x-1]):
                new_index[x] = int(new_index[x])

        # reindex the data frame with the new index, filling in missing values with NaNs
        df_stretched_nan = dataframe.reindex(new_index, fill_value=np.nan)
        df_stretched = df_stretched_nan.interpolate(
            method='linear').reset_index(drop=True)
        print(df_stretched)
    return df_stretched


def concatenate(times, dataframe):
    df_concat = dataframe
    for i in range(0, times):
        x_position = len(df_concat)
        df_concat = pd.concat([df_concat, dataframe], axis=0)
        df_concat = df_concat.reset_index(drop=True)
        # welche Anzahl Punkte? vlt abhängig von der differenz zwischen den beiden?
        for column in range(0, len(df_concat.axes[1])):
            df_concat.iloc[x_position-100:x_position+100, column] = utils.smooth(
                5, df_concat.iloc[x_position-100:x_position+100, column])

    return df_concat


def noise(factor, dataframe):
    for column in dataframe:
        noise = np.random.normal(
            0, dataframe[column].var()*factor, dataframe[column].shape)
        dataframe[column] = dataframe[column] + noise
    return dataframe


def smooth(factor, dataframe):
    for column in dataframe:
        dataframe[column] = utils.smooth(factor, dataframe[column],)
        print(dataframe[column])
    return dataframe


def standardize(column, desired_mean):
    mean = np.mean(column)
    std = np.std(column)

    normalized_data = (column - mean) / std
    # Assuming the desired range has the same standard deviation as the original data
    desired_std = std

    calibrated_data = (normalized_data * desired_std) + desired_mean
    return calibrated_data
