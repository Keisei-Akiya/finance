import datetime

import pandas_datareader as pdr

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()

# FTSEのデータを取得
ftse = pdr.get_data_yahoo("^FTSE", start, end)
print(ftse.head())
