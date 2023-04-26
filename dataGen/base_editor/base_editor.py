import pandas as pd
import numpy as np
from utils import utils


def stretching(factor, dataframe):
    if factor < 1:
        steps = round(1/(1-factor))
        df_stretched = dataframe.drop(index=dataframe.index[::steps])
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
        print('df_stretched_nan')
        print(df_stretched_nan)
        df_stretched = df_stretched_nan.interpolate(method='linear')
        print('df_stretched')
        print(df_stretched)
        df_stretched = df_stretched.reset_index(drop=True)
    return df_stretched


def concatenate(times, dataframe):
    df_concat = dataframe
    for i in range(0, times):
        x_position = len(df_concat)
        df_concat = pd.concat([df_concat, dataframe], axis=0)
        df_concat = df_concat.reset_index(drop=True)
        # welche Anzahl Punkte? vlt abhängig von der differenz zwischen den beiden?
        for column in range(0, len(df_concat.axes[1])):
            df_concat.iloc[x_position-10:x_position+10, column] = utils.smooth(
                df_concat.iloc[x_position-10:x_position+10, column])

    return df_concat


def noising(factor, dataframe):

    return df_concat
