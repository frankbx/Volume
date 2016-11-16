# -*- coding: utf8 -*-
import os
import pandas as pd

DATA_FILE_SUFFIX = {'D': '-D.csv', 'W': '-W.csv', 'M': '-M.csv'}
MINUTE_DATA_DIR = './data/minute'
FIVE_MINUTE_DATA_DIR = './data/5minutes'
DAILY_DATA_DIR = './data/daily'
WEEKLY_DATA_DIR = './data/weekly'
K_TYPES = ['m', '5m', 'D', 'W']
data_dir_dict = {
    'D': DAILY_DATA_DIR,
    'W': WEEKLY_DATA_DIR,
    'm': MINUTE_DATA_DIR,
    '5m': FIVE_MINUTE_DATA_DIR
}


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
