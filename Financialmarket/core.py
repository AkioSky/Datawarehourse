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
        print(ticker)
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    try:
        df = (pd.concat(datas, keys=tickers, names=['Ticker']))
    except:
        return None
    return df


def get_basic_finance():
    companies = CompanyInfo.objects.all()
    tickers = []
    #for company in companies:
    #    tickers.append(company.symbol)
    #print(tickers)

    #all_data = get(tickers, start, end)
    #print(all_data)
    for company in companies:
        try:
            all_data = pdr.get_data_yahoo(company.symbol, start=start, end=end)
            #print(all_data)
            if all_data is not None:
                print(company.symbol)
                all_data.reset_index(level=['Date'], inplace=True)

                #for company in companies:
                #df = all_data.loc[company.symbol]
                df = all_data
                print(df.head())
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
        except:
            print('failed - {}'.format(company.symbol))
            pass


def read_gold_prices():
    data_url = 'https://datahub.io/core/gold-prices/datapackage.json'
    package = datapackage.Package(data_url)
    resources = package.resources
    data = None
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
            #print(data.head())

    date_field = pd.to_datetime(data['Date'].astype(str), format='%Y-%m')
    data['Date'] = date_field
    #print(data)
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


def delete_all_gold_stocks():
    GoldPrice.objects.all().delete()


def get_last_stocks():
    start = datetime.now()
    end = datetime.now()
    companies = CompanyInfo.objects.all()
    tickers = []
    for company in companies:
        tickers.append(company.symbol)

    all_data = get(tickers, start, end)
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

#get_all_data()