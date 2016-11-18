'''
This script is to load all data files per parameters
'''
import pandas as pd
from time import ctime, time
from volumeUtils import *


class DataLoader:
    def __init__(self, start=None, end=None, ktype='D'):
        self.big_data = None
        print(os.path.abspath(os.path.curdir))
        data_dir = DATA_DIR_DICT[ktype]
        # data_dir = os.path.join(os.path.abspath(os.path.curdir), data_dir)
        print(data_dir)
        d = []
        for p, dir_name, filenames in os.walk(data_dir):
            for filename in filenames:
                print(os.path.join(p, filename))
                data = pd.read_csv(os.path.join(p, filename), encoding='cp936')
                # if self.big_data is None:
                #     self.big_data = [data]
                # else:
                #     self.big_data.append(data)
                d.append(data)
        self.big_data = pd.concat(d, ignore_index=True)

    def get_data(self):
        return self.big_data


if __name__ == '__main__':
    start = time()
    print('Start at:', ctime())

    dl = DataLoader(ktype='m')
    d = dl.get_data()
    print(d.tail(10))
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2))
