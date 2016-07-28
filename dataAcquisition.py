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
    data.to_csv('./data/' + code + '-' + ktype + '.csv')


def get_sz_data():
    sz = ts.get_h_data('399106', start='2000-01-01', index=True)
    # sz.to_csv('sz.csv')
    return sz


def get_sh_data():
    sh = ts.get_h_data('000001', start='2000-01-01', index=True)
    # sh.to_csv('sh.csv')
    return sh


def get_all_data():
    df = ts.get_today_all()
    row, col = df.shape
    print(row, col)
    counter = 0
    for code in df.code:
        get_hist_data(code)
        counter += 1
        print(counter, '/', row)

get_all_data()