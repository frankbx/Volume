# -*- coding: utf8 -*-
import tushare as ts

his_data = ts.get_hist_data('000681', retry_count=20, pause=3)
his_data['code'] = '000681'
# his_data.to_pickle('600493.dat')
# print(his_data.volume.head(5))
# print(his_data.shape)
df = his_data.loc[:, ['open', 'close', 'low', 'high', 'p_change', 'volume']]
print(df[df.p_change > 5])
