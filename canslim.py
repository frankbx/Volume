# -*- coding: utf8 -*-

import tushare as ts

print(ts.__version__)
report = ts.get_report_data(2016, 1)
report['year'] = 2016
report['quarter'] = 1
for y in range(2005, 2016):
    for q in range(1, 5):
        print(y, q)
        r = ts.get_report_data(y, q)
        r['year'] = y
        r['quarter'] = q
        report = report.append(r, ignore_index=True)

report.to_csv('report05Q4-16Q1.csv')
