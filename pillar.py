# -*- coding: utf8 -*-
import pandas as pd

df = pd.read_pickle('data.dat')
# print(df['volume'].head(5), df['p_change'].head(5), df['turnover'].head(5))

print(df.loc(['volume','p_change','turnover']))