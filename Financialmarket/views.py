from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline
from datapackage import Package
from Financialmarket.core import get_basic_finance, delete_all_stocks, read_gold_prices, \
    delete_all_gold_stocks, get_last_stocks
from Financialmarket.models import CompanyInfo, GoldPrice
from Financialmarket.forms import DateSelectForm, MonthYearSelectForm


package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')


def store_company():
    df = pd.read_csv('constituents.csv')
    print(df)


# Create your views here.
def home(request):
    #get_basic_finance()
    #delete_all_stocks()
    #read_gold_prices()
    #delete_all_gold_stocks()
    #get_last_stocks()
    company_list = CompanyInfo.objects.all()
    return render(request, 'company/company_list.html', {
        'company_list': company_list,
        'left_menu': 0,
        'title': 'Company List'
    })


def company_stock(request, company_id):
    try:
        company = CompanyInfo.objects.get(pk=company_id)
    except CompanyInfo.DoesNotExist:
        return redirect(reverse('page-not-found'))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(30)
    else:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')

    form = DateSelectForm()
    start_date_min = start_date - timedelta(4)
    print(start_date)
    print(end_date)

    df = pd.DataFrame(list(company.stocks.filter(date__range=[start_date_min, end_date])
                           .values('open', 'close', 'high', 'low', 'volume', 'adj_close', 'date')
                           .order_by('-date')[::-1]))
    df['SMA(5)'] = df['adj_close'].rolling(5).mean()
    df_result = df[df['SMA(5)'].notnull()]

    trace1 = go.Scatter(x=df_result['date'], y=df_result['adj_close'], mode='lines', name=company.name)
    trace2 = go.Scatter(x=df_result['date'], y=df_result['SMA(5)'], mode='lines', name='SMA(5)')
    data = [trace1, trace2]
    layout = go.Layout(
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        ),
        yaxis=dict(
            title='Adj Close',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        )
    )
    fig = go.Figure(data, layout=layout)
    graph = plotly.offline.plot(fig, auto_open=True, output_type='div')
    return render(request, 'company/company_stock.html', {
        'left_menu': 0,
        'graph': graph,
        'stocks': df_result.to_html(classes="table table-striped"),
        'form': form,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'title': '{} Finance'.format(company.symbol)
    })


def gold_price_page(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(1060)
        start_date = datetime(year=start_date.year, month=start_date.month, day=1)
    else:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')

    print(start_date)
    print(end_date)

    form = MonthYearSelectForm()

    df = pd.DataFrame(list(GoldPrice.objects.
                           filter(date__range=[start_date, end_date])
                           .values('date', 'price')
                           .order_by('-date')[::-1]))
    df['SMA(5)'] = df['price'].rolling(5).mean()
    df_result = df[df['SMA(5)'].notnull()]
    print(df.head())
    trace1 = go.Scatter(x=df_result['date'], y=df_result['price'], mode='lines', name='Gold Prices')
    trace2 = go.Scatter(x=df_result['date'], y=df_result['SMA(5)'], mode='lines', name='SMA(5)')
    data = [trace1, trace2]
    layout = go.Layout(
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        ),
        yaxis=dict(
            title='Price',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        )
    )
    fig = go.Figure(data, layout=layout)
    graph = plotly.offline.plot(fig, auto_open=True, output_type='div')
    print(start_date.date())
    print(end_date.date())
    return render(request, 'gold/index.html', {
        'left_menu': 1,
        'graph': graph,
        'title': 'Gold Price',
        'form': form,
        'start_date': '{}'.format(start_date.date()),
        'end_date': '{}'.format(end_date.date())
    })


def page_not_found(request):
    return render(request, '404.html', {
        'title': 'Page not found'
    })
