# -*- coding: utf8 -*-
import tushare as ts
from sqlalchemy import create_engine
from datetime import datetime

stock_basics = ts.get_stock_basics()

db = create_engine('sqlite:///stock.db')

stock_basics['date'] = datetime.now().date()
stock_basics.to_sql('stock_basics', db)
# print(stock_basics.head(10))
# print(datetime.now().date())
codes = list(stock_basics.index)
counter = 1
for code in codes:
    # 取得所有日线数据并存入数据库
    his_data = ts.get_hist_data(code, retry_count=20, pause=3)
    his_data['code'] = code
    print(code, counter, '/', len(codes), his_data.shape)
    counter += 1
    his_data.to_sql('history_data', db, if_exists='append')
