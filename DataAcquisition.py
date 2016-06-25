# -*- coding: utf8 -*-
import tushare as ts

print(ts.__version__)


def get_reports():
    report = ts.get_report_data(2016, 1)
    report['year'] = 2016
    report['quarter'] = 1
    for year in range(2005, 2016):
        for quarter in range(1, 5):
            print(year, quarter)
            r = ts.get_report_data(year, quarter)
            r['year'] = year
            r['quarter'] = quarter
            report = report.append(r, ignore_index=True)
    report.sort_values(by='year')
    report.to_excel('report.xlsx')


def get_hist_data(code, ktype='D'):
    data = ts.get_hist_data(code, ktype=ktype)
    data = data.sort_index(axis=0)
    data.to_csv(code + '-' + ktype + '.csv')


def get_sz_data():
    sz = ts.get_h_data('399106', index=True)
    return sz


get_hist_data('000681', 'W')
