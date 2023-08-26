import pandas as pd
import numpy as np
from dataGen.utils import utils

# factor times the size of the dataframe equals the new size


def stretch(factor, dataframe, method, limit_direction=False):
    print(dataframe)
    if factor < 1:
        if factor >= 0.5:
            steps = round(1/(1-factor))
            # drops every "step"-th row
            df_stretched = dataframe.drop(index=dataframe.index[::steps])
        else:
            df_stretched = dataframe.iloc[::round(1/factor)]
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
        if method == 'linear':
            df_stretched = df_stretched_nan.interpolate(
                method=method).reset_index(drop=True)
        if method == 'pad':
            df_stretched = df_stretched_nan.interpolate(
                method=method, limit_direction=limit_direction).reset_index(drop=True)

        print('df_stretched', df_stretched)
    return df_stretched


def concatenate(times, smooth_number, smooth_factor, dataframe):
    # dataframe times+1
    df_concat = dataframe
    for i in range(0, times):
        x_position = len(df_concat)
        df_concat = pd.concat([df_concat, dataframe], axis=0)
        df_concat = df_concat.reset_index(drop=True)
        # welche Anzahl Punkte? vlt abhängig von der differenz zwischen den beiden?
        for column in range(0, len(df_concat.axes[1])):
            df_concat.iloc[x_position-smooth_number:x_position+smooth_number, column] = utils.smooth(
                smooth_factor, df_concat.iloc[x_position-smooth_number:x_position+smooth_number, column])

    return df_concat


def noise(factor, dataframe):
    for column in dataframe:
        noise = np.random.normal(
            0, dataframe[column].var()*factor, dataframe[column].shape)
        dataframe[column] = dataframe[column] + noise
    return dataframe


def smooth(factor, dataframe):
    print(print(dataframe.dtypes))
    for column in dataframe:

        dataframe[column] = utils.smooth(factor, dataframe[column],)
        print('smooth', dataframe[column])
    return dataframe


def scale_and_shift_to_mean(column, desired_mean, min_val=0, max_val=2):
    # Scale to range [0, 2]
    normalized_data = min_val + (column - np.min(column)) * \
        (max_val - min_val) / (np.max(column) - np.min(column))

    # Shift to the desired mean
    shift = desired_mean - np.mean(normalized_data)
    shifted_data = normalized_data + shift

    return shifted_data
