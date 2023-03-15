import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
from sklearn.linear_model import LinearRegression

import tensorflow as tf
import tensorflow_probability as tfp
from scipy.stats import norm


def dateien_lesen(pfad):
    filenames = sorted(os.listdir(pfad))  # Liste der Dateien
    text_list = {}
    print(filenames)
    for fname in filenames:
        if fname != '.DS_Store' and fname != 'Thumbs.db' and fname != 'Versuchsplanung.pdf' and fname != 'Versuchsplanung.pptx' and fname != '316L_1200l_3m_min_30V' and fname != '316L_1200l_2m_min_30V':
            subfilenames = sorted(os.listdir(pfad + '/' + fname))
            df = {}
            for subfname in subfilenames:
                if subfname != '.DS_Store' and fname != 'Thumbs.db' and fname != 'TS-PL-21' and fname != 'TS-PL-22' and fname != 'TS-PL-23' and fname != 'TS-PL-24' and fname != 'TS-PL-25' and fname != 'TS-PL-26' and fname != 'TS-PL-27':

                    df_subfile = pd.read_csv(
                        pfad + '/' + fname + '/' + subfname, delimiter=';', skiprows=[1], encoding='latin-1', index_col=0)
                    df_subfile = df_subfile.replace(',', '.', regex=True)
                    df_subfile['angelegte Spannung'] = 35
                    df_subfile['angelegter Drahvorschub'] = 2
                    df_subfile['Spritzabstand'] = 100
                    if fname[-1] == '0':
                        df_subfile['Robotergeschwindigkeit'] = 25
                        df_subfile['Zerstäubergasmenge'] = 900
                    elif fname[-1] == '2':
                        df_subfile['Robotergeschwindigkeit'] = 75
                        df_subfile['Zerstäubergasmenge'] = 900
                    elif fname[-1] == '1':
                        df_subfile['Robotergeschwindigkeit'] = 25
                        df_subfile['Zerstäubergasmenge'] = 1300
                    elif fname[-1] == '3':
                        df_subfile['Robotergeschwindigkeit'] = 75
                        df_subfile['Zerstäubergasmenge'] = 1300
                    elif fname[-1] == '4':
                        df_subfile['Robotergeschwindigkeit'] = 50
                        df_subfile['Zerstäubergasmenge'] = 1100
                    elif fname[-1] == '7':
                        df_subfile['Robotergeschwindigkeit'] = 1
                        df_subfile['Zerstäubergasmenge'] = 1100
                    elif fname[-1] == '5':
                        df_subfile['Robotergeschwindigkeit'] = 100
                        df_subfile['Zerstäubergasmenge'] = 1100
                    elif fname[-1] == '6':
                        df_subfile['Robotergeschwindigkeit'] = 50
                        df_subfile['Zerstäubergasmenge'] = 1500
                    # df_subfile['Robotergeschwindigkeit'][0]='(mm/s)'
                    # df_subfile['Zerstäubergasmenge'][0]='(l/min)'
                    df[subfname] = df_subfile
            text_list[fname] = df
    return text_list
