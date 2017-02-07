import math

import numpy as np

from volumeUtils import *

corrlation_results = []

data = {}


def code_2_file(code):
    if code.startswith('6'):
        return './data/daily1/' + code + '.sh.csv'
    else:
        return './data/daily1/' + code + '.sz.csv'


def read_data(code, start='2014-12-31'):
    global data
    file_name = code_2_file(code)
    d = pd.read_csv(file_name)
    d.index = d.date
    data[code] = d[d.index > start]
    # return data[data.index > start]


def pair_correlation(code1, code2):
    global corrlation_results
    df1 = data[code1]
    df2 = data[code2]
    x = df1.close - df1.close.mean()
    y = df2.close - df2.close.mean()
    cor = (x * y).sum() / math.sqrt((x * x).sum() * (y * y).sum())
    corrlation_results.append({'code1': code1, 'code2': code2, 'corr': cor})


def calc_pair_correlation(combinations, params):
    for pair in combinations:
        code1, code2 = pair
        pair_correlation(code1, code2)


if __name__ == '__main__':
    # print(pair_correlation('600084', '601668'))
    basics = pd.read_csv('./basics.csv', dtype={'code': np.str})
    basics = basics[basics.timeToMarket < 20141231]
    basics = basics[basics.timeToMarket > 0]
    codes = list(basics.code)
    codes.sort()
    # print(codes)
    # length = ceil(len(codes) / 100)
    length = len(codes)
    print(length)
    combinations = []
    start = time()
    print('Start at:', ctime())
    for c in codes:
        read_data(c)
    end = time()
    print('Data loading End at:', ctime())
    print('Duration:', round(end - start, 2), 'seconds')
    for i in range(0, length):
        for j in range(i + 1, length):
            combinations.append((codes[i], codes[j]))
    parallel_processing(tasks=combinations, processing_func=calc_pair_correlation, chunck_size=850000)
    df = pd.DataFrame(corrlation_results)
    df.to_csv('results4.csv', index=False)
    # print(len(results))
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2), 'seconds')
