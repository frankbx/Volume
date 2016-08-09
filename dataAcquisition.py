# -*- coding: utf8 -*-
import os

import pandas as pd
import tushare as ts
import threading
from time import ctime, sleep, time
from math import ceil

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


def get_sz_data():
    sz = ts.get_h_data('399106', start='2000-01-01', index=True)
    # sz.to_csv('sz.csv')
    return sz


def get_sh_data():
    sh = ts.get_h_data('000001', start='2000-01-05', index=True)
    sh.to_csv('sh.csv')
    return sh


def get_all_data(ktype='D', test_flag=False):
    if not test_flag:
        df = ts.get_today_all()
        chuncks = split_into_chunck(df.code)
    else:
        df = pd.read_csv('./data/000681-D.csv')
        chuncks = split_into_chunck(df.date, 20)
    threads = list()
    for i in range(len(chuncks)):
        th = threading.Thread(target=process, args=(chuncks[i], ktype))
        threads.append(th)
    start = time()
    print('Start at:', ctime())
    print(len(threads))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2))


def split_into_chunck(data_list, chunck_size=100):
    l = len(data_list)
    n = ceil(l / chunck_size)
    deck = list()
    for i in range(n):
        if ((1 + i) * chunck_size) < l:
            deck.append(data_list[i * chunck_size:(i + 1) * chunck_size])
        else:
            deck.append(data_list[i * chunck_size:])
    print('Total length:', l)
    print('Chunck size:', chunck_size)
    print('Number of chuncks:', deck.__len__())
    return deck


def process(code_list, ktype='D'):
    for code in code_list:
        update_stock_data(code, ktype)
        # sleep(0.2)


def update_stock_data(code, ktype='D'):
    filename = './data/' + code + DATA_FILE_SUFFIX[ktype]
    # print(filename)
    # check if the file already exists
    if os.path.exists(filename):
        # get the latest date
        existing_data = pd.read_csv(filename)
        row, col = existing_data.shape
        latest_date = existing_data.date[row - 1]
        # retrieve data from the latest date
        data = ts.get_hist_data(code=code, start=latest_date, ktype=ktype, retry_count=20, pause=1)
        r, c = data.shape
        # discard duplicated data of the last day if there's more than 1 row
        if r > 1:
            # Locate by integer, not index
            delta_data = data.iloc[:r - 1].copy()
            # The data is sorted so that the latest data at the bottom of the file.
            # It's easier to append future data while keep the ascending order of date
            delta_data.sort_index(axis=0, inplace=True)
            # print(delta_data)
            # Append data to the file
            delta_data.to_csv(filename, mode='a', header=None)
    else:
        # Create the data file directly
        data = ts.get_hist_data(code=code, ktype=ktype, retry_count=20, pause=1)
        # Data can be None if it's a new stock
        if data is not None:
            # The data is sorted so that the latest data at the bottom of the file.
            # It's easier to append future data while keep the ascending order of date
            data.sort_index(axis=0, inplace=True)
            data.to_csv(filename)


get_all_data()
