# -*- coding: utf8 -*-
import tushare as ts

index_list = list()


def describe(code, p_change=None):
    global index_list
    his_data = ts.get_hist_data(code, retry_count=20, pause=3)
    df = his_data.loc[:, ['open', 'close', 'low', 'high', 'p_change', 'volume']]
    if p_change is not None:
        df_h = df[df.p_change > p_change]
    else:
        df_h = df
    total, col = df.shape
    match, col = df_h.shape
    print(match, '/', total, ':', match / total * 100, '%')
    d = df_h.describe()
    index_list = list(df_h.index)
    # print(d.loc['75%', ])
    print(d.loc[:, ['p_change', 'volume']])


describe('600493', 1)
describe('000681', 1)
describe('000001', 1)
describe('399106', 2)
# print(index_list)
