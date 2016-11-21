# -*- coding: utf8 -*-
import threading
from math import ceil
from time import ctime, time

import tushare as ts

from volumeUtils import *

print(ts.__version__)


# TODO load all data into single file
# TODO incremental add data
# TODO load tick data
'''
DataCollector is to download below kinds of data from internet:
1. Index: SH, SZ
2. Stock basics
3. Stock K data, including 1 min, 5 min, 15 min, 30 min, 60 min, Daily, Weekly and Monthly
4. Stock tick data

Requirements:
1. All data will be saved to local disk using HDF5 format
2. Data will be incrementally added to existing file
'''

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
    chuncks = split_into_chunck(df.code, 20)
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
        get_stock_data(code, ktype)
        # sleep(0.2)


def get_stock_data(code, ktype='D', start=None, end=None):
    filename = './data/' + code + DATA_FILE_SUFFIX[ktype]
    # print(filename)
    # check if the file already exists
    if os.path.exists(filename):
        # get the latest date
        # print(filename)
        existing_data = pd.read_csv(filename)
        row, col = existing_data.shape
        latest_date = existing_data.date[row - 1]
        # retrieve data from the latest date
        data = ts.get_hist_data(code=code, start=latest_date, ktype=ktype, retry_count=30, pause=2)
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
            print(code, 'updated')
    else:
        # Create the data file directly
        data = ts.get_hist_data(code=code, ktype=ktype, start=start, end=end,
                                retry_count=20, pause=1)
        # Data can be None if it's a new stock
        if data is not None:
            # The data is sorted so that the latest data at the bottom of the file.
            # It's easier to append future data while keep the ascending order of date
            data.sort_index(axis=0, inplace=True)
            data.to_csv(filename)
            print(code, 'created')


def get_stock_basics():
    basics = ts.get_stock_basics()
    basics.to_csv("./basics.csv", encoding='utf8')


def get_tick_data(code,start=None,end=None):
    pass

def convert_tongdaxing_data():
    pass

if __name__ == '__main__':
    get_stock_basics()
    get_all_data(ktype='D')
    # get_all_data(ktype='W')
