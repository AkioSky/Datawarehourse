from django.test import TestCase
import pandas_datareader.data as pdr
import fix_yahoo_finance as yf
import pandas as pd
import datapackage
from datetime import datetime

yf.pdr_override()
start = datetime(2019, 4, 6)
end = datetime.now()


# Create your tests here.

def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return (pd.concat(datas, keys=tickers, names=['Ticker']))

def get_cus(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    try:
        df = (pd.concat(datas, keys=tickers, names=['Ticker']))
    except:
        return None
    return df


tickers = ['SPY', 'IWM', 'GOOG']
all_data = get_cus(['SPY', 'IWM', 'GOOG'], start, end)
if all_data is not None:
    print(all_data)
else:
    print('None')

if all_data is not None:
    all_data.reset_index(level=['Date'], inplace=True)

    for company in tickers:
        df = all_data.loc[company]
        print(df['Open'])
#all_data.reset_index(level=['Date'], inplace=True)

#print(all_data)
#for company in tickers:
#    df = all_data.loc[company]
#    print(df)
    # print(df.head())

"""
print(all_data.keys())
for key in all_data.keys():
    print(all_data[key].head())

all_data.reset_index(level=['Date'], inplace=True)
print(all_data.loc['SPY'])
df = all_data.loc['SPY']
#df.reset_index(level=['Date'], inplace=True)
for index, row in df.iterrows():
    print(index)
    print(row['Date'])
"""
#print(df.loc('SPY'))