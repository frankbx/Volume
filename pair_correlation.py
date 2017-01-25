import math

import pandas as pd


def code_2_file(code):
    if code.startswith('6'):
        return './data/daily1/' + code + '.sh.csv'
    else:
        return './data/daily1/' + code + '.sz.csv'


def read_data(file_name, start='2014-12-31'):
    data = pd.read_csv(file_name)
    data.index = data.date
    return data[data.index > start]


def pair_correlation(code1, code2, start='2014-12-31'):
    name1 = code_2_file(code1)
    name2 = code_2_file(code2)
    df1 = read_data(name1, start)
    df2 = read_data(name2, start)
    x = df1.close - df1.close.mean()
    y = df2.close - df2.close.mean()
    cor = (x * y).sum() / math.sqrt((x * x).sum() * (y * y).sum())
    return cor


if __name__ == '__main__':
    print(pair_correlation('600084', '601668'))
