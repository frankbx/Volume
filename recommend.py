from time import ctime, time

import numpy as np

from volumeUtils import *


class RecommendEngine():
    def __init__(self):
        pass


start = time()
print('Start at:', ctime())
data = pd.read_csv('combo8.csv', dtype={'code': np.str})
data['p'] = data['1'] / data['100']
data.sort_values(by=['p'], inplace=True, ascending=False)

print(data[data['100'] > 700].loc[:, ['code', 'p', '1', '2', '3', '4', '5', '100']].head(20))

end = time()
print('End at:', ctime())
print('Duration:', round(end - start, 2), 'seconds')
