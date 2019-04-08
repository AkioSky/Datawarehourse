import pandas_datareader.data as pdr
import fix_yahoo_finance as yf
import pandas as pd
from Financialmarket.models import StockPrice, CompanyInfo
from datetime import datetime

yf.pdr_override()


def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    try:
        df = (pd.concat(datas, keys=tickers, names=['Ticker']))
    except:
        return None
    return df


def get_last_stocks():
    start = datetime.now()
    end = datetime.now()
    companies = CompanyInfo.objects.all()
    tickers = []
    for company in companies:
        tickers.append(company.symbol)

    all_data = get(tickers, start, end)
    all_data.reset_index(level=['Date'], inplace=True)
    print('called get_last_stocks--------------------------------------------------------')
    if all_data is not None:
        all_data.reset_index(level=['Date'], inplace=True)

        for company in companies:
            df = all_data.loc[company.symbol]
            #print(df.head())
            StockPrice.objects.create(
                company=company,
                open=df['Open'],
                close=df['Close'],
                high=df['High'],
                low=df['Low'],
                volume=df['Volume'],
                adj_close=df['Adj Close'],
                date=df['Date']
            )

