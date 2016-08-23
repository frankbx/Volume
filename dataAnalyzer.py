import os

import pandas as pd

from volumeConstants import *


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


describe('000681', p_change=2)
