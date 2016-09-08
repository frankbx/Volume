from time import ctime, time

import numpy as np

from volumeUtils import *


def market_overview():
    # Get an estimate of market performance of the day
    # Points of interest:
    # 1. SH, SZ change percent
    # 2. SH, SZ volume
    # 3. Number of stocks go up, down and flat
    # 4. Distribution of each group
    pass


def combo_counter(seq, counter):
    length = len(seq)
    s = pd.Series(range(min(seq), min(seq) + length))
    seq.index = range(0, length)
    d = {'origin': seq, 'i': s}
    df = pd.DataFrame(d)
    df['delta'] = seq - s
    #    print(df)
    n = len(df[df.delta == 0])
    #    print(n)
    for i in range(n, 0, -1):
        if i not in counter:
            counter[i] = 1
        else:
            counter[i] += 1
        for x in range(i - 1, 0, -1):
            if x not in counter:
                counter[x] = 1
            else:
                counter[x] += 1
    a = df[df.delta > 0].origin
    #    print(type(a))
    if length - n > 0:
        combo_counter(a, counter)


class AnalyticsEngine():
    def __init__(self, ktype='D'):
        self.ktype = ktype
        self.big_data = self.load_data()
        self.algorithms = []

    def load_data(self):
        data = None
        basics = pd.read_csv('./basics.csv', dtype={'code': np.str})
        codes = basics.code
        l = len(codes)
        c = 1
        for code in codes:
            d = read_data(code, self.ktype)
            if d is not None:
                d['code'] = code
            else:
                print("Not found...", code)
                c += 1
                continue
            if data is None:
                c += 1
                data = {code: d}
            else:
                c += 1
                print("Adding...", code, c, '/', l)
                data[code] = d
        return data

    def run_combo(self, percentage):
        codes = self.big_data.keys()
        result_list = []
        for code in codes:
            # print('Processing...', code)
            data = self.big_data[code].copy()
            if data is not None:
                data['intIdx'] = range(0, len(data))
                match = data[data.p_change > percentage].copy()
                #    print(match.intIdx)
                if len(match) > 0:
                    counter = {'code': code, 100: len(data)}
                    combo_counter(match.intIdx, counter)
                    result_list.append(counter)

        df = pd.DataFrame(result_list)
        df.fillna(value=0, inplace=True)
        df.set_index(df.code, inplace=True)
        df.pop('code')
        df.sort_index(axis=1, inplace=True)
        df.to_csv('combo' + str(percentage) + '.csv')


engine = AnalyticsEngine()
start = time()
print('Start at:', ctime())

print(len(engine.big_data))
engine.run_combo(8)
engine.run_combo(5)
engine.run_combo(7)
engine.run_combo(9.9)
end = time()
print('End at:', ctime())
print('Duration:', round(end - start, 2), 'seconds')
