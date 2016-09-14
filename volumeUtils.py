# -*- coding: utf8 -*-
import os
import pandas as pd

DATA_FILE_SUFFIX = {'D': '-D.csv', 'W': '-W.csv', 'M': '-M.csv'}


def read_data(code, ktype='D'):
    filename = './data/' + code + DATA_FILE_SUFFIX[ktype]
    data = None
    if os.path.exists(filename):
        data = pd.read_csv(filename)  # ,index_col='date',parse_dates=True)
    return data


def read_data_from_file(filename):
    data = None
    if os.path.exists(filename):
        data = pd.read_csv(filename)
    return data
