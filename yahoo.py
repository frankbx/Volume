import datetime

import tushare as ts

try:
    from matplotlib.finance import quotes_historical_yahoo_ochl
except ImportError:
    # quotes_historical_yahoo_ochl was named quotes_historical_yahoo before matplotlib 1.4
    from matplotlib.finance import quotes_historical_yahoo as quotes_historical_yahoo_ochl

start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2016, 11, 1)


def add_suffix(code):
    if code.startswith('6'):
        return code + '.ss'
    else:
        return code + '.sz'


basics = ts.get_stock_basics()
symbols = [add_suffix(c) for c in basics.index]
# print(symbols)
# symbols = ['601600.ss', '600362.ss']
yahoo_symbols =[]
for symbol in symbols:
    try:
        quote = quotes_historical_yahoo_ochl(symbol, start, end, asobject=True)
        yahoo_symbols.append(symbol)
    except Exception as e:
        print(symbol)
        continue
