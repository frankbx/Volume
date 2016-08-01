# -*- coding: utf8 -*-
import os

import pandas as pd
import tushare as ts

from volumeConstants import *

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
    report.to_excel('report.xlsx')


def get_hist_data(code, ktype='D'):
    data = ts.get_hist_data(code, ktype=ktype, retry_count=3)
    print(data.index[0])
    print(type(data.index[0]))
    data.to_csv('./data/' + code + '-' + ktype + '.csv')


def get_sz_data():
    sz = ts.get_h_data('399106', start='2000-01-01', index=True)
    # sz.to_csv('sz.csv')
    return sz


def get_sh_data():
    sh = ts.get_h_data('000001', start='2000-01-05', index=True)
    sh.to_csv('sh.csv')
    return sh


def get_all_data(ktype='D'):
    df = ts.get_today_all()
    row, col = df.shape
    counter = 0
    for code in df.code:
        update_all_data(code, ktype)
        counter += 1
        print(counter, '/', row)


def update_all_data(code, ktype='D'):
    # check if the file already exists
    filename = './data/' + code + data_file_suffix[ktype]
    # check if the file already exists
    if os.path.exists(filename):
        # get the latest date
        existing_data = pd.read_csv(filename)
        latest_date = existing_data.date[0]
        print(latest_date)
        # retrieve data from the latest date
        data = ts.get_hist_data(code=code, start=latest_date, ktype=ktype, retry_count=5)
        # discard duplicated data of the last day
        delta_data = data.iloc[1:]
        # Append data to the file
        delta_data.to_csv(filename, mode='a', header=None)
    else:
        # Create the data file directly
        data = ts.get_hist_data(code=code, ktype=ktype, retry_count=3)
        data.to_csv(filename)


# get_all_data()
update_all_data('000001')
