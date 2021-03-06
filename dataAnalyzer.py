import numpy as np

from volumeUtils import *

mkt_overview_columns = ['date', 'market', 'p_change', 'amount', 'up']


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


class AnalyticsEngine(object):
    def __init__(self, ktype='D', force_reload=False):
        self.ktype = ktype
        # TODO add param to force load from all stock files
        if os.path.exists('./daily.csv') and not force_reload:
            self.big_data = self.load_data_from_consolidated_file()
        else:
            self.big_data = self.load_data_from_files()
        self.algorithms = []
        print(self.big_data.shape, 'data loaded')

    def load_data_from_files(self):
        data = []
        basics = pd.read_csv('./basics.csv', dtype={'code': np.str})
        codes = basics.code
        l = len(codes)
        c = 1
        for code in codes:
            d = read_data(code, self.ktype)
            if d is not None:
                d['code'] = code
                # pass
            else:
                c += 1
                continue
            data.append(d)
        big_data = pd.concat(data, ignore_index=True)
        return big_data

    def load_data_from_consolidated_file(self):
        data = pd.read_csv('./daily.csv', dtype={'code': np.str})
        return data

    def save_data(self):
        self.big_data.to_csv('./daily.csv', index=False)

    # TODO add ktype
    # TODO add logic to handle missing start or end
    def data_in_period(self, original, start=None, end=None):
        if start is None and end is None:
            return original
        elif start is not None and end is not None:
            rng = pd.date_range(start, end)
            mask = pd.DataFrame(None, index=rng)
            data = mask.merge(original, left_index=True, right_index=True)
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
                    counter = {'code': code, 'total': len(data)}
                    combo_counter(match.intIdx, counter)
                    result_list.append(counter)

        df = pd.DataFrame(result_list)
        df.fillna(value=0, inplace=True)
        df.set_index('code', inplace=True)
        # df.pop('code')
        # df.sort_index(axis=1, inplace=True)
        df.to_csv('combo' + str(percentage) + '.csv')


# A strategy is to define a set of factors and score all stocks based on certain algorithm
# A strategy then is validated by test using data in specified time frame.
class Strategy(object):
    def __init__(self, **kwargs):
        print(kwargs)


if __name__ == '__main__':
    start = time()
    print('Start at:', ctime())
    engine = AnalyticsEngine(force_reload=True)
    print(engine.big_data.open, engine.big_data.close)
    engine.save_data()

    # paras = {'name': 'strategy', 'p_change': 5, 'turnover': 1}
    # strategy = Strategy(**paras)
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2), 'seconds')

    # 一般分析步骤：
    # 1. Turnover rate: select actively transaction in past 3 days
    # 2. Get tick data: buy > sell, amount delta
    # 3. Get big deals: buy > sell, amount delta
    # 4. Cluster analysis
