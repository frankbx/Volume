# -*- coding: utf8 -*-
import pandas as pd


def describe(code, p_change=None):
    his_data = pd.read_csv('./data/' + code + '-D.csv')
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


describe('000681', 2)
# describe('000001', 1)
# describe('399106', 2)
# print(index_list)
