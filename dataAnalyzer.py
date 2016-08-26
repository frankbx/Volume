import os
from time import ctime, time

import numpy as np
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


# describe('000681', p_change=2)

basics = pd.read_csv('./basics.csv', dtype={'code': np.str})
codes = basics.code
col = ['code', 'total', 'limit_up', 'percent']
limit_up_results = None
start = time()
print('Start at:', ctime())
limit_up_data = None

for code in codes:
    # print(code)
    filename = './data/' + code + DATA_FILE_SUFFIX['D']
    if os.path.exists(filename):
        # print(filename)
        data = pd.read_csv(filename)
        # print(data.shape)
        limit_up = data[data.p_change > 9.9].copy()
        limit_up['code'] = code
        if limit_up_data is None:
            limit_up_data = limit_up
        else:
            limit_up_data = limit_up_data.append(limit_up)
        # print(limit_up.shape)
        df = pd.DataFrame(
            [{'code': code, 'total': len(data), 'limit_up': len(limit_up), 'percent': len(limit_up) / len(data)}])
        if limit_up_results is None:
            limit_up_results = df
        else:
            limit_up_results = limit_up_results.append(df)
            # break
# print(limit_up_results.describe())
end = time()
limit_up_data.to_csv('limit_up_data.csv', encoding='utf8', index=False)
print(limit_up_results[limit_up_results.percent > 0.2].describe())
print('End at:', ctime())
print('Duration:', round(end - start, 2), 'seconds')
