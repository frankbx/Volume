# -*- coding: utf8 -*-
import tushare as ts
import pandas as pd
import numpy as np
import talib as ta

print(ts.__version__)


def get_reports():
    report = ts.get_report_data(2016, 1)
    report['year'] = 2016
    report['quarter'] = 1
    for year in range(2005, 2016):
        for quarter in range(1, 5):
            print(year, quarter)
            r = ts.get_report_data(year, quarter)
            r['year'] = year
            r['quarter'] = quarter
            report = report.append(r, ignore_index=True)
    report.sort_values(by='year')
    report.to_csv('report.csv')

data = ts.get_hist_data('000681')
data = data.sort_index(axis=0)

data.to_csv('000681.csv')
# close = data.close

get_reports()
