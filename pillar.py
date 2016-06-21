# -*- coding: utf8 -*-
import tushare as ts

his_data = ts.get_hist_data('600493', retry_count=20, pause=3)
his_data['code'] = '600493'
his_data.to_pickle('600493.dat')
# print(his_data.volume.head(5))
print(his_data.shape)
df = his_data.copy().loc[:, ['volume']]
print(type(df))
print(type(his_data.volume))
