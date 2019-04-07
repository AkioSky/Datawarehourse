import pandas_datareader.data as pdr
import fix_yahoo_finance as yf
import pandas as pd
import datapackage
from datetime import datetime
from .models import CompanyInfo, StockPrice, GoldPrice

yf.pdr_override()
start = datetime(2010, 12, 31)
end = datetime.now()


def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return (pd.concat(datas, keys=tickers, names=['Ticker']))


def get_basic_finance():
    companies = CompanyInfo.objects.all()
    tickers = []
    for company in companies:
        tickers.append(company.symbol)
    print(tickers)

    all_data = get(tickers, start, end)
    all_data.reset_index(level=['Date'], inplace=True)

    for company in companies:
        df = all_data.loc[company.symbol]
        #print(df.head())
        for index, row in df.iterrows():
            StockPrice.objects.create(
                company=company,
                open=row['Open'],
                close=row['Close'],
                high=row['High'],
                low=row['Low'],
                volume=row['Volume'],
                adj_close=row['Adj Close'],
                date=row['Date']
            )


def read_gold_prices():
    data_url = 'https://datahub.io/core/gold-prices/datapackage.json'
    package = datapackage.Package(data_url)
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
            print(data.head())
            break

    for index, row in data.iterrows():
        GoldPrice.objects.create(
            date=row['Date'],
            price=row['Price']
        )


def get_all_data():
    all_data = get(['SPY', 'IWM', 'GOOG'], start, end)

    print(all_data.head())
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
    #print(df.loc('SPY'))


def delete_all_stocks():
    StockPrice.objects.all().delete()

#get_all_data()