import os

import numpy as np

from volumeUtils import *

TDX_MINUTE_DATA_DIRECTORY = 'c:/data/minute/'
TDX_FIVE_MINUTES_DATA_DIRECTORY = 'c:/data/5minutes/'


def transform_tongdaxin_data(original_file, transformed_file):
    data = pd.read_csv(original_file,
                       header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount'],
                       encoding='cp936', dtype={'time': np.str})[:-1]
    if os.path.exists(transformed_file):
        existing_data = pd.read_csv(transformed_file, dtype={'time': np.str})
        r, c = existing_data.shape
        if r > 1:
            latest_date = existing_data.date[r - 1]
            # latest_time = existing_data.time[r - 1]
            # delta1 = data[data.date == latest_date][data.time > latest_time]
            delta2 = data[data.date > latest_date]
            # delta1.to_csv(transformed_file, mode='a', header=None, index=False)
            delta2.to_csv(transformed_file, mode='a', header=None, index=False)
    else:
        r, c = data.shape
        if r > 1:
            data.to_csv(transformed_file, index=False, encoding='utf-8', dtype={'time': np.str})


def transform_parallel(source, target):
    filenames = os.listdir(source)
    if not os.path.exists(target):
        os.mkdir(target)
    parallel_processing(tasks=filenames, processing_func=transform, chunck_size=200,
                        params={'source': source, 'target': target})


def transform(filenames, params):
    source = params['source']
    target = params['target']
    for file in filenames:
        # print(file, 'processed')
        original_file = os.path.join(source, file)
        transformed_file = os.path.join(target, file)
        transform_tongdaxin_data(original_file, transformed_file)


transform_parallel(TDX_FIVE_MINUTES_DATA_DIRECTORY, FIVE_MINUTE_DATA_DIR)
transform_parallel(TDX_MINUTE_DATA_DIRECTORY, MINUTE_DATA_DIR)
