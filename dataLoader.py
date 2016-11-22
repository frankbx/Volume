'''
This script is to load all data files per parameters
'''
import pandas as pd
from time import ctime, time
from volumeUtils import *


class DataLoader:
    def __init__(self, start=None, end=None, ktype='D'):
        self.big_data = None
        data_dir = DATA_DIR_DICT[ktype]
        print(data_dir)
        d = []
        for parent_dir_name, dir_names, file_names in os.walk(data_dir):
            for filename in file_names:
                print(os.path.join(parent_dir_name, filename))
                data = pd.read_csv(os.path.join(parent_dir_name, filename), encoding='cp936')
                # if self.big_data is None:
                #     self.big_data = [data]
                # else:
                #     self.big_data.append(data)
                d.append(data)
        # self.big_data = pd.concat(d, ignore_index=True)
        self.big_data = d

    def get_data(self):
        return self.big_data


if __name__ == '__main__':
    start = time()
    print('Start at:', ctime())

    dl = DataLoader(ktype='m')
    d = dl.get_data()
    print(d[-1])
    end = time()
    print('End at:', ctime())
    print('Duration:', round(end - start, 2), 'seconds')
