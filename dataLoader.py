'''
This script is to load all data files per parameters
'''
import pandas as pd
from time import ctime, time
from volumeUtils import *
import chardet


class DataLoader:
    def __init__(self, start=None, end=None, ktype='D', market='sz'):
        self.big_data = None
        # print(os.path.abspath(os.path.curdir))
        data_dir = DATA_DIR_DICT[ktype]
        d = []
        for p, dir_name, filenames in os.walk(data_dir):
            for filename in filenames:
                # print(os.path.join(p, filename))
                if filename.startswith('6'):
                    print(filename)
                    data = pd.read_csv(os.path.join(p, filename), encoding='cp936')
                    # if self.big_data is None:
                    #     self.big_data = data
                    # else:
                    #     self.big_data = pd.concat([self.big_data, data], ignore_index=True)
                    d.append(data)
        self.big_data = pd.concat(d)

    def get_data(self):
        # return self.big_data
        return len(self.big_data)


if __name__ == '__main__':
    start = time()
    print('Start at:', ctime())

    dl = DataLoader(ktype='5m')
    d = dl.get_data()
    print(d)
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2))
