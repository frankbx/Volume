import os
from time import ctime, time

import numpy as np
import pandas as pd

from volumeConstants import *


def read_data(code, ktype='D'):
    filename = './data/' + code + DATA_FILE_SUFFIX[ktype]
    data = None
    if os.path.exists(filename):
        data = pd.read_csv(filename)
    return data


def describe(code, ktype='D', p_change=None):
    filename = './data/' + code + DATA_FILE_SUFFIX[ktype]
    print(filename)
    if os.path.exists(filename):
        his_data = pd.read_csv(filename)
        df = his_data.loc[:, ['open', 'close', 'low', 'high', 'p_change', 'turnover']]
        if p_change is not None:
            df_h = df[df.p_change > p_change]
        else:
            df_h = df
        total, col = df.shape
        match, col = df_h.shape
        print(match, '/', total, ':', match / total * 100, '%')
        d = df_h.describe()
        print(d.loc[:, ['p_change', 'turnover']])


def market_overview():
    # Get an estimate of market performance of the day
    # Points of interest:
    # 1. SH, SZ change percent
    # 2. SH, SZ volume
    # 3. Number of stocks go up, down and flat
    # 4. Distribution of each group
    pass


def combo_counter(seq, counter):
    length = len(seq)
    s = pd.Series(range(min(seq), min(seq) + length))
    seq.index = range(0, length)
    d = {'origin': seq, 'i': s}
    df = pd.DataFrame(d)
    df['delta'] = seq - s
    #    print(df)
    n = len(df[df.delta == 0])
    #    print(n)
    for i in range(n, 0, -1):
        if i not in counter:
            counter[i] = 1
        else:
            counter[i] += 1
        for x in range(i - 1, 0, -1):
            if x not in counter:
                counter[x] = 1
            else:
                counter[x] += 1
    a = df[df.delta > 0].origin
    #    print(type(a))
    if length - n > 0:
        combo_counter(a, counter)


result_list = []


def combo_analyzer(code, ktype='D', start=None, end=None, percentage=9.9):
    data = read_data(code, ktype)
    if data is not None:
        data['intIdx'] = range(0, len(data))
        match = data[data.p_change > percentage].copy()
        #    print(match.intIdx)
        if len(match) > 0:
            counter = {'code': code}
            combo_counter(match.intIdx, counter)
            result_list.append(counter)


def run_combo():
    basics = pd.read_csv('./basics.csv', dtype={'code': np.str})
    codes = basics.code

    start = time()
    print('Start at:', ctime())

    for code in codes:
        print('Processing...', code)
        combo_analyzer(code)

    # combo_analyzer('000681')
    df = pd.DataFrame(result_list)
    df.fillna(value=0, inplace=True)
    # df = pd.read_csv('combo.csv', dtype={'code': np.str})
    df.set_index(df.code, inplace=True)
    df.pop('code')
    df.sort_index(axis=1, inplace=True)
    df.to_csv('combo.csv')

    print(df.head(5))

    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2), 'seconds')


df = pd.read_csv('combo.csv')
print(df.describe().T)
